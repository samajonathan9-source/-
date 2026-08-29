# RATISS One — API REST (FastAPI).
#
# Expose le MCT comme un service demontrable : generation, sante, preuve.
# Chaque reponse est accompagnee du score de confiance topologique, de
# l'etat emotionnel et de l'empreinte SHA-256 — la demonstration par le
# fonctionnement.

import os
import sys

from fastapi import FastAPI
from pydantic import BaseModel

# rendre le package skynet importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skynet.hybrid_mind import HybridMind

MODEL_DIR = os.environ.get(
    "RATIS_MODEL_DIR",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                                 "models", "RATISS-One")),
)

app = FastAPI(title="RATISS One API", version="1.0.0",
              description="Modele de Comprehension Topologique (MCT)")

_mind = None


def get_mind():
    global _mind
    if _mind is None:
        _mind = HybridMind(MODEL_DIR)
    return _mind


class GenerateRequest(BaseModel):
    prompt: str
    language: str = "auto"


class GenerateResponse(BaseModel):
    response: str
    confidence_score: float
    confidence_verdict: str
    language: str
    emotion: dict
    coherence: float
    proof: dict
    blocked: bool = False


@app.get("/health")
def health():
    mind = get_mind()
    ident = mind.identity()
    return {
        "status": "operational",
        "model": "RATISS-One",
        "nature": "MCT",
        "identity_seal": ident["seal"][:16],
        "identity_integrity": ident["integrity"],
        "conditions_agi": "9/10",
    }


@app.get("/identity")
def identity():
    return get_mind().identity()


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    mind = get_mind()
    lang = None if req.language == "auto" else req.language
    r = mind.respond(req.prompt, language=lang)
    return GenerateResponse(
        response=r["sentence"],
        confidence_score=r.get("confidence_score", 0.0),
        confidence_verdict=r.get("confidence_verdict", ""),
        language=r.get("language", lang or "fr"),
        emotion=r.get("emotion", {}),
        coherence=r.get("coherence", 0.0),
        proof=r.get("proof", {}),
        blocked=r.get("blocked", False),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
