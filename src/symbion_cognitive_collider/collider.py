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



def _cosine(a: dict, b: dict, keys) -> float:
    # a, b: dict[str,float]; keys: iterable of topics to align on
    import math
    dot = 0.0
    na = 0.0
    nb = 0.0
    for k in keys:
        av = float(a.get(k, 0.0)) if a else 0.0
        bv = float(b.get(k, 0.0)) if b else 0.0
        dot += av * bv
        na += av * av
        nb += bv * bv
    if na <= 0.0 or nb <= 0.0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))


def _choose_pole_b_diverse(
    ranked,
    depth: float,
    apostles: dict,
    topic_vector: dict,
    strength_floor: float = 0.65,
):
    """
    Choose a complementary pole_b among top candidates.
    Returns: (lang, score, meta_dict)
    meta_dict contains: select_mode, strength, diversity, utility
    """
    if not ranked or len(ranked) < 2:
        return None, 0.0, {"select_mode": "none"}
    keys = list((topic_vector or {}).keys())
    if not keys:
        keys = list(prof_a.keys())
    if not keys:
        # if topic_vector missing, fall back to score-only
        l, s = ranked[1]
        return l, float(s), {"select_mode": "runner_up"}

    langs = (apostles or {}).get("languages", {}) if apostles else {}
    first_lang, first_score = ranked[0]
    first_score = float(first_score) if first_score is not None else 0.0
    prof_a = (langs.get(str(first_lang), {}) or {}).get("profile") or {}
    # tilt across top2 active topics (helps pick a complementary pole_b on dense themes)
    _active = list((topic_vector or {}).keys()) if topic_vector else []
    _tilt_keys = _active[:2] if len(_active) >= 2 else []
    def _tilt(profile: dict) -> float:
        try:
            if len(_tilt_keys) == 2:
                a = float(profile.get(_tilt_keys[0], 0.0))
                b = float(profile.get(_tilt_keys[1], 0.0))
                return a - b
        except Exception:
            pass
        return 0.0
    _tilt_a = _tilt(prof_a)
    # baseline diversity against runner-up (dense-topic bonus)
    _baseline_div = None
    try:
        _ru_lang, _ru_score = ranked[1]
        _ru_prof = (langs.get(str(_ru_lang), {}) or {}).get('profile') or {}
        _k = list((topic_vector or {}).keys()) or list(prof_a.keys())
        _baseline_div = max(0.0, 1.0 - float(_cosine(prof_a, _ru_prof, _k)))
    except Exception:
        _baseline_div = None

    best = None
    best_meta = None

    # candidates from ranked[1:4]
    for lang, score in ranked[1:4]:
        sc = float(score)
        if first_score <= 0.0:
            continue
        strength = sc / first_score
        if strength < strength_floor:
            continue

        prof_b = (langs.get(str(lang), {}) or {}).get("profile") or {}
        cos = _cosine(prof_a, prof_b, keys)
        diversity = max(0.0, 1.0 - float(cos))
        # tilt distance (only meaningful if we have 2 active topics)
        tilt_b = _tilt(prof_b)
        tilt_dist = abs(float(tilt_b) - float(_tilt_a)) if _tilt_keys else 0.0
        # contribution distance on active topics (strong complement signal)
        dist = 0.0
        try:
            for k in keys:
                w = float((topic_vector or {}).get(k, 0.0)) if topic_vector else 0.0
                if w <= 0.0:
                    continue
                ca = float(prof_a.get(k, 0.0)) * w
                cb = float(prof_b.get(k, 0.0)) * w
                dist += abs(ca - cb)
        except Exception:
            dist = 0.0
        dist_norm = min(1.0, float(dist))

        # depth-sensitive weighting
        if float(depth) >= 0.6:
            utility = 0.55 * strength + 0.25 * diversity + 0.20 * dist_norm
        else:
            utility = 0.80 * strength + 0.20 * diversity

        # dense-topic diversity bonus: prefer distinctly different pole_b when depth is high
        try:
            if float(depth) >= 0.6 and _baseline_div is not None and diversity >= float(_baseline_div) + 0.08:
                utility += 0.03
        except Exception:
            pass

        meta = {
            "tilt": float(tilt_b) if _tilt_keys else None,
            "tilt_dist": float(tilt_dist) if _tilt_keys else None,
            "dist": float(dist_norm),
            "select_mode": "diverse",
            "strength": float(strength),
            "diversity": float(diversity),
            "utility": float(utility),
            "candidate": str(lang),
        }

        if best is None or utility > best_meta["utility"]:
            best = (str(lang), sc)
            best_meta = meta

    if best is None:
        # fallback to runner-up
        l, sc = ranked[1]
        return str(l), float(sc), {"select_mode": "runner_up"}

    return best[0], float(best[1]), best_meta


