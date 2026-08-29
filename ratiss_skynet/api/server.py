# RATISS One — API REST (FastAPI).
#
# Expose le MCT comme un service demontrable : generation, sante, preuve.
# Chaque reponse est accompagnee du score de confiance topologique, de
# l'etat emotionnel et de l'empreinte SHA-256 — la demonstration par le
# fonctionnement.

import os
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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


CHAT_HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RATISS One — MCT</title>
<style>
  :root { --bg:#0d1117; --panel:#161b22; --border:#30363d; --text:#e6edf3;
          --muted:#8b949e; --green:#3fb950; --gold:#d29922; --blue:#58a6ff; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--bg); color: var(--text);
         font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
         display: flex; flex-direction: column; height: 100vh; }
  header { padding: 14px 20px; border-bottom: 1px solid var(--border);
           display: flex; align-items: center; gap: 12px; background: var(--panel); }
  .dot { width: 10px; height: 10px; border-radius: 50%; background: var(--muted); }
  .dot.on { background: var(--green); box-shadow: 0 0 8px var(--green); }
  header h1 { font-size: 16px; font-weight: 600; }
  header .sub { color: var(--muted); font-size: 12px; }
  #seal { margin-left: auto; color: var(--gold); font-size: 11px;
          font-family: monospace; }
  #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex;
          flex-direction: column; gap: 14px; }
  .msg { max-width: 78%; padding: 12px 16px; border-radius: 12px;
         line-height: 1.5; font-size: 14px; white-space: pre-wrap; }
  .user { align-self: flex-end; background: #1f6feb; color: #fff;
          border-bottom-right-radius: 4px; }
  .ratis { align-self: flex-start; background: var(--panel);
           border: 1px solid var(--border); border-bottom-left-radius: 4px; }
  .meta { margin-top: 10px; padding-top: 8px; border-top: 1px solid var(--border);
          font-size: 11px; color: var(--muted); font-family: monospace;
          display: flex; flex-wrap: wrap; gap: 10px; }
  .meta .conf { color: var(--green); font-weight: 600; }
  .meta .conf.low { color: var(--gold); }
  .meta .emo { color: var(--blue); }
  #bar { padding: 14px 20px; border-top: 1px solid var(--border);
         display: flex; gap: 10px; background: var(--panel); }
  #input { flex: 1; background: var(--bg); border: 1px solid var(--border);
           border-radius: 8px; padding: 12px 14px; color: var(--text);
           font-size: 14px; outline: none; }
  #input:focus { border-color: var(--blue); }
  button { background: var(--green); color: #06110a; border: none;
           border-radius: 8px; padding: 0 22px; font-size: 14px;
           font-weight: 600; cursor: pointer; }
  button:disabled { opacity: 0.4; cursor: wait; }
  .thinking { color: var(--muted); font-style: italic; font-size: 13px; }
</style>
</head>
<body>
<header>
  <span class="dot" id="dot"></span>
  <div>
    <h1>RATISS One</h1>
    <div class="sub">Modèle de Compréhension Topologique — MCT</div>
  </div>
  <span id="seal"></span>
</header>
<div id="chat"></div>
<div id="bar">
  <input id="input" placeholder="Parlez à RATIS… (Entrée pour envoyer)"
         autocomplete="off" autofocus>
  <button id="send">Envoyer</button>
</div>
<script>
const chat = document.getElementById('chat');
const input = document.getElementById('input');
const btn = document.getElementById('send');
const dot = document.getElementById('dot');
const seal = document.getElementById('seal');

async function boot() {
  try {
    const h = await (await fetch('/health')).json();
    if (h.status === 'operational') {
      dot.classList.add('on');
      seal.textContent = 'sceau ' + h.identity_seal + ' · AGI ' + h.conditions_agi;
      addMsg('ratis', 'Je suis RATIS, un Modèle de Compréhension Topologique. ' +
        'Je mesure la cohérence de ce que je dis. Posez votre question.', null);
    }
  } catch (e) {
    addMsg('ratis', 'Initialisation du moteur en cours… réessayez dans un instant.', null);
  }
}

function addMsg(who, text, meta) {
  const d = document.createElement('div');
  d.className = 'msg ' + who;
  d.textContent = text;
  if (meta) {
    const m = document.createElement('div');
    m.className = 'meta';
    const cls = meta.confidence_score >= 60 ? 'conf' : 'conf low';
    m.innerHTML =
      '<span class="' + cls + '">confiance ' + meta.confidence_score + '/100</span>' +
      '<span>' + (meta.confidence_verdict || '') + '</span>' +
      (meta.emotion && meta.emotion.label
        ? '<span class="emo">émotion: ' + meta.emotion.label + '</span>' : '') +
      (meta.proof && meta.proof.digest
        ? '<span>preuve ' + String(meta.proof.digest).slice(0, 12) + '…</span>' : '');
    d.appendChild(m);
  }
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
  return d;
}

async function send() {
  const q = input.value.trim();
  if (!q) return;
  input.value = '';
  btn.disabled = true;
  addMsg('user', q, null);
  const thinking = addMsg('ratis', '…', null);
  thinking.classList.add('thinking');
  try {
    const r = await fetch('/generate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({prompt: q, language: 'auto'})
    });
    const data = await r.json();
    thinking.remove();
    addMsg('ratis', data.response, data);
  } catch (e) {
    thinking.textContent = 'Erreur de communication avec le moteur.';
  }
  btn.disabled = false;
  input.focus();
}

btn.addEventListener('click', send);
input.addEventListener('keydown', e => { if (e.key === 'Enter') send(); });
boot();
</script>
</body>
</html>"""


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


@app.get("/", response_class=HTMLResponse)
def chat_ui():
    return CHAT_HTML


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
