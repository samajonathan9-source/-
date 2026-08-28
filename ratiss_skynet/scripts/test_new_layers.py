#!/usr/bin/env python3
# RATISS-skynet : test des 3 nouvelles couches (boucle fermee, emotions, RLMxKTN).
# + test quantique Grover (rapide, sans LLM).

import os
import sys
import json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.abspath(os.path.join(REPO_ROOT, "..", "models", "SmolLM2-135M-Instruct"))

from skynet.confidence import TopologicalConfidence, lexical_uniqueness
from skynet.thermo_emotions import EmotionEngine, ThermoEnvironment
from skynet.quantum_select import grover_amplify, select_grover


def test_confidence():
    """Boucle fermee : le score distingue bon/mauvais."""
    print("=== COUCHE 1 : BOUCLE FERMEE (confiance) ===")
    tc = TopologicalConfidence()
    good = "Un trou noir est une region de l'espace-temps ou la gravite est si forte que rien ne s'echappe."
    bad = "trou noir trou noir trou noir il est il est il est trou noir"
    s_good, _ = tc.score(good, psig=95.0, facts=["Un trou noir est une region de l'espace-temps ou la gravite est forte."])
    s_bad, _ = tc.score(bad, psig=20.0, facts=[])
    print(f"  bonne reponse : {s_good}/100 ({tc.verdict(s_good)})")
    print(f"  mauvaise      : {s_bad}/100 ({tc.verdict(s_bad)})")
    ok = s_good > s_bad and s_good >= 70 and s_bad < 40
    print(f"  -> {'OK' if ok else 'ECHEC'} : la confiance distingue bon/mauvais")
    return ok


def test_thermo_emotions():
    """ETH : les emotions thermodynamiques modulent la generation."""
    print("\n=== COUCHE 2 : EMOTIONS THERMODYNAMIQUES (ETH) ===")
    eng = EmotionEngine()
    # etat de base
    base = eng.current_emotion()
    print(f"  etat de base  : {base['label']} (HR={base['heart_rate']}, tension={base['tension']})")
    # perturbation peur
    r1 = eng.step("J'ai peur du danger de la mort")
    print(f"  apres 'peur'  : {r1['emotion']['label']} (HR={r1['emotion']['heart_rate']}, tension={r1['emotion']['tension']})")
    print(f"    modulation  : temperature={r1['modulation']['temperature']}, ktn_seuil={r1['modulation']['ktn_threshold']}")
    eng2 = EmotionEngine()
    r2 = eng2.step("Merci beaucoup, quelle joie et amour")
    print(f"  apres 'joie'  : {r2['emotion']['label']} (HR={r2['emotion']['heart_rate']})")
    print(f"    modulation  : temperature={r2['modulation']['temperature']}, tone={r2['modulation']['tone']}")
    # l'emotion CHANGE les parametres : temperature differente
    ok = (r1["modulation"]["temperature"] != r2["modulation"]["temperature"] and
          r1["modulation"]["ktn_threshold"] != r2["modulation"]["ktn_threshold"])
    print(f"  -> {'OK' if ok else 'ECHEC'} : l'emotion module la generation")
    return ok


def test_quantum_grover():
    """Grover : amplification vers les candidats coherents."""
    print("\n=== COUCHE 3 : SELECTION QUANTIQUE (Grover) ===")
    # 8 candidats : 1 tres coherent, 7 moyens/faibles
    scores = np.array([10, 12, 8, 95, 11, 9, 13, 10], dtype=float)
    probs = grover_amplify(scores)
    idx, _ = select_grover(["c%d" % i for i in range(8)], scores)
    print(f"  scores bruts   : {scores.astype(int).tolist()}")
    print(f"  prob Grover    : {[round(float(p),3) for p in probs]}")
    print(f"  selectionne    : candidat #{idx} (score={scores[idx]})")
    ok = idx == 3  # le plus coherent doit etre selectionne
    print(f"  -> {'OK' if ok else 'ECHEC'} : Grover amplifie le candidat coherent")
    return ok


def test_rlm_ktn():
    """RLM x KTN : decomposition recursive + regeneration cristalline."""
    print("\n=== COUCHE 4 : RLM x KTN (recursion + repliement) ===")
    from skynet.hybrid_mind import HybridMind
    from skynet.rlm_layer import RecursiveLayer, decompose
    # decomposition pure (sans LLM)
    q = "Qu'est-ce qu'un trou noir ? Et puis explique la coherence topologique ?"
    parts = decompose(q)
    print(f"  decomposition  : {len(parts)} sous-questions")
    for p in parts:
        print(f"    - {p[:60]}")
    ok = len(parts) >= 2

    # recursion complete (avec LLM)
    mind = HybridMind(MODEL_DIR)
    rlm = RecursiveLayer(mind, max_depth=2)
    res = rlm.solve("Qu'est-ce qu'un trou noir ?", language="fr")
    print(f"  recursion      : sentence={res['sentence'][:70]}")
    print(f"    confiance    : {res.get('confidence_score', 0)}/100")
    print(f"    ktn_collapsed: {res.get('ktn_collapsed', False)}")
    ok = ok and "sentence" in res
    print(f"  -> {'OK' if ok else 'ECHEC'} : RLM decompose et repond")
    return ok


def main():
    print("RATISS-skynet : TEST DES 4 NOUVELLES COUCHES")
    print("=" * 70)
    results = {
        "boucle_fermee": test_confidence(),
        "emotions_thermo": test_thermo_emotions(),
        "quantum_grover": test_quantum_grover(),
        "rlm_ktn": test_rlm_ktn(),
    }
    print("\n" + "=" * 70)
    n = sum(results.values())
    print(f"RESULTAT : {n}/4 couches OK")
    out = os.path.join(REPO_ROOT, "artifacts", "new_layers_test.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"rapport : {out}")


if __name__ == "__main__":
    main()
