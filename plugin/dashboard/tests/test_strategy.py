"""Tests for read_strategy — pull target_offer_date and weekly_targets from strategy.md frontmatter."""
from pathlib import Path

from serve import read_strategy


def test_extracts_target_offer_date_and_weekly_targets(userdata: Path):
    s = read_strategy(userdata)
    assert s["target_offer_date"] == "2026-06-28"
    assert s["weekly_targets"] == {"outreach": 7, "applications": 3}


def test_returns_empty_dict_when_no_strategy_file(tmp_path: Path):
    assert read_strategy(tmp_path) == {}


def test_handles_missing_weekly_targets(tmp_path: Path):
    (tmp_path / "strategy.md").write_text("---\ntarget_offer_date: 2026-12-01\n---\n")
    s = read_strategy(tmp_path)
    assert s["target_offer_date"] == "2026-12-01"
    assert s["weekly_targets"] == {}
