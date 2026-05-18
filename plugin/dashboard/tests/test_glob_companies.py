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


def _write_meta(path: Path, company: str, position: str, status: str = "applied") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\ncompany: {company}\nstatus: {status}\ntier: P1\nposition: {position}\n---\n",
        encoding="utf-8",
    )


def test_flat_meta_dropped_when_company_has_subfolder_entries(tmp_path: Path):
    """Mid-migration state: company has both flat meta.md and role-slug subfolders.
    Per /today spec, prefer subfolder entries; drop the flat one to avoid duplicates."""
    companies = tmp_path / "companies"
    _write_meta(companies / "Plaid" / "meta.md", "Plaid", "Stale Position", status="rejected")
    _write_meta(companies / "Plaid" / "consumer-credit" / "meta.md", "Plaid", "Senior PM, Consumer Credit", status="interviewing")
    _write_meta(companies / "Plaid" / "growth-loops" / "meta.md", "Plaid", "Senior PM, Growth Loops", status="to_apply")

    positions = collect_companies(tmp_path)
    folder_paths = sorted(p["folder_path"] for p in positions)
    assert folder_paths == ["Plaid/consumer-credit", "Plaid/growth-loops"]
    assert all(p["is_multi_role"] for p in positions)
    # the stale flat "Stale Position" must NOT appear
    assert not any(p["position"] == "Stale Position" for p in positions)


def test_flat_meta_kept_when_no_subfolder_for_same_company(tmp_path: Path):
    """Sanity check: a flat-only company keeps its flat entry; only companies
    with mixed flat+sub layout drop the flat one."""
    companies = tmp_path / "companies"
    _write_meta(companies / "Lendable" / "meta.md", "Lendable", "Head of Product", status="offer")
    _write_meta(companies / "Stripe" / "lead-pm-growth" / "meta.md", "Stripe", "Lead PM, Growth", status="rejected")

    positions = collect_companies(tmp_path)
    folder_paths = sorted(p["folder_path"] for p in positions)
    assert folder_paths == ["Lendable", "Stripe/lead-pm-growth"]


def test_passes_through_status_specific_fields(tmp_path: Path):
    """Rejection / closed / next_event fields must pass through to API records.

    Previously these were dropped by _OPTIONAL_FIELDS whitelist, leaving the
    dashboard unable to render rejection-stage / closed-date / next-event signals.
    """
    companies = tmp_path / "companies"
    rejected_path = companies / "Fly.io" / "meta.md"
    rejected_path.parent.mkdir(parents=True, exist_ok=True)
    rejected_path.write_text(
        "---\n"
        "company: Fly.io\n"
        "status: rejected\n"
        "tier: P1\n"
        "position: Head of Product\n"
        "date_rejected: 2026-04-08\n"
        "rejection_stage: take-home\n"
        'rejection_note: "Strong submission; prioritising infra-PM experience."\n'
        "---\n",
        encoding="utf-8",
    )
    closed_path = companies / "Replit" / "meta.md"
    closed_path.parent.mkdir(parents=True, exist_ok=True)
    closed_path.write_text(
        "---\ncompany: Replit\nstatus: closed\ntier: P2\nposition: HoP, Edu\ndate_closed: 2026-05-03\n---\n",
        encoding="utf-8",
    )
    upcoming_path = companies / "Lendable" / "meta.md"
    upcoming_path.parent.mkdir(parents=True, exist_ok=True)
    upcoming_path.write_text(
        "---\n"
        "company: Lendable\n"
        "status: offer\n"
        "tier: P0\n"
        "position: Head of Product\n"
        'next_event: "Reference call Wed 2026-05-20 11:00"\n'
        "---\n",
        encoding="utf-8",
    )

    positions = {p["company"]: p for p in collect_companies(tmp_path)}

    fly = positions["Fly.io"]
    assert fly["date_rejected"] == "2026-04-08"
    assert fly["rejection_stage"] == "take-home"
    assert fly["rejection_note"] == "Strong submission; prioritising infra-PM experience."

    replit = positions["Replit"]
    assert replit["date_closed"] == "2026-05-03"

    lendable = positions["Lendable"]
    assert lendable["next_event"] == "Reference call Wed 2026-05-20 11:00"
