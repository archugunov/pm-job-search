"""Shared pytest fixtures for serve.py tests.

Builds a temp userdata/ tree mirroring the real layout so tests can exercise
the server's glob and write paths against a realistic structure.
"""
from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest


@pytest.fixture
def userdata(tmp_path: Path) -> Path:
    """Build a minimal userdata/ tree.

    Layout:
      userdata/
        companies/
          Plaid/meta.md                       (single-role, flat)
          Stripe/lead-pm-growth/meta.md       (multi-role, subfolder)
          Stripe/sr-pm-payments/meta.md       (multi-role, subfolder)
        strategy.md
        outputs/
          daily-brief-2026-05-18.md
    """
    root = tmp_path / "userdata"
    (root / "companies" / "Plaid").mkdir(parents=True)
    (root / "companies" / "Stripe" / "lead-pm-growth").mkdir(parents=True)
    (root / "companies" / "Stripe" / "sr-pm-payments").mkdir(parents=True)
    (root / "outputs").mkdir()

    (root / "companies" / "Plaid" / "meta.md").write_text(dedent("""\
        ---
        company: Plaid
        status: interviewing
        tier: P0
        score: 14
        position: Senior PM, Consumer Credit
        link: https://example.com/plaid
        date_added: 2026-04-22
        date_applied: 2026-04-25
        last_inbound: 2026-05-15
        ---

        # Plaid
        """))

    (root / "companies" / "Stripe" / "lead-pm-growth" / "meta.md").write_text(dedent("""\
        ---
        company: Stripe
        status: applied
        tier: P1
        score: 12
        position: Lead PM, Growth
        link: https://example.com/stripe-growth
        date_added: 2026-05-01
        date_applied: 2026-05-03
        ---

        # Stripe — Lead PM, Growth
        """))

    (root / "companies" / "Stripe" / "sr-pm-payments" / "meta.md").write_text(dedent("""\
        ---
        company: Stripe
        status: discovered
        tier: P2
        score: 9
        position: Sr PM, Payments
        link: https://example.com/stripe-payments
        date_added: 2026-05-10
        ---

        # Stripe — Sr PM, Payments
        """))

    (root / "strategy.md").write_text(dedent("""\
        ---
        target_offer_date: 2026-06-28
        weekly_targets:
          outreach: 7
          applications: 3
        ---

        # Strategy
        """))

    (root / "outputs" / "daily-brief-2026-05-18.md").write_text(
        "# Daily brief — 2026-05-18\n\nToday's brief body.\n"
    )

    return root
