
# Cognitive Collider (Symbion Space)

**Language as an Ontological Basis Switch — not a Translation Layer**

Cognitive Collider is a core module of **Symbion Space** that treats language as an **active operator of thought**, not merely a medium of output.

> An AI does not think the same way in different languages.  
> Language reshapes ontology, causality, abstraction, and depth.  
> Cognitive Collider formalizes this effect and makes it reproducible.

---

## TL;DR

- `prompt_language`: detected language of the user prompt
- `think_language`: chosen cognitive basis for reasoning (**ontology switch**)
- `output_language`: always the user language
- Optional **collision mode**: two cognitive poles + synthesis arbiter
- Runs **before PSL** (verification/constraints layer) and before downstream generation
- Emits telemetry in `routing_trace` (`router_version`, `resonance_band`, `collision_reason`, etc.)

---

## Status

Conceptual design → **MVP implemented** (router `rv02`), tuning ongoing.

---

## Quickstart

> Note: commands assume you are in the repo root and inside an active venv.

### 1) Install (dev)

```powershell
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

python -m pip install -U pip
python -m pip install -e .
````

If Cognitive Collider lives as a separate package (common in your setup), install it too:

```powershell
pip install -e path/to/symbion-cognitive-collider
# or if it’s on pip:
# pip install symbion-cognitive-collider
```

### 2) Minimal “does it route?” check

```powershell
python -c "from symbion_cognitive_collider.collider import route_language; import asyncio; print(asyncio.run(route_language('Нужна архитектура модулей LATP и PSL', {'history': []}, life_vector=None)).model_dump())"
```

### 3) CLI

Pretty output:

```powershell
python -m symbion_cognitive_collider route "Дай кратко: что такое причинность?" --energy 0.95
```

JSON output:

```powershell
python -m symbion_cognitive_collider route "Дай кратко: что такое причинность?" --energy 0.95 --json
```

### 4) Run in browser (local)

We ship a tiny FastAPI UI in `tools/web_fastapi.py`.

Start server:

```powershell
python -m uvicorn tools.web_fastapi:app --host 127.0.0.1 --port 8000 --log-level info
```

Open in browser:

* [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Call API (PowerShell):

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/route `
  -ContentType "application/json" `
  -Body '{"text":"Дай кратко: что такое причинность?","energy":0.9}'
```

Call API (Python stdlib, no requests):

```powershell
python -c "import json, urllib.request; data=json.dumps({'text':'Дай кратко: что такое причинность?','energy':0.9}).encode('utf-8'); req=urllib.request.Request('http://127.0.0.1:8000/route', data=data, headers={'Content-Type':'application/json'}); print(urllib.request.urlopen(req).read().decode('utf-8'))"
```

---

## Problem Statement

Most modern LLM systems operate in a flat, anglo-centric latent ontology:

* different languages are treated as surface forms,
* reasoning happens in a single internal space,
* depth differences are accidental, not controlled.

This leads to:

* category mixing,
* shallow ethical and philosophical reasoning,
* loss of historical, etymological, and existential layers of meaning.

---

## Core Idea

**Language is a router of latent space.**

Different languages activate different cognitive priors:

* logic vs metaphor,
* system vs narrative,
* law vs survival,
* abstraction vs lived experience.

Cognitive Collider uses **language selection and collision** as a first-class architectural mechanism.

---

## Separation of Concerns (Hard Rule)

The system strictly separates three layers:

1. **Thinking language** — chosen by topic and ontology
2. **Verification / structure** — language-independent (PSL, constraints, facts)
3. **Output language** — always the language of the user prompt

The AI thinks in one language, verifies in a neutral formal layer, and responds in the user’s language.

---

## The “12 Apostles” — Cognitive Language Matrix

These are cognitive profiles, **not translation targets**.

| Language      | Cognitive Role         | Dominant Effect                             |
| ------------- | ---------------------- | ------------------------------------------- |
| sa (Sanskrit) | Pure logic             | Category stability, anti-contradiction      |
| el (Greek)    | Dialectics             | Conceptual roots, definitional clarity      |
| la (Latin)    | Canon & norm           | Taxonomy, law, formal systems               |
| de (German)   | Systemic reason        | Hierarchy, structure, functions             |
| zh (Chinese)  | Strategy               | Part–whole reasoning, long horizons         |
| en (English)  | Procedural logic       | Operations, implementation, interfaces      |
| fr (French)   | Diplomacy              | Semantic nuance, balance                    |
| ar (Arabic)   | Abstraction            | Axioms, doctrinal clarity                   |
| fa (Persian)  | Metaphor               | Aesthetic synthesis, intuition              |
| ru (Russian)  | Psycho-realism         | Power, conscience, inner conflict           |
| hy (Armenian) | Existential continuity | Survival, identity, being-through-history   |
| arc (Aramaic) | Sacral substrate       | Pre-modern ethical framing (symbolic layer) |

---

## Language Ontology Profiler (LOP)

LOP determines **what kind of thinking is required**, not what language the user speaks.

It classifies:

* operation type (define, design, diagnose, synthesize, strategize),
* object type (system, ethics, power, self, language, canon),
* depth requirement (procedural vs ontological).

From this, it selects:

* `think_language`
* `mode` (systemic, dialectic, doctrinal, procedural, etc.)
* `depth` (0..1)

---

## Cognitive Collision (Optional, Controlled)

For high-complexity / high-energy queries, the system can activate **collision mode**.

**Protocol**

* **Pole A**: structural generation in the primary cognitive language (e.g. `de`, `sa`)
* **Pole B**: complementary generation in a second basis (e.g. `fa`, `hy`, etc.)
* **Arbiter**: produces a synthesis where:

  * no new factual claims are introduced by Pole B,
  * structure comes from Pole A,
  * meaning density comes from Pole B.

