"""Tests for position_slug — derive kebab-case slug from a position string."""
from serve import position_slug


def test_basic_kebab_case():
    assert position_slug("Senior PM, Consumer Credit") == "senior-pm-consumer-credit"


def test_collapses_runs_of_non_alnum():
    assert position_slug("Lead PM / Growth") == "lead-pm-growth"
    assert position_slug("Sr PM   Banking") == "sr-pm-banking"


def test_trims_leading_trailing_separators():
    assert position_slug(", Senior PM, ") == "senior-pm"
    assert position_slug("---Hello---") == "hello"


def test_preserves_numerics():
    assert position_slug("PM L5, Search Ranking") == "pm-l5-search-ranking"


def test_empty_input_returns_empty_string():
    assert position_slug("") == ""
    assert position_slug("   ") == ""
