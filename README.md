# RATISS-Skynet

**HYBRID MIND — la fusion de la Loi de Cohérence Topologique (LCT) et d'un LLM léger.**

> *Pas une compétition. Une symbiose : le LLM parle, la topologie le stabilise, le cristal régénère.*

[![Modèle](https://img.shields.io/badge/LLM-SmolLM2--135M-4f9cff)](#)
[![Langues](https://img.shields.io/badge/langues-FR%20%2F%20EN-00b894)](#)
[![Licence](https://img.shields.io/badge/licence-propri%C3%A9taire-d97706)](#)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--4092--5313-a6ce39)](https://orcid.org/0009-0000-4092-5313)

Projet de **Jonathan Evina** (RATIS Labs, 🇨🇲) avec son CTO technique (OpenHands).
Propriété intellectuelle : **JOHNKING0 & Jonathan Evina**.

**Règles de la maison** : *jamais figé, toujours itérer — la transdisciplinarité d'abord — la preuve par le fonctionnement — on n'est pas là pour se lamenter quand ça échoue.*

---

![Architecture HYBRID MIND](ratiss_skynet/docs/images/hybrid_mind_architecture.png)

---

## 🧠 L'architecture unifiée : HYBRID MIND

Une **seule** architecture, dans [`ratiss_skynet/skynet/hybrid_mind.py`](ratiss_skynet/skynet/hybrid_mind.py).
Six capacités fusionnées, dans l'ordre du pipeline :

| # | Capacité | Rôle | Principe |
|---|---|---|---|
| 0 | 💗 **RESSENTIR** | Corps thermodynamique simulé (ETH) | L'émotion **émerge** et **module** la génération |
| 1 | 🧭 **COMPRENDRE** | Concepts + faits vérifiés bilingues | Anti-hallucination (RATIS-Net) |
| 2 | 🗣️ **PARLER** | Le LLM génère, la topologie sélectionne | SmolLM2-135M + génération guidée LCT |
| 3 | 💎 **RÉGÉNÉRER** | Repliement cristallin si motif brisé | **KTN:Li**, seuil modulé par la tension |
| 4 | 🔄 **BOUCLE FERMÉE** | Score de confiance topologique **0-100%** | Auditabilité temps réel (pas softmax) |
| 5 | 🔏 **PROUVER** | Empreinte SHA-256 du sous-graphe actif | Reproductibilité |

**Couches expérimentales du laboratoire** (on teste, on itère) :

| Couche | Idée | Statut |
|---|---|---|
| 🔁 **RLM × KTN** (`rlm_layer.py`) | Décomposition récursive des questions complexes + repliement cristallin par maillon faible | ✅ testée |
| ⚛️ **Grover** (`quantum_select.py`) | Amplification d'amplitude vers les candidats cohérents (inspiré de l'algo quantique) | ✅ testée (1 bon/8 → p=0.76) |
| 🧩 **Induction few-shot** (`arc_induction.py`) | Apprendre une règle inconnue en 3 exemples (critère central AGI) — la règle juste préserve la signature topologique | ✅ démontrée |
| 🧠 **Mémoire contrôlée** (`memory.py`) | Épisodique + sémantique + procédurale, chaîne SHA-256 infalsifiable → transfert inter-domaines | ✅ démontrée |
| 🧭 **Planificateur topologique** (`planner.py`) | Autonomie : chemin de persistance (TPP) + carte de tension (MSTM) + descente vers invariant (RTD) + motifs de plans (PNE) | ✅ démontrée |

📊 **Évaluation face aux 10 conditions d'une vraie AGI** (fiche Manus AI) :
9 démontrées, 0 partielle, 1 absente (perception, gelée volontairement) — analyse honnête dans
[`artifacts/RAPPORT_AGI.md`](ratiss_skynet/artifacts/RAPPORT_AGI.md).

**La clef : la génération guidée par LCT** (`draft_guided`). Le LLM propose N candidats ;
la topologie — **P_sig**, la persistance homologique du graphe de corrélations —
**sélectionne** le plus cohérent. La loi est figée : `R = P_sig`, `ΔW = η·φ·P_sig·C`.

---

## 🔬 Preuve par le fonctionnement

| Question | LLM brut | HYBRID MIND | Verdict |
|---|---|---|---|
| *What is a black hole?* (EN) | cohérence 65 | **cohérence 97.5** | ⬆ transformé |
| *Qu'est-ce qu'un trou noir ?* (FR) | boucle pure | **cohérence 36 → 117, boucle CASSÉE** | ⬆ transformé |
| *Raconte une histoire de dragon.* (FR) | boucle | **unicité 0.42 → 0.85, boucle CASSÉE** | ⬆ transformé |

**3/3 cas** : la sélection topologique **casse les boucles de répétition** d'un petit
LLM de 135M paramètres et **augmente la cohérence**. La fusion ne donne pas des
connaissances au modèle — elle **stabilise et sélectionne** sa parole.

---

## 📦 Le repo

```
ratiss-Skynet/
├── models/SmolLM2-135M-Instruct/   # le LLM (Git LFS, 257 Mo)
└── ratiss_skynet/                  # ⭐ le code + les preuves
    ├── skynet/
    │   ├── hybrid_mind.py          #    l'architecture unifiée (pipeline complet)
    │   ├── confidence.py           #    🔄 boucle fermée (confiance 0-100%)
    │   ├── thermo_emotions.py      #    💗 émotions thermodynamiques (ETH)
    │   ├── rlm_layer.py            #    🔁 RLM récursif × KTN:Li
    │   └── quantum_select.py       #    ⚛️ sélection Grover-amplifiée
    ├── scripts/                    #    diagnostics, H1, démos, tests
    ├── artifacts/                  #    rapports JSON + SHA-256
    └── README.md                   #    documentation complète
```

👉 **Documentation complète : [`ratiss_skynet/README.md`](ratiss_skynet/README.md)**

## 🚀 Démarrer

```bash
git clone https://github.com/samajonathan9-source/ratiss-Skynet.git
cd ratiss-Skynet && git lfs pull
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install transformers peft scipy numpy gudhi
cd ratiss_skynet && python scripts/test_transform_fast.py
```

---

*© 2026 JOHNKING0 & Jonathan Evina.* La loi LCT est figée. Le reste, jamais.
