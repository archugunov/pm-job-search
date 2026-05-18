"""Tests for POST /api/positions/<folder_path>/notes."""
from __future__ import annotations

import json
import threading
import urllib.request
from pathlib import Path
from typing import Iterator

import pytest

from serve import build_server


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


def _post(url: str, body: dict) -> int:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def test_creates_notes_md_on_first_write(running_server: tuple[str, Path]):
    base, root = running_server
    status = _post(f"{base}/api/positions/Plaid/notes", {"note": "Recruiter called."})
    assert status == 200
    notes_path = root / "companies" / "Plaid" / "notes.md"
    assert notes_path.is_file()
    content = notes_path.read_text()
    assert content.startswith("# Notes — Plaid Senior PM, Consumer Credit\n")
    assert "Recruiter called." in content
    assert "\n## 2" in content


def test_appends_to_existing_notes_md(running_server: tuple[str, Path]):
    base, root = running_server
    _post(f"{base}/api/positions/Plaid/notes", {"note": "first"})
    _post(f"{base}/api/positions/Plaid/notes", {"note": "second"})
    content = (root / "companies" / "Plaid" / "notes.md").read_text()
    assert content.count("\n## 2") == 2
    assert "first" in content
    assert "second" in content


def test_writes_subfolder_layout(running_server: tuple[str, Path]):
    base, root = running_server
    from urllib.parse import quote
    path = quote("Stripe/lead-pm-growth", safe="")
    _post(f"{base}/api/positions/{path}/notes", {"note": "stripe note"})
    notes_path = root / "companies" / "Stripe" / "lead-pm-growth" / "notes.md"
    assert notes_path.is_file()
    assert "stripe note" in notes_path.read_text()


def test_returns_404_when_company_missing(running_server: tuple[str, Path]):
    base, _ = running_server
    assert _post(f"{base}/api/positions/NonExistent/notes", {"note": "x"}) == 404


def test_returns_400_when_note_missing(running_server: tuple[str, Path]):
    base, _ = running_server
    assert _post(f"{base}/api/positions/Plaid/notes", {}) == 400
