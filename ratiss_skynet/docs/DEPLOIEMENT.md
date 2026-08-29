# Déploiement — RATISS One

Trois modes de déploiement, par ordre de priorité. Le format de poids est
documenté dans [`FORMATS.md`](FORMATS.md).

---

## 1. Serveur API (priorité immédiate)

Expose RATISS One comme un service REST. C'est le mode de démonstration.

### En local

```bash
cd ratiss_skynet
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu
python api/server.py
```

Le serveur écoute sur `http://localhost:8000`.

### Avec Docker

```bash
# depuis la racine du depot
docker compose up --build
```

### Endpoints

| Méthode | Chemin | Fonction |
|---|---|---|
| `GET` | `/health` | État du service, sceau d'identité, intégrité |
| `GET` | `/identity` | Déclaration d'identité MCT complète |
| `POST` | `/generate` | Génération guidée par la LCT |

#### Exemple : `/generate`

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Qu est-ce qu un trou noir ?", "language": "fr"}'
```

Réponse :

```json
{
  "response": "Un trou noir est une region de l'espace-temps...",
  "confidence_score": 95.7,
  "confidence_verdict": "HAUTE CONFIANCE",
  "language": "fr",
  "emotion": {"label": "neutre", "valence": 0.0},
  "coherence": 117.3,
  "proof": {"sha256": "...", "n_concepts": 2, "n_facts": 1},
  "blocked": false
}
```

La documentation interactive (Swagger) est disponible sur `/docs`.

---

## 2. GGUF local (court terme)

Conversion du modèle SafeTensors en GGUF quantifié pour une utilisation
hors-ligne (llama.cpp, Ollama, LM Studio). Étape de packaging, à effectuer
après le fine-tuning. Voir [`FORMATS.md`](FORMATS.md).

## 3. Navigateur (moyen terme)

Exécution dans le navigateur via WebLLM/WebGPU, pour une accessibilité
maximale sans installation. Nécessite une optimisation spécifique.

---

*Le serveur API est le mode de démonstration recommandé : il expose la
confiance, l'émotion et la preuve SHA-256 en temps réel.*
