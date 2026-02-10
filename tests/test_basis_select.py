import pytest
from symbion_cognitive_collider.collider import route_language

@pytest.mark.asyncio
async def test_route_architecture():
    ctx = {}
    lv = {"energy_score": 0.9}
    r = await route_language("Нужна архитектура модулей LATP и PSL", ctx, life_vector=lv)
    assert r.output_language == r.prompt_language
    assert r.think_language in ["de", "en"]  # architecture -> de by default

@pytest.mark.asyncio
async def test_route_existential():
    ctx = {}
    lv = {"energy_score": 0.9}
    r = await route_language("В чем смысл выживания и идентичности?", ctx, life_vector=lv)
    assert r.output_language == r.prompt_language
    assert r.think_language == "hy"
