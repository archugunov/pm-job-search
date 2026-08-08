import json
import subprocess
import sys
from pathlib import Path

STATS = Path(__file__).resolve().parent / "judge-calibration" / "stats.py"


def run_stats(tmp_path, labels, gate=False):
    d = tmp_path / "labels"
    d.mkdir()
    for i, l in enumerate(labels):
        (d / f"run{i}.json").write_text(json.dumps(l))
    cmd = [sys.executable, str(STATS), str(d)] + (["--gate"] if gate else [])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout


def label(hard_judge="PASS", hard_human=None, spec_judge="PASS", spec_human=None,
          overall_judge="PASS", findings=(), blind=None,
          soft_count=0, critique_count=0):
    return {"run": "r",
            "verdicts": {
                "hard": {"judge": hard_judge, "human": hard_human},
                "spec": {"judge": spec_judge, "human": spec_human},
                "overall": {"judge": overall_judge, "human": None}},
            "advisory": {"soft_count": soft_count, "critique_count": critique_count},
            "findings": list(findings), "blind": blind}


def f(tier, human):
    return {"tier": tier, "summary": "s", "human": human, "note": None}


def test_precision_per_tier(tmp_path):
    labels = [label(findings=[f("hard", "agree"), f("hard", "disagree"),
                              f("spec", "agree"), f("spec", "agree")])]
    code, out = run_stats(tmp_path, labels)
    assert code == 0
    assert "hard: precision 0.50 (1/2)" in out
    assert "spec: criterion-adjudication precision 1.00 (2/2)" in out


def test_borderline_excluded_but_counted(tmp_path):
    labels = [label(findings=[f("soft", "agree"), f("soft", "borderline")])]
    _, out = run_stats(tmp_path, labels)
    assert "soft: precision 1.00 (1/1)" in out
    assert "borderline: 1" in out


def test_unlabelled_findings_reported_not_counted(tmp_path):
    labels = [label(findings=[f("hard", None)])]
    _, out = run_stats(tmp_path, labels)
    assert "unlabelled: 1" in out


def test_recall_from_blind(tmp_path):
    labels = [label(blind={"human_found": 5, "judge_matched": 4}),
              label(blind={"human_found": 5, "judge_matched": 3})]
    _, out = run_stats(tmp_path, labels)
    assert "recall 0.70 (7/10)" in out


def test_gate_fails_on_low_precision(tmp_path):
    findings = [f("spec", "agree")] * 4 + [f("spec", "disagree")] * 2  # 0.67, n=6 ≥ 5
    code, _ = run_stats(tmp_path, [label(findings=findings)], gate=True)
    assert code == 1


def test_gate_passes_when_thin_tiers_skipped(tmp_path):
    # only 2 hard findings adjudicated (< 5) — tier skipped by the gate
    findings = [f("hard", "agree"), f("hard", "disagree")]
    code, _ = run_stats(tmp_path, [label(findings=findings)], gate=True)
    assert code == 0


def test_off_spec_human_value_fails_loudly(tmp_path):
    d = tmp_path / "labels"
    d.mkdir()
    (d / "run0.json").write_text(json.dumps(label(findings=[f("hard", "maybe")])))
    proc = subprocess.run([sys.executable, str(STATS), str(d)],
                           capture_output=True, text=True)
    assert proc.returncode == 2
    assert "run0.json" in proc.stderr
    assert "maybe" in proc.stderr


def test_off_spec_tier_value_fails_loudly(tmp_path):
    d = tmp_path / "labels"
    d.mkdir()
    (d / "run0.json").write_text(json.dumps(label(findings=[f("typo", "agree")])))
    proc = subprocess.run([sys.executable, str(STATS), str(d)],
                           capture_output=True, text=True)
    assert proc.returncode == 2
    assert "run0.json" in proc.stderr
    assert "typo" in proc.stderr


def test_verdict_agreement_reported_per_rubric(tmp_path):
    labels = [label(hard_judge="PASS", hard_human="PASS", spec_judge="PASS", spec_human="FAIL"),
              label(hard_judge="FAIL", hard_human="FAIL", spec_judge="PASS", spec_human="PASS")]
    code, out = run_stats(tmp_path, labels)
    assert code == 0
    assert "hard verdict agreement: 2/2" in out
    assert "spec verdict agreement: 1/2" in out


