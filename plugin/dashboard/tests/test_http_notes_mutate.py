"""Tests for PUT / DELETE /api/positions/<folder_path>/notes."""
from __future__ import annotations

import json
import threading
import urllib.error
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


def _request(url: str, method: str, body: dict | None = None) -> int:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def _seed_two_notes(base: str) -> None:
    _request(f"{base}/api/positions/Plaid/notes", "POST", {"note": "first"})
    _request(f"{base}/api/positions/Plaid/notes", "POST", {"note": "second"})


def _read_notes(root: Path) -> str:
    return (root / "companies" / "Plaid" / "notes.md").read_text()


def _heading_of(content: str, position: int) -> str:
    headings = [line[3:].strip() for line in content.splitlines() if line.startswith("## ")]
    return headings[position]


def test_put_edits_body(running_server: tuple[str, Path]):
    base, root = running_server
    _seed_two_notes(base)
    heading = _heading_of(_read_notes(root), 0)
    status = _request(
        f"{base}/api/positions/Plaid/notes",
        "PUT",
        {"index": 0, "heading": heading, "body": "first (revised)"},
    )
    assert status == 200
    content = _read_notes(root)
    assert "first (revised)" in content
    assert "first" not in content.replace("first (revised)", "")
    assert "second" in content


def test_put_returns_409_on_heading_mismatch(running_server: tuple[str, Path]):
    base, _ = running_server
    _seed_two_notes(base)
    status = _request(
        f"{base}/api/positions/Plaid/notes",
        "PUT",
        {"index": 0, "heading": "fake-heading", "body": "x"},
    )
    assert status == 409


def test_put_returns_400_when_body_missing(running_server: tuple[str, Path]):
    base, root = running_server
    _seed_two_notes(base)
    heading = _heading_of(_read_notes(root), 0)
    status = _request(
        f"{base}/api/positions/Plaid/notes",
        "PUT",
        {"index": 0, "heading": heading},
    )
    assert status == 400


def test_delete_removes_entry(running_server: tuple[str, Path]):
    base, root = running_server
    _seed_two_notes(base)
    heading = _heading_of(_read_notes(root), 0)
    status = _request(
        f"{base}/api/positions/Plaid/notes",
        "DELETE",
        {"index": 0, "heading": heading},
    )
    assert status == 200
    content = _read_notes(root)
    assert content.count("\n## 2") == 1
    assert "second" in content


def test_delete_returns_409_on_heading_mismatch(running_server: tuple[str, Path]):
    base, _ = running_server
    _seed_two_notes(base)
    status = _request(
        f"{base}/api/positions/Plaid/notes",
        "DELETE",
        {"index": 0, "heading": "fake-heading"},
    )
    assert status == 409


def test_delete_returns_404_when_notes_file_missing(running_server: tuple[str, Path]):
    base, _ = running_server
    status = _request(
        f"{base}/api/positions/Plaid/notes",
        "DELETE",
        {"index": 0, "heading": "irrelevant"},
    )
    assert status == 404


def test_put_returns_404_when_notes_file_missing(running_server: tuple[str, Path]):
    base, _ = running_server
    status = _request(
        f"{base}/api/positions/Plaid/notes",
        "PUT",
        {"index": 0, "heading": "irrelevant", "body": "some text"},
    )
    assert status == 404
