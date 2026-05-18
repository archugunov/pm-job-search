"""Tests for the per-position artifact helpers + GET /api/positions/<folder>/artifacts."""
from __future__ import annotations

import json
import threading
import urllib.request
from pathlib import Path
from typing import Iterator

import pytest

from serve import (
    build_server,
    collect_artifacts,
    list_debrief_docs,
    list_prep_docs,
    read_artifact,
)


# ----- read_artifact ---------------------------------------------------------


def test_read_artifact_returns_contents(tmp_path: Path):
    (tmp_path / "research-brief.md").write_text("# Research\n\nBody.\n")
    assert read_artifact(tmp_path, "research-brief.md") == "# Research\n\nBody.\n"


def test_read_artifact_returns_none_when_missing(tmp_path: Path):
    assert read_artifact(tmp_path, "research-brief.md") is None


# ----- list_prep_docs --------------------------------------------------------


def test_list_prep_docs_returns_newest_first(tmp_path: Path):
    (tmp_path / "interview-prep-2026-05-15.md").write_text("later\n")
    (tmp_path / "interview-prep-2026-04-30.md").write_text("earlier\n")
    out = list_prep_docs(tmp_path)
    assert [d["date"] for d in out] == ["2026-05-15", "2026-04-30"]
    assert out[0]["markdown"] == "later\n"


def test_list_prep_docs_skips_malformed_filenames(tmp_path: Path):
    (tmp_path / "interview-prep-2026-05-15.md").write_text("kept\n")
    (tmp_path / "interview-prep-draft.md").write_text("skipped\n")
    (tmp_path / "interview-prep-2026-13-99.md").write_text("invalid date kept by regex but ignored downstream\n")
    out = list_prep_docs(tmp_path)
    # The regex accepts "13-99" as a date (it only checks shape), so 2 entries.
    # The truly malformed "interview-prep-draft.md" is dropped.
    filenames = [d["filename"] for d in out]
    assert "interview-prep-draft.md" not in filenames
    assert "interview-prep-2026-05-15.md" in filenames


def test_list_prep_docs_empty_when_no_matches(tmp_path: Path):
    (tmp_path / "notes.md").write_text("not a prep doc\n")
    assert list_prep_docs(tmp_path) == []


# ----- list_debrief_docs -----------------------------------------------------


def test_list_debrief_docs_parses_stage_and_orders(tmp_path: Path):
    (tmp_path / "interview-debrief-2026-05-12-panel.md").write_text("panel notes\n")
    (tmp_path / "interview-debrief-2026-05-18-cpo-round.md").write_text("cpo notes\n")
    (tmp_path / "interview-debrief-2026-04-22-hm.md").write_text("hm notes\n")
    out = list_debrief_docs(tmp_path)
    assert [(d["date"], d["stage"]) for d in out] == [
        ("2026-05-18", "cpo-round"),  # multi-segment stage preserved
        ("2026-05-12", "panel"),
        ("2026-04-22", "hm"),
    ]


def test_list_debrief_docs_requires_stage(tmp_path: Path):
    # Missing stage segment shouldn't match — debriefs need a stage in the
    # filename, otherwise they're ambiguous.
    (tmp_path / "interview-debrief-2026-05-12.md").write_text("no stage\n")
    assert list_debrief_docs(tmp_path) == []


# ----- collect_artifacts -----------------------------------------------------


def test_collect_artifacts_empty_folder_returns_nulls_and_empty_lists(tmp_path: Path):
    out = collect_artifacts(tmp_path)
    assert out == {"research": None, "preps": [], "debriefs": []}


def test_collect_artifacts_full_folder(tmp_path: Path):
    (tmp_path / "research-brief.md").write_text("# Research\n")
    (tmp_path / "interview-prep-2026-05-15.md").write_text("prep\n")
    (tmp_path / "interview-debrief-2026-05-12-panel.md").write_text("debrief\n")
    out = collect_artifacts(tmp_path)
    assert out["research"] == "# Research\n"
    assert len(out["preps"]) == 1
    assert out["preps"][0]["date"] == "2026-05-15"
    assert len(out["debriefs"]) == 1
    assert out["debriefs"][0]["stage"] == "panel"


# ----- HTTP endpoint ---------------------------------------------------------


@pytest.fixture
def running_server(userdata: Path) -> Iterator[tuple[str, Path]]:
    server, port = build_server(userdata_root=userdata, preferred_port=0, dist_dir=None)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://localhost:{port}", userdata
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def _get_json(url: str) -> tuple[int, dict | None]:
    try:
        with urllib.request.urlopen(url) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, None


def test_endpoint_returns_empty_payload_for_position_with_no_artifacts(running_server: tuple[str, Path]):
    base, _ = running_server
    status, body = _get_json(f"{base}/api/positions/Plaid/artifacts")
    assert status == 200
    assert body == {"research": None, "preps": [], "debriefs": []}


def test_endpoint_populates_research_when_present(running_server: tuple[str, Path]):
    base, root = running_server
    (root / "companies" / "Plaid" / "research-brief.md").write_text("# Plaid\n")
    _, body = _get_json(f"{base}/api/positions/Plaid/artifacts")
    assert body["research"] == "# Plaid\n"


def test_endpoint_returns_404_when_position_missing(running_server: tuple[str, Path]):
    base, _ = running_server
    status, _ = _get_json(f"{base}/api/positions/NonExistent/artifacts")
    assert status == 404


def test_endpoint_works_for_subfolder_layout(running_server: tuple[str, Path]):
    base, root = running_server
    folder = root / "companies" / "Stripe" / "lead-pm-growth"
    (folder / "interview-prep-2026-05-15.md").write_text("# Prep\n")
    from urllib.parse import quote
    _, body = _get_json(f"{base}/api/positions/{quote('Stripe/lead-pm-growth', safe='')}/artifacts")
    assert len(body["preps"]) == 1
    assert body["preps"][0]["date"] == "2026-05-15"
