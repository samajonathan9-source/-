# RATISS-skynet : COUCHE RLM (Recursive Language Model) x KTN:Li.
#
# Principe RLM : une question complexe est DECOMPOSEE en sous-questions,
# chacune resolue recursivement (profondeur bornee), puis les reponses
# partielles sont FUSIONNEES en une reponse coherente.
#
# Couplage KTN:Li : a chaque niveau de recursion, le score de confiance
# topologique agit comme CRISTAL DE REFERENCE. Si la confiance tombe sous
# le seuil (motif brise = hallucination), le sous-module est REGENERE par
# repliement cristallin : on se rabat sur le fait verifie le plus proche
# (le motif stable du reseau), comme le cristal KTN:Li qui retrouve sa
# structure apres perturbation.
#
# C'est la brique qui rapproche HYBRID MIND des criteres AGI :
#   - decomposer un probleme jamais vu (generalisation)
#   - surveiller sa propre confiance (auto-controle)
#   - se corriger soi-meme (regeneration, pas repetition)

import numpy as np


CONNECTORS_FR = ["et puis", "ensuite", "et aussi", "puis", "et enfin"]
QUESTION_MARKS = ["?", " ?", "。","；", ";"]


def decompose(query):
    """Decompose une question composee en sous-questions simples.

    Heuristique legere : split sur les marqueurs multi-questions et les
    connecteurs enumeratifs. Retourne au moins 1 sous-question.
    """
    q = query.strip()
    parts = [q]
    # split sur plusieurs '?' (questions en rafale)
    if q.count("?") > 1:
        parts = [p.strip() + "?" for p in q.split("?") if p.strip()]
    elif len(q.split()) > 18:
        # longue question : split sur connecteurs enumeratifs
        for conn in CONNECTORS_FR:
            if conn in q.lower():
                idx = q.lower().index(conn)
                parts = [q[:idx].strip(), q[idx + len(conn):].strip()]
                break
    return [p for p in parts if len(p.split()) >= 2] or [q]


class RecursiveLayer:
    """Couche RLM : recursion bornee + regeneration cristalline KTN:Li."""

    def __init__(self, mind, max_depth=2, ktn_threshold=0.30):
        self.mind = mind              # HybridMind
        self.max_depth = max_depth
        self.ktn_threshold = ktn_threshold
        self.recursion_log = []

    def _respond_atomic(self, query, language, depth):
        """Reponse atomique (non recursive) + confiance + eventuelle regen."""
        res = self.mind.respond(query, language=language, guided=True)
        conf = res.get("confidence_score", 0.0)
        regenerated = res.get("regenerated", False)
        # KTN:Li : si confiance critique ET faits dispo, repliement cristallin
        if conf < self.ktn_threshold * 100 and res.get("facts"):
            # repliement : la reponse devient le fait verifie le plus proche
            res["sentence"] = res["facts"][0]
            res["ktn_collapsed"] = True
            conf = max(conf, 55.0)  # un fait verifie est au moins fiable
        else:
            res["ktn_collapsed"] = False
        self.recursion_log.append({
            "depth": depth, "query": query[:60],
            "confidence": conf, "regenerated": regenerated,
            "ktn_collapsed": res["ktn_collapsed"],
        })
        return res

    def solve(self, query, language=None, depth=0):
        """Resolution recursive avec decomposition et fusion."""
        parts = decompose(query) if depth == 0 else [query]
        if len(parts) <= 1 or depth >= self.max_depth:
            return self._respond_atomic(query, language, depth)

        # recursion sur chaque sous-question
        sub_results = []
        for p in parts:
            sub = self.solve(p, language=language, depth=depth + 1)
            sub_results.append(sub)

        # fusion : combiner les reponses partielles coherentes
        sentences = [s["sentence"] for s in sub_results if s.get("sentence")]
        fused = " ".join(sentences)
        # confiance de la fusion = min des confiances (maillon faible)
        confs = [s.get("confidence_score", 0) for s in sub_results]
        conf_fused = min(confs) if confs else 0.0

        all_facts = []
        all_concepts = []
        for s in sub_results:
            all_facts.extend(s.get("facts", []))
            all_concepts.extend(s.get("concepts", []))

        return {
            "query": query, "sentence": fused, "language": language or "fr",
            "concepts": all_concepts[:10], "facts": all_facts[:5],
            "confidence_score": conf_fused,
            "decomposed": True, "n_parts": len(parts),
            "sub_confidences": confs,
            "ktn_collapsed": any(s.get("ktn_collapsed") for s in sub_results),
            "recursion_log": list(self.recursion_log),
        }
