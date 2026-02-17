from __future__ import annotations

from typing import Dict, Optional, Any, List, Tuple
from .schemas import CognitionLanguageVector, CollisionPlan, CollisionPole
from .detect_language import detect_prompt_language
from .utils_hash import sha256_text
from .lop import classify_topic


import yaml
from pathlib import Path


def _load_yaml(name: str) -> dict:
    p = Path(__file__).parent / name
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


_APOSTLES = _load_yaml("apostles_map.yaml")
_COMPLEMENTS = _load_yaml("complements.yaml")  # optional legacy fallback


def _topic_contribution(topic_vector: Dict[str, float], profile: Dict[str, float]) -> Dict[str, float]:
    """Per-topic contribution to dot product (for mode derivation)."""
    contrib: Dict[str, float] = {}
    for t, w in topic_vector.items():
        if w <= 0:
            continue
        contrib[t] = float(w) * float(profile.get(t, 0.0))
    return contrib


def _resonate(topic_vector: Dict[str, float], depth: float, apostles: dict) -> List[Tuple[str, float]]:
    """
    Returns ranked list of (lang, resonance_score).
    Dot product: topic_vector × language.profile
    Depth modulation:
      - shallow (<0.3): boost procedural/system langs
      - deep (>0.7): boost languages that strongly match activated topics
    """
    languages = (apostles or {}).get("languages") or {}
    results: List[Tuple[str, float]] = []

    for lang_code, lang_data in languages.items():
        profile = (lang_data or {}).get("profile") or {}

        score = 0.0
        for topic, w in topic_vector.items():
            score += float(w) * float(profile.get(topic, 0.0))

        # depth modulation
        if depth < 0.3:
            if lang_code in ("en", "de", "la"):
                score *= 1.3
        elif depth > 0.7:
            # boost if this language is "deeply aligned" with any strongly activated topic
            strong_topics = [t for t, w in topic_vector.items() if w > 0.5]
            max_profile_val = 0.0
            for t in strong_topics:
                max_profile_val = max(max_profile_val, float(profile.get(t, 0.0)))
            if max_profile_val > 0.7:
                score *= (1.0 + float(depth) * 0.3)

        results.append((lang_code, float(score)))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def _derive_mode(topic_vector: Dict[str, float], lang_code: str, apostles: dict) -> str:
    """
    Mode is derived from the topic that contributed most to the winning language score.
    Uses legacy topic->mode mapping if present in complements.yaml or apostles_map old structure,
    otherwise defaults to procedural.
    """
    # 1) If complements.yaml keeps legacy mapping: topics -> mode
    # (We keep this flexible; if not found, proceed.)
    legacy_topic_modes = (_COMPLEMENTS or {}).get("topic_modes") or {}

    languages = (apostles or {}).get("languages") or {}
    profile = ((languages.get(lang_code) or {}).get("profile")) or {}

    contrib = _topic_contribution(topic_vector, profile)
    if contrib:
        top_topic = max(contrib.items(), key=lambda kv: kv[1])[0]
    else:
        top_topic = max(topic_vector.items(), key=lambda kv: kv[1])[0] if topic_vector else "procedural"

    # Try explicit legacy mapping first
    if top_topic in legacy_topic_modes:
        return str(legacy_topic_modes[top_topic])

    # 2) Fall back: if old apostles structure existed (topics: {topic: {mode: ...}})
    old_topics = (apostles or {}).get("topics") or {}
    if top_topic in old_topics and isinstance(old_topics[top_topic], dict):
        m = old_topics[top_topic].get("mode")
        if m:
            return str(m)

    # 3) Default heuristic
    default_modes = {
        "architecture": "system",
        "logic_definition": "precision",
        "etymology_dialectic": "dialectic",
        "canon_norm": "canon",
        "strategy": "strategy",
        "procedural": "procedural",
        "existential": "existential",
        "psycho_realism": "psycho_realism",
        "metaphor_synthesis": "mythic",
        "diplomacy_nuance": "nuance",
        "abstraction_doctrine": "doctrine",
        "sacral_symbolic": "symbolic",
    }
    return default_modes.get(top_topic, "procedural")


