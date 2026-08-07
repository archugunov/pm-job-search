from pathlib import Path
from textwrap import dedent

from validate_userdata import Finding, parse_frontmatter, validate_tree


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(dedent(text))


GOOD_META = """\
    ---
    company: Plaid
    position: Senior PM, Consumer Credit
    status: interviewing
    link: https://example.com/plaid
    ---

    # Plaid
    """


def test_parse_frontmatter_top_level_keys():
    fm = parse_frontmatter(dedent(GOOD_META))
    assert fm["company"] == "Plaid"
    assert fm["status"] == "interviewing"


def test_parse_frontmatter_nested_key_collapses_to_empty():
    text = "---\nweekly_targets:\n  applications: 3\n---\n"
    fm = parse_frontmatter(text)
    assert "weekly_targets" in fm and fm["weekly_targets"] == ""
    assert "applications" not in fm  # indented keys are not top-level


def test_parse_frontmatter_no_block_returns_empty():
    assert parse_frontmatter("# Just a heading\n") == {}


def test_clean_meta_yields_no_findings(tmp_path):
    write(tmp_path / "companies" / "Plaid" / "meta.md", GOOD_META)
    assert validate_tree(tmp_path) == []


def test_meta_missing_required_key(tmp_path):
    write(tmp_path / "companies" / "Plaid" / "meta.md", """\
        ---
        company: Plaid
        status: applied
        link: https://example.com/x
        ---
        """)
    rules = [f.rule for f in validate_tree(tmp_path)]
    assert rules == ["meta.required"]


def test_meta_bad_status_enum(tmp_path):
    write(tmp_path / "companies" / "Plaid" / "meta.md", GOOD_META.replace(
        "status: interviewing", "status: discovered"))
    findings = validate_tree(tmp_path)
    assert [f.rule for f in findings] == ["meta.status-enum"]
    assert "discovered" in findings[0].detail


def test_meta_bad_link_format(tmp_path):
    write(tmp_path / "companies" / "Plaid" / "meta.md", GOOD_META.replace(
        "link: https://example.com/plaid", "link: example.com/plaid"))
    assert [f.rule for f in validate_tree(tmp_path)] == ["meta.link-format"]


def test_meta_empty_link_allowed(tmp_path):
    write(tmp_path / "companies" / "Plaid" / "meta.md", GOOD_META.replace(
        "link: https://example.com/plaid", "link:"))
    assert validate_tree(tmp_path) == []


def test_meta_forbidden_role_key(tmp_path):
    write(tmp_path / "companies" / "Plaid" / "meta.md", """\
        ---
        company: Plaid
        role: Senior PM
        position: Senior PM
        status: applied
        link: https://example.com/x
        ---
        """)
    assert "meta.forbidden-key" in [f.rule for f in validate_tree(tmp_path)]


def test_meta_role_slug_subfolder_is_scanned(tmp_path):
    write(tmp_path / "companies" / "Stripe" / "lead-pm" / "meta.md", GOOD_META.replace(
        "status: interviewing", "status: nonsense"))
    findings = validate_tree(tmp_path)
    assert findings[0].path == "companies/Stripe/lead-pm/meta.md"
    assert findings[0].rule == "meta.status-enum"
