import asyncio
from symbion_cognitive_collider.collider import route_language

async def test_truth():
    text = "Что такое истина, если она не поддаётся доказательству?"
    
    print("\n=== ТЕСТ ТРЁХ ТИПОВ ИСТИНЫ ===")
    print(f"Запрос: {text}\n")
    
    r = await route_language(text, {"history": []}, {"energy_score": 0.95})
    
    print(f"think_language: {r.think_language}")
    print(f"topic: {r.topic}")
    print(f"mode: {r.mode}")
    print(f"depth: {r.depth}")
    print(f"top3: {[(x['lang'], round(x['score'], 3)) for x in r.top_candidates]}")
    print(f"collision: {r.collision.enabled}")
    if r.collision.enabled:
        print(f"  pole_a: {r.collision.pole_a.lang}")
        print(f"  pole_b: {r.collision.pole_b.lang}")
    print(f"band: {r.routing_trace.get('resonance_band')}")
    print(f"collision_reason: {r.routing_trace.get('collision_reason')}")

if __name__ == "__main__":
    asyncio.run(test_truth())
