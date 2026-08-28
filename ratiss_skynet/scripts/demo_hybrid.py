#!/usr/bin/env python3
# RATISS-skynet : demo de l'architecture unifiee HYBRID MIND.
# Tests de langue FR + EN : comprendre, parler, ressentir, prouver, regenerer.

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.abspath(os.path.join(REPO_ROOT, "..", "models", "SmolLM2-135M-Instruct"))

from skynet.hybrid_mind import HybridMind

# Tests de langue : FR + EN, faits connus + question piege (hallucination)
QUERIES = [
    "Qu'est-ce qu'un trou noir ?",                 # FR, fait connu
    "Explique la coherence topologique.",           # FR, fait connu
    "What is a black hole?",                        # EN, fait connu
    "What is persistent homology?",                 # EN, fait connu
    "Raconte-moi une histoire sur un dragon.",      # FR, PAS de fait -> LLM libre
]


def main():
    print("RATISS-skynet : HYBRID MIND — tests de langue FR/EN")
    print("=" * 70)
    mind = HybridMind(MODEL_DIR)

    results = []
    for q in QUERIES:
        res = mind.respond(q)
        results.append(res)
        print(f"\nQ ({res['language']}): {q}")
        print(f"  concepts : {res['concepts'][:6]}")
        print(f"  faits    : {len(res['facts'])} trouve(s)")
        if res["facts"]:
            print(f"             -> {res['facts'][0][:80]}...")
        print(f"  emotion  : {res['emotion']['label']} "
              f"(val={res['emotion']['valence']}, aro={res['emotion']['arousal']})")
        print(f"  coherence topologique : {res['coherence']}")
        print(f"  regeneration KTN:Li   : {'OUI' if res['regenerated'] else 'non'}")
        print(f"  reponse  : {res['sentence'][:150]}")
        print(f"  preuve   : {res['proof']['digest'][:20]}... "
              f"({res['proof']['n_concepts']} concepts, {res['proof']['n_facts']} faits)")

    outpath = os.path.join(REPO_ROOT, "artifacts", "hybrid_demo.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\n" + "=" * 70)
    print(f"rapport ecrit: {outpath}")


if __name__ == "__main__":
    main()
