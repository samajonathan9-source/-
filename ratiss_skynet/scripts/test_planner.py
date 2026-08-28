#!/usr/bin/env python3
# RATISS-skynet : test du PLANIFICATEUR TOPOLOGIQUE (condition AGI n°6).
# TPP (chemin de persistance) + MSTM (carte de tension) + RTD (descente).

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.abspath(os.path.join(REPO_ROOT, "..", "models", "RATISS-One"))

from skynet.hybrid_mind import HybridMind
from skynet.planner import TopologicalPlanner, TensionMap, state_persistence
import numpy as np


def test_tension_map():
    """MSTM : confiance globale = produit des persistances (maillon faible)."""
    print("=== MSTM : carte de tension multi-echelle ===")
    tm = TensionMap()
    tm.add("etape stable A", 0.90, "stable")
    tm.add("etape stable B", 0.85, "stable")
    tm.add("etape FRAGILE", 0.20, "fragile")
    conf = tm.global_confidence()
    weak = tm.weakest_link()
    print(tm.render())
    # un maillon faible doit effondrer la confiance globale
    ok = conf < 20 and weak["name"] == "etape FRAGILE"
    print(f"  -> {'OK' if ok else 'ECHEC'} : le maillon faible effondre le plan "
          f"(confiance globale = {conf}/100)")
    return ok


def test_persistence():
    """TPP : un etat coherent a une persistance plus haute qu'un etat chaotique."""
    print("\n=== TPP : persistance d'etat ===")
    embed = lambda t: np.array([len(t) / 50.0, t.count("trou") / 3.0])
    coherent = ["trou noir gravite", "trou noir espace-temps", "trou noir lumiere"]
    chaotic = ["trou noir", "banane velo", "xyzzy quantum football"]
    p_coh = state_persistence(coherent, embed)
    p_cha = state_persistence(chaotic, embed)
    print(f"  etat coherent  : P={p_coh:.3f}")
    print(f"  etat chaotique : P={p_cha:.3f}")
    ok = p_coh > p_cha
    print(f"  -> {'OK' if ok else 'ECHEC'} : la persistance distingue coherent/chaotique")
    return ok


def test_full_planner():
    """Plan complet : decomposition + tension + descente RTD."""
    print("\n=== PLANIFICATEUR COMPLET (TPP+MSTM+RTD) ===")
    mind = HybridMind(MODEL_DIR)
    planner = TopologicalPlanner(mind, critical_tension=0.70)
    objective = "Expliquer la coherence topologique et ses applications"
    result = planner.plan(objective, language="fr")
    print(f"  objectif : {objective}")
    print(f"  etapes   : {result['n_steps']}")
    for s in result["plan"]:
        tag = " [DESCENTE]" if s.get("descended") else ""
        print(f"    - P={s['persistence']:.2f} {s['task'][:55]}{tag}")
    print(f"  confiance globale : {result['global_confidence']}/100")
    print(f"  transfert memoire : {result['transferred_from_memory']}")
    print("  trace :")
    for t in result["trace"]:
        print(f"    {t}")
    ok = result["n_steps"] >= 2 and result["global_confidence"] > 0
    print(f"  -> {'OK' if ok else 'ECHEC'} : plan topologique construit")
    return ok, result


def main():
    print("RATISS-skynet : PLANIFICATEUR TOPOLOGIQUE (condition AGI n°6)")
    print("=" * 70)
    ok1 = test_tension_map()
    ok2 = test_persistence()
    ok3, result = test_full_planner()
    print("\n" + "=" * 70)
    n = sum([ok1, ok2, ok3])
    print(f"RESULTAT : {n}/3 tests du planificateur")
    out = os.path.join(REPO_ROOT, "artifacts", "planner_test.json")
    # rendre serialisable
    result_ser = {k: v for k, v in result.items() if k != "execution"}
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"mstm": ok1, "tpp": ok2, "planner": ok3,
                   "plan": result_ser}, f, indent=2, ensure_ascii=False)
    print(f"rapport : {out}")


if __name__ == "__main__":
    main()
