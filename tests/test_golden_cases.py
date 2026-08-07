"""Golden-set label integrity: every case's arithmetic must be internally
consistent with the frozen profile's thresholds. Catches label typos and
silent edits to the frozen profile — with zero LLM calls."""
import json
from pathlib import Path

import pytest

GOLDEN = Path(__file__).resolve().parent / "golden" / "evaluate-position"
CASES = sorted((GOLDEN / "cases").glob("*.json"))
P0, P1 = 13, 11  # frozen thresholds — must match tests/golden/evaluate-position/profile.md
DIMS = ["role_fit", "domain_fit", "business_health", "location_fit", "competitive_edge"]


def test_profile_thresholds_still_frozen():
    text = (GOLDEN / "profile.md").read_text()
    assert "p0: 13" in text and "p1: 11" in text, \
        "frozen profile thresholds changed — every golden label is now suspect"


@pytest.mark.parametrize("path", CASES, ids=lambda p: p.stem)
def test_case_labels_consistent(path):
    case = json.loads(path.read_text())
    assert case["synthetic"] is True
    assert len(case["jd"].split()) >= 60, "JD too thin to score five dimensions"
    label = case["label"]
    if label["tier"] == "filtered":
        assert label["hard_filter"], "filter case must name the expected filter"
        assert label["score"] is None and label["dimensions"] is None
        return
    dims = label["dimensions"]
    assert set(dims) == set(DIMS)
    assert all(v in (1, 2, 3) for v in dims.values())
    assert label["score"] == sum(dims.values()) + label["shape_adjustment"]
    expected_tier = "P0" if label["score"] >= P0 else "P1" if label["score"] >= P1 else "P2"
    assert label["tier"] == expected_tier


def test_case_count_and_spread():
    labels = [json.loads(p.read_text())["label"] for p in CASES]
    tiers = [l["tier"] for l in labels]
    assert len(CASES) == 12
    assert tiers.count("filtered") == 3
    assert {"P0", "P1", "P2"} <= set(tiers)
