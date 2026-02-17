from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Dict, Optional

class CollisionPole(BaseModel):
    lang: str
    role: str  # "structure" | "metaphor" | "dialectic" | etc.

class CollisionPlan(BaseModel):
    enabled: bool = False
    pole_a: Optional[CollisionPole] = None
    pole_b: Optional[CollisionPole] = None
    arbiter: str = "synthesis"

class CognitionLanguageVector(BaseModel):
    prompt_language: str
    think_language: str
    output_language: str  # MUST equal prompt_language
    topic: str
    mode: str
    confidence: float = Field(ge=0.0, le=1.0)
    glossary: Dict[str, str] = Field(default_factory=dict)
    collision: CollisionPlan = Field(default_factory=CollisionPlan)

    # Optional enrichment fields (added by collider; safe defaults)
    resonance_score: Optional[float] = None
    resonance_gap: Optional[float] = None
    depth: Optional[float] = None
    top_candidates: Optional[list[dict]] = None

    routing_trace: Dict = Field(default_factory=dict)
    raw_input_hash: str
