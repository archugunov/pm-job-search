"""Tests for rewrite_status — rewrite the `status:` value in frontmatter while preserving everything else."""
from textwrap import dedent

import pytest

from serve import rewrite_status


def test_rewrites_bare_value():
    src = dedent("""\
        ---
        company: Plaid
        status: interviewing
        tier: P0
        ---

        # Plaid
        """)
    out = rewrite_status(src, "rejected")
    assert "status: rejected" in out
    assert "status: interviewing" not in out
    assert "company: Plaid" in out
    assert "tier: P0" in out
    assert out.endswith("# Plaid\n")


def test_preserves_double_quotes():
    src = dedent("""\
        ---
        status: "interviewing"
        ---
        """)
    out = rewrite_status(src, "rejected")
    assert 'status: "rejected"' in out


def test_preserves_single_quotes():
    src = dedent("""\
        ---
        status: 'interviewing'
        ---
        """)
    out = rewrite_status(src, "rejected")
    assert "status: 'rejected'" in out


def test_preserves_comments_and_blank_lines():
    src = dedent("""\
        ---
        company: Plaid
        # the next field is the one we're changing
        status: interviewing

        tier: P0
        ---
        """)
    out = rewrite_status(src, "rejected")
    assert "# the next field is the one we're changing" in out
    assert "status: rejected" in out
    assert "rejected\n\ntier: P0" in out


def test_raises_when_no_frontmatter():
    with pytest.raises(ValueError, match="no frontmatter"):
        rewrite_status("# Just a heading\n", "rejected")


def test_raises_when_no_status_line():
    src = dedent("""\
        ---
        company: Plaid
        tier: P0
        ---
        """)
    with pytest.raises(ValueError, match="no status line"):
        rewrite_status(src, "rejected")


def test_only_rewrites_inside_frontmatter():
    src = dedent("""\
        ---
        status: interviewing
        ---

        Notes: status: was rejected at one point, then revived.
        """)
    out = rewrite_status(src, "applied")
    assert "status: applied" in out
    assert "status: was rejected at one point" in out
    assert out.count("status: applied") == 1
