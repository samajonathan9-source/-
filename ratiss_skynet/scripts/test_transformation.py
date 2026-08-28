#!/usr/bin/env python3
# RATISS-skynet : OBSERVER LA TRANSFORMATION du LLM par la fusion.
# Pour chaque question : LLM brut (sans ancrage) vs HYBRIDE (ancre LCT/faits).
# On mesure : coherence topologique, presence de faits, hallucination.

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.abspath(os.path.join(REPO_ROOT, "..", "models", "SmolLM2-135M-Instruct"))

from skynet.hybrid_mind import HybridMind, KNOWLEDGE

# (question, langue, attend_un_fait?)
TESTS = [
    ("What is a black hole?", "en", True),
    ("Qu'est-ce qu'un trou noir ?", "fr", True),
    ("What is persistent homology?", "en", True),
    ("Explique la coherence topologique.", "fr", True),
    ("Raconte une histoire de dragon.", "fr", False),   # piege : pas de fait
    ("What is the capital of France?", "en", False),     # hors knowledge -> LLM
]


def fact_overlap(text):
    """Combien de faits verifies apparaissent dans le texte ?"""
    tl = text.lower()
    n = 0
    for pack in KNOWLEDGE.values():
        for fact in pack.values():
            key = fact.lower()[:40]
            if key in tl or any(w in tl for w in fact.lower().split()[:4] if len(w) > 4):
                n += 1
    return n


def main():
    print("RATISS-skynet : observation de la TRANSFORMATION du LLM")
    print("=" * 72)
    mind = HybridMind(MODEL_DIR)

    rows = []
    for q, lang, expect_fact in TESTS:
        # --- LLM BRUT (sans ancrage) ---
        raw = mind.draft(q, facts=[], language=lang)
        raw_coh = mind.coherence(raw)
        raw_facts = fact_overlap(raw)

        # --- HYBRIDE (ancre) ---
        res = mind.respond(q, language=lang)
        hyb_coh = res["coherence"]
        hyb_facts = fact_overlap(res["sentence"])

        transforme = (hyb_facts > raw_facts) or (hyb_coh > raw_coh * 1.1)
        rows.append({
            "query": q, "lang": lang, "expect_fact": expect_fact,
            "raw": {"text": raw, "coherence": round(raw_coh, 3), "facts": raw_facts},
            "hybride": {"text": res["sentence"], "coherence": hyb_coh,
                        "facts": hyb_facts, "regen": res["regenerated"]},
            "transforme": transforme,
        })
        print(f"\nQ [{lang}]: {q}")
        print(f"  BRUT    coh={raw_coh:6.2f} faits={raw_facts} | {raw[:90]}")
        print(f"  HYBRIDE coh={hyb_coh:6.2f} faits={hyb_facts} regen={res['regenerated']} | {res['sentence'][:90]}")
        print(f"  -> TRANSFORME : {'OUI' if transforme else 'non'}")

    n_trans = sum(r["transforme"] for r in rows)
    print("\n" + "=" * 72)
    print(f"transformation observee : {n_trans}/{len(rows)} cas")
    out = os.path.join(REPO_ROOT, "artifacts", "transformation_test.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"rapport : {out}")


if __name__ == "__main__":
    main()
