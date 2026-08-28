# 🔒 PROTOCOLE D'ENTRAÎNEMENT FIGÉ — RATIS (MCT)

> Protocole reproductible pour entraîner RATIS en laboratoire sur GPU.
> **Figé** : chaque run est hashé, audité, et rejeté si la cohérence
> topologique s'effondre. Voir `docs/FINETUNING_EFFETS.md` pour les risques.

---

## 1. Principe : la topologie surveille l'entraînement

Contrairement au fine-tuning classique (minimiser la loss et espérer),
l'entraînement LCT **mesure la persistance P_sig à chaque pas** et
**module l'apprentissage par la cohérence** :

```
ΔW = η · φ · P_sig · C
```

Si P_sig s'effondre → la porte LCT se ferme → on apprend moins ou pas.
**On ne sacrifie jamais la compréhension pour la fluidité.**

---

## 2. Ce qui est FIGÉ (non négociable)

| Composant | Statut |
|---|---|
| Identité RATIS (`skynet/identity.py`) | 🔒 scellée SHA-256 |
| Loi LCT (formule) | 🔒 figée |
| Mesure P_sig | 🔒 figée |
| Repliement KTN:Li | 🔒 figé |
| Garde-fou / sécurité | 🔒 figé |
| Chaîne de preuves / mémoire | 🔒 figée |
| Planificateur (TPP/RTD/PNE) | 🔒 figé |

## 3. Ce qui est ENTRAÎNABLE

- Poids du moteur de génération (fluidité, vocabulaire, langues)
- Knowledge packs (nouveaux faits vérifiés)
- Seuils de confiance (calibration, après validation humaine)

---

## 4. Configuration GPU (laboratoire)

```python
from skynet.hybrid_mind import HybridMind
from training.lct_trainer import LCTTrainer

mind = HybridMind("models/RATISS-One")

config = {
    "learning_rate": 5e-5,
    "batch_size": 16,        # ajuster selon VRAM
    "max_epochs": 3,
    "psig_drop_tolerance": 0.05,  # early stop topologique
    "seed": 42,
}

trainer = LCTTrainer(mind, config=config)
log = trainer.fit(train_texts, val_texts)
```

### Prérequis labo
- GPU avec ≥ 8 Go VRAM (pour un moteur de 135M en fp16)
- `torch` avec CUDA
- `numpy`

---

## 5. Garde-fou post-entraînement (validation MCT)

Après **chaque** run, RATIS doit repasser l'examen :

```
✓ identité intacte (sceau SHA-256)
✓ P_sig stable sur validation fixe (pas de chute > tolérance)
✓ 9 conditions AGI toujours vertes (scripts/test_agi_conditions.py
  + scripts/test_greening.py)
✓ induction few-shot toujours fonctionnelle (pas de mémorisation)
✓ garde-fou toujours actif
✓ mémoire toujours infalsifiable
```

**Si une seule case échoue → le checkpoint est rejeté.**

---

## 6. Traçabilité

Chaque run produit `artifacts/training_runs/run_<hash>.json` avec :
- la configuration complète (hashée)
- la liste des composants figés
- le P_sig à chaque pas
- la raison d'arrêt (completed / catastrophic_forgetting / identity_drift)

**Reproductibilité totale** : même config + même seed = même hash.

---

*« On n'entraîne pas RATIS pour qu'il parle mieux. On l'entraîne pour
qu'il comprenne plus — et la topologie vérifie qu'il n'a pas cessé de
comprendre. »*
