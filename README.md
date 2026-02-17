# symbion-cognitive-collider

Minimal MVP router that:
- classifies topic + depth (LOP)
- selects think language by resonance profiles
- optionally enables a "collision" (two-pole plan) gated by resonance gap band + depth + energy
- emits telemetry in `routing_trace` (router_version, band/confidence, collision_reason)

## Install (dev)

    python -m pip install -e .

## Run (CLI)

Route (human):

    python -m symbion_cognitive_collider route "Развернуто объясни природу причинности и сущности бытия в онтологии ньяя и санкхья. Дай глубоко, не кратко." --energy 0.95

Route (JSON):

    python -m symbion_cognitive_collider route "Дай кратко: что такое причинность?" --energy 0.95 --json

Include routing trace in human mode:

    python -m symbion_cognitive_collider route "..." --energy 0.9 --trace

## Smoke tests

    python .\tools\smoke_router.py

## Telemetry contract (routing_trace)

Key fields:
- `router_version`: current router build tag (e.g. `rv02`)
- `raw_scores` / `normalized` / `dominant_topic`
- `depth`: `{depth, reasons[]}`
- `resonance_band`: `ambiguous | mixed | confident | none`
- `resonance_confidence`: float [0..1]
- `collision_reason`: one-line decision explanation
