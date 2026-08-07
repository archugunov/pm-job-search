#!/usr/bin/env python3
"""Judge-calibration report: per-tier precision, blind recall, per-rubric
verdict agreement (hard, spec, derived overall), judge self-contradiction,
advisory counts.

Usage: python3 stats.py <labels-dir> [--gate]
Report always prints; exit 0. With --gate: exit 1 unless precision >= 0.9
for every tier holding >= 5 adjudicated findings, and recall >= 0.8 when
any blind data exists. Thin tiers are reported but never gate. Verdict
agreement, self-contradiction, and advisory counts are reported only —
never gated, at this corpus size.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

MIN_N, P_BAR, R_BAR = 5, 0.9, 0.8
VALID_TIERS = ("hard", "soft", "spec", "critique")
VALID_HUMAN = ("agree", "disagree", "borderline", None)
VALID_RUBRIC_VERDICT = ("PASS", "FAIL", None)


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
        verdicts = run.get("verdicts", {})
        for rubric in ("hard", "spec"):
            rubric_human = verdicts.get(rubric, {}).get("human")
            if rubric_human not in VALID_RUBRIC_VERDICT:
                print(f"error: {p.name}: unrecognised {rubric} verdict {rubric_human!r}"
                      f" (valid: PASS, FAIL, null)", file=sys.stderr)
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

    for rubric in ("hard", "spec"):
        pairs = [(r["verdicts"][rubric]["judge"], r["verdicts"][rubric]["human"])
                 for r in labels if r.get("verdicts", {}).get(rubric, {}).get("human")]
        if pairs:
            hits = sum(j.startswith("PASS") == h.startswith("PASS") for j, h in pairs)
            print(f"{rubric} verdict agreement: {hits}/{len(pairs)}")

    # Overall is never read from the judge's own overall verdict for
    # agreement purposes — it's derived from the two human sub-verdicts
    # (PASS iff both PASS) and compared against what the judge asserted.
    overall_pairs = []
    for r in labels:
        v = r.get("verdicts", {})
        hard_h = v.get("hard", {}).get("human")
        spec_h = v.get("spec", {}).get("human")
        if hard_h is not None and spec_h is not None:
            derived_human = "PASS" if hard_h == "PASS" and spec_h == "PASS" else "FAIL"
            overall_pairs.append((v.get("overall", {}).get("judge"), derived_human))
    if overall_pairs:
        hits = sum(j.startswith("PASS") == h.startswith("PASS") for j, h in overall_pairs)
        print(f"overall verdict agreement: {hits}/{len(overall_pairs)}")

    # Self-contradiction: the judge's own overall verdict disagreeing with
    # the aggregation of its own hard/spec verdicts. This is a defect in
    # the judge's output contract, independent of any human labelling —
    # never corrected, only reported.
    contradictions = []
    for r in labels:
        v = r.get("verdicts", {})
        hard_j = v.get("hard", {}).get("judge")
        spec_j = v.get("spec", {}).get("judge")
        overall_j = v.get("overall", {}).get("judge")
        derived_pass = hard_j == "PASS" and spec_j == "PASS"
        if overall_j is not None and (overall_j.startswith("PASS")) != derived_pass:
            contradictions.append(r.get("run", "?"))
    if contradictions:
        print(f"judge self-contradiction: {len(contradictions)} run(s)"
              f" — {', '.join(contradictions)}")

    soft_total = sum(r.get("advisory", {}).get("soft_count", 0) for r in labels)
    critique_total = sum(r.get("advisory", {}).get("critique_count", 0) for r in labels)
    print(f"advisory: {soft_total} soft, {critique_total} critiques")

    if gate:
        print("GATE " + ("PASS" if gate_ok else "FAIL"))
        return 0 if gate_ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
