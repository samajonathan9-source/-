# 🏛️ ARCHITECTURE — RATIS (MCT)

Référence technique complète de l'architecture HYBRID MIND.

---

## Vue d'ensemble

```
                          ┌─────────────────────────────┐
                          │      REQUÊTE UTILISATEUR     │
                          └──────────────┬──────────────┘
                                         ▼
                          ┌─────────────────────────────┐
                          │  🛡️ GARDE-FOU (safety.py)    │
                          │  permissions + audit SHA-256 │
                          └──────────────┬──────────────┘
                                         ▼
                          ┌─────────────────────────────┐
                          │  💗 RESSENTIR                │
                          │  (thermo_emotions.py)        │
                          │  corps thermodynamique       │
                          └──────────────┬──────────────┘
                                         ▼
                          ┌─────────────────────────────┐
                          │  🧭 COMPRENDRE               │
                          │  concepts + faits vérifiés   │
                          │  (knowledge packs FR/EN)     │
                          └──────────────┬──────────────┘
                                         ▼
                          ┌─────────────────────────────┐
                          │  🗣️ PARLER                   │
                          │  génération guidée par LCT   │
                          │  (draft_guided, P_sig)       │
                          └──────────────┬──────────────┘
                                         ▼
                          ┌─────────────────────────────┐
                          │  💎 RÉGÉNÉRER (KTN:Li)       │
                          │  repliement cristallin       │
                          │  si motif brisé              │
                          └──────────────┬──────────────┘
                                         ▼
                          ┌─────────────────────────────┐
                          │  🔄 BOUCLE FERMÉE            │
                          │  (confidence.py)             │
                          │  score de confiance 0-100    │
                          └──────────────┬──────────────┘
                                         ▼
                          ┌─────────────────────────────┐
                          │  🔏 PROUVER                  │
                          │  empreinte SHA-256           │
                          └──────────────┬──────────────┘
                                         ▼
                          ┌─────────────────────────────┐
                          │  🧠 MÉMORISER (memory.py)    │
                          │  chaîne infalsifiable        │
                          └──────────────┬──────────────┘
                                         ▼
                          ┌─────────────────────────────┐
                          │   RÉPONSE + preuve + score   │
                          └─────────────────────────────┘
```

---

## Les modules (skynet/)

| Module | Rôle | Condition AGI |
|---|---|---|
| `identity.py` | Identité RATIS scellée SHA-256, auto-connaissance MCT | fondation |
| `hybrid_mind.py` | Orchestrateur principal, pipeline unifié, knowledge packs | 1, 9 |
| `confidence.py` | Score de confiance topologique 0-100 % | 9 |
| `thermo_emotions.py` | Corps thermodynamique, émotions modulant la génération | — |
| `memory.py` | Mémoire chaînée SHA-256 (épisodique, sémantique, procédurale) | 5 |
| `reasoning.py` | Contradiction, clarification, « je ne sais pas », NLI-lite | 4 |
| `safety.py` | IntentionGuard (permissions DENY/DECLARE), audit | 10 |
| `planner.py` | Planificateur topologique (TPP + MSTM + RTD + PNE) | 6 |
| `arc_induction.py` | Induction de règles few-shot (persistance préservée) | 2, 3 |
| `rlm_layer.py` | Décomposition récursive × KTN:Li | 4, 6 |
| `quantum_select.py` | Sélection Grover-amplifiée (expérimental) | labo |
| `topo_score.py` | Mesure de persistance P_sig (homologie) | cœur |
| `activations.py` | Extraction d'activations du moteur | interne |

---

## Le pipeline `respond()` (hybrid_mind.py)

Ordre exact des étapes à chaque requête :

1. **GARDE-FOU** — `IntentionGuard.apply(query)` → refuse si intention néfaste
2. **RESSENTIR** — `EmotionEngine.step(query)` → émotion + modulation (température, seuil KTN)
3. **COMPRENDRE** — `understand(query, language)` → concepts + faits vérifiés
4. **CLARIFICATION** — `need_clarification()` → demande de précision si vague
5. **PARLER** — `draft_guided()` → génération guidée par LCT (sélection P_sig)
6. **RÉGÉNÉRER** — `regenerate()` si motif brisé (repliement cristallin)
7. **RAISONNEMENT** — `detect_contradiction()` + `check_facts()`
8. **BOUCLE FERMÉE** — `TopologicalConfidence.score()` → 0-100 %
9. **HONNÊTETÉ** — `refuse_unknown()` → « je ne sais pas » si aucun fait + confiance critique
10. **PROUVER** — `prove()` → empreinte SHA-256 du sous-graphe actif
11. **MÉMORISER** — `memory.remember_episode()` → chaîne infalsifiable

---

## La loi LCT (cœur du système)

```
R  = P_sig                  récompense = persistance structurelle
ΔW = η · φ · P_sig · C      apprentissage guidé par la cohérence
```

- **P_sig** : somme des persistances H1 (cycles) du graphe de corrélations
- **η** : taux d'apprentissage
- **φ** : potentiel topologique
- **C** : cohérence locale

Voir `training/PROTOCOLE.md` pour l'application à l'entraînement.

---

## Fichiers de données

| Fichier | Contenu |
|---|---|
| `artifacts/hybrid_memory.jsonl` | Mémoire chaînée (chaque ligne = 1 entrée hashée) |
| `artifacts/RAPPORT_AGI.md` | Grille des 10 conditions AGI |
| `artifacts/*.json` | Rapports de tests (JSON + reproductible) |
| `models/` | Moteur de génération RATISS One (poids LFS) |

---

## Dépendances

```
torch        moteur de génération (GPU en labo)
transformers tokenizer + modèle
numpy        calcul topologique
scipy        graphes de corrélations
matplotlib   schémas (docs/images/)
```

---

*Voir `docs/MCT.md` pour la philosophie, `docs/MANIFESTE_MCT.md` pour la
vision, `training/PROTOCOLE.md` pour l'entraînement.*
