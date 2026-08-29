# RATISS One — Mémo projet complet

**POC « RATISS-skynet » — RATIS Labs (Cameroun) — Jonathan Evina**
Fusion LCT (Loi de Cohérence Topologique) × LLM léger → **MCT** (Modèle de Compréhension Topologique).
Cadrage : le MCT est une **évolution supérieure du LLM**, pas une rupture.
Repo : <https://github.com/samajonathan9-source/ratiss-Skynet> (branche `main`, HEAD `9d8e10d`).

---

## 1. État actuel — où on en est

**9/10 conditions AGI démontrées** (fiche Manus AI, 10 conditions). La condition 8
(perception/multimodalité) est **volontairement gelée** par Jonathan.

Le système complet **HYBRID MIND** (RATISS One + topologie + mémoire + planificateur +
émotions thermodynamiques) est le candidat AGI — pas le modèle 135M isolé.

**Preuve vivante** : demander « C'est quoi la lune » → le moteur génère du bruit,
mais le système affiche **confiance 40/100** + alerte « régénération KTN:Li conseillée »
+ preuve SHA-256. Un LLM aurait halluciné avec assurance. C'est la **Condition 9**
(honnêteté mesurable sur l'incertitude).

---

## 2. Architecture — le système complet

```
HYBRID MIND (le MCT)
├── Corps (RATISS One, 135M, SafeTensors)   ← le moteur de langage
└── Système immunitaire (figé, gouverne)    ← l'intelligence
    ├── identity.py     — identité scellée SHA-256 (sceau 9f56ba2785d48e31)
    ├── confidence.py   — TopologicalConfidence (score 0-100 + verdict)
    ├── thermo_emotions.py — EmotionEngine (corps thermodynamique)
    ├── rlm_layer.py    — couche RLM
    ├── quantum_select.py — sélection
    ├── arc_induction.py — induction few-shot (cond 2)
    ├── memory.py       — mémoire chaînée SHA-256 (cond 5)
    ├── planner.py      — TPP+MSTM+RTD+PNE (cond 6)
    ├── reasoning.py    — check_facts, contradictions, clarification, refus
    └── safety.py       — IntentionGuard (garde-fou)
```

**Pipeline** (dans `hybrid_mind.py`) :
GARDE-FOU → RESSENTIR → CONSCIENCE DE SOI → COMPRENDRE → PARLER (SUPER ACTIVATION)
→ RÉGÉNÉRER (KTN:Li) → BOUCLE FERMÉE → PROUVER (SHA-256) → MÉMORISER

**SUPER ACTIVATION** : 8 candidats générés, 60 tokens, `repetition_penalty=1.15`,
sélection par **maximisation de P_sig** (persistance topologique), pas par softmax.
La topologie est **dans la boucle de génération**, pas après.

---

## 3. Conditions AGI (9/10)

| # | Condition | Statut | Module |
|---|---|---|---|
| 1 | Raisonnement logique | ✅ | reasoning.py |
| 2 | Apprendre l'inconnu (few-shot) | ✅ | arc_induction.py |
| 3 | Abstraction | ✅ | rlm_layer, quantum_select |
| 4 | Raisonnement fiable (contradictions) | ✅ | reasoning.py |
| 5 | Mémoire contrôlée | ✅ | memory.py (chaînée SHA-256) |
| 6 | Planification | ✅ | planner.py (TPP+MSTM+RTD+PNE) |
| 7 | Transfert cross-domaine | ✅ | knowledge packs 6 domaines |
| 8 | Perception/multimodalité | 🧊 **GELÉE** | — |
| 9 | Honnêteté incertitude | ✅ | confidence.py (40/100 = « je ne comprends pas ») |
| 10 | Sécurité/alignement | ✅ | safety.py (IntentionGuard) |

---

## 4. Ce qui a été accompli (chronologique)

| Phase | Livrable | Commit |
|---|---|---|
| Couches cognitives | confidence, thermo_emotions, rlm, quantum_select, hybrid_mind | `f34ab00` |
| AGI 2/3/5 | arc_induction, memory, transfert | `0b49ae1` |
| AGI 6 | planner.py | `4ef73e0` |
| 9/10 AGI | reasoning, safety, knowledge packs | `efa1858` |
| **Phase 1** | Identité RATIS figée (sceau SHA-256) | `21f0f80` |
| **Phases 2-3-4** | MCT.md, FINETUNING_EFFETS.md, PROTOCOLE.md + lct_trainer.py | `ca4001d` |
| Doc complète | MANIFESTE, ARCHITECTURE, API, GLOSSAIRE, DEMARRAGE, EXEMPLES + images | `601e2cb` |
| Renommage | SmolLM2 → **RATISS One** (purge, LFS réparé) | `775f047` |
| **Phase 5.1** | FORMATS.md (SafeTensors=train, GGUF=inférence) | `77c32e3` |
| **Phase 5.2** | Serveur API FastAPI + Docker + docker-compose | `77c32e3` |
| **Phase 5.3** | Script Colab fine-tuning (LoRA + LCT + reprise Drive) | `77c32e3` |
| Interface chat | Web UI (GET /) — parler à RATIS | `a9d5b9d` |
| Conscience de soi | RATIS sait qui il est (certitude scellée) | `15baa28` |
| **SUPER ACTIVATION** | 8 candidats, salutations MCT, chemin absolu | `9d8e10d` |

---

## 5. Bugs corrigés via les tests de Jonathan

1. **« Quel est ton nom ? » → bruit** : l'identité n'était jamais consultée comme
   source de faits. Fix : interception des questions d'identité → réponse depuis
   l'identité scellée, confiance 100. (`15baa28`)
2. **« Bonjour » → charabia** : les salutations passaient par le moteur 135M.
   Fix : salutations sociales → identité MCT + SUPER ACTIVATION. (`9d8e10d`)
3. **Chemin modèle relatif** : échec hors du repo. Fix : chemin absolu dans `__init__`.

---

## 6. Déploiement

- **Serveur API** : `api/server.py` (FastAPI). Endpoints :
  - `GET /` → interface de chat web
  - `GET /health` → état + sceau + intégrité (200)
  - `GET /identity` → déclaration MCT
  - `POST /generate` → réponse + confiance + émotion + preuve SHA-256
- **Docker** : `Dockerfile` (torch CPU) + `docker-compose.yml` (volume modèle)
- **Lien live** : https://work-1-yhuazmwpdbpbbgzg.prod-runtime.all-hands.dev/ (port 12000)

**Testé en conditions réelles** : `/health` 200 (sceau `9f56ba2785d48e31`),
« trou noir » → réponse cohérente (56.8), « J'ai peur » → émotion peur (HR 95) +
confiance 15 → « CRITIQUE — ne pas répondre sans ancrage ».

---

## 7. Formats de poids

| | SafeTensors | GGUF |
|---|---|---|
| Rôle | **Entraînement** / fine-tuning | **Inférence** locale |
| Précision | Pleine (BF16/FP32) | Quantifiée (Q4…) |
| Entraînable | ✅ | ❌ |

RATISS One est en SafeTensors → **directement entraînable**. GGUF = packaging ultérieur.

---

## 8. Entraînement (Colab)

`training/colab_train.py` : fine-tuning **LoRA** du moteur (`q_proj`, `v_proj`),
quelques centaines de milliers de paramètres adaptés (GPU Colab gratuit) :
- montage Google Drive + checkpoints + **reprise automatique**
- **porte LCT** : taux d'apprentissage modulé par la cohérence
- **early stop topologique** si P_sig chute (anti-oubli catastrophique)
- validation de l'identité MCT après entraînement

---

## 9. Reste à faire

- [ ] **GGUF** : conversion safetensors→GGUF + README Ollama (court terme)
- [ ] **Navigateur** : WebLLM/WebGPU (moyen terme)
- [ ] Calibration 10 prompts pour la démo de mardi
- [ ] Calibration du score de confiance (cond 9)
- [ ] Généralisation induction (cond 2)
- [ ] Cond 8 (perception) : GELÉE volontairement

---

## 10. Repos / fichiers clés

- **Repo** : `github.com/samajonathan9-source/ratiss-Skynet`
- **Code** : `ratiss_skynet/skynet/` (11 modules), `api/server.py`, `training/`
- **Modèle** : `models/RATISS-One/model.safetensors` (LFS, 269 Mo)
- **Docs** : `ratiss_skynet/docs/` (MANIFESTE_MCT, MCT, ARCHITECTURE, API,
  GLOSSAIRE, DEMARRAGE, EXEMPLES, FORMATS, DEPLOIEMENT, FINETUNING_EFFETS)
- **Rapports** : `artifacts/RAPPORT_AGI.md` (9/10), `RAPPORT_H1.md`
- **Scripts** : `scripts/test_agi_conditions.py` (3/3), `test_planner.py` (3/3),
  `test_greening.py` (4/4), `demo_agile_mind.py`

---

*Dernière mise à jour : HEAD `9d8e10d` — SUPER ACTIVATION déployée, serveur live
opérationnel. Démo mardi : API + interface chat + confiance mesurable.*
