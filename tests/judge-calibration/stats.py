#!/usr/bin/env python3
"""Judge-calibration report, rubric-first.

The unit is the rubric verdict, not the finding. You read five verdicts per
run, disagree with some, and label those; findings are an optional drill-down.
So per-rubric verdict agreement is the primary number here, and finding-level
precision is reported only where someone actually drilled in.

Usage: python3 stats.py <labels-dir> [--gate]

Report always prints; exit 0. With --gate: exit 1 unless verdict agreement
>= 0.9 for every rubric with >= 5 adjudicated runs, finding precision >= 0.9
for every rubric with >= 5 adjudicated findings, and recall >= 0.8 when any
blind data exists. Thin rubrics are reported but never gate.

Exit 2 on an off-spec label file. Label files are hand-edited mid-session, and
a typo must stop the run loudly rather than silently vanish a finding or coerce
one into a bucket that quietly shifts a number.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

MIN_N, P_BAR, R_BAR = 5, 0.9, 0.8

RUBRICS = ("lint", "groundedness", "coherence", "conformance", "tone")
GATING = ("lint", "groundedness", "conformance")   # these decide Overall
ADVISORY = ("coherence", "tone")                   # reported, never in the gate

# Coherence enters the gate only once it has earned it. Same bar the harness
# states in test-personas/SKILL.md; reported here so the decision is driven by
# a number rather than by a run that "obviously" should have failed.
PROMOTION_BAR, PROMOTION_MIN_N = 0.9, 10

VALID_HUMAN = ("agree", "disagree", "borderline", None)
VALID_VERDICT = ("PASS", "FAIL", None)


def _passish(v: str) -> bool:
    """Judge verdicts carry suffixes — 'FAIL (confirmed)', 'FAIL (one-of-two)'."""
    return v.startswith("PASS")


def load(labels_dir: str) -> tuple[list[Path], list[dict]]:
    paths = [p for p in sorted(Path(labels_dir).glob("*.json"))
             if p.name != "TEMPLATE.json"]
    return paths, [json.loads(p.read_text()) for p in paths]


def validate(paths: list[Path], labels: list[dict]) -> str | None:
    """Returns an error message, or None when every file is well-formed."""
    for p, run in zip(paths, labels):
        for finding in run.get("findings", []):
            rubric = finding.get("rubric")
            if rubric not in RUBRICS:
                return (f"{p.name}: unrecognised finding rubric {rubric!r}"
                        f" (valid: {', '.join(RUBRICS)})")
            if finding.get("human") not in VALID_HUMAN:
                return (f"{p.name}: unrecognised human value"
                        f" {finding.get('human')!r} (valid: agree, disagree,"
                        f" borderline, null)")
        verdicts = run.get("verdicts", {})
        for rubric in RUBRICS:
            for side in ("judge", "human"):
                v = verdicts.get(rubric, {}).get(side)
                if v is not None and not isinstance(v, str):
                    return f"{p.name}: {rubric}.{side} must be a string or null"
                if side == "human" and v not in VALID_VERDICT:
                    return (f"{p.name}: unrecognised {rubric} human verdict"
                            f" {v!r} (valid: PASS, FAIL, null)")
        if run.get("overall", {}).get("human") is not None:
            return (f"{p.name}: overall.human must stay null — overall is"
                    f" derived from the gating rubrics, never set by hand")
    return None


def excluded_suffix(n: int) -> str:
    if not n:
        return ""
    return f" ({n} run{'s' if n != 1 else ''} excluded: judge verdict unavailable)"


def verdict_agreement(labels: list[dict], rubric: str):
    """(hits, measurable, excluded). A null judge verdict is missing data, not
    a FAIL — it must never be compared against a human call. Runs the human
    adjudicated anyway are reported as excluded, not silently dropped, so the
    denominator's shrinkage stays visible."""
    adjudicated = [r for r in labels
                   if r.get("verdicts", {}).get(rubric, {}).get("human")]
    measurable = [(r["verdicts"][rubric]["judge"], r["verdicts"][rubric]["human"])
                  for r in adjudicated
                  if r["verdicts"][rubric].get("judge") is not None]
    hits = sum(_passish(j) == _passish(h) for j, h in measurable)
    return hits, len(measurable), len(adjudicated) - len(measurable)


