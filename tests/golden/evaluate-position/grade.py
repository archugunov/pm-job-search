#!/usr/bin/env python3
"""Grade a candidate run of /evaluate-position against the frozen golden labels.

Usage: python3 grade.py results.json
Gate:  tier agreement >= 0.8 over scoreable cases AND every filter case
       detected its hard filter. Exit 0 pass / 1 fail / 2 usage error.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = 0.8


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: grade.py <results.json>", file=sys.stderr)
        return 2
    results_path = Path(argv[1])
    try:
        parsed = json.loads(results_path.read_text())
    except json.JSONDecodeError as e:
        print(f"{results_path}: not valid JSON ({e})", file=sys.stderr)
        return 2
    if not isinstance(parsed, list):
        print(f"{results_path}: expected a JSON array of result objects, "
              f"got {type(parsed).__name__}", file=sys.stderr)
        return 2
    try:
        results = {r["id"]: r for r in parsed}
    except (TypeError, KeyError) as e:
        print(f"{results_path}: each result must be an object with an 'id' "
              f"key ({e})", file=sys.stderr)
        return 2
    cases = [json.loads(p.read_text()) for p in sorted((HERE / "cases").glob("*.json"))]

    missing = [c["id"] for c in cases if c["id"] not in results]
    tier_hits, tier_total, deltas, filter_misses, rows = 0, 0, [], [], []

    for case in cases:
        if case["id"] in missing:
            continue
        label, got = case["label"], results[case["id"]]
        if label["tier"] == "filtered":
            ok = got.get("matched_filter") == label["hard_filter"]
            if not ok:
                filter_misses.append(case["id"])
            rows.append((case["id"], label["tier"], got.get("tier"),
                         "ok" if ok else "MISSED FILTER"))
        else:
            tier_total += 1
            ok = got.get("tier") == label["tier"]
            tier_hits += ok
            if isinstance(got.get("score"), int):
                deltas.append(abs(got["score"] - label["score"]))
            rows.append((case["id"], label["tier"], got.get("tier"),
                         "ok" if ok else "TIER MISS"))

    for r in rows:
        print(f"  {r[0]:<24} label={r[1]:<9} got={str(r[2]):<9} {r[3]}")
    if missing:
        print(f"  missing from results: {', '.join(missing)}")
    agreement = tier_hits / tier_total if tier_total else 0.0
    print(f"tier agreement: {tier_hits}/{tier_total} = {agreement:.2f} (gate {GATE})")
    if deltas:
        print(f"mean |Δscore|: {sum(deltas) / len(deltas):.2f}")

    failed = bool(missing) or filter_misses or agreement < GATE
    print("FAIL" if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
