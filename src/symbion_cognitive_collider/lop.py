from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Any


# Topic space (keep in sync with apostles_map.yaml profiles)
TOPICS: List[str] = [
    "logic_definition",
    "etymology_dialectic",
    "abstraction_doctrine",
    "existential",
    "canon_norm",
    "sacral_symbolic",
    "architecture",
    "strategy",
    "procedural",
    "psycho_realism",
    "metaphor_synthesis",
    "diplomacy_nuance",
]

# Multilingual keyword map (RU + EN baseline; extend progressively)
KEYWORD_MAP: Dict[str, Dict[str, Any]] = {
    "architecture": {
        "weight": 1.2,
        "keywords": [
            # RU
            "архитект", "система", "модул", "оркестр", "пайплайн", "репозитор", "сборк",
            # EN
            "architecture", "system", "module", "orchestr", "pipeline", "repository", "build",
            "latp", "psl",
        ],
    },
    "logic_definition": {
        "weight": 1.0,
        "keywords": [
            # RU
            "определи", "определение", "дефиниц", "аксиом", "логик", "категор", "противореч", "причин",
            # EN
            "define", "definition", "axiom", "logic", "category", "contradict",
            "causality", "cause", "syllogism",
        ],
    },
    "etymology_dialectic": {
        "weight": 1.0,
        "keywords": [
            # RU
            "этимолог", "корень", "происхожд", "понятие", "диалектик", "смысл слова",
            # EN
            "etymology", "root", "origin", "dialectic", "conceptual roots",
        ],
    },
    "canon_norm": {
        "weight": 1.0,
        "keywords": [
            # RU
            "норма", "канон", "закон", "юрид", "таксоном", "классификац", "регламент",
            # EN
            "norm", "canon", "law", "legal", "taxonomy", "classification", "regulation",
        ],
    },
    "strategy": {
        "weight": 1.0,
        "keywords": [
            # RU
            "стратег", "тактик", "ход", "игра", "долгоср", "часть-целое", "план",
            # EN
            "strategy", "tactic", "move", "game", "long-term", "part-whole", "plan",
        ],
    },
    "procedural": {
        "weight": 1.0,
        "keywords": [
            # RU
            "сделай", "пошаг", "как установить", "команда", "инструкция", "api", "код", "настрой",
            # EN
            "step by step", "how to", "install", "command", "instructions", "api", "code", "setup",
        ],
    },
    "existential": {
        "weight": 1.0,
        "keywords": [
            # RU
            "смысл", "бытие", "выживание", "идентичн", "экзистенц", "жизнь", "судьб",
            # EN
            "meaning", "being", "survival", "identity", "existential", "life", "fate",
        ],
    },
    "psycho_realism": {
        "weight": 1.0,
        "keywords": [
            # RU
            "власть", "совесть", "страх", "стыд", "вина", "конфликт", "травм",
            # EN
            "power", "conscience", "fear", "shame", "guilt", "conflict", "trauma",
        ],
    },
    "metaphor_synthesis": {
        "weight": 1.0,
        "keywords": [
            # RU
            "метафор", "поэтич", "синтез", "символ", "миф", "образ",
            # EN
            "metaphor", "poetic", "synthesis", "symbol", "myth", "imagery",
        ],
    },
    "diplomacy_nuance": {
        "weight": 0.9,
        "keywords": [
            # RU
            "нюанс", "дипломат", "тонко", "аккуратн", "деликатн", "баланс",
            # EN
            "nuance", "diplomacy", "tact", "careful", "delicate", "balance",
        ],
    },
    "abstraction_doctrine": {
        "weight": 0.9,
        "keywords": [
            # RU
            "доктрин", "абстракц", "принцип", "догмат", "постулат", "аксиоматик",
            # EN
            "doctrine", "abstraction", "principle", "dogma", "postulate", "axiomatic",
            "причин", "причинность", "causality",

        ],
    },
    "sacral_symbolic": {
        "weight": 0.9,
        "keywords": [
            # RU
            "сакрал", "свящ", "ритуал", "символ", "мистич", "этик", "грех",
            # EN
            "sacral", "sacred", "ritual", "symbolic", "mystic", "ethic", "sin",
            # translit / common
            "halakh", "torah", "talmud",
        ],
    },
}

PHILOSOPHY_TERMS: List[str] = [
    # RU / translit
    "ньяя", "санкхья", "вайшешика", "миманса", "веданта", "мадхьямака",
    # EN
    "nyaya", "samkhya", "vaisheshika", "mimamsa", "vedanta", "madhyamaka",
]

DEPTH_PHRASES_HIGH: List[str] = [
    "что есть", "что такое", "природа", "сущность", "онтолог", "глубок",
    "what is", "nature of", "essence", "ontolog", "deep",
]

DEPTH_PHRASES_LOW: List[str] = [
    "кратко", "быстро", "пошаг", "по шагам",
    "brief", "quick", "step by step",
]


