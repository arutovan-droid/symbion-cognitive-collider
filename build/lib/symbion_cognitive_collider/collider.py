from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

import yaml

from .schemas import CognitionLanguageVector, CollisionPlan, CollisionPole
from .detect_language import detect_prompt_language
from .lop import classify_topic
from .utils_hash import sha256_text

def _load_yaml(name: str) -> dict:
    p = Path(__file__).with_name(name)
    return yaml.safe_load(p.read_text(encoding="utf-8"))

_APOSTLES = _load_yaml("apostles_map.yaml")
_COMPLEMENTS = _load_yaml("complements.yaml")

def _choose_from_apostles(topic: str) -> tuple[str, str]:
    topics = _APOSTLES.get("topics", {})
    defaults = _APOSTLES.get("defaults", {"lang": "en", "mode": "procedural"})
    entry = topics.get(topic, defaults)
    return entry.get("lang", defaults["lang"]), entry.get("mode", defaults["mode"])

def _maybe_collision(think_lang: str, confidence: float, life_vector: Optional[dict]) -> CollisionPlan:
    rules = (_COMPLEMENTS.get("rules") or {}).get("enable_if", {})
    min_energy = float(rules.get("min_energy", 1.0))
    min_conf = float(rules.get("min_confidence", 1.0))

    energy = 0.0
    if life_vector:
        try:
            energy = float(life_vector.get("energy_score", 0.0))
        except Exception:
            energy = 0.0

    if energy < min_energy or confidence < min_conf:
        return CollisionPlan(enabled=False)

    pairs = _COMPLEMENTS.get("pairs", {})
    b = pairs.get(think_lang)
    if not b:
        return CollisionPlan(enabled=False)

    return CollisionPlan(
        enabled=True,
        pole_a=CollisionPole(lang=think_lang, role="structure"),
        pole_b=CollisionPole(lang=b, role="complement"),
        arbiter="synthesis",
    )

async def route_language(raw_input: str, dialog_context: Dict, life_vector: Optional[dict] = None) -> CognitionLanguageVector:
    raw_hash = sha256_text(raw_input or "")

    prompt_lang = detect_prompt_language(raw_input)
    lop = classify_topic(raw_input, dialog_context)

    think_lang, mode = _choose_from_apostles(lop.topic)

    collision = _maybe_collision(think_lang, lop.confidence, life_vector)

    return CognitionLanguageVector(
        prompt_language=prompt_lang,
        think_language=think_lang,
        output_language=prompt_lang,
        topic=lop.topic,
        mode=mode,
        confidence=lop.confidence,
        glossary={},
        collision=collision,
        routing_trace=lop.trace,
        raw_input_hash=raw_hash,
    )
