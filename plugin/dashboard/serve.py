"""pm-job-search dashboard — Python stdlib HTTP server.

Implementation lands across tasks A2-A12. Each task adds one pure helper
or one HTTP endpoint via TDD.
"""
from __future__ import annotations

import re
from typing import Tuple


_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.DOTALL)
_INDENT_RE = re.compile(r"^(\s+)(\S)")


def parse_frontmatter(md: str) -> Tuple[dict[str, str], str]:
    """Parse YAML-ish frontmatter from a markdown string.

    Returns (frontmatter_dict, body). Frontmatter values are returned as
    strings (quotes stripped). Nested one-level mappings are flattened with
    dot-notation keys, e.g. `weekly_targets.outreach` -> "7".

    Lines starting with '#' inside the frontmatter are treated as comments
    and ignored. Returns ({}, original_md) if no frontmatter present.
    """
    match = _FRONTMATTER_RE.match(md)
    if not match:
        return {}, md

    raw_block, body = match.group(1), match.group(2)
    out: dict[str, str] = {}
    current_parent: str | None = None
    current_indent = 0

    for raw_line in raw_block.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent_match = _INDENT_RE.match(raw_line)
        is_nested = indent_match is not None

        if is_nested and current_parent is not None:
            key, _, value = stripped.partition(":")
            out[f"{current_parent}.{key.strip()}"] = _strip_quotes(value.strip())
            continue

        key, sep, value = stripped.partition(":")
        if not sep:
            continue
        key = key.strip()
        value = value.strip()

        if value == "":
            current_parent = key
            current_indent = 0
        else:
            current_parent = None
            out[key] = _strip_quotes(value)

    return out, body


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        return value[1:-1]
    return value


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def position_slug(position: str) -> str:
    """Lowercase, replace runs of non-alphanumeric with a single hyphen, trim hyphens.

    "Senior PM, Consumer Credit" -> "senior-pm-consumer-credit"
    """
    lowered = position.lower()
    hyphenated = _SLUG_RE.sub("-", lowered)
    return hyphenated.strip("-")
