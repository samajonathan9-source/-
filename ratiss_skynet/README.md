# RATIS — du LLM au MCT : l'évolution supérieure

**RATIS est un MCT (Modèle de Compréhension Topologique) : l'évolution du LLM vers une architecture supérieure.**

> *Un LLM prédit le mot le plus probable. RATIS hérite de cette fluidité, puis ajoute l'organe qui manque au LLM : la mesure de sa propre cohérence structurelle. Là où le LLM hallucine, le MCT se replie. Là où le LLM devine, le MCT prouve.*

📚 **[Documentation complète](docs/README.md)** · 📜 **[Manifeste MCT](docs/MANIFESTE_MCT.md)** · 🧠 **[Du LLM au MCT](docs/MCT.md)** · 🚀 **[Démarrage](docs/DEMARRAGE.md)**

[![Nature](https://img.shields.io/badge/nature-MCT%20%E2%80%94%20%C3%A9volution%20du%20LLM-3fb950)](docs/MCT.md)
[![Loi](https://img.shields.io/badge/loi-LCT%20%3A%20R%20%3D%20P__sig-4f9cff)](#)
[![Identité](https://img.shields.io/badge/identit%C3%A9-scell%C3%A9e%20SHA--256-d97706)](skynet/identity.py)
[![AGI](https://img.shields.io/badge/conditions%20AGI-9%2F10%20vertes-00b894)](artifacts/RAPPORT_AGI.md)
[![Langues](https://img.shields.io/badge/langues-FR%20%2F%20EN-00b894)](#)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--4092--5313-a6ce39)](https://orcid.org/0009-0000-4092-5313)

Projet de **Jonathan Evina** (RATIS Labs, 🇨🇲) avec son CTO technique (OpenHands).
Propriété intellectuelle : **JOHNKING0 & Jonathan Evina**.

**Principes directeurs** : itération permanente — transdisciplinarité — démonstration par le fonctionnement.

---

![Architecture HYBRID MIND](docs/images/hybrid_mind_architecture.png)

![LLM vs MCT](docs/images/mct_vs_llm.png)

---

## 🧠 L'architecture unifiée : HYBRID MIND

Une **seule** architecture, intégrée dans ce repo (`skynet/hybrid_mind.py`).
Six capacités fusionnées, dans l'ordre du pipeline :

| # | Capacité | Rôle | Principe |
|---|---|---|---|
| 0 | 💗 **RESSENTIR** | Corps thermodynamique simulé (ETH) | L'émotion **émerge** et **module** la génération |
| 1 | 🧭 **COMPRENDRE** | Concepts + faits vérifiés bilingues | Anti-hallucination (RATIS-Net) |
| 2 | 🗣️ **PARLER** | Le moteur génère, la topologie sélectionne | RATISS One + génération guidée LCT |
| 3 | 💎 **RÉGÉNÉRER** | Repliement cristallin si motif brisé | **KTN:Li**, seuil modulé par la tension |
| 4 | 🔄 **BOUCLE FERMÉE** | Score de confiance topologique **0-100%** | Auditabilité temps réel (pas softmax) |
| 5 | 🔏 **PROUVER** | Empreinte SHA-256 du sous-graphe actif | Reproductibilité |

**Couches expérimentales du laboratoire** : 🔁 **RLM × KTN** (`rlm_layer.py`, décomposition récursive) · ⚛️ **Grover** (`quantum_select.py`, amplification vers les candidats cohérents) · 🧩 **Induction few-shot** (`arc_induction.py`, apprendre une règle inconnue en 3 exemples — la règle juste préserve la signature topologique) · 🧠 **Mémoire contrôlée** (`memory.py`, épisodique + sémantique + procédurale, chaîne SHA-256 infalsifiable) · 🧭 **Planificateur topologique** (`planner.py`, chemin de persistance TPP + carte de tension MSTM + descente RTD + motifs PNE).

📊 **Face aux 10 conditions d'une vraie AGI** (fiche Manus AI) : 9 démontrées, 0 partielle, 1 absente (perception, gelée volontairement) — analyse honnête dans [`artifacts/RAPPORT_AGI.md`](artifacts/RAPPORT_AGI.md).

**La clef : la génération guidée par LCT** (`draft_guided`). Le LLM propose N candidats ;
la topologie — **P_sig**, la persistance homologique du graphe de corrélations —
**sélectionne** le plus cohérent. La loi est figée : `R = P_sig`, `ΔW = η·φ·P_sig·C`.

---

## 🔬 Preuve par le fonctionnement

Test : `scripts/test_transform_fast.py` — LLM brut vs HYBRID MIND, FR + EN.

| Question | LLM brut | HYBRID MIND | Verdict |
|---|---|---|---|
| *What is a black hole?* (EN) | cohérence 65 | **cohérence 97.5** | ⬆ transformé |
| *Qu'est-ce qu'un trou noir ?* (FR) | boucle pure (« un trou noir, il est un trou noir… ») | **cohérence 36 → 117, boucle CASSÉE** | ⬆ transformé |
| *Raconte une histoire de dragon.* (FR) | boucle (« livre de dragon… ») | **unicité 0.42 → 0.85, boucle CASSÉE** | ⬆ transformé |

**3/3 cas** : la sélection topologique **casse les boucles de répétition** —
le défaut n°1 d'un petit LLM de 135M paramètres — et **augmente la cohérence**.

> Note d'honnêteté : un modèle de 135M paramètres ne peut répondre que sur ce
> qu'il a vu. La fusion ne lui donne pas des connaissances — elle **stabilise
> et sélectionne** sa parole. C'est ça, la transformation.

---

## 📜 Le chemin parcouru (tout est documenté, même les échecs)

| Phase | Question | Résultat | Verdict |
|---|---|---|---|
| **0** | Le pipeline synthétique tourne ? | Reproductible, preuve SHA-256 | ✅ |
| **1** | Capturer les vraies activations du LLM | 30 couches × 576 neurones, hooks PyTorch | ✅ |
| **2** | La LCT voit-elle une structure dans le LLM ? | Contraste inter-couches **ratio 26.7×**, Kruskal-Wallis **p = 9.7e-21** | ✅ **signal réel** |
| **3/4** | H1 : LoRA guidé par LCT bat-il LoRA uniforme ? | Uniforme 46.2 ± 4.3 vs ciblé 52.5 ± 5.3 (5 seeds), **p = 0.047** | ❌ **échec documenté** |
| **5** | La **fusion** transforme-t-elle le LLM ? | Boucles cassées, cohérence ↑, **3/3 cas** | ✅ |

**La leçon de H1** : P_sig mesure la *structure*, pas l'*utilité pour l'apprentissage*.
Un échec rigoureux (multi-seeds, t-test appairé) vaut plus qu'une victoire bruitée.
Détail complet : [`artifacts/RAPPORT_H1.md`](artifacts/RAPPORT_H1.md).

---

## 📦 Structure

```
ratiss_skynet/
├── skynet/
│   ├── hybrid_mind.py          # ⭐ l'architecture unifiée (5 capacités)
│   ├── activations.py          # hooks PyTorch + capture
│   └── topo_score.py           # score LCT par couche
├── ratiss/
│   └── topo/science_core.py    # P_sig, LCT, Vietoris-Rips (AEON ODV)
├── scripts/
│   ├── diagnose_lct.py  # Phase 2 — diagnostic LCT (gudhi, ~1 min)
│   ├── run_h1_lora.py          # Phase 3 — H1 LoRA ciblé vs uniforme
│   ├── run_h1_robust.py        # Phase 4 — benchmark multi-seeds
│   ├── demo_hybrid.py          # démo HYBRID MIND (FR/EN)
│   └── test_transform_fast.py  # ⭐ preuve de transformation (3/3)
├── artifacts/                  # rapports JSON + preuves SHA-256
└── docs/images/                # schéma d'architecture
```

Le moteur RATISS One (`models/`, Git LFS) vit **dans ce repo** —
pas de téléchargement externe.

---

## 🚀 Démarrer

```bash
git clone https://github.com/samajonathan9-source/ratiss-Skynet.git
cd ratiss-Skynet
git lfs pull        # poids du modèle (257 Mo)
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install transformers peft scipy numpy gudhi

cd ratiss_skynet
python scripts/demo_hybrid.py            # HYBRID MIND répond FR/EN
python scripts/test_transform_fast.py    # la preuve de transformation
python scripts/diagnose_lct.py    # le diagnostic topologique
```

---

## 🧭 La suite (on itère, toujours)

- Enrichir les **knowledge packs** (domaines sourcés, bilingue)
- **KTN:Li** : régénération cristalline multi-échelle (pas juste re-prompt)
- **Émotions** : faire varier le style de génération selon la valence
- **Boucle fermée** : la cohérence topologique comme signal de confiance affiché

---

*© 2026 JOHNKING0 & Jonathan Evina.* La loi LCT est figée. Le reste, jamais.
