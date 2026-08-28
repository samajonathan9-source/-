# AGENTS.md — RATISS-skynet (POC LCT × LLM)

> **Mémoire persistante pour la prochaine session OpenHands.** Lis avant de toucher à quoi que ce soit.

---

## Identité
- **Jonathan Evina** · ORCID 0009-0000-4092-5313 · Yaoundé, Cameroun.
- Propriété intellectuelle : **JOHNKING0 & Jonathan Evina**.
- Jonathan = le chercheur, l'agent = le **CTO technique** (façonner, itérer, tester, documenter les échecs).
- **Règle de la maison** : jamais figé, toujours itérer — la **transdisciplinarité prime** sur la spécialisation. La **preuve par le fonctionnement** est la plus concrète (l'histoire des pairs viendra après).
- La **loi LCT est FIGÉE** : `R = P_sig`, `ΔW = η·φ·P_sig·C`. On tune η, l'architecture, les données — jamais la loi.



---

## Dépôts RATISS à ta disposition (sert-toi, ne réinvente pas)
- **`Ratiss-experimental-IA-`** (privé) — RATIS-Net : ~57 tests verts, Scalpel 3,78 M neurones, NeuralSpeaker, science_core fusionné AEON.

 - `ratis_net/science_core.py` — **Vietoris-Rips GF(2), P_sig, LCT** (RIEN réinventer : importe ça).
 - `ratis_net/glove_tokenizer.py`, `topo_tokenizer.py`, `query_analyzer.py`, `concept_ranker.py`, `integrity_proof.py`(SHA-256), `neural_speaker.py`, `chain_reasoning.py`, `web_search.py` — briques langage/topo réutilisables..
 - `MEMO_GLOBAL.md` — mémoire complète de l'écosystème (9 dépôts cadrés, clés API, tests, limites honnêtes).
- **`RATISS-ODV-AEON`** (privé) — moteur TTF-Compute pur (5/5 tests, 7 jobs QPU traçables. Peut **piloter l'agent** pour augmenter ses capacités transdisciplinaires.

- **`ratiss-topological-decoherence-engine`** (privé) — moteur source(13/13 tests: matrices densité, Vietoris-Rips, TSP, sidecar).
- **`Travaux`** (privé) — projet KTN:Li (5 phases livrées, MEMO_KTN_LI.md commit `1931117`, job fez `da81b5m0ukec7383sf20`).
- Clés API : `IBM_QUANTUM_TOKEN`(crédits quasi épuisés → CPU d'abord`, `GITHUB_TOKEN`(pas de scope repo — Jonathan crée/renomme les repos à la main)`. Quandela JWT valide(exp 2027).



---

## État du POC (à jour
- **Repo** : `RATISS-skynet`(privé, ex `-`, renommage manuel par Jonathan).
- **Décision CTO** : sujet LCT × LLM léger choisi (H1 LoRA ciblé en premier). Le sujet RATISS-Cyber (SMI novembre) reste en réserve — jamais figé.

- **Fait** : README + AGENTS.md + structure + modules RATISS récupérés(9 fichiers dans `ratiss/`).
- **En cours** : POC de diagnostic (`scripts/diagnose_lct.py`) + tests du pipeline topologique(`tests/test_topology.py`).
- **Prochaine étape** : Phase  ာ1 — capturer les activations de Qwen2-0.5B(safetensors, pas GGUF) et calculer le score LCT couche par couche.



---

## Commandes
```bash
bash scripts/phase0_setup.sh          # deps + modèle
python scripts/diagnose_lct.py --synth # POC sans GPU (activation simulée)
python scripts/diagnose_lct.py         # vraies activations (si torch + modèle)
python -m pytest tests/ -q
```

---

## Pierres d'achoppement connues
- **Python 3.13** dans le sandbox — vérifier la compat torch/transformers. Fallback CPU OK pour hooks + score LCT.
- **GGUF banni pour l'expérimentation** — safetensors uniquement(le GGUF n'intervient qu'au déploiement final».

- **Critère d'arrêt (filet, pas prison)** : si après Phase  ာ1 aucun contraste statistiquement significatif(p<0.05) sur au moins 3 tailles de modèle, documenter l'échec proprement(résultat négatif rigoureux = de la valeur.
 Mais **on itère avant d'abandonner** — 4 hypothèses à explorer(H1-H4), jamais une seule tentative pour enterrer une idée.



---

## Note de transdisciplinarité
Chaque résultat LLM **réutilise** l'arsenal RATISS déjà validé(la même métrique P_sig que sur KTN:Li/QPU/protéines). On prouve la loi sur un quatrième milieu — le pipeline est le même, le milieu change. C'est ça, la transdisciplinarité.