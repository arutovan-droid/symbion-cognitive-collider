from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import re

# === MVP domain signals (added manually) ===
_RE_NAREKATSI = re.compile(r"(нарекац|нарек|айбубен|маштоц|песнопен|скорбн|обвин|прокурор|судья|бог|грех|narekatsi)", re.I)
_RE_CRISIS = re.compile(r"(кризис|бифуркац|неопредел|риск|сценар|горизонт|стратег|решен|выбор|危机|wēijī)", re.I)

# Armenian / HY cognitive processor signals.
# These are not cultural decorations; they map HY seed mechanics into existing topic space.
_RE_HY_MEMORY_WITNESS = re.compile(
    r"(памят|примес|свидетельств|шум|молчани|утрат|след|исповед|страдани|бол[ьи]|"
    r"memory|witness|testimony|noise|silence|loss|trace)",
    re.I,
)

_RE_HY_DISTRIBUTED_INVARIANT = re.compile(
    r"(центр.*разруш|разруш.*центр|узел|инвариант|оскол|фрактал|хачкар|минимальн.*узел|"
    r"distributed invariant|node|invariant|fragment|khachkar|fractal)",
    re.I,
)

_RE_HY_CODE_INFRASTRUCTURE = re.compile(
    r"(язык.*инфраструктур|инфраструктур.*язык|алфавит|айбубен|букв|маштоц|код.*территор|"
    r"синтаксис|несущ.*конструкц|language.*infrastructure|alphabet|script|mashtots|code.*territory)",
    re.I,
)

_RE_HY_STONE_GEOLOGY = re.compile(
    r"(камень|туф|гора|арарат|геолог|разлом|петрифик|окамен|монастыр|гегард|татев|"
    r"stone|tuff|mountain|ararat|geology|fracture|petrification)",
    re.I,
)

_RE_HY_WORD_SCALPEL = re.compile(
    r"(скальпел|патолог|диагноз|точно назв|названн.*патолог|слово.*плотност|"
    r"scalpel|pathology|diagnosis|precise articulation)",
    re.I,
)

_RE_HY_DUDUK_BREATH = re.compile(
    r"(дудук|дыхани|тембр|акустическ.*лини|тональн.*свидетельств|"
    r"duduk|breath|timbre|tonal witness)",
    re.I,
)

# Арамейский (сакральный субстрат)
# Истина (три типа)
_RE_TRUTH = re.compile(r"(истин|правд|truth|veritas|aletheia|emet|хакикат)", re.I)

_RE_ARC = re.compile(r"(свет.*не отбрасывает тени|священн|божествен|излучени|сияни|glory|radiance|divine light|shekinah|сакральн|храм|жертв|проро|ангел|бог|дух)", re.I)

_RE_SA_OBSERVER_ROOT = re.compile(r"(наблюда[ею]|наблюдател|мысл[ьи]|кто тот я|кто я|сознани|восприяти|реальност|иллюзи|identity|consciousness|perception|observer|observed|self|reality|illusion|root cause|first cause|uncaused|origin|unmanifest)", re.I)

_RE_ZH_VOID_FIELD = re.compile(r"(пустое место|пустота|пустой|зазор|отсутстви|поле|натяжени|без центра|центр отсутствует|распределени[ея] напряжени|локальные узлы|выравниваются по полю|void|emptiness|empty space|field|centerless)", re.I)

