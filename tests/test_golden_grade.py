import json
import subprocess
import sys
from pathlib import Path

GOLDEN = Path(__file__).resolve().parent / "golden" / "evaluate-position"


def run_grade(tmp_path, results):
    rf = tmp_path / "results.json"
    rf.write_text(json.dumps(results))
    proc = subprocess.run(
        [sys.executable, str(GOLDEN / "grade.py"), str(rf)],
        capture_output=True, text=True)
    return proc.returncode, proc.stdout


def perfect_results():
    out = []
    for p in sorted((GOLDEN / "cases").glob("*.json")):
        case = json.loads(p.read_text())
        l = case["label"]
        out.append({"id": case["id"], "tier": l["tier"], "score": l["score"],
                    "matched_filter": l["hard_filter"]})
    return out


def test_perfect_run_passes(tmp_path):
    code, out = run_grade(tmp_path, perfect_results())
    assert code == 0
    assert "tier agreement: 9/9" in out


def test_two_tier_misses_fail_gate(tmp_path):
    results = perfect_results()
    flipped = 0
    for r in results:
        if r["tier"] in ("P0", "P1") and flipped < 2:
            r["tier"] = "P2"; flipped += 1
    code, out = run_grade(tmp_path, results)
    assert code == 1          # 7/9 = 0.78 < 0.8
    assert "FAIL" in out


def test_missed_filter_fails_even_with_perfect_tiers(tmp_path):
    results = perfect_results()
    for r in results:
        if r["matched_filter"]:
            r["matched_filter"] = None
            r["tier"] = "P1"
            break
    code, out = run_grade(tmp_path, results)
    assert code == 1
    assert "filter" in out.lower()


def test_missing_case_reported(tmp_path):
    code, out = run_grade(tmp_path, perfect_results()[:-1])
    assert code == 1
    assert "missing" in out.lower()
