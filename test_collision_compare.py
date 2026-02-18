import asyncio
from symbion_cognitive_collider.collider import route_language

async def test_collision_with_el():
    text = "Развернуто объясни природу причинности и сущности бытия в онтологии ньяя и санкхья. Дай глубоко, не кратко."
    
    # Временно подменяем выбор pole_b через жизненный вектор (если поддерживается)
    # Или просто выводим информацию для ручного сравнения
    
    print("\n=== ТЕКУЩИЙ ВЫБОР (ar) ===")
    r1 = await route_language(text, {"history": []}, {"energy_score": 0.95})
    print(f"pole_b: {r1.collision.pole_b.lang}")
    
    # Если хотите принудительно el - нужно править collider.py
    print("\nДЛЯ СРАВНЕНИЯ С el:")
    print("Временно измените в collider.py строку выбора pole_b")

if __name__ == "__main__":
    asyncio.run(test_collision_with_el())
