"""Tests for collect_companies — glob and parse all meta.md files into Position records."""
from pathlib import Path

from serve import collect_companies


def test_returns_one_record_per_meta_md(userdata: Path):
    positions = collect_companies(userdata)
    assert len(positions) == 3


def test_single_role_company_has_flat_folder_path(userdata: Path):
    positions = {p["company"]: p for p in collect_companies(userdata) if not p["is_multi_role"]}
    assert positions["Plaid"]["folder_path"] == "Plaid"


def test_multi_role_company_has_subfolder_path(userdata: Path):
    positions = [p for p in collect_companies(userdata) if p["company"] == "Stripe"]
    assert len(positions) == 2
    paths = sorted(p["folder_path"] for p in positions)
    assert paths == ["Stripe/lead-pm-growth", "Stripe/sr-pm-payments"]


def test_multi_role_flag_set_correctly(userdata: Path):
    positions = collect_companies(userdata)
    plaid = next(p for p in positions if p["company"] == "Plaid")
    stripe = next(p for p in positions if p["company"] == "Stripe")
    assert plaid["is_multi_role"] is False
    assert stripe["is_multi_role"] is True


def test_position_slug_derived(userdata: Path):
    positions = collect_companies(userdata)
    plaid = next(p for p in positions if p["company"] == "Plaid")
    assert plaid["position_slug"] == "senior-pm-consumer-credit"


def test_passes_through_optional_fields(userdata: Path):
    positions = collect_companies(userdata)
    plaid = next(p for p in positions if p["company"] == "Plaid")
    assert plaid["score"] == "14"
    assert plaid["link"] == "https://example.com/plaid"
    assert plaid["date_added"] == "2026-04-22"
    assert plaid["last_inbound"] == "2026-05-15"


def test_returns_empty_list_when_no_companies(tmp_path: Path):
    (tmp_path / "companies").mkdir()
    assert collect_companies(tmp_path) == []
