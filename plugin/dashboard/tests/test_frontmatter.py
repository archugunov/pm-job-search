"""Tests for parse_frontmatter — extract YAML-style key/value pairs from md frontmatter."""
from __future__ import annotations

from textwrap import dedent

from serve import parse_frontmatter


def test_parses_simple_keys():
    md = dedent("""\
        ---
        company: Plaid
        status: interviewing
        tier: P0
        ---

        body
        """)
    fm, body = parse_frontmatter(md)
    assert fm["company"] == "Plaid"
    assert fm["status"] == "interviewing"
    assert fm["tier"] == "P0"
    assert body.strip() == "body"


def test_strips_quotes():
    md = dedent("""\
        ---
        status: "interviewing"
        note: 'hello'
        ---
        """)
    fm, _ = parse_frontmatter(md)
    assert fm["status"] == "interviewing"
    assert fm["note"] == "hello"


def test_parses_integers_as_strings_by_default():
    md = dedent("""\
        ---
        score: 14
        ---
        """)
    fm, _ = parse_frontmatter(md)
    assert fm["score"] == "14"


def test_handles_nested_block_as_raw_text():
    md = dedent("""\
        ---
        target_offer_date: 2026-06-28
        weekly_targets:
          outreach: 7
          applications: 3
        ---
        """)
    fm, _ = parse_frontmatter(md)
    assert fm["target_offer_date"] == "2026-06-28"
    assert fm["weekly_targets.outreach"] == "7"
    assert fm["weekly_targets.applications"] == "3"


def test_returns_empty_dict_when_no_frontmatter():
    fm, body = parse_frontmatter("# Just a heading\n\nNo frontmatter here.\n")
    assert fm == {}
    assert body.startswith("# Just a heading")


def test_ignores_lines_starting_with_hash_inside_frontmatter():
    md = dedent("""\
        ---
        # this is a comment
        company: Plaid
        ---
        """)
    fm, _ = parse_frontmatter(md)
    assert fm == {"company": "Plaid"}


def test_skips_leading_html_comments_before_frontmatter():
    md = dedent("""\
        <!-- Example file. Replace with your own via /setup. -->
        <!--
          Multi-line comment block
          with documentation for humans reading the source.
        -->
        ---
        company: Plaid
        tier: P0
        ---

        body
        """)
    fm, body = parse_frontmatter(md)
    assert fm["company"] == "Plaid"
    assert fm["tier"] == "P0"
    assert body.strip() == "body"
