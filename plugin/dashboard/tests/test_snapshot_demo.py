"""Tests for scripts/snapshot_demo.py — the static-snapshot builder for the demo bundle."""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest

# Make scripts/ importable.
_DASHBOARD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_DASHBOARD / "scripts"))

from snapshot_demo import build_snapshot  # noqa: E402


def test_emits_state_json_with_expected_top_level_shape(userdata: Path, tmp_path: Path):
    out = tmp_path / "demo"
    build_snapshot(userdata, out, today=date(2026, 5, 18))

    state = json.loads((out / "state.json").read_text())
    assert set(state.keys()) >= {"companies", "strategy", "weekly_progress", "latest_brief", "userdata_root"}
    assert isinstance(state["companies"], list)


def test_redacts_userdata_root_in_state(userdata: Path, tmp_path: Path):
    out = tmp_path / "demo"
    build_snapshot(userdata, out, today=date(2026, 5, 18))

    state = json.loads((out / "state.json").read_text())
    # The on-disk path must not leak into the public bundle.
    assert str(userdata) not in state["userdata_root"]
    assert state["userdata_root"].startswith("<demo:")


def test_emits_one_artifacts_file_per_position(userdata: Path, tmp_path: Path):
    out = tmp_path / "demo"
    build_snapshot(userdata, out, today=date(2026, 5, 18))

    state = json.loads((out / "state.json").read_text())
    for record in state["companies"]:
        path = out / "artifacts" / f"{record['folder_path']}.json"
        assert path.is_file(), f"missing artifacts file for {record['folder_path']}"
        payload = json.loads(path.read_text())
        assert set(payload.keys()) == {"research", "preps", "debriefs"}


def test_emits_notes_md_per_position_empty_when_no_notes(userdata: Path, tmp_path: Path):
    out = tmp_path / "demo"
    build_snapshot(userdata, out, today=date(2026, 5, 18))

    state = json.loads((out / "state.json").read_text())
    for record in state["companies"]:
        path = out / "notes" / f"{record['folder_path']}.md"
        assert path.is_file()


def test_subfolder_position_creates_nested_artifact_path(userdata: Path, tmp_path: Path):
    out = tmp_path / "demo"
    build_snapshot(userdata, out, today=date(2026, 5, 18))

    # The Stripe/lead-pm-growth subfolder position from the fixture should
    # produce a nested file under artifacts/Stripe/.
    nested = out / "artifacts" / "Stripe" / "lead-pm-growth.json"
    assert nested.is_file()


def test_raises_when_persona_has_no_companies_dir(tmp_path: Path):
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(FileNotFoundError):
        build_snapshot(empty, tmp_path / "out", today=date(2026, 5, 18))


def test_pinned_today_drives_weekly_progress_window(userdata: Path, tmp_path: Path):
    out = tmp_path / "demo"
    # Monday 2026-05-18 → window_days=1, Wednesday 2026-05-20 → window_days=3.
    build_snapshot(userdata, out, today=date(2026, 5, 20))
    state = json.loads((out / "state.json").read_text())
    assert state["weekly_progress"]["window_days"] == 3
