# Cognitive Collider (Symbion Space)

**Language as an Ontological Basis Switch — not a Translation Layer**

Cognitive Collider is a core module of **Symbion Space** that treats language as an **active operator of thought**, not merely a medium of output.

> **An AI does not think the same way in different languages.  
> Language reshapes ontology, causality, abstraction, and depth.**

Cognitive Collider formalizes this effect and makes it reproducible.

---

## TL;DR

- **prompt_language**: detected language of the user prompt  
- **think_language**: chosen cognitive basis for reasoning (ontology switch)  
- **output_language**: always the user language  
- Optional **collision mode**: two cognitive poles + synthesis arbiter  
- Integrates **before PSL** (verification/constraints layer) and before downstream generation.

---

## Status

**Conceptual design → implementation in progress** as part of **Symbion Space**.

---

## Quickstart

> Note: examples assume you are in the repository root and inside an active venv.

### 1) Install

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

pip install -U pip
pip install -e .
If Cognitive Collider lives as a separate package (common in your setup), install it too:

pip install -e path/to/symbion-cognitive-collider
# or if it’s on pip:
# pip install symbion-cognitive-collider
2) Minimal “does it route?” check
python -c "from symbion_cognitive_collider.collider import route_language; import asyncio; print(asyncio.run(route_language('Нужна архитектура модулей LATP и PSL', {'history': []}, life_vector=None)).model_dump())"
3) Through Orchestrator (if your wiring is enabled)
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

Thinking language — chosen by topic and ontology.

Verification / structure — language-independent (PSL, constraints, facts).

Output language — always the language of the user prompt.

The AI thinks in one language,
structures and verifies in a neutral formal layer,
and responds in the user’s language.

The “12 Apostles” — Cognitive Language Matrix
The system operates with a fixed set of cognitive language bases.

Language	Cognitive Role	Dominant Effect
sa (Sanskrit)	Pure logic	Category stability, anti-contradiction
el (Greek)	Dialectics	Conceptual roots, definitional clarity
la (Latin)	Canon & norm	Taxonomy, law, formal systems
de (German)	Systemic reason	Hierarchy, structure, functions
zh (Chinese)	Strategy	Part–whole reasoning, long horizons
en (English)	Procedural logic	Operations, implementation, interfaces
fr (French)	Diplomacy	Semantic nuance, balance
ar (Arabic)	Abstraction	Axioms, doctrinal clarity
fa (Persian)	Metaphor	Aesthetic synthesis, intuition
ru (Russian)	Psycho-realism	Power, conscience, inner conflict
hy (Armenian)	Existential continuity	Survival, identity, being-through-history
arc (Aramaic)	Sacral substrate	Pre-modern ethical framing (symbolic layer)
These are cognitive profiles, not translation targets.

Language Ontology Profiler (LOP)
LOP determines:

what kind of thinking is required, not what language the user speaks.

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
Pole A: structural generation in the primary cognitive language
(e.g. de for systems, sa for logic).

Pole B: complementary generation in an opposing language
(e.g. fa for metaphor, hy for existential depth).

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
Signature (conceptual):

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

confidence is a routing confidence, not truth confidence

collision.enabled may be enabled only by policy/thresholds (not by “prompt hacks”)

Integration Points (LATP + Orchestrator)
A) LATP integration (before generation)
LATP should call Cognitive Collider before model generation and optionally inject the result:

attach to session context (if present): core_session.context["cog_lang"] = cog_dict

inject into history for downstream visibility:

role=system
content="[LATP CogLang] {json...}"
cog_lang={...}
B) Orchestrator integration (basis_select before draft answer)
Orchestrator performs “Phase 0.5” routing and stores the result:

ctx.cog_lang = cog_dict

appends a system message into full_history (trace-visible):

role=system
content="[Orchestrator CogLang] {json...}"
cog_lang={...}
Important: history passed into get_answer() is not mutated if you build a new list:
full_history = history + [...]
If you need the caller to see injected messages, expose a trace method returning full_history.

Trace Mode (recommended)
If you want to inspect what the Orchestrator injected:

get_answer(...) -> str
Returns just the answer.

get_answer_with_trace(...) -> (answer, full_history, ctx)
Returns:

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
  # ...
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

pip install -e path/to/symbion-cognitive-collider
# or pip install symbion-cognitive-collider
“Why don’t I see CogLang in my history list?”
Because full_history = history + [...] creates a new list.
Return the trace list, or mutate the caller list intentionally (not recommended by default).

Roadmap (short)
LOP v1: stable taxonomy for topic/mode selection

Collision v1: controlled dual-pole + arbiter synthesis

PSL integration: verification/constraints consume cog_lang

Librarium metadata: store/retrieve with ontological compatibility

Apostles tuning: config-driven weights + tests

License
See license file.