def test_overall_is_derived_not_read(tmp_path):
    # hard PASS + spec FAIL must derive overall FAIL, disagreeing with a judge PASS
    labels = [label(hard_human="PASS", spec_human="FAIL", overall_judge="PASS")]
    _, out = run_stats(tmp_path, labels)
    assert "overall verdict agreement: 0/1" in out


def test_null_judge_verdict_excluded_from_agreement_not_a_crash(tmp_path):
    # Mirrors the real corpus: 2 of 11 runs write "judges disagreed" for
    # Hard violations, so the export has {"judge": null, "human": "PASS"} —
    # a human call with no judge verdict to compare it to. Must not raise
    # AttributeError from `None.startswith(...)`, and must not silently
    # vanish from the report — it's reported as excluded.
    labels = [label(hard_judge=None, hard_human="PASS", spec_judge="PASS", spec_human="PASS"),
              label(hard_judge="PASS", hard_human="PASS", spec_judge="PASS", spec_human="PASS")]
    code, out = run_stats(tmp_path, labels)
    assert code == 0
    assert "hard verdict agreement: 1/1 (1 run excluded: judge verdict unavailable)" in out
    assert "spec verdict agreement: 2/2" in out


def test_null_judge_verdict_excluded_from_overall_agreement(tmp_path):
    # Both sub-verdicts adjudicated (so a derived overall exists), but the
    # judge's stated Overall is null — nothing to compare the derived
    # overall against. Must not crash and must not silently drop the run.
    labels = [label(hard_judge="PASS", hard_human="PASS",
                     spec_judge="PASS", spec_human="PASS",
                     overall_judge=None)]
    code, out = run_stats(tmp_path, labels)
    assert code == 0
    assert "overall verdict agreement: n/a (1 run excluded: judge verdict unavailable)" in out


def test_all_null_judge_hard_verdicts_reported_as_na(tmp_path):
    labels = [label(hard_judge=None, hard_human="PASS", spec_judge="PASS", spec_human="PASS")]
    code, out = run_stats(tmp_path, labels)
    assert code == 0
    assert "hard verdict agreement: n/a (1 run excluded: judge verdict unavailable)" in out


def test_runs_with_unset_rubric_verdicts_excluded(tmp_path):
    labels = [label(hard_human="PASS", spec_human=None)]
    _, out = run_stats(tmp_path, labels)
    assert "hard verdict agreement: 1/1" in out
    assert "spec verdict agreement:" not in out
    assert "overall verdict agreement:" not in out


def test_judge_self_contradiction_reported(tmp_path):
    # judge says Overall PASS while its own Spec gaps verdict is FAIL
    labels = [label(hard_judge="PASS", spec_judge="FAIL", overall_judge="PASS"),
              label(hard_judge="PASS", spec_judge="PASS", overall_judge="PASS")]
    _, out = run_stats(tmp_path, labels)
    assert "judge self-contradiction: 1 run" in out


def test_no_self_contradiction_line_when_none(tmp_path):
    _, out = run_stats(tmp_path, [label()])
    assert "self-contradiction" not in out


def test_self_contradiction_guards_null_judge_hard_verdict(tmp_path):
    # hard.judge is null ("judges disagreed") — there's nothing to aggregate,
    # so this must NOT be flagged as a self-contradiction just because
    # `None == "PASS"` is False. Missing data is not a FAIL.
    labels = [label(hard_judge=None, spec_judge="PASS", overall_judge="PASS")]
    code, out = run_stats(tmp_path, labels)
    assert code == 0
    assert "self-contradiction" not in out


def test_advisory_counts_totalled(tmp_path):
    labels = [label(soft_count=2, critique_count=4), label(soft_count=3, critique_count=1)]
    _, out = run_stats(tmp_path, labels)
    assert "advisory: 5 soft, 5 critiques" in out


def test_off_spec_rubric_verdict_fails_loudly(tmp_path):
    labels = [label(hard_human="MAYBE")]
    code, out = run_stats(tmp_path, labels)
    assert code == 2
