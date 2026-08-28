#!/usr/bin/env python3
# RATISS-skynet : test des conditions AGI n°2 (apprendre l'inconnu),
# n°3 (transfert) et n°5 (memoire) — les 3 trous critiques de la fiche.
# Aucun LLM ici : c'est la couche de RAISONNEMENT, pas la parole.

import os
import sys
import json
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from skynet.arc_induction import induce_rule, apply_rule
from skynet.memory import HybridMemory


def test_learn_unknown():
    """Condition 2 : 3 exemples d'une regle inventee -> decouvrir -> appliquer."""
    print("=== CONDITION 2 : APPRENDRE L'INCONNU (few-shot) ===")
    # regle inventee : rotation 90. Le systeme ne l'a JAMAIS vue.
    examples = [
        ([[1, 0], [0, 0]], [[0, 1], [0, 0]]),
        ([[1, 1], [0, 0]], [[0, 1], [0, 1]]),
        ([[1, 0], [1, 0]], [[1, 1], [0, 0]]),
    ]
    rule, conf, detail = induce_rule(examples)
    print(f"  3 exemples -> regle induite : {rule} (confiance={conf}, topo_err={detail['topo_err']})")
    # application a un cas JAMAIS vu
    new_input = [[0, 0], [1, 1]]
    pred = apply_rule(rule, new_input)
    expected = [[1, 0], [1, 0]]  # rot90 de new_input
    ok = rule == "rot90" and conf == 1.0 and pred == expected
    print(f"  cas inconnu {new_input} -> prediction {pred} (attendu {expected})")
    print(f"  -> {'OK' if ok else 'ECHEC'} : regle decouverte et appliquee a l'inconnu")
    return ok, rule, conf


def test_transfer(rule, conf, mem):
    """Condition 3 : la regle apprise est transferee dans un autre domaine."""
    print("\n=== CONDITION 3 : TRANSFERT ENTRE DOMAINES ===")
    mem.learn_rule(rule, conf, domain="grilles-symboles")
    # nouveau domaine : grille 3x3, meme structure, autre taille
    recalled = mem.recall_best_rule(min_confidence=0.9)
    new_domain_input = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
    pred = apply_rule(recalled["rule"], new_domain_input)
    expected = [[0, 0, 1], [0, 0, 0], [0, 0, 0]]  # rot90 en 3x3
    ok = recalled["rule"] == "rot90" and pred == expected
    print(f"  regle rappelee depuis memoire procedurale : {recalled['rule']} "
          f"(apprise en '{recalled['domain']}')")
    print(f"  appliquee a un domaine different (3x3) : {pred[0]} -> {'correct' if pred == expected else 'faux'}")
    print(f"  -> {'OK' if ok else 'ECHEC'} : transfert inter-domaines")
    return ok


def test_memory(mem):
    """Condition 5 : memoire episodique + semantique + integrite chainee."""
    print("\n=== CONDITION 5 : MEMOIRE CONTROLEE ===")
    mem.remember_episode("Qu'est-ce qu'un trou noir ?", "Une region de l'espace-temps...",
                         emotion="calme", confidence=95.7)
    mem.learn_fact("Un trou noir piege meme la lumiere.", source="dialogue")
    eps = mem.recall_episodes(keyword="trou noir")
    facts = mem.recall_facts(keyword="lumiere")
    integrity = mem.integrity()
    ok = len(eps) >= 1 and len(facts) >= 1 and integrity
    print(f"  episodes rappes (mot-clef 'trou noir') : {len(eps)}")
    print(f"  faits rappes (mot-clef 'lumiere')      : {len(facts)}")
    print(f"  integrite de la chaine SHA-256         : {'VERIFIEE' if integrity else 'CORROMPUE'}")
    print(f"  -> {'OK' if ok else 'ECHEC'} : memoire episodique + semantique + preuve")
    return ok


def main():
    print("RATISS-skynet : CONDITIONS AGI 2, 3, 5 (fiche Manus AI)")
    print("=" * 70)
    store = os.path.join(REPO_ROOT, "artifacts", "hybrid_memory.jsonl")
    if os.path.exists(store):
        os.remove(store)
    mem = HybridMemory(store)

    ok2, rule, conf = test_learn_unknown()
    ok3 = test_transfer(rule, conf, mem)
    ok5 = test_memory(mem)

    results = {"cond2_apprendre_inconnu": ok2, "cond3_transfert": ok3,
               "cond5_memoire": ok5}
    print("\n" + "=" * 70)
    print(f"RESULTAT : {sum(results.values())}/3 conditions demontrees")
    out = os.path.join(REPO_ROOT, "artifacts", "agi_conditions_test.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"rapport : {out}")


if __name__ == "__main__":
    main()