def _dynamic_collision(
    ranked: List[Tuple[str, float]],
    depth: float,
    life_vector: Optional[dict],
    resonance_gap: float = 0.0,
    topic_vector: Optional[dict] = None,
    telemetry: Optional[dict] = None,
) -> CollisionPlan:
    """
    Collision activates when:
      1) Top2 close: ratio > 0.75
      2) depth > 0.5
      3) optional energy gate: energy_score > 0.4 (or no life_vector)
    """
    if not ranked or len(ranked) < 2:
        return CollisionPlan(enabled=False, arbiter="none")

    first_lang, first_score = ranked[0]

    second_lang, second_score = ranked[1]

    # Depth-sensitive, profile-diverse pole_b choice (telemetry-only; keeps collision gates intact)
    try:
        chosen_lang, chosen_score, meta = _choose_pole_b_diverse(
            ranked,
            depth=float(depth),
            apostles=_APOSTLES,
            topic_vector=topic_vector or {},
        )
        if chosen_lang:
            second_lang, second_score = chosen_lang, chosen_score
        # stash meta on function attribute-like local for route_language to capture (best-effort)
        if telemetry is not None and isinstance(telemetry, dict):
            telemetry['collision_pole_b_meta'] = meta
    except Exception:
        if telemetry is not None and isinstance(telemetry, dict):
            telemetry['collision_pole_b_meta'] = {'select_mode': 'runner_up'}

    if float(first_score) <= 0.0:
        return CollisionPlan(enabled=False, arbiter="none")

    proximity = float(second_score) / float(first_score)

    band = _resonance_band(float(resonance_gap)) if resonance_gap is not None else "none"
    if band == "ambiguous":
        return CollisionPlan(enabled=False, arbiter="none")

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
        return CollisionPlan(enabled=False, arbiter="none")

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


    # telemetry versioning
    try:
        lop.trace["router_version"] = "rv02"
    except Exception:
        pass

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
    _collision_telemetry = {}
    collision = _dynamic_collision(ranked, lop.depth, life_vector, resonance_gap, lop.topic_vector, _collision_telemetry)

    # Explain collision decision in routing_trace (telemetry only)
    try:
        band = lop.trace.get("resonance_band", "none")
        gap = float(resonance_gap) if resonance_gap is not None else 0.0

        # Recompute key gates for explainability (keep consistent with _dynamic_collision)
        proximity = None
        first_score = None
        energy = 0.0

        if ranked and len(ranked) >= 2:
            first_score = float(ranked[0][1])
            second_score = float(ranked[1][1])
            if first_score > 0.0:
                proximity = float(second_score) / float(first_score)

        if life_vector is not None:
            try:
                energy = float(life_vector.get("energy_score", 0.0))
            except Exception:
                energy = 0.0

        # Thresholds mirrored from _dynamic_collision
        proximity_threshold = 0.75
        if band == "confident":
            proximity_threshold = 0.70

        enabled = getattr(collision, "enabled", False)

        if not ranked or len(ranked) < 2:
            reason = "disabled: ranked<2"
        elif first_score is not None and first_score <= 0.0:
            reason = "disabled: first_score<=0"
        elif band == "ambiguous":
            reason = f"disabled: band=ambiguous gap={gap:.3f}"
        else:
            parts = [f"band={band}", f"gap={gap:.3f}"]
            # pole_b selection meta (if available)
            try:
                meta = (_collision_telemetry.get('collision_pole_b_meta') if isinstance(_collision_telemetry, dict) else {}) or {}
                if isinstance(meta, dict):
                    lop.trace["collision_pole_b_select"] = meta.get("select_mode")
                    if meta.get("select_mode") == "diverse":
                        lop.trace["collision_pole_b_strength"] = float(meta.get("strength", 0.0))
                        lop.trace["collision_pole_b_diversity"] = float(meta.get("diversity", 0.0))
                        lop.trace["collision_pole_b_tilt"] = meta.get("tilt")
                        lop.trace["collision_pole_b_tilt_dist"] = meta.get("tilt_dist")
                        lop.trace["collision_pole_b_dist"] = float(meta.get("dist", 0.0))
                        parts.append(f"pole_b_dist={float(meta.get('dist',0.0)):.3f}")
                        if meta.get('tilt_dist') is not None:
                            parts.append(f"pole_b_tilt_dist={float(meta.get('tilt_dist',0.0)):.3f}")
                        parts.append(f"pole_b_strength={float(meta.get('strength',0.0)):.3f}")
                        parts.append(f"pole_b_diversity={float(meta.get('diversity',0.0)):.3f}")
            except Exception:
                pass
            if proximity is not None:
                parts.append(f"proximity={proximity:.3f}>{proximity_threshold:.2f}" if proximity > proximity_threshold else f"proximity={proximity:.3f}<={proximity_threshold:.2f}")
            parts.append(f"depth={float(lop.depth):.3f}>0.50" if float(lop.depth) > 0.5 else f"depth={float(lop.depth):.3f}<=0.50")
            if life_vector is None:
                parts.append("energy=none")
            else:
                parts.append(f"energy={energy:.3f}>0.40" if energy > 0.4 else f"energy={energy:.3f}<=0.40")

            # Detect whether pole_b came from top3 (heuristic)
            try:
                pole_b = getattr(getattr(collision, "pole_b", None), "lang", None)
                if pole_b and len(ranked) >= 3 and str(pole_b) == str(ranked[2][0]):
                    parts.append("pole_b=top3")
            except Exception:
                pass

            reason = ("enabled: " if enabled else "disabled: ") + " ".join(parts)

        lop.trace["collision_reason"] = reason
    except Exception:
        pass

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