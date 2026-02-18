import asyncio
import json
from symbion_cognitive_collider.collider import route_language

async def test_epistemological_nuance():
    queries = [
        {
            "name": "Свет без теней (сакральный)",
            "text": "Объясни природу света, который не отбрасывает тени",
            "expect": {"primary": "arc", "collision": ["arc", "hy"]}
        },
        {
            "name": "Истина без доказательства (эпистемология)",
            "text": "Что такое истина, если она не поддаётся доказательству?",
            "expect": {"primary": "sa", "collision": ["sa", "el"], "arc_rank": 2, "hy_rank": 3}
        },
        {
            "name": "Кризис (стратегия)",
            "text": "как принимать решения в условиях кризиса?",
            "expect": {"primary": "zh", "collision": False}
        },
        {
            "name": "Нарекаци (экзистенциальный конфликт)",
            "text": "почему Нарекаци называют 'Книгой скорбных песнопений', если это журнал обвинений?",
            "expect": {"primary": "hy", "collision": ["hy", "ru"]}
        }
    ]
    
    print("=" * 80)
    print("ТЕСТ ЭПИСТЕМОЛОГИЧЕСКОГО НЮАНСА")
    print("=" * 80)
    
    for q in queries:
        print(f"\n--- {q['name']} ---")
        print(f"Запрос: {q['text']}")
        
        r = await route_language(q["text"], {"history": []}, {"energy_score": 0.95})
        
        print(f"think: {r.think_language} (ожидалось: {q['expect']['primary']})")
        print(f"topic: {r.topic}")
        print(f"depth: {r.depth:.2f}")
        print(f"top3: {[(x['lang'], round(x['score'], 3)) for x in r.top_candidates]}")
        print(f"collision: {r.collision.enabled}")
        if r.collision.enabled:
            print(f"  pole_a: {r.collision.pole_a.lang}")
            print(f"  pole_b: {r.collision.pole_b.lang}")
        
        # Верификация
        if r.think_language == q['expect']['primary']:
            print("✅ primary language CORRECT")
        else:
            print(f"❌ primary language WRONG (expected {q['expect']['primary']})")
        
        if 'arc_rank' in q['expect']:
            arc_idx = next((i for i, (lang, _) in enumerate(r.top_candidates) if lang == 'arc'), None)
            if arc_idx is not None and arc_idx + 1 == q['expect']['arc_rank']:
                print(f"✅ arc rank {arc_idx+1} CORRECT")
            else:
                actual = arc_idx + 1 if arc_idx is not None else "not in top3"
                print(f"❌ arc rank WRONG (expected {q['expect']['arc_rank']}, got {actual})")
        
        if 'hy_rank' in q['expect']:
            hy_idx = next((i for i, (lang, _) in enumerate(r.top_candidates) if lang == 'hy'), None)
            if hy_idx is not None and hy_idx + 1 == q['expect']['hy_rank']:
                print(f"✅ hy rank {hy_idx+1} CORRECT")
            else:
                actual = hy_idx + 1 if hy_idx is not None else "not in top3"
                print(f"❌ hy rank WRONG (expected {q['expect']['hy_rank']}, got {actual})")
    
    print("\n" + "=" * 80)
    print("ТЕСТ ЗАВЕРШЁН")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_epistemological_nuance())
