import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from symbion_cognitive_collider.collider import route_language

app = FastAPI(title="Symbion Cognitive Collider")

class Req(BaseModel):
    text: str
    energy: float = 0.9

@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!doctype html>
<html>
<head><meta charset="utf-8"/><title>Symbion Router</title></head>
<body style="font-family: sans-serif; max-width: 900px; margin: 20px auto;">
  <h1>Symbion Router MVP</h1>
  <textarea id="t" rows="6" style="width:100%"></textarea><br/><br/>
  <label>energy_score: <input id="e" type="number" step="0.05" value="0.9" min="0" max="1"/></label>
  <button onclick="go()">Route</button>
  <pre id="out" style="white-space: pre-wrap; background:#f5f5f5; padding:12px;"></pre>
<script>
async function go(){
  const text = document.getElementById('t').value;
  
  // client-side guard (avoid sending empty requests)
  const _out = (typeof out !== 'undefined' && out) ? out : document.getElementById('out');
  if (!text || !String(text).trim()){
    if (_out) _out.textContent = "ERROR: empty_input";
    return;
  }
const energy = parseFloat(document.getElementById('e').value || '0.9');
  const r = await fetch('/route', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({text, energy})});
  const j = await r.json();
  document.getElementById('out').textContent = JSON.stringify(j, null, 2);
}
</script>
</body>
</html>
"""

@app.post("/route")
async def route(req: Req):
    if not (req.text or '').strip():
        raise HTTPException(status_code=400, detail='empty_input')

    r = await route_language(req.text, {"history": []}, {"energy_score": float(req.energy)})
    try:
        return r.model_dump()
    except Exception:
        return r.__dict__
