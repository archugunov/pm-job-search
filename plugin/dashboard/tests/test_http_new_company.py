"""Tests for POST /api/companies."""
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
        try:
            return e.code, json.loads(e.read())
        except (json.JSONDecodeError, ValueError):
            return e.code, {}


def test_creates_new_company_flat_layout(running_server: tuple[str, Path]):
    base, root = running_server
    status, body = _post(f"{base}/api/companies", {
        "company": "Lendable",
        "position": "Senior PM, Underwriting",
        "tier": "P1",
        "link": "https://example.com/lendable",
        "status": "discovered",
    })
    assert status == 201
    assert body["folder_path"] == "Lendable"
    meta = (root / "companies" / "Lendable" / "meta.md").read_text()
    assert "company: Lendable" in meta
    assert "position: Senior PM, Underwriting" in meta
    assert "tier: P1" in meta
    assert "status: discovered" in meta
    assert "link: https://example.com/lendable" in meta
    assert "score: 0" in meta
    assert "date_added: 2" in meta


def test_rejects_duplicate_company_position(running_server: tuple[str, Path]):
    base, _ = running_server
    status, body = _post(f"{base}/api/companies", {
        "company": "Plaid",
        "position": "Senior PM, Consumer Credit",
        "tier": "P0",
        "link": "x",
        "status": "discovered",
    })
    assert status == 409
    assert "exists" in body["error"].lower() or "duplicate" in body["error"].lower()


def test_rejects_second_role_on_flat_layout_company(running_server: tuple[str, Path]):
    base, _ = running_server
    status, body = _post(f"{base}/api/companies", {
        "company": "Plaid",
        "position": "Lead PM, Identity",
        "tier": "P1",
        "link": "x",
        "status": "discovered",
    })
    assert status == 409
    assert "multi-role" in body["error"].lower() or "/evaluate-position" in body["error"]


def test_allows_third_role_on_existing_multi_role_company(running_server: tuple[str, Path]):
    base, root = running_server
    status, body = _post(f"{base}/api/companies", {
        "company": "Stripe",
        "position": "Group PM, Atlas",
        "tier": "P1",
        "link": "x",
        "status": "discovered",
    })
    assert status == 201
    assert body["folder_path"] == "Stripe/group-pm-atlas"
    assert (root / "companies" / "Stripe" / "group-pm-atlas" / "meta.md").is_file()


def test_rejects_missing_required_fields(running_server: tuple[str, Path]):
    base, _ = running_server
    status, _ = _post(f"{base}/api/companies", {"company": "X"})
    assert status == 400
