import argparse
import asyncio
import json
import sys

from symbion_cognitive_collider.collider import route_language


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="symbion_cognitive_collider")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("route", help="Route input to think/output language + collision plan")
    r.add_argument("text", nargs="?", help="Input text. If omitted, reads from stdin.")
    r.add_argument("--energy", type=float, default=0.9, help="life_vector.energy_score (default: 0.9)")
    r.add_argument("--history", type=str, default="[]", help="JSON list for dialog_context.history (default: [])")
    r.add_argument("--json", action="store_true", help="Print full result as JSON")
    r.add_argument("--trace", action="store_true", help="Include routing_trace in non-JSON output")
    return p


async def _cmd_route(args: argparse.Namespace) -> int:
    text = args.text
    if not text:
        text = sys.stdin.read()
    text = (text or "").strip()
    if not text:
        print("ERROR: empty input text", file=sys.stderr)
        return 2

    try:
        history = json.loads(args.history)
        if not isinstance(history, list):
            history = []
    except Exception:
        history = []

    dialog_context = {"history": history}
    life_vector = {"energy_score": float(args.energy)}

    r = await route_language(text, dialog_context, life_vector)

    if args.json:
        # pydantic v2: model_dump(); fallback to dict
        try:
            payload = r.model_dump()
        except Exception:
            payload = r.__dict__
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    # compact human output
    enabled = getattr(r.collision, "enabled", None)
    print(f"prompt={r.prompt_language} think={r.think_language} output={r.output_language} topic={r.topic} mode={r.mode} conf={r.confidence:.3f}")
    try:
        print(f"resonance_score={r.resonance_score:.3f} gap={r.resonance_gap:.3f} depth={r.depth:.3f} band={r.routing_trace.get('resonance_band')}")
    except Exception:
        print(f"depth={r.depth:.3f} band={r.routing_trace.get('resonance_band')}")

    print(f"collision_enabled={enabled} pole_a={getattr(r.collision,'pole_a',None)} pole_b={getattr(r.collision,'pole_b',None)}")
    if args.trace:
        print("\nTRACE:")
        print(json.dumps(r.routing_trace, ensure_ascii=False, indent=2))

    return 0


def main(argv=None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "route":
        return asyncio.run(_cmd_route(args))

    print("ERROR: unknown command", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