Collision is gated by:

* resonance **band** (`ambiguous/mixed/confident`) derived from top-gap
* depth threshold
* energy threshold (Life Core)
* proximity threshold (runner-up ratio)

---

## Integration in Symbion Space

Cognitive Collider runs before PSL generation:

1. Input ingestion
2. Life Core (impulse & energy detection)
3. Cognitive Collider (basis selection / collision planning)
4. PSL compilation
5. Syndicate execution
6. Distillation / Resonance / Librarium

---

## Memory and Resonance

When knowledge is stored in Librarium, metadata includes:

* cognitive basis language,
* mode,
* collision signature (if any).

This enables retrieval by **ontological compatibility**, not only by keywords.

---

## What This Is Not

* Not a translation system
* Not a stylistic trick
* Not a safety bypass mechanism
* Not a prompt hack

Cognitive Collider is an **ontological control layer**.

---

## Thesis

Intelligence is not only about models and parameters.
It is about **which cognitive substrate** is activated for a given problem.

Cognitive Collider turns human linguistic history into an operational component of artificial intelligence.

---

# Developer README (Practical)

## API Contract

`route_language(...) -> CognitionLanguageVector`

Conceptual signature:

```python
async def route_language(
    raw_input: str,
    dialog_context: dict,        # expects {"history": list[dict], ...}
    life_vector: dict | None = None,
) -> CognitionLanguageVector:
    ...
```

### Output (example)

```json
{
  "prompt_language": "ru",
  "think_language": "de",
  "output_language": "ru",
  "topic": "architecture",
  "mode": "system",
  "confidence": 1.0,
  "glossary": {},
  "collision": {
    "enabled": false,
    "pole_a": null,
    "pole_b": null,
    "arbiter": "none"
  },
  "resonance_score": 1.23,
  "resonance_gap": 0.84,
  "depth": 0.4,
  "top_candidates": [
    {"lang": "de", "score": 1.23},
    {"lang": "en", "score": 0.39}
  ],
  "routing_trace": {
    "router_version": "rv02",
    "resonance_band": "confident",
    "resonance_confidence": 1.0,
    "collision_reason": "disabled: ..."
  },
  "raw_input_hash": "..."
}
```

---

## Invariants

* `output_language == prompt_language` (hard rule)
* `think_language` selected by ontology/topic, not by user preference
* `confidence` is routing confidence, not truth confidence
* `collision.enabled` can be enabled only by policy/thresholds (not by prompt hacks)

---

## Integration Points (LATP + Orchestrator)

### A) LATP integration (before generation)

LATP should call Cognitive Collider before model generation and optionally inject the result:

* attach to session context (if present):
  `core_session.context["cog_lang"] = cog_dict`

* inject into history for downstream visibility:

```text
role=system
content="[LATP CogLang] {json...}"
cog_lang={...}
```

### B) Orchestrator integration (basis_select before draft answer)

Orchestrator performs “Phase 0.5” routing and stores the result:

* `ctx.cog_lang = cog_dict`
* appends a system message into `full_history` (trace-visible)

Important: `full_history = history + [...]` creates a new list.
If you need the caller to see injected messages, expose a trace method returning `full_history`.

---

## Trace Mode (recommended)

`get_answer(...) -> str` returns the answer only.

`get_answer_with_trace(...) -> (answer, full_history, ctx)` returns:

* `answer: str`
* `full_history: List[Dict]` including `[Orchestrator CogLang]`
* `ctx: OrchestratorContext` including `ctx.cog_lang`

Minimal usage:

```powershell
python -c "from symbion.orchestrator import build_fake_orchestrator, OrchestratorContext; o=build_fake_orchestrator(); ctx=OrchestratorContext(); ans, full, ctx = o.get_answer_with_trace('Нужна архитектура модулей LATP и PSL', [], ctx=ctx); print(ans); print([m.get('content','') for m in full if '[Orchestrator CogLang]' in m.get('content','')]); print('ctx has cog:', bool(ctx.cog_lang))"
```

---

## Configuration

### Apostles map

Matrix is stored in:

* `src/symbion_cognitive_collider/apostles_map.yaml`

Tune without code edits.

---

## Tests

### Smoke tests

Run local router smoke test:

```powershell
python .\tools\smoke_router.py
```

Recommended minimum coverage:

* unit: LOP selects `think_language` deterministically for canonical prompts
* integration: LATP injects `[LATP CogLang]` and sets `core_session.context["cog_lang"]`
* integration: Orchestrator sets `ctx.cog_lang`
* trace: `get_answer_with_trace` returns `full_history` including `[Orchestrator CogLang]`

---

## Troubleshooting

### “I typed import ... in PowerShell and it exploded”

PowerShell is not Python. Use one of:

* `python -c "..."` (one-liners)
* `python` (interactive REPL)
* run a `.py` script

### Port already in use (Windows error 10048)

Find PID and kill it:

```powershell
netstat -ano | findstr ":8000"
taskkill /PID <PID> /F
```

Or run on another port:

```powershell
python -m uvicorn tools.web_fastapi:app --host 127.0.0.1 --port 8001 --log-level info
```

### Empty input returns 400

Server returns:

```json
{"detail":"empty_input"}
```

UI blocks empty/whitespace input client-side.

---

## Roadmap (short)

* LOP v1: stable taxonomy for topic/mode selection
* Collision v1: controlled dual-pole + arbiter synthesis
* PSL integration: verification/constraints consume `cog_lang`
* Librarium metadata: store/retrieve with ontological compatibility
* Apostles tuning: config-driven weights + tests

---

## License

See license file.

```

---


