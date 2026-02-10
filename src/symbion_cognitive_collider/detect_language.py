from __future__ import annotations
import re
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # детерминизм

_RE_CYR = re.compile(r"[\u0400-\u04FF]")     # Cyrillic
_RE_ARM = re.compile(r"[\u0530-\u058F]")     # Armenian
_RE_AR  = re.compile(r"[\u0600-\u06FF]")     # Arabic
_RE_HAN = re.compile(r"[\u4E00-\u9FFF]")     # CJK Unified Ideographs

def detect_prompt_language(text: str) -> str:
    t = (text or "").strip()
    if not t:
        return "en"

    # fast script-based routing (MVP, deterministic)
    if _RE_ARM.search(t):
        return "hy"
    if _RE_CYR.search(t):
        return "ru"
    if _RE_AR.search(t):
        return "ar"
    if _RE_HAN.search(t):
        return "zh"

    # fallback to langdetect for latin-based languages
    try:
        return detect(t)
    except Exception:
        return "en"
