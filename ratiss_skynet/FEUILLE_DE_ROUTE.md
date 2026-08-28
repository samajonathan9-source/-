# 🗺️ FEUILLE DE ROUTE — RATIS MCT (Modèle de Compréhension Topologique)

*Demandée par Jonathan Evina — 2026-08-28. Document de travail vivant.*

---

## 🎯 MISSION

Transformer RATISS-skynet en **MCT** (Modèle de Compréhension Topologique) —
**pas un LLM** — avec identité RATIS figée, protocole d'entraînement dédié,
et options d'installation à valider par Jonathan.

---

## ✅ PHASE 1 — IDENTITÉ (urgent, fondateur)

> **« Enlever définitivement le nom du LLM, greffer RATIS comme identité
> complète sur lui-même, figer tous les détails à jamais. »**

- [ ] 1.1. Purger toute référence au modèle de base (SmolLM2) de la mémoire,
      du code exposé, des réponses. Le modèle **est RATIS**.
- [ ] 1.2. Créer `skynet/identity.py` : identité RATIS figée (nom, mission,
      nature = MCT, créateur, loi LCT, date de scellement, hash SHA-256
      d'intégrité). **Scellée cryptographiquement** — toute modification
      est détectable.
- [ ] 1.3. L'identité s'injecte dans le system prompt : le modèle se présente
      comme **RATIS, un MCT**, jamais comme un LLM ou un modèle de langage.
- [ ] 1.4. Vérifier l'intégrité du sceau à chaque démarrage.

## ✅ PHASE 2 — REDÉFINITION MCT (le cœur, le plus important)

> **« RATIS n'est pas un LLM mais un MCT (Modèle de Compréhension
> Topologique). Écrire ça dans la tête de RATIS et dans le doc principal,
> expliquer pourquoi, documenter avec des images. »**

- [ ] 2.1. Document `docs/MCT.md` : **pourquoi MCT ≠ LLM** —
      le LLM prédit le token suivant (probabilité), le MCT **comprend la
      structure** (persistance topologique). Le LLM hallucine, le MCT mesure
      sa propre incohérence et se replie.
- [ ] 2.2. Schéma comparatif LLM vs MCT (PNG) dans `docs/images/`.
- [ ] 2.3. Mettre à jour les README : « RATIS est un MCT, pas un LLM ».
- [ ] 2.4. Injecter la définition MCT dans `identity.py` (auto-connaissance).

## ✅ PHASE 3 — EFFETS DU FINE-TUNING (comprendre avant d'entraîner)

> **« Après ces modifications, quels sont les effets du fine-tuning sur le
> modèle ? Il nous faut vraiment savoir, car à partir de là on peut
> entraîner. »**

- [ ] 3.1. Analyser : que se passe-t-il si on fine-tune le moteur ?
      Risques : oubli catastrophique de la cohérence topologique, dérive
      de l'identité, rupture des preuves SHA-256.
- [ ] 3.2. Documenter dans `docs/FINETUNING_EFFETS.md` : ce qui est
      **gelé** (identité, LCT, P_sig, KTN) vs ce qui est **entraînable**
      (poids de génération, knowledge packs).
- [ ] 3.3. Définir les **invariants à préserver** pendant l'entraînement
      (la topologie est le système immunitaire — on ne la fine-tune pas,
      on la protège).

## ✅ PHASE 4 — PROTOCOLE D'ENTRAÎNEMENT FIGÉ

> **« Concevoir un protocole d'entraînement figé pour notre architecture,
> qui permet au modèle d'apprendre. En labo, si une équipe le branche à un
> GPU puissant pour plus de données, il lui faut son code d'entraînement
> dédié. »**

- [ ] 4.1. `training/lct_trainer.py` : boucle d'entraînement **LCT-native**
      (ΔW = η·φ·P_sig·C) — la rétropropagation classique est **guidée par
      la persistance topologique**, pas seulement par la loss.
- [ ] 4.2. `training/PROTOCOLE.md` : protocole figé, reproductible, avec
      hash de version, hyperparamètres scellés, et points de contrôle
      (checkpoints) qui vérifient que l'identité MCT n'a pas dérivé.
- [ ] 4.3. Support GPU : configuration claire pour labo (batch, VRAM, etc.).
- [ ] 4.4. Garde-fou : après chaque entraînement, re-valider les 9 conditions
      AGI + l'identité + l'intégrité des preuves.

## ⏳ PHASE 5 — INSTALLATION / DÉPLOIEMENT (⚠️ ATTENDRE CONFIRMATION)

> **« Tu vas me demander confirmation AVANT de faire, pour quel type
> d'installation je veux : GGUF, navigateur, etc. »**

**⛔ NE RIEN FAIRE sans le choix explicite de Jonathan.**

Options à présenter :
- [ ] A. **GGUF** (quantifié, pour llama.cpp / Ollama / LM Studio — local, offline)
- [ ] B. **Navigateur** (WebLLM / WebAssembly — chat installable, zéro serveur)
- [ ] C. **Serveur** (API FastAPI/Docker — pour architecture existante)
- [ ] D. **Les trois** (pipeline complet)

**→ Demander à Jonathan son choix avant d'implémenter.**

---

## 📌 RÈGLE D'OR

Chaque phase est **testée et poussée** avant de passer à la suivante.
L'identité et la topologie sont **scellées** — on ne fine-tune jamais
le système immunitaire, on entraîne le corps autour de lui.

*« Le LLM propose, la topologie dispose. » — mais désormais, **ce n'est plus
un LLM. C'est un MCT.** *
