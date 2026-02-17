from __future__ import annotations

from symbion_cognitive_collider.collider import _APOSTLES, _resonate, _choose_pole_b_diverse

DENSE_DEPTH = 0.8
TOPN = 30
CAND_SLICE = 4

def main():
    apostles = _APOSTLES or {}
    langs = apostles.get("languages") or {}
    if not langs:
        raise SystemExit("ERROR: apostles languages not loaded")

    # topics = union of all profile keys
    topics = set()
    for _, cfg in langs.items():
        prof = (cfg or {}).get("profile") or {}
        topics.update(prof.keys())
    topics = sorted(topics)

    rows = []
    for topic in topics:
        topic_vector = {topic: 1.0}
        ranked = (_resonate(topic_vector, DENSE_DEPTH, apostles) or [])[:CAND_SLICE]
        if len(ranked) < 2:
            continue

        a_lang, a_score = ranked[0]
        b_lang, b_score, meta = _choose_pole_b_diverse(
            ranked,
            depth=DENSE_DEPTH,
            apostles=apostles,
            topic_vector=topic_vector,
            strength_floor=0.60,
        )
        if not b_lang:
            continue

        strength = float(b_score) / float(a_score) if float(a_score) > 0 else 0.0
        util = meta.get("utility") if isinstance(meta, dict) else None

        rows.append({
            "topic": topic,
            "a": str(a_lang),
            "b": str(b_lang),
            "a_score": float(a_score),
            "b_score": float(b_score),
            "strength": float(strength),
            "utility": float(util) if util is not None else None,
            "select": (meta.get("select_mode") if isinstance(meta, dict) else None),
            "div": float(meta.get("diversity", 0.0)) if isinstance(meta, dict) else 0.0,
            "dist": float(meta.get("dist", 0.0)) if isinstance(meta, dict) else 0.0,
            "tilt_dist": (float(meta.get("tilt_dist")) if (isinstance(meta, dict) and meta.get("tilt_dist") is not None) else None),
        })

    def sort_key(r):
        u = r["utility"]
        if u is None:
            return (r["dist"], r["strength"])
        return (u, r["dist"], r["strength"])

    rows.sort(key=sort_key, reverse=True)

    print(f"\nDENSE PAIRS (depth={DENSE_DEPTH}) — top {TOPN}\n")
    for i, r in enumerate(rows[:TOPN], 1):
        td = f"{r['tilt_dist']:.3f}" if r["tilt_dist"] is not None else "-"
        u  = f"{r['utility']:.3f}" if r["utility"] is not None else "-"
        print(
            f"{i:>2}. {r['topic']:<22}  "
            f"{r['a']}→{r['b']}  "
            f"a={r['a_score']:.3f} b={r['b_score']:.3f}  "
            f"str={r['strength']:.3f} div={r['div']:.3f} dist={r['dist']:.3f} tiltΔ={td} util={u}  "
            f"({r['select']})"
        )
    print(f"\nTotal topics checked: {len(topics)} | pairs produced: {len(rows)}\n")

if __name__ == "__main__":
    main()
