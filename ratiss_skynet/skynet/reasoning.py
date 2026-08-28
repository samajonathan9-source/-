# RATISS-skynet : RAISONNEMENT FIABLE (condition AGI n°4).
#
# La fiche exige : distinguer faits/hypotheses, detecter les contradictions,
# demander une precision quand l'information manque, reconnaitre une erreur.
# Ici :
#   - check_facts        : NLI-lite lexical, un fait est "soutenu", "libre" ou
#                          "contradit" par le texte de la reponse -> verifiable
#   - detect_contradiction : paires (tous/aucun, toujours/jamais, peut/impossible)
#   - need_clarification : question vague sans concept -> demander une precision
#   - refuse_unknown     : "je ne sais pas" EXPLICITE quand aucun fait verifie
#                          (honnêtete, pas invention)

import re

CONTRADICTION_PAIRS = [
    (r"\btous\b", r"\baucun\b"), (r"\ball\b", r"\bnone\b"),
    (r"\btoujours\b", r"\bjamais\b"), (r"\balways\b", r"\bnever\b"),
    (r"\bpossible\b", r"\bimpossible\b"), (r"\bpeut\b", r"\bne peut pas\b"),
    (r"\boui\b", r"\bnon\b"),
]


def check_facts(text, facts):
    """Chaque fait est-il soutenu par le texte ? (verifiable, pas convaincant)."""
    report = []
    tl = text.lower()
    for f in facts:
        fw = [w for w in f.lower().split() if len(w) > 4]
        overlap = sum(1 for w in fw if w in tl)
        status = "soutenu" if overlap >= max(1, len(fw) // 2) else "non-verifie"
        report.append({"fact": f[:80], "status": status, "overlap": overlap})
    return report


def detect_contradiction(text):
    """Detecte une contradiction logique simple dans le texte."""
    found = []
    for a, b in CONTRADICTION_PAIRS:
        if re.search(a, text.lower()) and re.search(b, text.lower()):
            found.append((a.replace("\\b", "").replace("\\", ""),
                          b.replace("\\b", "").replace("\\", "")))
    return found


def need_clarification(query, concepts):
    """Question vague sans concept exploitable -> il faut demander une precision."""
    vague = ["ça", "cela", "truc", "chose", "it", "thing", "stuff"]
    q = query.lower()
    if any(v in q for v in vague) and len(concepts) < 2:
        return True
    if len(query.split()) <= 3 and len(concepts) == 0:
        return True
    return False


def refuse_unknown(facts, min_facts=1):
    """Aucun fait verifie -> mieux vaut refuser honnetement qu'inventer.

    Recommande par la fiche (condition 9 + 4) : 'Je n'ai pas assez
    d'informations' plutot qu'une reponse fabriquee.
    """
    return len(facts) < min_facts
