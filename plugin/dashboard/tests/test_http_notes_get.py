"""Tests for GET /api/positions/<folder_path>/notes."""
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


def test_returns_existing_notes_on_get(running_server: tuple[str, Path]):
    base, root = running_server
    notes_path = root / "companies" / "Plaid" / "notes.md"
    notes_path.write_text("# Notes — Plaid\n\n## 2026-05-18 09:00\n\nfirst note\n")
    with urllib.request.urlopen(f"{base}/api/positions/Plaid/notes") as r:
        body = json.loads(r.read())
    assert "first note" in body["markdown"]


def test_returns_empty_markdown_when_no_notes_md(running_server: tuple[str, Path]):
    base, _ = running_server
    with urllib.request.urlopen(f"{base}/api/positions/Plaid/notes") as r:
        body = json.loads(r.read())
    assert body["markdown"] == ""
