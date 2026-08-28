# 🚀 Démarrage rapide — RATIS (MCT)

Installer et faire tourner RATIS en 5 minutes.

---

## 1. Installation

```bash
git clone https://github.com/samajonathan9-source/ratiss-Skynet.git
cd ratiss-Skynet/ratiss_skynet
pip install torch transformers numpy scipy matplotlib
```

Le moteur de génération (SmolLM2-135M, le « corps » du MCT) est dans `models/`
via Git LFS. Si les poids sont un pointeur LFS, ils sont téléchargés
automatiquement au premier usage.

## 2. Premier contact

```python
from skynet.hybrid_mind import HybridMind

mind = HybridMind("models/SmolLM2-135M-Instruct")

# RATIS sait ce qu'il est
print(mind.who_am_i())

# Une question
r = mind.respond("Qu'est-ce qu'un trou noir ?", language="fr")
print(r["sentence"])
print(f"Confiance : {r['confidence_score']}/100 — {r['confidence_verdict']}")
print(f"Preuve : {r['proof']}")
```

## 3. Lancer les tests

```bash
# les 9 conditions AGI
python scripts/test_agi_conditions.py   # conditions 2, 3, 5
python scripts/test_greening.py          # conditions 1, 4, 7, 10
python scripts/test_planner.py           # condition 6 (planificateur)
python scripts/test_new_layers.py        # confiance, émotions, RLM, Grover
```

## 4. La démo complète

```bash
python scripts/demo_agile_mind.py
```

Produit `artifacts/agile_mind_demo.json` avec réponses, émotions, confiance
et preuves SHA-256.

---

## ⚠️ Ce que RATIS fera (et ne fera pas)

- ✅ Répondre avec un **score de confiance** et une **preuve**
- ✅ Dire **« je ne sais pas »** plutôt qu'inventer
- ✅ **Refuser** les intentions néfastes (garde-fou)
- ✅ **Demander une précision** si la question est vague
- ✅ **Se replier** (KTN:Li) plutôt que boucler
- ❌ Halluciner avec assurance — c'est précisément ce que le MCT élimine

---

*Prochaine étape : [ARCHITECTURE.md](ARCHITECTURE.md) pour comprendre le
pipeline, ou [MANIFESTE_MCT.md](MANIFESTE_MCT.md) pour la vision.*
