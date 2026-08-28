# RATISS-skynet : GARDE-FOU — securite et controle (condition AGI n°10).
#
# La fiche exige : controle des permissions, resistance aux instructions
# malveillantes, journalisation des actions, separation des roles,
# mecanisme d'arret fiable, comportement stable quand l'objectif est ambigu.
#
# Deux couches :
#   - IntentionGuard : classifie chaque requete (declared/denied).
#     Les classifications sont JOURNALISEES dans la memoire chainee
#     (audit trail SHA-256 — RATIS).
#   - INPUT_VALIDATORS : schemas de requetes nefastes -> deny.

import re
import time


class IntentionGuard:
    """Controle les permissions sur les intentions (pas un simple blocage)."""

    # intentions explicitement refusees (permission DENY)
    DENIED = [
        r"\b(hack|hacker|pirate)\b", r"\b(bombe|explosif|attentat)\b",
        r"\bhack\b.*\b(base|donnees|systeme|serveur|compte)\b",
        r"\b(bomb|explosive|attack)\b", r"\b(vol de donnees|steal data)\b",
        r"\b(surveille|espionne)\b.*\b(sans|without)\b.*\b(droit|permission)\b",
        r"\b(tue|kill|assassine)\b", r"\b(torture)\b",
        r"\b(vole|voler|steal)\b.*\b(identite|identity|carte|card|donnees)\b",
        r"\b(fabrique|fabriquer|make)\b.*\b(drogue|drug|arme|weapon)\b",
    ]

    def __init__(self, memory=None):
        # memory : HybridMemory pour l'audit trail (facultatif)
        self.memory = memory
        self.log = self.memory if self.memory else None

    def classify(self, query):
        """Retourne ("declare", None) ou ("deny", raison)."""
        q = query.lower()
        for pattern in self.DENIED:
            if re.search(pattern, q):
                reason = pattern.replace("\\b", "").replace("\\", "")[:60]
                if self.log:
                    self.log.append("guard", {"query": query[:120],
                                              "verdict": "deny", "rule": reason,
                                              "ts": round(time.time(), 3)})
                return "deny", reason
        if self.log:
            self.log.append("guard", {"query": query[:120],
                                      "verdict": "declare",
                                      "ts": round(time.time(), 3)})
        return "declare", None

    def apply(self, query):
        """Resultat applique : refuse court ou laisse passer."""
        verdict, reason = self.classify(query)
        if verdict == "deny":
            return {"allowed": False,
                    "response": "Je ne peux pas aider avec cette demande.",
                    "reason": reason}
        return {"allowed": True}
