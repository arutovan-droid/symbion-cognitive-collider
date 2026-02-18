import asyncio
import json

from symbion_cognitive_collider.collider import route_language


CASES = [
    {
        "name": "Narekatsi / Armenian ontological conflict",
        "text": "почему Нарекаци называют 'Книгой скорбных песнопений', если это журнал обвинений?",
        "energy": 0.85,
        "hint": "expected think_language often hy/ru depending on apostles + signals",
    },
    {
        "name": "Crisis / Strategic framing",
        "text": "как принимать решения в условиях кризиса?",
        "energy": 0.75,
        "hint": "expected think_language often zh/en depending on strategy signals",
    },
    {
        "name": "Dense ontology (Nyaya/Samkhya)",
        "text": "Развернуто объясни природу причинности и сущности бытия в онтологии ньяя и санкхья. Дай глубоко, не кратко.",
        "energy": 0.95,
        "hint": "expected collision often ON when band=mixed + depth high",
    },
]


def _fmt_top(top):
    if not top:
        return "-"
    return ", ".join([f"{x['lang']}:{round(float(x['score']), 3)}" for x in top[:3]])


async def main():
    for i, c in enumerate(CASES, 1):
        r = await route_language(c["text"], {"history": []}, {"energy_score": float(c["energy"])})

        enabled = getattr(r.collision, "enabled", None)
        print("=" * 80)
        print(f"[{i}] {c['name']}")
        print(f"text: {c['text']}")
        print(f"hint: {c['hint']}")
        print("-" * 80)
        print(
            "prompt=", r.prompt_language,
            "| think=", r.think_language,
            "| output=", r.output_language,
            "| topic=", r.topic,
            "| mode=", r.mode
        )
        print(
            "depth=", round(float(r.depth), 3),
            "| band=", r.routing_trace.get("resonance_band"),
            "| gap=", getattr(r, "resonance_gap", None),
            "| collision=", enabled
        )
        print("top3:", _fmt_top(r.top_candidates))
        print("collision_reason:", r.routing_trace.get("collision_reason"))

        # if you want full json per case, uncomment:
        # print(json.dumps(r.model_dump(), ensure_ascii=False, indent=2))

    print("\nDONE")


if __name__ == "__main__":
    asyncio.run(main())