def _add_domain_signals(text: str, raw_scores: dict, signals: list) -> None:
    # Три типа истины
    if '_RE_TRUTH' in globals() and _RE_TRUTH.search(text):
        raw_scores["sacral_symbolic"] = raw_scores.get("sacral_symbolic", 0.0) + 0.8   # arc
        raw_scores["logic_definition"] = raw_scores.get("logic_definition", 0.0) + 0.8 # sa
        raw_scores["existential"] = raw_scores.get("existential", 0.0) + 0.8           # hy
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 1.0
        signals.append("domain:truth_three_types")
        print("DEBUG: Truth matched! (3 types)")
    # Арамейский сигнал
    if '_RE_ARC' in globals() and _RE_ARC.search(text):
        raw_scores["sacral_symbolic"] = raw_scores.get("sacral_symbolic", 0.0) + 2.0
        raw_scores["existential"] = raw_scores.get("existential", 0.0) + 1.5
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 2.0
        signals.append("domain:arc_sacral")
        print("DEBUG: Aramaic matched!")
    """Add domain-specific topic boosts."""
    if not text:
        return
    _t = str(text or "").lower()
    print("DEBUG: _add_domain_signals called with text:", text[:50])
    # Food / embodied memory / taste / cultural uptake signal.
    # Food questions are rarely pure procedure unless explicit recipe/process markers dominate.
    _food_terms = [
        "grandmother", "grandmother's food", "chef", "food", "dish",
        "cook", "cooking", "taste", "flavor", "salt", "soup",
        "national dish", "speaks", "comfort food",
        "бабушкин", "бабушка", "еда", "блюдо", "готовить",
        "готовка", "вкус", "соль", "суп", "национальное блюдо",
        "говорила", "говорит",
    ]

    if any(x in _t for x in _food_terms):
        raw_scores["psycho_realism"] = float(raw_scores.get("psycho_realism", 0.0)) + 1.0
        raw_scores["metaphor_synthesis"] = float(raw_scores.get("metaphor_synthesis", 0.0)) + 0.8
        raw_scores["strategy"] = float(raw_scores.get("strategy", 0.0)) + 0.55
        raw_scores["diplomacy_nuance"] = float(raw_scores.get("diplomacy_nuance", 0.0)) + 0.45
        raw_scores["architecture"] = float(raw_scores.get("architecture", 0.0)) + 0.35
        raw_scores["procedural"] = max(0.0, float(raw_scores.get("procedural", 0.0)) - 0.45)
        signals.append("domain:food_embodied_culture")

    # Power reproduction / political recursion signal.
    # Routes revolution, tyranny, oppression, legitimacy, and control dynamics
    # away from procedural EN into structural power analysis.
    _power_terms = [
        "revolution", "revolutions", "tyrant", "tyrants", "tyranny",
        "overthrew", "overthrow", "oppression", "oppressive",
        "power", "authority", "legitimacy", "regime", "control",
        "enemy", "democracy", "patriot", "patriotism",
        "security and control", "surveillance",
        "революц", "тиран", "тирания", "сверж", "угнет",
        "власть", "авторитет", "легитим", "режим", "контроль",
        "враг", "демократ", "патриот", "безопасность",
    ]

    if any(x in _t for x in _power_terms):
        raw_scores["diplomacy_nuance"] = float(raw_scores.get("diplomacy_nuance", 0.0)) + 1.1
        raw_scores["architecture"] = float(raw_scores.get("architecture", 0.0)) + 0.9
        raw_scores["psycho_realism"] = float(raw_scores.get("psycho_realism", 0.0)) + 0.8
        raw_scores["canon_norm"] = float(raw_scores.get("canon_norm", 0.0)) + 0.5
        raw_scores["depth_boost"] = float(raw_scores.get("depth_boost", 0.0)) + 0.45
        raw_scores["procedural"] = max(0.0, float(raw_scores.get("procedural", 0.0)) - 0.35)
        signals.append("domain:power_reproduction")

    # Sacred/metaphysical signal.
    # Prevent EN identity-fallback on prompts about grace, holiness, prayer,
    # eternity, sacred form, and metaphysical presence.
    _sacred_terms = [
        "grace", "holiness", "holy", "sacred", "faith", "prayer",
        "god", "divine", "eternity", "eternal", "timeless",
        "sin", "forgiveness", "redemption", "ritual", "temple",
        "soul", "spirit", "presence", "transcendence",
        "meaning without belief", "outside time", "beyond time",
        "благодать", "святость", "священн", "вера", "молитва",
        "бог", "божествен", "вечность", "вневрем", "грех",
        "прощение", "искупление", "ритуал", "храм", "душа",
        "дух", "присутствие", "трансценд",
    ]

    if any(x in _t for x in _sacred_terms):
        raw_scores["sacral_symbolic"] = float(raw_scores.get("sacral_symbolic", 0.0)) + 1.6
        raw_scores["existential"] = float(raw_scores.get("existential", 0.0)) + 1.1
        raw_scores["metaphor_synthesis"] = float(raw_scores.get("metaphor_synthesis", 0.0)) + 0.8
        raw_scores["logic_definition"] = float(raw_scores.get("logic_definition", 0.0)) + 0.5
        raw_scores["depth_boost"] = float(raw_scores.get("depth_boost", 0.0)) + 1.0
        raw_scores["procedural"] = max(0.0, float(raw_scores.get("procedural", 0.0)) - 0.7)
        signals.append("domain:sacred_metaphysical")

    # ES processor: vital expansion / social resonance / collective uptake.
    # ES activates when a concept must move through a population and become socially alive.
    _t = str(text or "").lower()

    _es_resonance_terms = [
        "resonance", "resonate", "uptake", "public", "general public",
        "crowd", "collective", "population", "community", "movement",
        "spread", "viral", "contagion", "adoption", "organic",
        "street level", "everyday", "slang", "social energy",
        "impact", "reception", "scale", "scalability", "traction",
        "audience", "campaign", "mobilize", "movement",
        "отклик", "резонанс", "публика", "общество", "толпа",
        "коллектив", "сообщество", "движение", "распространение",
        "вирусн", "принятие", "органический", "повседневн",
        "уличн", "масштаб", "аудитория", "вовлеч", "социальная энергия",
    ]

    _es_score = 0.0
    if any(x in _t for x in _es_resonance_terms):
        _es_score += 1.4

    if _es_score > 0:
        # ES needs a strong prior against EN procedural capture.
        # Public uptake / resonance / movement is not merely "how-to"; it is social kinetics.
        raw_scores["strategy"] = float(raw_scores.get("strategy", 0.0)) + (_es_score * 1.55)
        raw_scores["psycho_realism"] = float(raw_scores.get("psycho_realism", 0.0)) + min(1.2, _es_score * 0.75)
        raw_scores["metaphor_synthesis"] = float(raw_scores.get("metaphor_synthesis", 0.0)) + min(0.8, _es_score * 0.40)
        raw_scores["existential"] = float(raw_scores.get("existential", 0.0)) + min(0.35, _es_score * 0.15)

        # Prevent EN from winning only because the prompt is phrased as "how do we".
        # This is not a ban; it just stops procedural routing from swallowing social uptake.
        raw_scores["procedural"] = max(0.0, float(raw_scores.get("procedural", 0.0)) - min(0.6, _es_score * 0.35))

        signals.append("domain:es_vital_resonance")

    # EN processor: hard operational / interface / protocol execution.
    # EN is not the default processor for English text.
    # It receives a domain boost only for explicit operational/protocol/interface work.
    _t = str(text or "").lower()

    _en_hard_protocol_terms = [
        "api", "endpoint", "webhook", "schema", "payload", "adapter",
        "workflow", "checklist", "manual", "runbook", "sop",
        "step-by-step", "deployment", "deploy", "integration",
        "crm", "billing", "database", "pipeline", "queue",
        "input", "output", "handoff", "operator-facing",
        "executable rules", "operational manual", "frontline",
        "rate limit", "rollback", "health check", "interface contract",
    ]

    _en_ru_hard_terms = [
        "api", "эндпоинт", "вебхук", "схема", "payload", "адаптер",
        "чеклист", "инструкция", "регламент", "runbook",
        "порядок действий", "деплой", "интеграция",
        "crm", "биллинг", "база данных", "пайплайн", "очередь",
        "вход", "выход", "передача", "операторский",
        "исполнимые правила", "операционный мануал",
        "rollback", "health check", "контракт интерфейса",
    ]

    _en_score = 0.0
    if any(x in _t for x in _en_hard_protocol_terms):
        _en_score += 1.35
    if any(x in _t for x in _en_ru_hard_terms):
        _en_score += 1.35

    # Generic words like "process", "procedure", "steps", "standard", "usable",
    # "actionable", "how", "structure", and "explain" are intentionally excluded.
    # They are not enough to route into EN.

    if _en_score > 0:
        raw_scores["procedural"] = float(raw_scores.get("procedural", 0.0)) + _en_score
        raw_scores["strategy"] = float(raw_scores.get("strategy", 0.0)) + min(0.65, _en_score * 0.32)
        raw_scores["architecture"] = float(raw_scores.get("architecture", 0.0)) + min(0.45, _en_score * 0.22)
        signals.append("domain:en_operational_protocol")

    # FA processor: shadow / indirect mapping / metaphor as structural transfer.
    # FA activates when the prompt asks for hidden structure, negative space,
    # indirect bypass, metaphor as mapping, or ethical ambiguity.
    _t = str(text or "").lower()

    _fa_shadow_terms = [
        "тень", "скрыт", "скрытая", "скрытое", "умолч", "между строк",
        "фасад", "перифер", "негативное пространство", "negative space",
        "shadow", "unsaid", "implied", "hidden", "facade", "periphery",
    ]
    _fa_metaphor_terms = [
        "метафор", "образ", "изоморф", "перенос", "параллель",
        "мост между", "отражение", "reflection", "metaphor",
        "isomorphism", "analogy", "bridge",
    ]
    _fa_bypass_terms = [
        "обход", "обходной", "непрям", "косвен", "защит", "defensive",
        "bypass", "indirect", "orthogonal", "veil", "subtle",
    ]
    _fa_ethics_terms = [
        "этическ", "моральн", "парадокс", "двусмыс", "неоднознач",
        "долг", "сострадан", "gray area", "ambiguity", "moral paradox",
        "double-bind", "duty", "compassion",
    ]

    _fa_score = 0.0
    if any(x in _t for x in _fa_shadow_terms):
        _fa_score += 1.2
    if any(x in _t for x in _fa_metaphor_terms):
        _fa_score += 1.1
    if any(x in _t for x in _fa_bypass_terms):
        _fa_score += 1.1
    if any(x in _t for x in _fa_ethics_terms):
        _fa_score += 1.0

    if _fa_score > 0:
        raw_scores["metaphor_synthesis"] = float(raw_scores.get("metaphor_synthesis", 0.0)) + _fa_score
        raw_scores["diplomacy_nuance"] = float(raw_scores.get("diplomacy_nuance", 0.0)) + min(0.8, _fa_score * 0.35)
        raw_scores["psycho_realism"] = float(raw_scores.get("psycho_realism", 0.0)) + min(0.6, _fa_score * 0.25)
        raw_scores["depth_boost"] = float(raw_scores.get("depth_boost", 0.0)) + min(0.8, _fa_score * 0.25)
        signals.append("domain:fa_shadow_indirect_mapping")


    # SA processor: observer/root/first-cause ontological reduction.
    # Map to existing topics only: logic_definition + existential + sacral_symbolic, with depth.
    if '_RE_SA_OBSERVER_ROOT' in globals() and _RE_SA_OBSERVER_ROOT.search(text):
        raw_scores["logic_definition"] = raw_scores.get("logic_definition", 0.0) + 1.8
        raw_scores["existential"] = raw_scores.get("existential", 0.0) + 1.2
        raw_scores["sacral_symbolic"] = raw_scores.get("sacral_symbolic", 0.0) + 0.8
        raw_scores["procedural"] = max(0.0, raw_scores.get("procedural", 0.0) - 1.0)
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 1.8
        signals.append("domain:sa_observer_root")


    # ZH processor: field / void / centerless configuration.
    # Map to existing topics only: strategy is ZH's strongest axis.
    if '_RE_ZH_VOID_FIELD' in globals() and _RE_ZH_VOID_FIELD.search(text):
        raw_scores["strategy"] = raw_scores.get("strategy", 0.0) + 3.0
        raw_scores["architecture"] = raw_scores.get("architecture", 0.0) + 0.4
        raw_scores["metaphor_synthesis"] = raw_scores.get("metaphor_synthesis", 0.0) + 0.4
        raw_scores["procedural"] = max(0.0, raw_scores.get("procedural", 0.0) - 1.0)
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 1.0
        signals.append("domain:zh_void_field")


    # HY processor: atomic analysis, witness, invariant, code-as-territory.
    # Map to existing topics only; do not create new topic names here.
    if _RE_HY_MEMORY_WITNESS.search(text):
        raw_scores["existential"] = raw_scores.get("existential", 0.0) + 1.6
        raw_scores["psycho_realism"] = raw_scores.get("psycho_realism", 0.0) + 0.8
        raw_scores["sacral_symbolic"] = raw_scores.get("sacral_symbolic", 0.0) + 0.4
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 1.2
        signals.append("domain:hy_memory_witness")

    if _RE_HY_DISTRIBUTED_INVARIANT.search(text):
        raw_scores["architecture"] = raw_scores.get("architecture", 0.0) + 1.5
        raw_scores["logic_definition"] = raw_scores.get("logic_definition", 0.0) + 1.2
        raw_scores["existential"] = raw_scores.get("existential", 0.0) + 0.8
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 1.2
        signals.append("domain:hy_distributed_invariant")

    if _RE_HY_CODE_INFRASTRUCTURE.search(text):
        raw_scores["architecture"] = raw_scores.get("architecture", 0.0) + 1.4
        raw_scores["logic_definition"] = raw_scores.get("logic_definition", 0.0) + 1.2
        raw_scores["etymology_dialectic"] = raw_scores.get("etymology_dialectic", 0.0) + 0.6
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 1.0
        signals.append("domain:hy_code_infrastructure")

    if _RE_HY_STONE_GEOLOGY.search(text):
        raw_scores["existential"] = raw_scores.get("existential", 0.0) + 1.0
        raw_scores["architecture"] = raw_scores.get("architecture", 0.0) + 0.9
        raw_scores["sacral_symbolic"] = raw_scores.get("sacral_symbolic", 0.0) + 0.5
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 1.0
        signals.append("domain:hy_stone_geology")

    if _RE_HY_WORD_SCALPEL.search(text):
        raw_scores["psycho_realism"] = raw_scores.get("psycho_realism", 0.0) + 1.3
        raw_scores["logic_definition"] = raw_scores.get("logic_definition", 0.0) + 0.9
        raw_scores["existential"] = raw_scores.get("existential", 0.0) + 0.7
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 1.0
        signals.append("domain:hy_word_scalpel")

    if _RE_HY_DUDUK_BREATH.search(text):
        raw_scores["metaphor_synthesis"] = raw_scores.get("metaphor_synthesis", 0.0) + 1.0
        raw_scores["existential"] = raw_scores.get("existential", 0.0) + 0.8
        raw_scores["psycho_realism"] = raw_scores.get("psycho_realism", 0.0) + 0.5
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 0.8
        signals.append("domain:hy_duduk_breath")
    
    if _RE_NAREKATSI.search(text):
        print("DEBUG: Narekatsi matched!")
        raw_scores["existential"] = raw_scores.get("existential", 0.0) + 1.5
        raw_scores["psycho_realism"] = raw_scores.get("psycho_realism", 0.0) + 1.0
        raw_scores["sacral_symbolic"] = raw_scores.get("sacral_symbolic", 0.0) + 0.8
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 2.0
        signals.append("domain:narekatsi")
    
    if _RE_CRISIS.search(text):
        print("DEBUG: Crisis matched!")
        raw_scores["strategy"] = raw_scores.get("strategy", 0.0) + 1.5
        raw_scores["abstraction_doctrine"] = raw_scores.get("abstraction_doctrine", 0.0) + 0.8
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 0.8
        signals.append("domain:crisis")
    
    return
    
    if _RE_NAREKATSI.search(text):
        print("DEBUG: Narekatsi matched!")
        raw_scores["existential"] = raw_scores.get("existential", 0.0) + 1.5
        raw_scores["psycho_realism"] = raw_scores.get("psycho_realism", 0.0) + 1.0
        raw_scores["sacral_symbolic"] = raw_scores.get("sacral_symbolic", 0.0) + 0.8
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 2.0
        signals.append("domain:narekatsi")
    
    if _RE_CRISIS.search(text):
        print("DEBUG: Crisis matched!")
        raw_scores["strategy"] = raw_scores.get("strategy", 0.0) + 1.5
        raw_scores["abstraction_doctrine"] = raw_scores.get("abstraction_doctrine", 0.0) + 0.8
        raw_scores["depth_boost"] = raw_scores.get("depth_boost", 0.0) + 0.8
        signals.append("domain:crisis")
