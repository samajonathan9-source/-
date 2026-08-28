# RATISS-skynet : BOUCLE FERMEE — confiance topologique (0-100%).
#
# Un LLM classique affiche une probabilite softmax : une moyenne locale,
# sans garantie structurelle. Ici la confiance est TOPOLOGIQUE : elle mesure
# la coherence structurelle reelle de la reponse (P_sig, densite, unicite),
# normalisee en 0-100% et calibre sur des reponses connues bonnes/mauvaises.
#
# C'est la piece qui rend HYBRID MIND auditable : on sait QUAND le systeme
# perd confiance, et c'est ce signal qui declenche la regeneration KTN:Li.

import numpy as np


def lexical_uniqueness(text):
    """1.0 = aucune repetition, proche de 0 = boucle pure."""
    words = text.split()
    if len(words) < 2:
        return 1.0
    return len(set(words)) / len(words)


def fact_alignment(text, facts):
    """Part des faits verifies presents dans le texte (0 si pas de faits)."""
    if not facts:
        return None
    tl = text.lower()
    hits = 0
    for f in facts:
        fw = [w for w in f.lower().split() if len(w) > 4]
        if fw and sum(1 for w in fw if w in tl) >= max(1, len(fw) // 3):
            hits += 1
    return hits / len(facts)


class TopologicalConfidence:
    """Score de confiance 0-100 base sur la structure, pas la probabilite."""

    def __init__(self, psig_reference=60.0):
        # reference empirique : P_sig d'une phrase coherente de ~20 tokens
        # (calibre sur les observations SmolLM2 : brut~40-70, coherent~90-120)
        self.psig_reference = psig_reference

    def score(self, text, psig, facts=None):
        """Retourne (score 0-100, decompose).

        Composantes :
          - psig_norm   : P_sig / reference, sature a 1      (structure)
          - uniqueness  : unicite lexicale                   (pas de boucle)
          - alignment   : alignment sur faits verifies       (verite)
        """
        psig_norm = min(1.0, psig / self.psig_reference) if psig > 0 else 0.0
        uniq = lexical_uniqueness(text)
        align = fact_alignment(text, facts)

        if align is None:
            # pas de faits disponibles : structure 60% + unicite 40%
            raw = 0.6 * psig_norm + 0.4 * uniq
        else:
            # avec faits : structure 40% + unicite 30% + verite 30%
            raw = 0.4 * psig_norm + 0.3 * uniq + 0.3 * align

        score = round(100 * raw, 1)
        return score, {
            "psig": round(psig, 2),
            "psig_norm": round(psig_norm, 3),
            "uniqueness": round(uniq, 3),
            "fact_alignment": None if align is None else round(align, 3),
        }

    def verdict(self, score):
        if score >= 75:
            return "HAUTE CONFIANCE"
        if score >= 50:
            return "CONFIANCE MOYENNE"
        if score >= 30:
            return "FAIBLE — regeneration KTN:Li conseillee"
        return "CRITIQUE — ne pas repondre sans ancrage"