@dataclass(frozen=True)
class LOPResult:
    topic_vector: Dict[str, float]     # activated topics with weights (normalized; top=1.0)
    dominant_topic: str                # highest-scoring topic (backward compat)
    depth: float                       # 0..1 (procedural..ontological)
    confidence: float                  # overall routing confidence 0..1
    trace: Dict[str, Any]              # debug trace


def _scan_keywords(text: str) -> Dict[str, float]:
    t = (text or "").lower()
    scores: Dict[str, float] = {}
    signals: List[str] = []

    for topic, spec in KEYWORD_MAP.items():
        w = float(spec.get("weight", 1.0))
        kws = spec.get("keywords", [])
        hit = False
        for kw in kws:
            if kw and kw in t:
                scores[topic] = scores.get(topic, 0.0) + w
                signals.append(f"{topic}+{w}:{kw}")
                hit = True
        # If no hit, keep absent (sparse vector)
        _ = hit

    return scores


def _accumulate_context(current_scores: Dict[str, float], history: List[Dict[str, Any]], decay: float = 0.3) -> Dict[str, float]:
    if not history:
        return current_scores

    for msg in history[-3:]:
        text = (msg or {}).get("content", "")
        hist_scores = _scan_keywords(text)
        for topic, w in hist_scores.items():
            current_scores[topic] = current_scores.get(topic, 0.0) + float(w) * decay

    return current_scores


def _estimate_depth(text: str, topic_scores: Dict[str, float]) -> Dict[str, Any]:
    t = (text or "").lower()
    depth = 0.0
    reasons: List[str] = []

    # length > 200 chars
    if len(t) > 200:
        depth += 0.2
        reasons.append("len>200:+0.2")

    # philosophy school names
    if any(term in t for term in PHILOSOPHY_TERMS):
        depth += 0.3
        reasons.append("philosophy_terms:+0.3")

    # essence / what is / nature
    if any(p in t for p in DEPTH_PHRASES_HIGH):
        depth += 0.2
        reasons.append("essence_phrases:+0.2")

    # multiple topics active (3+)
    active_topics = [k for k, v in topic_scores.items() if v > 0.0]
    if len(active_topics) >= 3:
        depth += 0.1
        reasons.append("multi_topic>=3:+0.1")

    # explicitly requesting depth
    if "глуб" in t or "deep" in t or "онтолог" in t or "ontolog" in t:
        depth += 0.2
        reasons.append("explicit_depth:+0.2")

    # cap
    depth = min(1.0, depth)

    # low-depth dampeners
    # IMPORTANT: don't dampen when user explicitly negates brevity (e.g., "не кратко", "not brief")
    low_hit = any(p in t for p in DEPTH_PHRASES_LOW)
    negated = ("не кратко" in t) or ("не-кратко" in t) or ("not brief" in t) or ("not quick" in t)

    if low_hit and not negated:
        depth *= 0.5
        reasons.append("low_depth_phrase:*0.5")

    # single keyword hit with no philosophy terms
    if len(active_topics) <= 1 and not any(term in t for term in PHILOSOPHY_TERMS):
        depth *= 0.7
        reasons.append("single_topic_no_philo:*0.7")

    return {"depth": float(depth), "reasons": reasons}

def _normalize_by_max(scores: Dict[str, float]) -> Dict[str, float]:
    if not scores:
        return {}
    m = max(scores.values()) or 1.0
    return {k: float(v) / m for k, v in scores.items() if v > 0.0}


def classify_topic(raw_input: str, dialog_context: Dict[str, Any]) -> LOPResult:
    text = raw_input or ""
    current_scores = _scan_keywords(text)

    history = []
    try:
        history = (dialog_context or {}).get("history") or []
    except Exception:
        history = []

    # topic momentum from last 3 messages
    raw_scores = _accumulate_context(dict(current_scores), history, decay=0.3)

    if not raw_scores:
        # fallback
        return LOPResult(
            topic_vector={"procedural": 1.0},
            dominant_topic="procedural",
            depth=0.0,
            confidence=0.4,
            trace={"signals": [], "raw_scores": {}, "normalized": {"procedural": 1.0}, "depth": {"depth": 0.0, "reasons": ["fallback"]}},
        )

    dominant_topic = max(raw_scores.items(), key=lambda kv: kv[1])[0]
    top = float(raw_scores[dominant_topic])
    total = float(sum(raw_scores.values()) or 1.0)

    # confidence = top share, with floor like before
    confidence = min(1.0, max(0.45, top / total))

    norm = _normalize_by_max(raw_scores)

    depth_info = _estimate_depth(text, raw_scores)

    trace = {
        "raw_scores": raw_scores,
        "normalized": norm,
        "dominant_topic": dominant_topic,
        "confidence_calc": {"top": top, "total": total, "top_over_total": (top / total if total else 0.0)},
        "depth": depth_info,
        "context_used": bool(history),
    }

    return LOPResult(
        topic_vector=norm,
        dominant_topic=dominant_topic,
        depth=float(depth_info["depth"]),
        confidence=float(confidence),
        trace=trace,
    )



