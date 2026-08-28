#!/usr/bin/env python3
# RATISS-skynet : DEMO INTEGREE — HYBRID MIND complet.
# Boucle fermee + emotions thermo + RLMxKTN sur questions emotionnelles.

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.abspath(os.path.join(REPO_ROOT, "..", "models", "RATISS-One"))

from skynet.hybrid_mind import HybridMind
from skynet.rlm_layer import RecursiveLayer

QUERIES = [
    "J'ai peur : c'est quoi la coherence topologique ?",
    "What is a black hole?",
]


def main():
    print("RATISS-skynet : HYBRID MIND COMPLET (confiance + emotions + RLMxKTN)")
    print("=" * 70)
    mind = HybridMind(MODEL_DIR)
    rlm = RecursiveLayer(mind, max_depth=1)
    out = []
    for q in QUERIES:
        res = rlm.solve(q)
        emo = res.get("emotion", {})
        conf = res.get("confidence_score", 0)
        print(f"\nQ : {q}")
        print(f"  emotion    : {emo.get('label','?')} (valence={emo.get('valence')}, HR={emo.get('heart_rate')})")
        print(f"  modulation : {res.get('modulation', {})}")
        print(f"  reponse    : {res['sentence'][:90]}")
        print(f"  confiance  : {conf}/100 — {res.get('confidence_verdict','')}")
        print(f"  ktn/regen  : collapsed={res.get('ktn_collapsed')} regen={res.get('regenerated', False)}")
        out.append(res)
    path = os.path.join(REPO_ROOT, "artifacts", "agile_mind_demo.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\nrapport : {path}")


if __name__ == "__main__":
    main()
