# RATISS-skynet

**POC — Couplage Loi de Cohérence Topologique (LCT) × LLM léger (Qwen2-0.5B)**

> *Rendre le fine-tuning ultra-léger via une architecture guidée par la topologie.*

Projet ouvert par **Jonathan Evina** (ORCID 0009-0000-4092-5313) avec son CTO technique (OpenHands/agents). Propriété intellectuelle : **JOHNKING0 & Jonathan Evina**.

**Règle de la maison** : *jamais figé, toujours itérer — la transdisciplinarité prime sur la spécialisation. La preuve par le fonctionnement est la plus concrète.*

---

## 🧭 Pourquoi

La Loi LCT a été validée sur des milieux physiques — cristaux ferroélectriques (KTN:Li, Nature 2026), protéines, QPU IBM. Question : peut-elle **guider l'apprentissage d'un LLM** ? Un LLM statistique travaille avec le connu ; nous, on crée. Ce POC teste notre loi sur un quatrième milieu : **les activations d'un transformer**.

Objectif : **preuve par le fonctionnement** — pas une publication. Un contraste topologique interprétable + un LoRA ciblé qui bat le LoRA uniforme à budget égal ou réduit.



---

## 🏗️ Architecture du POC

```
Qwen2-0.5B (safetensors)
   └─ hooks PyTorch → activations par couche/tête
        └─ graphe de corrélations entre neurones (Vietoris-Rips GF(2))
             └─ score LCT par couche : P_sig + edge − 0,1×entropie
                  └─ H1 : LoRA ciblé (rang élevé sur zones critiques, faible sur zones stables)
                       └─ benchmark : perplexité + robustesse vs LoRA uniforme
```

**Réutilisation** : `ratiss/topo/science_core.py` (AEON ODV fusionné — rips_persistence, P_sig, LCT) + modules LLM de RATIS-Net (tokenizers, rankers, preuves SHA-256.. — le cerveau RATISS pilote le projet, pas de réinvention.



---

## 📦 Structure

```
ratiss_skynet/
├── ratiss/
│   ├── topo/science_core.py      # AEON ODV fusionné (P_sig, LCT, Vietoris-Rips)
│   └── llm/                      # briques RATIS-Net (tokenizers, rankers, proofs)
├── skynet/
│   ├── activations.py            # hooks PyTorch + capture
│   ├── topology.py               # graphe de corrélations + score LCT par couche
│   ├── lora_guided.py          # H1 — LoRA ciblé par score LCT
│   └── benchmark.py             # perplexité + robustesse (catastrophic forgetting, adversarial)
├── scripts/
│   ├── phase0_setup.sh          # env + modèle
│   ├── diagnose_lct.py          # POC diagnostic — contraste LCT sur activations
│   └── run_h1.py               # H1 — LoRA ciblé vs uniforme
└── tests/
    └── test_topology.py        # tests du pipeline topologique
```

---

## 🚀 Démarrer (Phase 0)

```bash
bash scripts/phase0_setup.sh          # installe deps + modèle (ou snapshot_download)
python scripts/diagnose_lct.py --synth # POC immédiat sur activation simulée (sans GPU)
python scripts/diagnose_lct.py         # avec le vrai Qwen2-0.5B (si torch + modèle dispo)
```

---

## 🎯 Critères de succès (maison, par le fonctionnement)

1. **Phase  ာ1** : le score LCT montre un **contraste** entre couches (pas plat) — test statistique(p < 0.05 sur la variance inter-couches)
2. **H1** : le **LoRA ciblé** égale ou dépasse le **LoRA uniforme** avec **≥20% de paramètres en moins**.
3. Chaque résultat est accompagné d'une **preuve SHA-256** du sous-graphe(s) qui a déclenché le contraste.



---

## Limites honnêtes (documentées au fur et à měre

- Le lien topologie physique ↔ dynamique d'un réseau de neurones n'est **pas encore démontré** — c'est exactement ce que ce POC teste.

---

*© 2026 JOHNKING0 & Jonathan Evina*. Projet privé. La loi LCT est FIGÉE (`R = P_sig`, `ΔW = η·φ·P_sig·C`). Ne la change jamais.