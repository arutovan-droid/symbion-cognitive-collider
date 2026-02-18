import asyncio
from symbion_cognitive_collider.collider import route_language

async def test_collision():
    text = "Развернуто объясни природу причинности и сущности бытия в онтологии ньяя и санкхья. Дай глубоко, не кратко."
    
    print("\n=== СТАНДАРТНЫЙ ЗАПУСК ===")
    r = await route_language(text, {"history": []}, {"energy_score": 0.95})
    print(f"pole_a: {r.collision.pole_a.lang}")
    print(f"pole_b: {r.collision.pole_b.lang}")
    print(f"top3: {[(x['lang'], round(x['score'], 3)) for x in r.top_candidates]}")
    
    print("\n=== ИНФОРМАЦИЯ О КОЛЛАЙДЕРЕ ===")
    print(f"enabled: {r.collision.enabled}")
    print(f"arbiter: {r.collision.arbiter}")
    print(f"depth: {r.depth}")
    print(f"band: {r.routing_trace.get('resonance_band')}")

if __name__ == "__main__":
    asyncio.run(test_collision())
