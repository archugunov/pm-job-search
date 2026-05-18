"""Tests for read_strategy — pull target_offer_date and weekly_targets from strategy.md frontmatter."""
from pathlib import Path

import pytest

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


# Regression: Maya's shipped strategy.md opens with an HTML comment line
# before the `---` frontmatter fence. The parser must skip leading blank
# lines + HTML comments (see parse_frontmatter in serve.py). If someone
# reverts that handling, this test fails with empty fields rather than
# the dashboard silently going blank against the example data.
def test_mayas_shipped_strategy_parses_with_leading_html_comment():
    maya_root = Path(__file__).resolve().parents[3] / "userdata" / "examples" / "maya"
    strategy_path = maya_root / "strategy.md"
    if not strategy_path.is_file():
        pytest.skip(f"Maya example not present at {strategy_path}")

    # Guard: the test is only meaningful while Maya's file actually carries
    # a leading HTML comment. If it ever stops, update the test to point at
    # something else (or delete it).
    head = strategy_path.read_text(encoding="utf-8").splitlines()[:2]
    assert head[0].lstrip().startswith("<!--"), (
        "Maya's strategy.md no longer opens with an HTML comment — "
        "this regression test must be updated or removed."
    )
    assert head[1].strip() == "---", (
        "Maya's strategy.md should have `---` on the line after the leading comment; "
        "if its structure changed, update this regression test."
    )

    s = read_strategy(maya_root)
    assert s["target_offer_date"] == "2026-08-01"
    assert s["weekly_targets"] == {"warm_outreach": 5, "applications": 3}