def derived_overall(run: dict) -> str | None:
    """PASS iff every gating rubric passes.

    Lint is not a judgement and is not normally labelled — it is script output,
    and it enters the gate as a fact. So its own verdict is used unless a human
    deliberately overrode it (which grades the RULE, not a model). The two
    judged gating rubrics do need a human call; a partial label can't imply a
    gate, so None until both are set."""
    v = run.get("verdicts", {})
    lint = v.get("lint", {}).get("human") or v.get("lint", {}).get("judge")
    if lint is None:
        return None
    humans = [v.get(r, {}).get("human") for r in GATING if r != "lint"]
    if any(h is None for h in humans):
        return None
    return "PASS" if _passish(lint) and all(h == "PASS" for h in humans) else "FAIL"


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if a != "--gate"]
    gate = "--gate" in argv[1:]
    if len(args) != 1 or not Path(args[0]).is_dir():
        print("usage: stats.py <labels-dir> [--gate]", file=sys.stderr)
        return 2

    paths, labels = load(args[0])
    err = validate(paths, labels)
    if err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    if not labels:
        print("no label files yet — nothing to report.")
        return 0

    gate_ok = True

    # Standard confusion matrix over run verdicts, positive class = FAIL
    # ("the judge flagged this run"). Accuracy alone hides direction: two
    # rubrics can sit at the same accuracy while one over-fires and the other
    # misses, which is the single most useful thing to know when deciding what
    # to change.
    print(f"== verdict level, positive class = FAIL — {len(labels)} label file(s)")
    print(f"{'rubric':>13}  {'TP':>3} {'FP':>3} {'FN':>3} {'TN':>3}   "
          f"{'prec':>5} {'rec':>5} {'acc':>5}")
    for rubric in RUBRICS:
        pairs = [(r["verdicts"][rubric]["judge"], r["verdicts"][rubric]["human"])
                 for r in labels
                 if r.get("verdicts", {}).get(rubric, {}).get("human")
                 and r["verdicts"][rubric].get("judge") is not None]
        excluded = sum(1 for r in labels
                       if r.get("verdicts", {}).get(rubric, {}).get("human")
                       and r["verdicts"][rubric].get("judge") is None)
        tag = " [gating]" if rubric in GATING else " [advisory]"
        if rubric == "lint":
            tag = " [gating] script, not judge"
        if not pairs:
            print(f"{rubric:>13}:  no adjudicated runs{excluded_suffix(excluded)}{tag}")
            continue
        tp = sum(1 for j, h in pairs if not _passish(j) and h == "FAIL")
        fp = sum(1 for j, h in pairs if not _passish(j) and h == "PASS")
        fn = sum(1 for j, h in pairs if _passish(j) and h == "FAIL")
        tn = sum(1 for j, h in pairs if _passish(j) and h == "PASS")
        prec = f"{tp / (tp + fp):.2f}" if tp + fp else "  n/a"
        rec = f"{tp / (tp + fn):.2f}" if tp + fn else "  n/a"
        acc = (tp + tn) / len(pairs)
        print(f"{rubric:>13}  {tp:>3} {fp:>3} {fn:>3} {tn:>3}   "
              f"{prec:>5} {rec:>5} {acc:>5.2f}"
              f"{excluded_suffix(excluded)}{tag}")
        if gate and len(pairs) >= MIN_N and acc < P_BAR:
            gate_ok = False
    print("  prec = of the runs it FAILED, how many deserved it (over-firing)")
    print("  rec  = of the runs that deserved FAIL, how many it caught (missing)")
    print("  NOTE: verdict-level recall only catches a miss big enough to flip the")
    print("        verdict. On a zero-tolerance rubric, finding 1 of 5 problems still")
    print("        reads as a hit. Partial misses show up only in blind recall below.")

    # Overall is never taken from a human. It is derived from the human's
    # gating verdicts and compared against what the judge asserted.
    pairs, overall_excluded = [], 0
    for r in labels:
        dh = derived_overall(r)
        if dh is None:
            continue
        oj = r.get("overall", {}).get("judge")
        if oj is None:
            overall_excluded += 1
            continue
        pairs.append((oj, dh))
    if pairs:
        hits = sum(_passish(j) == _passish(h) for j, h in pairs)
        print(f"{'overall':>13}: {hits}/{len(pairs)} (derived from human gating"
              f" verdicts){excluded_suffix(overall_excluded)}")
    elif overall_excluded:
        print(f"{'overall':>13}: n/a{excluded_suffix(overall_excluded)}")

    # The judge's own stated overall disagreeing with the aggregation of its
    # own gating verdicts. A defect in the judge's output contract, independent
    # of any human labelling — reported, never corrected.
    contradictions = []
    for r in labels:
        v = r.get("verdicts", {})
        judges = [v.get(x, {}).get("judge") for x in GATING]
        oj = r.get("overall", {}).get("judge")
        if oj is None or any(j is None for j in judges):
            continue
        if _passish(oj) != all(_passish(j) for j in judges):
            contradictions.append(r.get("run", "?"))
    if contradictions:
        print(f"\njudge self-contradiction: {len(contradictions)} run(s)"
              f" — {', '.join(contradictions)}")

    # Drill-down. Absent by design on most runs: you only open a rubric's
    # findings when you disagree with its verdict, or on a spot-check.
    tally = defaultdict(lambda: {"agree": 0, "disagree": 0, "borderline": 0, None: 0})
    for run in labels:
        for finding in run.get("findings", []):
            tally[finding["rubric"]][finding.get("human")] += 1
    if tally:
        print("\n== finding precision (drill-down, where labelled)")
        for rubric in RUBRICS:
            t = tally[rubric]
            n = t["agree"] + t["disagree"]
            if n:
                precision = t["agree"] / n
                print(f"{rubric:>13}: {precision:.2f} ({t['agree']}/{n})"
                      f"  borderline: {t['borderline']}  unlabelled: {t[None]}")
                if gate and n >= MIN_N and precision < P_BAR:
                    gate_ok = False
            elif t["borderline"] or t[None]:
                print(f"{rubric:>13}: no adjudicated findings"
                      f"  borderline: {t['borderline']}  unlabelled: {t[None]}")

    found = sum(r["blind"]["human_found"] for r in labels if r.get("blind"))
    matched = sum(r["blind"]["judge_matched"] for r in labels if r.get("blind"))
    if found:
        recall = matched / found
        print(f"\nrecall {recall:.2f} ({matched}/{found}) over blind-labelled runs")
        if gate and recall < R_BAR:
            gate_ok = False

    # Promotion check for coherence: does it now clear the bar to enter the gate?
    hits, n, _ = verdict_agreement(labels, "coherence")
    print("\n== coherence promotion")
    if n >= PROMOTION_MIN_N and hits / n >= PROMOTION_BAR:
        print(f"  ELIGIBLE — {hits}/{n} = {hits/n:.2f} over {n} runs"
              f" (bar: {PROMOTION_BAR} over {PROMOTION_MIN_N}). Promoting is a"
              f" deliberate one-line change to the gate, not automatic.")
    else:
        shortfall = (f"{hits}/{n} = {hits/n:.2f}" if n else "no adjudicated runs")
        print(f"  not yet — {shortfall}; bar is {PROMOTION_BAR} over"
              f" {PROMOTION_MIN_N} runs. Stays advisory.")

    if gate:
        print("\nGATE " + ("PASS" if gate_ok else "FAIL"))
        return 0 if gate_ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
