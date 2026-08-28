#!/usr/bin/env python3
# RATISS-skynet : test RAPIDE de transformation du LLM (135M).
# Principe juste : le modele n'a pas ete entraine sur la topologie,
# donc on ne mesure PAS la connaissance, mais si la fusion LCT ameliore
# la COHERENCE et reduit les boucles/hallucinations sur CE qu'il peut dire.

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.abspath(os.path.join(REPO_ROOT, "..", "models", "SmolLM2-135M-Instruct"))

from skynet.hybrid_mind import HybridMind

TESTS = [
    ("What is a black hole?", "en"),
    ("Qu'est-ce qu'un trou noir ?", "fr"),
    ("Raconte une histoire de dragon.", "fr"),
]


def count_repetition(text):
    """Score de repetition : 1.0 = pas de boucle, 0.0 = boucle pure."""
    words = text.split()
    if len(words) < 2:
        return 1.0
    return round(len(set(words)) / len(words), 3)


def main():
    print("RATISS-skynet : TRANSFORMATION du LLM 135M (test juste)")
    print("=" * 70)
    mind = HybridMind(MODEL_DIR)

    rows = []
    for q, lang in TESTS:
        # BRUT : generation libre, 1 seul passage
        raw = mind.draft(q, facts=[], language=lang, max_new_tokens=40)
        raw_coh = mind.coherence(raw)
        raw_rep = count_repetition(raw)

        # HYBRIDE : guide LCT (2 candidats), dedup, ancrage faits
        u = mind.understand(q, lang)
        hyb, hyb_score = mind.draft_guided(q, u["facts"], lang,
                                           max_new_tokens=40, n_candidates=2)
        hyb_rep = count_repetition(hyb)

        better_rep = hyb_rep > raw_rep
        better_coh = hyb_score > raw_coh
        transforme = better_rep or better_coh
        rows.append({
            "query": q, "lang": lang,
            "brut": {"text": raw, "coherence": round(raw_coh, 2), "unicite": raw_rep},
            "hybride": {"text": hyb, "coherence": round(hyb_score, 2), "unicite": hyb_rep},
            "transforme": transforme,
        })
        print(f"\nQ [{lang}]: {q}")
        print(f"  BRUT    coh={raw_coh:5.1f} uniq={raw_rep} | {raw[:70]}")
        print(f"  HYBRIDE coh={hyb_score:5.1f} uniq={hyb_rep} | {hyb[:70]}")
        print(f"  -> moins de boucle: {'OUI' if better_rep else 'non'} | "
              f"plus coherent: {'OUI' if better_coh else 'non'}")

    n = sum(r["transforme"] for r in rows)
    print("\n" + "=" * 70)
    print(f"transformation observee : {n}/{len(rows)} cas")
    out = os.path.join(REPO_ROOT, "artifacts", "transform_fast.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"rapport : {out}")


if __name__ == "__main__":
    main()
