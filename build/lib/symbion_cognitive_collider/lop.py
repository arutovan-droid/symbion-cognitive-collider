from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class LOPResult:
    topic: str
    confidence: float
    trace: Dict

def classify_topic(raw_input: str, dialog_context: Dict) -> LOPResult:
    t = (raw_input or "").lower()

    score: Dict[str, float] = {}
    signals = []

    def bump(topic: str, w: float, why: str):
        score[topic] = score.get(topic, 0.0) + w
        signals.append(f"{topic}+{w}:{why}")

    # architecture / systems
    if any(k in t for k in ["архитект", "система", "модул", "оркестр", "pipeline", "latp", "psl", "репозитор"]):
        bump("architecture", 1.2, "system/architecture keywords")

    # logic/definitions
    if any(k in t for k in ["определи", "дефиниц", "аксиом", "логик", "категор", "противореч"]):
        bump("logic_definition", 1.0, "logic/definition keywords")

    # etymology/dialectic
    if any(k in t for k in ["этимолог", "корень", "происхожд", "понятие", "диалектик"]):
        bump("etymology_dialectic", 1.0, "roots/etymology keywords")

    # canon/norm
    if any(k in t for k in ["норма", "канон", "закон", "юрид", "таксоном", "классификац"]):
        bump("canon_norm", 1.0, "canon/norm keywords")

    # strategy
    if any(k in t for k in ["стратег", "тактик", "ход", "игра", "долгоср", "часть-целое"]):
        bump("strategy", 1.0, "strategy keywords")

    # procedural
    if any(k in t for k in ["сделай", "пошаг", "как установить", "команда", "инструкция", "api", "код"]):
        bump("procedural", 1.0, "procedural keywords")

    # existential
    if any(k in t for k in ["смысл", "бытие", "выживание", "идентичн", "экзистенц", "жизнь"]):
        bump("existential", 1.0, "existential keywords")

    # psycho realism
    if any(k in t for k in ["власть", "совесть", "страх", "стыд", "вина", "политик", "конфликт"]):
        bump("psycho_realism", 1.0, "psycho-realism keywords")

    # metaphor/synthesis
    if any(k in t for k in ["метафор", "поэтич", "синтез", "символ", "миф"]):
        bump("metaphor_synthesis", 1.0, "metaphor keywords")

    # diplomacy/nuance
    if any(k in t for k in ["нюанс", "дипломат", "тонко", "аккуратн", "деликатн"]):
        bump("diplomacy_nuance", 0.9, "nuance keywords")

    # abstraction/doctrine
    if any(k in t for k in ["доктрин", "абстракц", "принцип", "догмат", "постулат"]):
        bump("abstraction_doctrine", 0.9, "doctrine keywords")

    # pick max
    if not score:
        return LOPResult(topic="procedural", confidence=0.4, trace={"signals": [], "scores": {}})

    topic = max(score.items(), key=lambda kv: kv[1])[0]
    top = score[topic]
    total = sum(score.values()) or 1.0
    confidence = min(1.0, max(0.45, top / total))

    return LOPResult(topic=topic, confidence=confidence, trace={"signals": signals, "scores": score})
