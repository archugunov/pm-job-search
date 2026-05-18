"""Tests for count_warm_outreach / count_recent_applications.

Window is the current ISO week: [Monday of this week, today] inclusive.
TODAY is fixed to Friday 2026-05-15 so the window is Mon 2026-05-11 → Fri 2026-05-15.
Anything before 2026-05-11 or after 2026-05-15 is out of window.
"""
from __future__ import annotations

from datetime import date
from textwrap import dedent

from serve import count_recent_applications, count_warm_outreach, compute_weekly_progress


TODAY = date(2026, 5, 15)  # Friday — week runs Mon 2026-05-11 through Fri 2026-05-15.


# ----- count_warm_outreach ----------------------------------------------------


def test_empty_journal_returns_zero():
    assert count_warm_outreach("", TODAY) == 0
    assert count_warm_outreach("# Journal\n\n", TODAY) == 0


def test_counts_bullet_with_keyword_in_window():
    md = dedent("""\
        # Journal

        ## 2026-05-13

        - Sent a DM to David about the Stripe role.
        """)
    assert count_warm_outreach(md, TODAY) == 1


def test_skips_bullet_before_week_start():
    # 2026-05-10 is Sunday of the previous ISO week — out of window.
    md = dedent("""\
        ## 2026-05-10

        - Sent a DM to David.
        """)
    assert count_warm_outreach(md, TODAY) == 0


def test_skips_bullet_after_today():
    # 2026-05-16 is tomorrow — out of window.
    md = dedent("""\
        ## 2026-05-16

        - Sent a DM to David.
        """)
    assert count_warm_outreach(md, TODAY) == 0


def test_includes_week_start_and_today_boundary():
    # Monday (week start) and Friday (today) inclusive.
    md = dedent("""\
        ## 2026-05-11

        - Sent a DM.

        ## 2026-05-15

        - Coffee with Tom.
        """)
    assert count_warm_outreach(md, TODAY) == 2


def test_one_bullet_with_multiple_keywords_counts_once():
    md = dedent("""\
        ## 2026-05-13

        - Sent a DM and grabbed coffee with David — also got an intro to Ramp.
        """)
    assert count_warm_outreach(md, TODAY) == 1


def test_two_bullets_each_with_a_keyword_count_separately():
    md = dedent("""\
        ## 2026-05-13

        - Sent a DM to David.
        - Coffee with Tom on Friday.
        - Plaid 2nd-round panel went well. (no keyword — not counted)
        """)
    assert count_warm_outreach(md, TODAY) == 2


def test_keyword_match_is_case_insensitive():
    md = dedent("""\
        ## 2026-05-13

        - sent a dm to David.
        - REACHED OUT to two PMs.
        """)
    assert count_warm_outreach(md, TODAY) == 2


def test_substring_does_not_match_keyword():
    # "introduction" should not match the "intro" keyword as a substring;
    # \b boundary keeps the match whole-word.
    md = dedent("""\
        ## 2026-05-13

        - Wrote the introduction section of the case study.
        """)
    assert count_warm_outreach(md, TODAY) == 0


def test_bullet_continuation_lines_are_part_of_same_bullet():
    md = dedent("""\
        ## 2026-05-13

        - Two new LinkedIn DMs from senior PMs at adjacent companies asking
          about the pricing framework. Worth a coffee if either has a referral path.
        """)
    # Two keywords (DMs, coffee) in one bullet → 1
    assert count_warm_outreach(md, TODAY) == 1


def test_multiple_dated_sections_some_in_window_some_not():
    md = dedent("""\
        ## 2026-05-08

        - Sent a DM to David. (Friday of previous week — out of window)

        ## 2026-05-13

        - Coffee with Tom. (Wed of current week — in window)

        ## 2026-05-15

        - Got an intro from Sarah. (today — in window)
        """)
    assert count_warm_outreach(md, TODAY) == 2


def test_malformed_date_heading_closes_window():
    md = dedent("""\
        ## 2026-05-13

        - DM to David. (in window — counts)

        ## not-a-date

        - DM to Alice. (window closed by bad heading)
        """)
    assert count_warm_outreach(md, TODAY) == 1


def test_text_outside_any_bullet_does_not_count():
    md = dedent("""\
        ## 2026-05-13

        Free-form prose mentioning DM and coffee but not in a bullet.

        - Real bullet: messaged David.
        """)
    assert count_warm_outreach(md, TODAY) == 1


def test_monday_today_window_is_one_day():
    # On Monday morning the window collapses to just today.
    monday = date(2026, 5, 18)
    md = dedent("""\
        ## 2026-05-17

        - DM on Sunday (previous week — out).

        ## 2026-05-18

        - DM on Monday (in window).
        """)
    assert count_warm_outreach(md, monday) == 1


# ----- count_recent_applications ---------------------------------------------


def test_application_in_window_counted():
    companies = [{"date_applied": "2026-05-13"}]
    assert count_recent_applications(companies, TODAY) == 1


def test_application_at_week_boundaries_counted():
    companies = [
        {"date_applied": "2026-05-11"},  # Monday — week start
        {"date_applied": "2026-05-15"},  # Friday — today
    ]
    assert count_recent_applications(companies, TODAY) == 2


def test_application_outside_window_not_counted():
    companies = [
        {"date_applied": "2026-05-10"},  # Sunday of previous week
        {"date_applied": "2026-05-16"},  # Saturday — tomorrow
    ]
    assert count_recent_applications(companies, TODAY) == 0


def test_missing_or_malformed_dates_skipped():
    companies = [
        {},
        {"date_applied": ""},
        {"date_applied": "not-a-date"},
        {"date_applied": "2026-05-13"},
    ]
    assert count_recent_applications(companies, TODAY) == 1


# ----- compute_weekly_progress ----------------------------------------------


def test_window_days_matches_position_in_iso_week(tmp_path):
    # Monday → 1, Wednesday → 3, Sunday → 7.
    cases = [
        (date(2026, 5, 18), 1),  # Monday
        (date(2026, 5, 20), 3),  # Wednesday
        (date(2026, 5, 24), 7),  # Sunday
    ]
    for today, expected in cases:
        out = compute_weekly_progress(tmp_path, [], today=today)
        assert out["window_days"] == expected, f"{today}: expected {expected}, got {out['window_days']}"
