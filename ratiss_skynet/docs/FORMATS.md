# Formats de poids — entraînement et déploiement de RATISS One

Ce document précise, une fois pour toutes, **quel format de fichier RATIS
utilise pour quoi**, afin d'éviter toute reconstruction inutile.

---

## Principe directeur

> **On entraîne en SafeTensors. On déploie en GGUF (local) ou en SafeTensors
> (serveur). On ne mélange jamais les deux rôles.**

Ces deux formats ne sont pas concurrents : ils couvrent deux étapes
distinctes du cycle de vie du modèle.

| | **SafeTensors** (`.safetensors`) | **GGUF** (`.gguf`) |
|---|---|---|
| **Rôle** | Entraînement / fine-tuning | Inférence locale |
| **Précision** | Pleine (BF16/FP16/FP32) | Quantifiée (Q2 à Q8) |
| **Contenu** | Poids uniquement (+ config, tokenizer séparés) | Tout-en-un (poids + métadonnées + tokenizer) |
| **Écosystème** | PyTorch, HuggingFace, PEFT/LoRA | llama.cpp, Ollama, LM Studio |
| **Entraînable** | **Oui** | **Non** |
| **Lecture** | Memory-mapped, zero-copy, sûr (pas de pickle) | Standalone, sans Python |

---

## Ce que RATIS utilise

### 1. Entraînement et fine-tuning → SafeTensors

RATISS One est déjà stocké en SafeTensors (`models/RATISS-One/model.safetensors`).
C'est le format standard des frameworks d'entraînement :

- compatible avec **LoRA / QLoRA** (PEFT) pour un fine-tuning efficace sur
  GPU modeste ou Google Colab ;
- chargement memory-mapped (rapide, faible empreinte mémoire) ;
- format sûr (pas d'exécution de code arbitraire, contrairement au pickle) ;
- pleine précision — indispensable pour ne pas dégrader la cohérence
  topologique pendant l'apprentissage.

**Conclusion : aucun format à reconstruire pour l'entraînement.** Le fichier
existant est directement entraînable via `training/lct_trainer.py` et le
script Colab (`training/colab_train.py`).

### 2. Déploiement serveur → SafeTensors

Pour l'API (FastAPI/Docker), le modèle est chargé directement depuis
SafeTensors via `transformers`. Aucune conversion n'est nécessaire.

### 3. Déploiement local / navigateur → GGUF (conversion ultérieure)

Pour une utilisation hors-ligne sur machine standard (llama.cpp, Ollama,
LM Studio), le modèle SafeTensors sera **converti en GGUF quantifié**
(Q4_K_M recommandé). Cette conversion est une étape de **packaging**, pas
d'entraînement : elle est effectuée une fois le fine-tuning terminé, à l'aide
du convertisseur de llama.cpp. Elle n'est pas requise pour la démonstration.

---

## Pipeline résumé

```
                    entraînement                    déploiement
                         │                              │
   SafeTensors ──► LoRA / QLoRA (LCT) ──► SafeTensors ──┼──► Serveur (FastAPI/Docker)
   (existant)      fine-tuning           (checkpoint)   │
                                                         └──► conversion GGUF ──► local (Ollama)
```

- **SafeTensors** : le format de travail et de vérité.
- **GGUF** : un artefact de distribution, produit à la demande.

---

*Voir `training/PROTOCOLE.md` pour le protocole d'entraînement et
`training/colab_train.py` pour l'exécution sur Google Colab.*
