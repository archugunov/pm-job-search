#!/usr/bin/env python3
"""Validate a userdata/ tree against the documented file schemas.

Single source of truth for machine-checkable schema rules. Called three ways:
  * test-personas Phase 3.5 — after a journey, over the userdata/ it produced
  * CI (tests/test_snapshots_conform.py) — over each tests/snapshots/* fixture
  * by hand: python3 scripts/validate_userdata.py userdata/

Rules are defined in plugin/schemas/*.schema.md. Stdlib only, no deps.
Exit 0 = clean, 1 = findings, 2 = usage error.
"""
from __future__ import annotations

import re
import sys
from collections import namedtuple
from pathlib import Path

Finding = namedtuple("Finding", ["path", "rule", "detail"])

STATUS_ENUM = {"new", "to_apply", "applied", "interviewing", "offer",
               "rejected", "not_interested"}
META_REQUIRED = ["company", "position", "status", "link"]
META_FORBIDDEN = ["role", "target_date"]
PROFILE_REQUIRED = ["name", "target_titles", "tier_weights", "tier_thresholds"]
STRATEGY_REQUIRED = ["target_offer_date", "weekly_targets"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")


def parse_frontmatter(text: str) -> dict[str, str]:
    """Top-level frontmatter keys only. Nested/indented keys are ignored;
    a key introducing a nested block maps to ''. Values keep inline text,
    with trailing '# comment' stripped.

    The opening '---' may be preceded by blank lines and/or any number of
    leading HTML comment blocks (each possibly spanning multiple lines),
    interspersed with blank lines — both templates
    (plugin/templates/profile.template.md, strategy.template.md) and real
    userdata files open with such comments before the frontmatter. Some real
    files (e.g. tests/snapshots/diego-reflection/strategy.md) have TWO
    consecutive comment blocks: a short one-liner followed by the longer
    template comment."""
    text = text.lstrip("﻿")  # UTF-8 BOM, if present, precedes everything
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        if i < len(lines) and lines[i].strip().startswith("<!--"):
            if "-->" not in lines[i]:
                i += 1
                while i < len(lines) and "-->" not in lines[i]:
                    i += 1
            i += 1  # past the line containing '-->'
            continue
        break
    if i >= len(lines) or lines[i].strip() != "---":
        return {}
    fm: dict[str, str] = {}
    for line in lines[i + 1:]:
        if line.strip() == "---":
            return fm
        m = KEY_RE.match(line)  # anchored: indented keys don't match
        if m:
            raw = m.group(2)
            # Only treat '#' as starting a trailing comment when it begins the
            # value or is preceded by whitespace — a bare '#' inside a value
            # (e.g. a URL fragment like https://x/y#frag) is not a comment.
            cm = re.search(r"(?:^|\s)#", raw)
            value = (raw[:cm.start()] if cm else raw).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            fm[m.group(1)] = value
    return {}  # unterminated block — treat as no frontmatter


def _rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def _check_meta(root: Path, p: Path) -> list[Finding]:
    fm = parse_frontmatter(p.read_text())
    rel = _rel(root, p)
    out = []
    missing = [k for k in META_REQUIRED if k not in fm or (k != "link" and not fm[k])]
    if missing:
        out.append(Finding(rel, "meta.required", f"missing/empty: {', '.join(missing)}"))
    if fm.get("status") and fm["status"] not in STATUS_ENUM:
        out.append(Finding(rel, "meta.status-enum", f"status '{fm['status']}' not in enum"))
    link = fm.get("link", "")
    if link and not link.startswith(("http://", "https://")):
        out.append(Finding(rel, "meta.link-format", f"link '{link}' is not http(s)"))
    present_forbidden = [k for k in META_FORBIDDEN if k in fm]
    if present_forbidden:
        out.append(Finding(rel, "meta.forbidden-key",
                           f"forbidden: {', '.join(present_forbidden)}"))
    return out


def _check_profile(root: Path, p: Path) -> list[Finding]:
    text = p.read_text()
    fm = parse_frontmatter(text)
    rel = _rel(root, p)
    out = []
    missing = [k for k in PROFILE_REQUIRED if k not in fm]
    if missing:
        out.append(Finding(rel, "profile.required", f"missing: {', '.join(missing)}"))
    if not re.search(r"^## Positioning\s*$", text, re.MULTILINE):
        out.append(Finding(rel, "profile.positioning", "no '## Positioning' section"))
    return out


def _check_strategy(root: Path, p: Path) -> list[Finding]:
    fm = parse_frontmatter(p.read_text())
    rel = _rel(root, p)
    out = []
    missing = [k for k in STRATEGY_REQUIRED if k not in fm]
    if missing:
        out.append(Finding(rel, "strategy.required", f"missing: {', '.join(missing)}"))
    tod = fm.get("target_offer_date", "")
    if tod and tod != "null" and not DATE_RE.match(tod):
        out.append(Finding(rel, "strategy.date-format",
                           f"target_offer_date '{tod}' is not YYYY-MM-DD or null"))
    if "target_date" in fm:
        out.append(Finding(rel, "strategy.forbidden-key",
                           "'target_date:' found — schema key is 'target_offer_date:'"))
    return out


def _check_brief(root: Path, p: Path) -> list[Finding]:
    rel = _rel(root, p)
    out = []
    m = re.search(r"^\*\*Source:\*\*\s*(\S+)", p.read_text(), re.MULTILINE)
    if not m or not m.group(1).startswith(("http://", "https://")):
        out.append(Finding(rel, "brief.source-line",
                           "no '**Source:** http…' line in research-brief"))
        return out
    meta = p.parent / "meta.md"
    if meta.exists():
        link = parse_frontmatter(meta.read_text()).get("link", "")
        if link and link != m.group(1):
            out.append(Finding(rel, "brief.link-mismatch",
                               f"Source '{m.group(1)}' != meta link '{link}'"))
    return out


def validate_tree(root: Path) -> list[Finding]:
    root = Path(root)
    out: list[Finding] = []
    companies = root / "companies"
    if companies.is_dir():
        for pattern in ("*/meta.md", "*/*/meta.md"):
            for p in sorted(companies.glob(pattern)):
                out.extend(_check_meta(root, p))
        for pattern in ("*/research-brief.md", "*/*/research-brief.md"):
            for p in sorted(companies.glob(pattern)):
                out.extend(_check_brief(root, p))
    profile = root / "profile.md"
    if profile.exists():
        out.extend(_check_profile(root, profile))
    strategy = root / "strategy.md"
    if strategy.exists():
        out.extend(_check_strategy(root, strategy))
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 2 or not Path(argv[1]).is_dir():
        print("usage: validate_userdata.py <userdata-tree>", file=sys.stderr)
        return 2
    findings = validate_tree(Path(argv[1]))
    for f in findings:
        print(f"{f.path}: {f.rule} — {f.detail}")
    if not findings:
        print("No schema drift found.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