def _dynamic_collision(
    ranked: List[Tuple[str, float]],
    depth: float,
    life_vector: Optional[dict],
    resonance_gap: float = 0.0,
) -> CollisionPlan:
    """
    Collision activates when:
      1) Top2 close: ratio > 0.75
      2) depth > 0.5
      3) optional energy gate: energy_score > 0.4 (or no life_vector)
    """
    if not ranked or len(ranked) < 2:
        return CollisionPlan(enabled=False)

    first_lang, first_score = ranked[0]
    second_lang, second_score = ranked[1]

    # Prefer a more complementary pole_b from top3 if it is not too weak.
    # This helps avoid always picking the immediate runner-up when a strong 3rd candidate exists.
    if len(ranked) >= 3:
        third_lang, third_score = ranked[2]
        try:
            if float(third_score) / float(first_score) > 0.65:
                second_lang, second_score = third_lang, third_score
        except Exception:
            pass

    if float(first_score) <= 0.0:
        return CollisionPlan(enabled=False)

    proximity = float(second_score) / float(first_score)

    band = _resonance_band(float(resonance_gap)) if resonance_gap is not None else "none"
    if band == "ambiguous":
        return CollisionPlan(enabled=False)

    proximity_threshold = 0.75
    if band == "confident":
        proximity_threshold = 0.70

    energy = 0.0
    if life_vector is not None:
        try:
            energy = float(life_vector.get("energy_score", 0.0))
        except Exception:
            energy = 0.0

    enable = (
        proximity > float(proximity_threshold)
        and float(depth) > 0.5
        and (energy > 0.4 or life_vector is None)
    )

    if not enable:
        return CollisionPlan(enabled=False)

    return CollisionPlan(
        enabled=True,
        pole_a=CollisionPole(lang=str(first_lang), role="structure"),
        pole_b=CollisionPole(lang=str(second_lang), role="complement"),
        arbiter="synthesis",
    )



def _resonance_band(gap: float) -> str:
    # start thresholds (can be tuned after telemetry)
    if gap < 0.10:
        return "ambiguous"
    if gap < 0.25:
        return "mixed"
    return "confident"


def _resonance_confidence(gap: float) -> float:
    # maps gap from [0.10..0.25] roughly to [0..1], clamps outside
    if gap <= 0.10:
        return 0.0
    if gap >= 0.25:
        return 1.0
    return (gap - 0.10) / (0.25 - 0.10)


async def route_language(raw_input: str, dialog_context: Dict, life_vector: Optional[dict] = None) -> CognitionLanguageVector:
    raw_hash = sha256_text(raw_input or "")
    prompt_lang = detect_prompt_language(raw_input)

    # Vector LOP
    lop = classify_topic(raw_input, dialog_context)

    # Resonance selection
    ranked = _resonate(lop.topic_vector, lop.depth, _APOSTLES)
    if ranked:
        think_lang = ranked[0][0]
        resonance_score = ranked[0][1]
        resonance_gap = (ranked[0][1] - ranked[1][1]) if len(ranked) > 1 else ranked[0][1]
        top_candidates = [{"lang": l, "score": s} for (l, s) in ranked[:3]]
        resonance_band = _resonance_band(float(resonance_gap))
        resonance_conf = _resonance_confidence(float(resonance_gap))

        # enrich routing trace (no schema changes needed)
        try:
            lop.trace["resonance_band"] = resonance_band
            lop.trace["resonance_confidence"] = float(resonance_conf)
        except Exception:
            pass
    else:
        defaults = (_APOSTLES or {}).get("defaults") or {}
        think_lang = defaults.get("fallback_lang", "en")
        resonance_score = 0.0
        resonance_gap = 0.0
        top_candidates = []

        resonance_band = "none"
        resonance_conf = 0.0
        try:
            lop.trace["resonance_band"] = resonance_band
            lop.trace["resonance_confidence"] = float(resonance_conf)
        except Exception:
            pass
    mode = _derive_mode(lop.topic_vector, think_lang, _APOSTLES)

    # Dynamic collision
    collision = _dynamic_collision(ranked, lop.depth, life_vector, resonance_gap)

    # Keep external contract unchanged (we only add optional fields if schemas.py supports them)
    payload = dict(
        prompt_language=prompt_lang,
        think_language=think_lang,
        output_language=prompt_lang,
        topic=lop.dominant_topic,  # backward compat
        mode=mode,
        confidence=lop.confidence,
        glossary={},
        collision=collision,
        routing_trace=lop.trace,
        raw_input_hash=raw_hash,
    )

    # Optional enrichment if model has those fields
    # (Pydantic v2: we can pass extra only if model allows; safest is try/except)
    try:
        payload.update(
            resonance_score=float(resonance_score),
            resonance_gap=float(resonance_gap),
            depth=float(lop.depth),
            top_candidates=top_candidates,
        )
    except Exception:
        pass
    return CognitionLanguageVector(**payload)