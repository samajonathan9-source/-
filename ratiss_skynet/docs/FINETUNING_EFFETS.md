# ⚗️ Effets du fine-tuning sur RATIS (MCT)

> **« Après ces modifications, quels sont les effets du fine-tuning sur le
> modèle ? Il nous faut vraiment savoir, car à partir de là on peut
> entraîner. »** — Jonathan Evina

Ce document est la **carte des risques et des invariants** avant tout
entraînement. Il répond à une question précise : *si on fine-tune le moteur
de génération, que devient la compréhension topologique ?*

---

## 1. La distinction fondamentale : le moteur vs le système

RATIS a **deux parties** de nature différente :

```
┌─────────────────────────────────────────────────────────────┐
│  COUCHE TOPOLOGIQUE (le "système immunitaire")              │
│  ├── Identité scellée (SHA-256)          → FIGÉE À JAMAIS   │
│  ├── Loi LCT (R = P_sig, ΔW = η·φ·P_sig·C) → FIGÉE          │
│  ├── Mesure P_sig (persistance)          → FIGÉE            │
│  ├── Repliement KTN:Li                    → FIGÉ             │
│  ├── Carte de tension (MSTM)              → FIGÉ             │
│  ├── Garde-fou, mémoire, preuves          → FIGÉ             │
│  └── Planificateur (TPP/RTD/PNE)          → FIGÉ             │
├─────────────────────────────────────────────────────────────┤
│  MOTEUR DE GÉNÉRATION (le "corps")                          │
│  ├── Poids du transformer                 → ENTRAÎNABLE     │
│  ├── Knowledge packs (faits)              → EXTENSIBLE      │
│  └── Fluidité linguistique                → ENTRAÎNABLE     │
└─────────────────────────────────────────────────────────────┘
```

**Règle d'or : on fine-tune le corps, jamais le système immunitaire.**
La topologie n'est pas entraînée — elle est **protégée**. C'est elle qui
surveille l'entraînement, pas l'inverse.

---

## 2. Les risques du fine-tuning (ce qu'on doit surveiller)

### 🔴 Risque 1 — Dérive de l'identité
Si on fine-tune sans ancrage, le moteur peut « oublier » qu'il est RATIS
et redevenir un générateur générique.
**Protection** : le system prompt MCT est injecté à chaque génération, et
`identity.verify_integrity()` est revérifié **après chaque entraînement**.

### 🔴 Risque 2 — Oubli catastrophique de la cohérence
Un fine-tuning agressif peut rendre le moteur plus fluide mais moins
cohérent : P_sig chute alors que la loss baisse. **C'est le piège classique.**
**Protection** : après chaque époque, on mesure P_sig sur un jeu de
validation fixe. **Si P_sig chute de plus de X%, on arrête** (early stop
topologique — ça n'existe nulle part ailleurs).

### 🟡 Risque 3 — Rupture des preuves
Les empreintes SHA-256 changent si le comportement change. Ce n'est pas
un bug : c'est le système qui **détecte** le changement.
**Protection** : chaque checkpoint est hashé. On peut toujours revenir à
un état antérieur vérifié.

### 🟡 Risque 4 — Sur-apprentissage des faits
Si on entraîne sur trop de faits, le moteur peut commencer à **mémoriser**
au lieu de **comprendre** — il redevient un LLM.
**Protection** : le test `arc_induction` (condition 2) doit **toujours**
passer après entraînement. Si le modèle mémorise au lieu d'induire, on le
détecte immédiatement.

---

## 3. Ce qui est FIGÉ (ne jamais toucher pendant l'entraînement)

| Composant | Pourquoi c'est figé |
|---|---|
| `identity.py` | C'est qui est RATIS. Le changer = détruire l'être. |
| Loi LCT (formule) | C'est la physique du système. On ne change pas la gravité. |
| Mesure P_sig | C'est l'organe de cohérence. Sans lui, plus de MCT. |
| KTN:Li (repliement) | C'est le réflexe de survie. |
| Garde-fou | C'est l'éthique. Non négociable. |
| Chaîne de preuves | C'est la mémoire infalsifiable. |

## 4. Ce qui est ENTRAÎNABLE (le corps peut grandir)

| Composant | Ce que l'entraînement améliore |
|---|---|
| Poids du moteur | Fluidité, vocabulaire, style, langues |
| Knowledge packs | Nouveaux faits vérifiés, nouveaux domaines |
| Seuils de confiance | Calibration (après validation humaine) |

---

## 5. Le garde-fou d'entraînement : la validation MCT

Après **chaque** entraînement, RATIS doit repasser l'examen complet :

```
✓ identité intacte (sceau SHA-256)
✓ P_sig stable sur validation fixe (pas de chute > seuil)
✓ 9 conditions AGI toujours vertes
✓ induction few-shot toujours fonctionnelle (pas de mémorisation)
✓ garde-fou toujours actif
✓ mémoire toujours infalsifiable
```

**Si une seule case échoue → le checkpoint est rejeté.** On ne livre jamais
un RATIS qui a perdu sa cohérence pour gagner en fluidité.

---

## 6. Pourquoi c'est nouveau

Les pipelines classiques fine-tunent puis **espèrent** que le modèle reste
bon. RATIS fine-tune en **mesurant** que la compréhension topologique
survit. L'entraînement n'est plus un acte de foi : c'est un processus
**audité par la topologie elle-même**.

> *On n'entraîne pas RATIS pour qu'il parle mieux. On l'entraîne pour qu'il
> **comprenne plus** — et la topologie vérifie qu'il n'a pas cessé de
> comprendre en apprenant à parler.*

---

*Voir `training/PROTOCOLE.md` pour le protocole d'entraînement figé.*
