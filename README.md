# Cognitive Collider (Symbion Space)
**Language as an Ontological Basis Switch — not a Translation Layer**

Cognitive Collider is a core module of Symbion Space that treats language as an active operator of thought, not merely a medium of output.

An AI does not think the same way in different languages.  
Language reshapes ontology, causality, abstraction, and depth.

Cognitive Collider formalizes this effect and makes it reproducible.

## TL;DR
- `prompt_language`: detected language of the user prompt
- `think_language`: chosen cognitive basis for reasoning (**ontology switch**)
- `output_language`: always the user language
- Optional **collision mode**: two cognitive poles + synthesis arbiter
- Integrates **before PSL** (verification/constraints layer) and before downstream generation.

## Status
Conceptual design → implementation in progress as part of Symbion Space.

---

# Quickstart
> Note: examples assume you are in the repository root and inside an active venv.

## 1) Install
```powershell
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

python -m pip install -U pip
python -m pip install -e .
python -m pip install -e path/to/symbion-cognitive-collider
# or if it’s on pip:
# python -m pip install symbion-cognitive-collider
python -c "from symbion_cognitive_collider.collider import route_language; import asyncio; print(asyncio.run(route_language('Нужна архитектура модулей LATP и PSL', {'history': []}, life_vector=None)).model_dump())"
python -c "from symbion.orchestrator import build_fake_orchestrator, OrchestratorContext; o=build_fake_orchestrator(); ctx=OrchestratorContext(); print(o.get_answer('Нужна архитектура модулей LATP и PSL', [], ctx=ctx)); print('COG:', bool(ctx.cog_lang)); print(ctx.cog_lang)"
Problem Statement

Most modern LLM systems operate in a flat, anglo-centric latent ontology:

different languages are treated as surface forms,

reasoning happens in a single internal space,

depth differences are accidental, not controlled.

This leads to:

category mixing,

shallow ethical and philosophical reasoning,

loss of historical, etymological, and existential layers of meaning.

Core Idea

Language is a router of latent space.

Different languages activate different cognitive priors:

logic vs metaphor,

system vs narrative,

law vs survival,

abstraction vs lived experience.

Cognitive Collider uses language selection and collision as a first-class architectural mechanism.

Separation of Concerns (Hard Rule)

The system strictly separates three layers:

Thinking language — chosen by topic and ontology

Verification / structure — language-independent (PSL, constraints, facts)

Output language — always the language of the user prompt

The AI thinks in one language,
structures and verifies in a neutral formal layer,
and responds in the user’s language.

The “12 Apostles” — Cognitive Language Matrix

The system operates with a fixed set of cognitive language bases.

LanguageCognitive RoleDominant Effect
sa (Sanskrit)Pure logicCategory stability, anti-contradiction
el (Greek)DialecticsConceptual roots, definitional clarity
la (Latin)Canon & normTaxonomy, law, formal systems
de (German)Systemic reasonHierarchy, structure, functions
zh (Chinese)StrategyPart–whole reasoning, long horizons
en (English)Procedural logicOperations, implementation, interfaces
fr (French)DiplomacySemantic nuance, balance
ar (Arabic)AbstractionAxioms, doctrinal clarity
fa (Persian)MetaphorAesthetic synthesis, intuition
ru (Russian)Psycho-realismPower, conscience, inner conflict
hy (Armenian)Existential continuitySurvival, identity, being-through-history
arc (Aramaic)Sacral substratePre-modern ethical framing (symbolic layer)

These are cognitive profiles, not translation targets.

Language Ontology Profiler (LOP)

LOP determines what kind of thinking is required, not what language the user speaks.

It classifies:

operation type (define, design, diagnose, synthesize, strategize),

object type (system, ethics, power, self, language, canon),

depth requirement (procedural vs ontological).

From this, it selects:

think_language

mode (systemic, dialectic, mythic, procedural, etc.)

Cognitive Collision (Optional, Controlled)

For high-complexity or high-energy queries, the system can activate collision mode.

Protocol

Pole A: structural generation in the primary cognitive language (e.g. de for systems, sa for logic)

Pole B: complementary generation in an opposing language (e.g. fa for metaphor, hy for existential depth)

Arbiter: produces a synthesis where:

no new factual claims are introduced by Pole B,

structure comes from Pole A,

meaning density comes from Pole B.

This is a controlled dialectical synthesis, not freeform creativity.

Integration in Symbion Space

Cognitive Collider is integrated before PSL generation:

Input ingestion

Life Core (impulse & energy detection)

Cognitive Collider (basis selection / collision planning)

PSL compilation

Syndicate execution

Distillation / Resonance / Librarium

Memory and Resonance

When knowledge is stored in Librarium, metadata includes:

cognitive basis language,

mode,

collision signature (if any).

This allows future retrieval not only by structure, but by ontological compatibility.

What This Is Not

Not a translation system.

Not a stylistic trick.

Not a safety bypass mechanism.

Not a prompt hack.

Cognitive Collider is an ontological control layer.

Thesis

Intelligence is not only about models and parameters.
It is about which cognitive substrate is activated for a given problem.

Cognitive Collider turns human linguistic history into an operational component of artificial intelligence.

Developer README (Practical)

Everything below is the “how”.

API Contract

route_language(...) -> CogResult

Conceptual signature:

async def route_language(
    user_text: str,
    ctx: dict,                 # expects {"history": list[dict], ...}
    life_vector: dict | None = None
) -> CogResult

CogResult fields (expected)

Typical output (example):

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
    "arbiter": "synthesis"
  },
  "routing_trace": {
    "signals": ["architecture+1.2:system/architecture keywords"],
    "scores": {"architecture": 1.2}
  },
  "raw_input_hash": "..."
}

Invariants

output_language == prompt_language (hard rule)

think_language is selected by ontology/topic, not by user preference

confidence is routing confidence, not truth confidence

collision.enabled may be enabled only by policy/thresholds (not by “prompt hacks”)

Integration Points (LATP + Orchestrator)
A) LATP integration (before generation)

LATP should call Cognitive Collider before model generation and optionally inject the result:

attach to session context (if present):
core_session.context["cog_lang"] = cog_dict

inject into history for downstream visibility:

role=system
content="[LATP CogLang] {json...}"
cog_lang={...}

B) Orchestrator integration (basis_select before draft answer)

Orchestrator performs “Phase 0.5” routing and stores the result:

ctx.cog_lang = cog_dict

And appends a system message into full_history (trace-visible):

role=system
content="[Orchestrator CogLang] {json...}"
cog_lang={...}


Important: history passed into get_answer() is not mutated if you build a new list:

full_history = history + [...]


If you need the caller to see injected messages, expose a trace method returning full_history.

Trace Mode (recommended)

If you want to inspect what the Orchestrator injected:

get_answer(...) -> str returns just the answer.

get_answer_with_trace(...) -> (answer, full_history, ctx) returns:

answer: str

full_history: List[Dict] including [Orchestrator CogLang]

ctx: OrchestratorContext including ctx.cog_lang

Minimal usage:

python -c "from symbion.orchestrator import build_fake_orchestrator, OrchestratorContext; o=build_fake_orchestrator(); ctx=OrchestratorContext(); ans, full, ctx = o.get_answer_with_trace('Нужна архитектура модулей LATP и PSL', [], ctx=ctx); print(ans); print([m.get('content','') for m in full if '[Orchestrator CogLang]' in m.get('content','')]); print('ctx has cog:', bool(ctx.cog_lang))"

Configuration
Apostles map

Preferred: keep the matrix in a config file so it can be tuned without code edits.

Example file: symbion_cognitive_collider/config/apostles.yaml (or .json)

Suggested structure:

languages:
  de:
    role: "Systemic reason"
    effects: ["hierarchy", "structure", "functions"]
  ru:
    role: "Psycho-realism"
    effects: ["power", "conscience", "inner conflict"]

Policy knobs (recommended)

collision.enabled_default: bool

collision.threshold: float (complexity/energy)

routing.weights.* for signals

fallback_think_language (safe default, e.g. en or de)

Tests

Run:

pytest -q


Recommended minimum coverage:

unit: LOP selects think_language deterministically for canonical prompts

integration: LATP injects [LATP CogLang] and sets core_session.context["cog_lang"]

integration: Orchestrator sets ctx.cog_lang

trace: get_answer_with_trace returns full_history that includes [Orchestrator CogLang]

Troubleshooting (common traps)
“I typed import ... in PowerShell and it exploded”

PowerShell is not Python. Use one of:

python -c "..." (one-liners)

python (enter interactive REPL)

run a .py script

asyncio.run() inside a running event loop

If you call Collider from a context that already has an event loop (e.g. some async frameworks), use a safe wrapper:

detect running loop

if running: execute coroutine in a new thread with its own event loop

else: asyncio.run(...)

ModuleNotFoundError: symbion_cognitive_collider

Means your venv doesn’t have the package.

Fix:

python -m pip install -e path/to/symbion-cognitive-collider
# or python -m pip install symbion-cognitive-collider

“Why don’t I see CogLang in my history list?”

Because full_history = history + [...] creates a new list.
Return the trace list, or mutate the caller list intentionally (not recommended by default).

Roadmap (short)

LOP v1: stable taxonomy for topic/mode selection

Collision v1: controlled dual-pole + arbiter synthesis

PSL integration: verification/constraints consume cog_lang

Librarium metadata: store/retrieve with ontological compatibility

Apostles tuning: config-driven weights + tests

symbion-cognitive-collider (MVP Router)

Minimal MVP router that:

classifies topic + depth (LOP)

selects think language by resonance profiles (apostles_map.yaml)

optionally enables a "collision" (two-pole plan) gated by resonance band + depth + energy

emits telemetry in routing_trace (router_version, band/confidence, collision_reason, etc.)

Requirements

Python 3.11+

Windows PowerShell (or any shell)

Install (dev)

From repo root:

python -m pip install -e .

CLI

Route one prompt (pretty):

python -m symbion_cognitive_collider route "Дай кратко: что такое причинность?" --energy 0.95


Route one prompt (JSON):

python -m symbion_cognitive_collider route "Дай кратко: что такое причинность?" --energy 0.95 --json

Run in browser (local)

We ship a tiny FastAPI UI in tools/web_fastapi.py.

1) Start server

Important: if port 8000 is busy, pick another port (e.g. 8001).

python -m uvicorn tools.web_fastapi:app --host 127.0.0.1 --port 8000 --log-level info


Open in browser:

http://127.0.0.1:8000/

2) Call API (PowerShell)
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/route `
  -ContentType "application/json" `
  -Body '{"text":"Дай кратко: что такое причинность?","energy":0.9}'

3) Call API (Python stdlib, no requests)
python -c "import json, urllib.request; data=json.dumps({'text':'Дай кратко: что такое причинность?','energy':0.9}).encode('utf-8'); req=urllib.request.Request('http://127.0.0.1:8000/route', data=data, headers={'Content-Type':'application/json'}); print(urllib.request.urlopen(req).read().decode('utf-8'))"

Troubleshooting
Port already in use (Windows error 10048)

Find PID and kill it:

netstat -ano | findstr ":8000"
taskkill /PID <PID> /F


Or run on another port:

python -m uvicorn tools.web_fastapi:app --host 127.0.0.1 --port 8001 --log-level info

Empty input returns 400

Server returns:

{"detail":"empty_input"}


UI also blocks empty/whitespace input client-side.

Smoke tests

Run the local router smoke test:

python .\tools\smoke_router.py

License

See license file.