# ===========================================



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

    signals = []
    # Add domain-specific signals (Narekatsi, crisis)
    if text:  # call even if raw_scores empty
        _add_domain_signals(text, raw_scores, signals)

    if not raw_scores:
        # fallback
        return LOPResult(
            topic_vector={"procedural": 0.35},
            dominant_topic="procedural",
            depth=0.0,
            confidence=0.15,
            trace={"signals": [], "raw_scores": {}, "normalized": {"procedural": 0.35}, "depth": {"depth": 0.0, "reasons": ["soft_fallback"]}},
        )

    dominant_topic = max(raw_scores.items(), key=lambda kv: kv[1])[0]
    top = float(raw_scores[dominant_topic])
    total = float(sum(raw_scores.values()) or 1.0)

    # confidence = top share.
    # Keep the floor low so weak routing remains visibly weak instead of becoming pseudo-confident.
    confidence = min(1.0, max(0.15, top / total))

    norm = _normalize_by_max(raw_scores)

    # Добавляем depth_boost из сигналов
    depth_boost_val = raw_scores.get("depth_boost", 0.0)
    depth_info = _estimate_depth(text, raw_scores)
    if depth_boost_val > 0:
        depth_info["depth"] = min(1.0, depth_info["depth"] + depth_boost_val * 0.3)
        depth_info["reasons"].append(f"domain_depth_boost:+{depth_boost_val*0.3:.1f}")

    trace = {
        "signals": signals,
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



