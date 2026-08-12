import json
import subprocess
import sys
from pathlib import Path

STATS = Path(__file__).resolve().parent / "judge-calibration" / "stats.py"
RUBRICS = ("lint", "groundedness", "coherence", "conformance", "tone")
GATING = ("lint", "groundedness", "conformance")


def run_stats(tmp_path, labels, gate=False, name="labels"):
    d = tmp_path / name
    d.mkdir()
    for i, l in enumerate(labels):
        (d / f"run{i}.json").write_text(json.dumps(l))
    cmd = [sys.executable, str(STATS), str(d)] + (["--gate"] if gate else [])
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def label(run="r", overall_judge="PASS", findings=(), blind=None, **verdicts):
    """Every rubric defaults to judge PASS / human unlabelled. Override with
    e.g. groundedness=("FAIL", "FAIL") meaning (judge, human)."""
    v = {}
    for r in RUBRICS:
        judge, human = verdicts.get(r, ("PASS", None))
        v[r] = {"judge": judge, "human": human}
    return {"run": run, "verdicts": v, "overall": {"judge": overall_judge},
            "findings": list(findings), "blind": blind}


def f(rubric, human, turn=None):
    return {"rubric": rubric, "turn": turn, "summary": "s", "human": human,
            "note": None}


def all_gating(human):
    return {r: ("PASS", human) for r in GATING}


# --- verdict agreement (the primary metric) ----------------------------------

def test_verdict_agreement_per_rubric(tmp_path):
    labels = [
        label(groundedness=("FAIL", "FAIL"), tone=("FAIL", "PASS")),
        label(groundedness=("FAIL", "FAIL"), tone=("FAIL", "FAIL")),
    ]
    code, out = run_stats(tmp_path, labels)
    assert code == 0
    assert "groundedness: 1.00 (2/2)" in out
    assert "tone: 0.50 (1/2)" in out


def test_unadjudicated_rubric_reports_na(tmp_path):
    code, out = run_stats(tmp_path, [label()])
    assert code == 0
    assert "coherence: n/a — no adjudicated runs" in out


def test_gating_and_advisory_are_labelled(tmp_path):
    code, out = run_stats(tmp_path, [label()])
    for line in out.splitlines():
        if line.strip().startswith("groundedness:"):
            assert "[gating]" in line
        if line.strip().startswith("tone:"):
            assert "[advisory]" in line


def test_lint_is_marked_as_script_not_judge(tmp_path):
    """A human FAIL on lint grades the rule, not a model — it must not read as
    a judge error."""
    code, out = run_stats(tmp_path, [label()])
    assert "script, not judge" in out


def test_judge_verdict_suffixes_compare_correctly(tmp_path):
    """Judge verdicts carry suffixes: 'FAIL (confirmed)', 'FAIL (one-of-two)'."""
    labels = [label(groundedness=("FAIL (confirmed)", "FAIL"))]
    code, out = run_stats(tmp_path, labels)
    assert "groundedness: 1.00 (1/1)" in out


def test_null_judge_verdict_is_excluded_not_counted_as_fail(tmp_path):
    labels = [label(groundedness=(None, "PASS")),
              label(groundedness=("PASS", "PASS"))]
    code, out = run_stats(tmp_path, labels)
    assert code == 0
    assert "groundedness: 1.00 (1/1) (1 run excluded: judge verdict unavailable)" in out


def test_all_null_judge_verdicts_report_na_with_exclusions(tmp_path):
    labels = [label(coherence=(None, "PASS")), label(coherence=(None, "FAIL"))]
    code, out = run_stats(tmp_path, labels)
    assert "coherence: n/a — no adjudicated runs (2 runs excluded" in out


# --- derived overall ---------------------------------------------------------

def test_overall_derived_from_human_gating_verdicts(tmp_path):
    labels = [label(overall_judge="FAIL", **all_gating("PASS"))]
    code, out = run_stats(tmp_path, labels)
    assert "overall: 0/1 (derived from human gating verdicts)" in out


def test_overall_ignores_advisory_rubrics(tmp_path):
    """coherence/tone FAIL must not drag the derived overall to FAIL."""
    labels = [label(overall_judge="PASS", coherence=("FAIL", "FAIL"),
                    tone=("FAIL", "FAIL"), **all_gating("PASS"))]
    code, out = run_stats(tmp_path, labels)
    assert "overall: 1/1" in out


def test_overall_skipped_when_gating_only_partly_adjudicated(tmp_path):
    labels = [label(lint=("PASS", "PASS"), groundedness=("PASS", "PASS"))]
    code, out = run_stats(tmp_path, labels)
    assert "overall:" not in out


def test_one_gating_fail_makes_derived_overall_fail(tmp_path):
    labels = [label(overall_judge="FAIL", lint=("PASS", "PASS"),
                    groundedness=("FAIL", "FAIL"), conformance=("PASS", "PASS"))]
    code, out = run_stats(tmp_path, labels)
    assert "overall: 1/1" in out


# --- self-contradiction ------------------------------------------------------

def test_judge_self_contradiction_detected(tmp_path):
    labels = [label(run="bad", overall_judge="PASS", groundedness=("FAIL", None))]
    code, out = run_stats(tmp_path, labels)
    assert "judge self-contradiction: 1 run(s) — bad" in out


def test_no_self_contradiction_when_consistent(tmp_path):
    labels = [label(overall_judge="FAIL", groundedness=("FAIL", None))]
    code, out = run_stats(tmp_path, labels)
    assert "self-contradiction" not in out


