#!/usr/bin/env python3
"""Judge-calibration report: per-tier precision, blind recall, verdict agreement.

Usage: python3 stats.py <labels-dir> [--gate]
Report always prints; exit 0. With --gate: exit 1 unless precision >= 0.9
for every tier holding >= 5 adjudicated findings, and recall >= 0.8 when
any blind data exists. Thin tiers are reported but never gate.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

MIN_N, P_BAR, R_BAR = 5, 0.9, 0.8
VALID_TIERS = ("hard", "soft", "spec", "critique")
VALID_HUMAN = ("agree", "disagree", "borderline", None)


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if a != "--gate"]
    gate = "--gate" in argv[1:]
    if len(args) != 1:
        print("usage: stats.py <labels-dir> [--gate]", file=sys.stderr)
        return 2
    paths = [p for p in sorted(Path(args[0]).glob("*.json")) if p.name != "TEMPLATE.json"]
    labels = [json.loads(p.read_text()) for p in paths]

    # Label files are hand-edited by a human mid-labelling-session (per the
    # protocol README). A typo in `tier` or `human` must stop the run loudly
    # rather than silently vanish a finding or coerce it into a bucket that
    # quietly shifts a precision number.
    for p, run in zip(paths, labels):
        for finding in run.get("findings", []):
            tier = finding.get("tier")
            if tier not in VALID_TIERS:
                print(f"error: {p.name}: unrecognised tier {tier!r}"
                      f" (valid: {', '.join(VALID_TIERS)})", file=sys.stderr)
                return 2
            human = finding.get("human")
            if human not in VALID_HUMAN:
                print(f"error: {p.name}: unrecognised human value {human!r}"
                      f" (valid: agree, disagree, borderline, null)", file=sys.stderr)
                return 2

    tally = defaultdict(lambda: {"agree": 0, "disagree": 0, "borderline": 0, None: 0})
    for run in labels:
        for finding in run.get("findings", []):
            tally[finding["tier"]][finding.get("human")] += 1

    gate_ok = True
    for tier in ("hard", "soft", "spec", "critique"):
        t = tally[tier]
        n = t["agree"] + t["disagree"]
        if n:
            precision = t["agree"] / n
            print(f"{tier}: precision {precision:.2f} ({t['agree']}/{n})"
                  f"  borderline: {t['borderline']}  unlabelled: {t[None]}")
            if gate and n >= MIN_N and precision < P_BAR:
                gate_ok = False
        elif t["borderline"] or t[None]:
            print(f"{tier}: no adjudicated findings"
                  f"  borderline: {t['borderline']}  unlabelled: {t[None]}")

    found = sum(r["blind"]["human_found"] for r in labels if r.get("blind"))
    matched = sum(r["blind"]["judge_matched"] for r in labels if r.get("blind"))
    if found:
        recall = matched / found
        print(f"recall {recall:.2f} ({matched}/{found}) over blind-labelled runs")
        if gate and recall < R_BAR:
            gate_ok = False

    judged = [(r["verdict_judge"], r["verdict_human"]) for r in labels
              if r.get("verdict_human")]
    if judged:
        hits = sum(j.startswith("PASS") == h.startswith("PASS") for j, h in judged)
        print(f"verdict agreement: {hits}/{len(judged)}")

    if gate:
        print("GATE " + ("PASS" if gate_ok else "FAIL"))
        return 0 if gate_ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
