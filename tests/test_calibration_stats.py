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


def label(verdict_judge="PASS", verdict_human="PASS", findings=(), blind=None):
    return {"run": "r", "verdict_judge": verdict_judge,
            "verdict_human": verdict_human, "findings": list(findings),
            "blind": blind}


def f(tier, human):
    return {"tier": tier, "summary": "s", "human": human, "note": None}


def test_precision_per_tier(tmp_path):
    labels = [label(findings=[f("hard", "agree"), f("hard", "disagree"),
                              f("spec", "agree"), f("spec", "agree")])]
    code, out = run_stats(tmp_path, labels)
    assert code == 0
    assert "hard: precision 0.50 (1/2)" in out
    assert "spec: precision 1.00 (2/2)" in out


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


def test_verdict_agreement(tmp_path):
    labels = [label(), label(verdict_judge="FAIL (confirmed)", verdict_human="PASS")]
    _, out = run_stats(tmp_path, labels)
    assert "verdict agreement: 1/2" in out


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
