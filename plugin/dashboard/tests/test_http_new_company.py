"""Tests for POST /api/companies (link + status payload)."""
from __future__ import annotations

import json
import threading
import urllib.request
from pathlib import Path
from typing import Iterator

import pytest

from serve import build_server, derive_company_from_url


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


def _post(url: str, body: dict) -> tuple[int, dict]:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return e.code, {}


def test_derives_company_from_simple_host():
    assert derive_company_from_url("https://www.plaid.com/jobs/senior-pm") == "Plaid"
    assert derive_company_from_url("https://jobs.ramp.com/123") == "Ramp"


def test_derives_company_from_ats_path():
    assert derive_company_from_url("https://boards.greenhouse.io/stripe/jobs/4567") == "Stripe"
    assert derive_company_from_url("https://jobs.lever.co/lendable/abc") == "Lendable"


def test_derives_company_handles_hyphens_in_ats_slug():
    assert derive_company_from_url("https://boards.greenhouse.io/anthropic-pbc/jobs/1") == "Anthropic Pbc"


def test_creates_scaffold_with_link_and_status(running_server: tuple[str, Path]):
    base, root = running_server
    status, body = _post(f"{base}/api/companies", {
        "link": "https://www.lendable.com/jobs/senior-pm",
        "status": "new",
    })
    assert status == 201
    assert body["folder_path"] == "Lendable"
    meta = (root / "companies" / "Lendable" / "meta.md").read_text()
    assert "company: Lendable" in meta
    assert "status: new" in meta
    assert "link: https://www.lendable.com/jobs/senior-pm" in meta
    assert "tier: \n" in meta or "tier:\n" in meta
    assert "position: \n" in meta or "position:\n" in meta
    assert "/pm-job-search:evaluate-position" in meta


def test_default_status_is_new(running_server: tuple[str, Path]):
    base, root = running_server
    status, body = _post(f"{base}/api/companies", {
        "link": "https://www.fresh.example.com/jobs/x",
    })
    assert status == 201
    meta = (root / "companies" / body["folder_path"] / "meta.md").read_text()
    assert "status: new" in meta


def test_appends_suffix_on_collision(running_server: tuple[str, Path]):
    # First create: Plaid (clean folder name).
    base, root = running_server
    # Maya install already has Plaid flat-layout — the new endpoint should detect
    # and append a suffix rather than overwrite.
    status, body = _post(f"{base}/api/companies", {
        "link": "https://www.plaid.com/jobs/different-role",
        "status": "new",
    })
    assert status == 201
    assert body["folder_path"] == "Plaid-2"
    assert (root / "companies" / "Plaid-2" / "meta.md").is_file()


def test_rejects_invalid_link(running_server: tuple[str, Path]):
    base, _ = running_server
    status, body = _post(f"{base}/api/companies", {"link": "not-a-url", "status": "new"})
    assert status == 400


def test_rejects_missing_link(running_server: tuple[str, Path]):
    base, _ = running_server
    status, _ = _post(f"{base}/api/companies", {"status": "new"})
    assert status == 400


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
