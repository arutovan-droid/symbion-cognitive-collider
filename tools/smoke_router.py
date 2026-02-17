import asyncio

from symbion_cognitive_collider.collider import route_language


def _assert_between(x, lo, hi, name):
    assert x is not None, f"{name} is None"
    assert lo <= float(x) <= hi, f"{name}={x} not in [{lo},{hi}]"


async def main():
    cases = [
        # brief → low depth, collision off expected
        ("Дай кратко: что такое причинность?", 0.0, 0.25, {"collision": False}),
        # deep + not brief (negated brevity) → depth should NOT be dampened by low-depth phrase
        ("Дай онтологически глубоко, не кратко: что такое причинность?", 0.30, 1.00, {"collision": None}),
        # dense philosophy → likely mixed/confident band and collision maybe on depending on gap/energy
        ("Развернуто объясни природу причинности и сущности бытия в онтологии ньяя и санкхья. Дай глубоко, не кратко.", 0.50, 1.00, {"collision": True}),
        # neutral explain → medium depth
        ("Объясни структуру аргумента.", 0.00, 0.80, {"collision": False}),
        # another brief instruction
        ("Ответь кратко: что такое сущность?", 0.0, 0.25, {"collision": False}),
    ]

    life_hi = {"energy_score": 0.95}
    life_mid = {"energy_score": 0.60}

    for i, (text, dlo, dhi, expect) in enumerate(cases, 1):
        life = life_hi if "глубоко" in text or "Развернуто" in text else life_mid
        r = await route_language(text, {"history": []}, life)

        # router_version present
        assert r.routing_trace.get("router_version") == "rv02", "router_version missing or wrong"

        # depth range
        _assert_between(r.depth, dlo, dhi, f"case{i}.depth")

        # resonance telemetry exists (schema optional fields now in place)
        assert r.routing_trace.get("resonance_band") is not None, f"case{i}.resonance_band missing"
        assert r.routing_trace.get("resonance_confidence") is not None, f"case{i}.resonance_confidence missing"

        # collision expectation
        exp = expect.get("collision")
        enabled = getattr(r.collision, "enabled", None)
        if exp is True:
            assert enabled is True, f"case{i}.collision expected True, got {enabled}"
        elif exp is False:
            assert enabled is False, f"case{i}.collision expected False, got {enabled}"
        else:
            # don't care
            pass

        print(f"[OK] case{i}: depth={r.depth:.3f} band={r.routing_trace.get('resonance_band')} gap={getattr(r,'resonance_gap',None)} collision={enabled}")

    print("\nALL SMOKE TESTS PASSED")


if __name__ == "__main__":
    asyncio.run(main())