def test_null_judge_verdict_skips_contradiction_check(tmp_path):
    """Missing data must not be read as an implicit FAIL."""
    labels = [label(overall_judge="PASS", groundedness=(None, None))]
    code, out = run_stats(tmp_path, labels)
    assert "self-contradiction" not in out


# --- drill-down findings -----------------------------------------------------

def test_finding_precision_reported_when_labelled(tmp_path):
    labels = [label(findings=[f("groundedness", "agree"),
                              f("groundedness", "disagree")])]
    code, out = run_stats(tmp_path, labels)
    assert "finding precision (drill-down, where labelled)" in out
    assert "groundedness: 0.50 (1/2)" in out


def test_no_drilldown_section_when_no_findings(tmp_path):
    code, out = run_stats(tmp_path, [label()])
    assert "finding precision" not in out


def test_borderline_excluded_from_precision_but_counted(tmp_path):
    labels = [label(findings=[f("tone", "agree"), f("tone", "borderline")])]
    code, out = run_stats(tmp_path, labels)
    assert "tone: 1.00 (1/1)" in out
    assert "borderline: 1" in out


# --- validation --------------------------------------------------------------

def test_unrecognised_finding_rubric_exits_2(tmp_path):
    labels = [label(findings=[f("spec", "agree")])]
    code, out = run_stats(tmp_path, labels)
    assert code == 2 and "unrecognised finding rubric" in out


def test_unrecognised_human_finding_value_exits_2(tmp_path):
    labels = [label(findings=[f("tone", "yes")])]
    code, out = run_stats(tmp_path, labels)
    assert code == 2 and "unrecognised human value" in out


def test_unrecognised_human_verdict_exits_2(tmp_path):
    labels = [label(groundedness=("PASS", "pass"))]
    code, out = run_stats(tmp_path, labels)
    assert code == 2 and "unrecognised groundedness human verdict" in out


def test_hand_set_overall_human_exits_2(tmp_path):
    """Overall is derived. Setting it by hand silently competes with the
    derivation, so it is refused rather than ignored."""
    l = label()
    l["overall"]["human"] = "PASS"
    code, out = run_stats(tmp_path, [l])
    assert code == 2 and "overall.human must stay null" in out


def test_missing_labels_dir_exits_2(tmp_path):
    proc = subprocess.run([sys.executable, str(STATS), str(tmp_path / "nope")],
                          capture_output=True, text=True)
    assert proc.returncode == 2


def test_empty_labels_dir_is_not_an_error(tmp_path):
    code, out = run_stats(tmp_path, [])
    assert code == 0 and "no label files yet" in out


def test_template_json_is_ignored(tmp_path):
    d = tmp_path / "labels"
    d.mkdir()
    (d / "TEMPLATE.json").write_text('{"nonsense": true}')
    proc = subprocess.run([sys.executable, str(STATS), str(d)],
                          capture_output=True, text=True)
    assert proc.returncode == 0 and "no label files yet" in proc.stdout


def test_shipped_template_is_valid_json():
    p = STATS.parent / "labels" / "TEMPLATE.json"
    data = json.loads(p.read_text())
    assert set(data["verdicts"]) == set(RUBRICS)
    assert data["overall"].get("human") is None


# --- gate --------------------------------------------------------------------

def test_gate_fails_on_low_verdict_agreement_at_size(tmp_path):
    labels = [label(groundedness=("PASS", "FAIL")) for _ in range(5)]
    code, out = run_stats(tmp_path, labels, gate=True)
    assert code == 1 and "GATE FAIL" in out


def test_gate_ignores_thin_rubric(tmp_path):
    labels = [label(groundedness=("PASS", "FAIL")) for _ in range(4)]
    code, out = run_stats(tmp_path, labels, gate=True)
    assert code == 0 and "GATE PASS" in out


def test_gate_fails_on_low_recall(tmp_path):
    labels = [label(blind={"human_found": 10, "judge_matched": 3})]
    code, out = run_stats(tmp_path, labels, gate=True)
    assert code == 1 and "recall 0.30" in out


def test_gate_passes_clean(tmp_path):
    labels = [label(groundedness=("PASS", "PASS")) for _ in range(6)]
    code, out = run_stats(tmp_path, labels, gate=True)
    assert code == 0 and "GATE PASS" in out


# --- coherence promotion -----------------------------------------------------

def test_coherence_promotion_not_yet_below_bar(tmp_path):
    labels = [label(coherence=("PASS", "PASS")) for _ in range(9)]
    code, out = run_stats(tmp_path, labels)
    assert "not yet — 9/9" in out and "Stays advisory" in out


def test_coherence_promotion_eligible_at_bar(tmp_path):
    labels = [label(coherence=("PASS", "PASS")) for _ in range(10)]
    code, out = run_stats(tmp_path, labels)
    assert "ELIGIBLE — 10/10" in out
    assert "deliberate one-line change" in out


def test_coherence_promotion_blocked_by_agreement(tmp_path):
    labels = ([label(coherence=("PASS", "FAIL")) for _ in range(3)]
              + [label(coherence=("PASS", "PASS")) for _ in range(9)])
    code, out = run_stats(tmp_path, labels)
    assert "not yet — 9/12" in out


def test_promotion_never_gates(tmp_path):
    """Falling short of promotion must not fail the release gate."""
    labels = [label(coherence=("PASS", "PASS"))]
    code, out = run_stats(tmp_path, labels, gate=True)
    assert code == 0 and "GATE PASS" in out
