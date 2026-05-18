"""Tests for count_warm_outreach / count_recent_applications.

Mirrors the /today skill's algorithm so the dashboard and /today agree.
"""
from __future__ import annotations

from datetime import date
from textwrap import dedent

from serve import count_recent_applications, count_warm_outreach


TODAY = date(2026, 5, 18)  # Monday


# ----- count_warm_outreach ----------------------------------------------------


def test_empty_journal_returns_zero():
    assert count_warm_outreach("", TODAY) == 0
    assert count_warm_outreach("# Journal\n\n", TODAY) == 0


def test_counts_bullet_with_keyword_in_window():
    md = dedent("""\
        # Journal

        ## 2026-05-15

        - Sent a DM to David about the Stripe role.
        """)
    assert count_warm_outreach(md, TODAY) == 1


def test_skips_bullet_outside_window():
    # Today − 7 is out of the rolling 7-day window.
    md = dedent("""\
        ## 2026-05-11

        - Sent a DM to David.
        """)
    assert count_warm_outreach(md, TODAY) == 0


def test_includes_boundary_dates():
    # Today − 6 and today inclusive.
    md = dedent("""\
        ## 2026-05-12

        - Sent a DM.

        ## 2026-05-18

        - Coffee with Tom.
        """)
    assert count_warm_outreach(md, TODAY) == 2


def test_one_bullet_with_multiple_keywords_counts_once():
    md = dedent("""\
        ## 2026-05-15

        - Sent a DM and grabbed coffee with David — also got an intro to Ramp.
        """)
    assert count_warm_outreach(md, TODAY) == 1


def test_two_bullets_each_with_a_keyword_count_separately():
    md = dedent("""\
        ## 2026-05-15

        - Sent a DM to David.
        - Coffee with Tom on Friday.
        - Plaid 2nd-round panel went well. (no keyword — not counted)
        """)
    assert count_warm_outreach(md, TODAY) == 2


def test_keyword_match_is_case_insensitive():
    md = dedent("""\
        ## 2026-05-15

        - sent a dm to David.
        - REACHED OUT to two PMs.
        """)
    assert count_warm_outreach(md, TODAY) == 2


def test_substring_does_not_match_keyword():
    # "introduction" should not match the "intro" keyword as a substring;
    # \b boundary keeps the match whole-word.
    md = dedent("""\
        ## 2026-05-15

        - Wrote the introduction section of the case study.
        """)
    assert count_warm_outreach(md, TODAY) == 0


def test_bullet_continuation_lines_are_part_of_same_bullet():
    md = dedent("""\
        ## 2026-05-15

        - Two new LinkedIn DMs from senior PMs at adjacent companies asking
          about the pricing framework. Worth a coffee if either has a referral path.
        """)
    # Two keywords (DMs, coffee) in one bullet → 1
    assert count_warm_outreach(md, TODAY) == 1


def test_multiple_dated_sections_some_in_window_some_not():
    md = dedent("""\
        ## 2026-05-08

        - Sent a DM to David. (out of window)

        ## 2026-05-13

        - Coffee with Tom. (in window — 5 days back)

        ## 2026-05-18

        - Got an intro from Sarah. (today)
        """)
    assert count_warm_outreach(md, TODAY) == 2


def test_malformed_date_heading_closes_window():
    md = dedent("""\
        ## 2026-05-15

        - DM to David. (in window — counts)

        ## not-a-date

        - DM to Alice. (window closed by bad heading)
        """)
    assert count_warm_outreach(md, TODAY) == 1


def test_text_outside_any_bullet_does_not_count():
    md = dedent("""\
        ## 2026-05-15

        Free-form prose mentioning DM and coffee but not in a bullet.

        - Real bullet: messaged David.
        """)
    assert count_warm_outreach(md, TODAY) == 1


# ----- count_recent_applications ---------------------------------------------


def test_application_in_window_counted():
    companies = [{"date_applied": "2026-05-15"}]
    assert count_recent_applications(companies, TODAY) == 1


def test_application_at_window_boundaries_counted():
    companies = [
        {"date_applied": "2026-05-12"},  # today - 6
        {"date_applied": "2026-05-18"},  # today
    ]
    assert count_recent_applications(companies, TODAY) == 2


def test_application_outside_window_not_counted():
    companies = [
        {"date_applied": "2026-05-11"},  # today - 7
        {"date_applied": "2026-05-19"},  # today + 1
    ]
    assert count_recent_applications(companies, TODAY) == 0


def test_missing_or_malformed_dates_skipped():
    companies = [
        {},
        {"date_applied": ""},
        {"date_applied": "not-a-date"},
        {"date_applied": "2026-05-15"},
    ]
    assert count_recent_applications(companies, TODAY) == 1
