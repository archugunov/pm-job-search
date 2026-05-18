"""Tests for latest_brief — find the newest daily-brief-YYYY-MM-DD.md."""
from pathlib import Path

from serve import latest_brief


def test_returns_latest_by_filename_date(userdata: Path):
    out = latest_brief(userdata)
    assert out is not None
    assert out["date"] == "2026-05-18"
    assert out["markdown"].startswith("# Daily brief")


def test_picks_newest_when_multiple(userdata: Path):
    (userdata / "outputs" / "daily-brief-2026-05-10.md").write_text("# older\n")
    (userdata / "outputs" / "daily-brief-2026-05-20.md").write_text("# newest\n")
    out = latest_brief(userdata)
    assert out["date"] == "2026-05-20"
    assert "newest" in out["markdown"]


def test_returns_none_when_no_briefs(tmp_path: Path):
    (tmp_path / "outputs").mkdir()
    assert latest_brief(tmp_path) is None


def test_returns_none_when_outputs_dir_missing(tmp_path: Path):
    assert latest_brief(tmp_path) is None


def test_ignores_non_brief_files(userdata: Path):
    (userdata / "outputs" / "applications.md").write_text("# apps\n")
    (userdata / "outputs" / "daily-brief-bad.md").write_text("# bad name\n")
    out = latest_brief(userdata)
    assert out["date"] == "2026-05-18"
