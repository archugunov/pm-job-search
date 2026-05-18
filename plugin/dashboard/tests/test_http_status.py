"""Tests for PATCH /api/positions/<folder_path>/status."""
from __future__ import annotations

import json
import threading
import urllib.request
from pathlib import Path
from typing import Iterator
from urllib.parse import quote

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


def _patch(url: str, body: dict) -> int:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="PATCH",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def test_patches_flat_layout_company(running_server: tuple[str, Path]):
    base, root = running_server
    status = _patch(f"{base}/api/positions/Plaid/status", {"status": "rejected"})
    assert status == 200
    content = (root / "companies" / "Plaid" / "meta.md").read_text()
    assert "status: rejected" in content
    assert "company: Plaid" in content


def test_patches_subfolder_layout_company(running_server: tuple[str, Path]):
    base, root = running_server
    path = quote("Stripe/lead-pm-growth", safe="")
    status = _patch(f"{base}/api/positions/{path}/status", {"status": "interviewing"})
    assert status == 200
    content = (root / "companies" / "Stripe" / "lead-pm-growth" / "meta.md").read_text()
    assert "status: interviewing" in content


def test_returns_404_when_company_missing(running_server: tuple[str, Path]):
    base, _ = running_server
    assert _patch(f"{base}/api/positions/NonExistent/status", {"status": "applied"}) == 404


def test_returns_400_when_body_missing_status(running_server: tuple[str, Path]):
    base, _ = running_server
    assert _patch(f"{base}/api/positions/Plaid/status", {}) == 400


def test_rejects_path_traversal(running_server: tuple[str, Path]):
    base, _ = running_server
    path = quote("../../etc", safe="")
    assert _patch(f"{base}/api/positions/{path}/status", {"status": "applied"}) == 400
