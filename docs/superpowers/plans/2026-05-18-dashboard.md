# pm-job-search dashboard — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a browser-based dashboard that replaces Notion as the user's daily working surface for the pm-job-search plugin. Read pipeline state from md; write status changes, timestamped notes, and new-company scaffolds back to md.

**Architecture:** Python stdlib HTTP server serves a pre-built React + Mantine SPA. Browser ↔ server ↔ md files. Source of truth stays markdown; dashboard is the working view. `dist/` is committed so installation costs zero.

**Tech Stack:** Python 3 (stdlib only at runtime), React 18, TypeScript, Mantine v7, Vite, react-markdown, @tabler/icons-react. Pytest for Python TDD (dev-only).

**Spec:** [docs/superpowers/specs/2026-05-18-dashboard-design.md](../specs/2026-05-18-dashboard-design.md)

---

## Wave structure (parallel dispatch)

- **Wave 1 (parallel):** Slice A (Python API server) + Slice B (Vite + Mantine shell).
- **Wave 2 (parallel):** Slice C (Table + writes UI) + Slice D (Top + bottom zones) + Slice E (`/dashboard` SKILL.md).
- **Wave 3:** Slice F (Docs, privacy, CI, build, commit `dist/`).

A task from a later wave MAY start only after every task in its predecessor wave is committed.

---

## Slice A — Python API server

### Task A1: Project scaffold and dev-deps

**Files:**
- Create: `plugin/dashboard/serve.py` (empty placeholder)
- Create: `plugin/dashboard/tests/__init__.py` (empty)
- Create: `plugin/dashboard/tests/conftest.py`
- Create: `plugin/dashboard/requirements-dev.txt`

- [ ] **Step 1: Create directories**

```bash
mkdir -p plugin/dashboard/tests
```

- [ ] **Step 2: Write `plugin/dashboard/requirements-dev.txt`**

```
pytest>=8.0
```

- [ ] **Step 3: Write `plugin/dashboard/tests/__init__.py`**

Empty file.

- [ ] **Step 4: Write `plugin/dashboard/tests/conftest.py`**

```python
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
```

- [ ] **Step 5: Write `plugin/dashboard/serve.py` (placeholder)**

```python
"""pm-job-search dashboard — Python stdlib HTTP server.

Implementation lands across tasks A2-A12. Each task adds one pure helper
or one HTTP endpoint via TDD.
"""
```

- [ ] **Step 6: Verify scaffold**

Run: `cd plugin/dashboard && python3 -m pytest tests/ -v`
Expected: `no tests ran` (exit 5). Confirms pytest discovers the directory.

- [ ] **Step 7: Commit**

```bash
git add plugin/dashboard/
git commit -m "feat(dashboard): scaffold Python server + pytest harness"
```

---

### Task A2: Frontmatter parser (TDD)

**Files:**
- Modify: `plugin/dashboard/serve.py`
- Create: `plugin/dashboard/tests/test_frontmatter.py`

- [ ] **Step 1: Write the failing tests**

Create `plugin/dashboard/tests/test_frontmatter.py`:

```python
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
    # The dashboard treats all frontmatter values as strings; consumers cast.
    md = dedent("""\
        ---
        score: 14
        ---
        """)
    fm, _ = parse_frontmatter(md)
    assert fm["score"] == "14"


def test_handles_nested_block_as_raw_text():
    # weekly_targets is a sub-mapping; we don't need full YAML, just preserve raw text.
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
    # Nested keys flattened with dot-notation keys
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_frontmatter.py -v`
Expected: All FAIL with `ImportError: cannot import name 'parse_frontmatter' from 'serve'`.

- [ ] **Step 3: Implement `parse_frontmatter` in `serve.py`**

Append to `plugin/dashboard/serve.py`:

```python
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

        # Top-level line
        key, sep, value = stripped.partition(":")
        if not sep:
            continue
        key = key.strip()
        value = value.strip()

        if value == "":
            # Mapping header (e.g. `weekly_targets:`)
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_frontmatter.py -v`
Expected: All 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add plugin/dashboard/serve.py plugin/dashboard/tests/test_frontmatter.py
git commit -m "feat(dashboard): parse_frontmatter helper (TDD)"
```

---

### Task A3: Position slug derivation (TDD)

**Files:**
- Modify: `plugin/dashboard/serve.py`
- Create: `plugin/dashboard/tests/test_slug.py`

- [ ] **Step 1: Write the failing tests**

Create `plugin/dashboard/tests/test_slug.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_slug.py -v`
Expected: All FAIL with `ImportError: cannot import name 'position_slug'`.

- [ ] **Step 3: Implement `position_slug` in `serve.py`**

Append to `plugin/dashboard/serve.py`:

```python
_SLUG_RE = re.compile(r"[^a-z0-9]+")


def position_slug(position: str) -> str:
    """Lowercase, replace runs of non-alphanumeric with a single hyphen, trim hyphens.

    "Senior PM, Consumer Credit" -> "senior-pm-consumer-credit"
    """
    lowered = position.lower()
    hyphenated = _SLUG_RE.sub("-", lowered)
    return hyphenated.strip("-")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_slug.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add plugin/dashboard/serve.py plugin/dashboard/tests/test_slug.py
git commit -m "feat(dashboard): position_slug helper (TDD)"
```

---

### Task A4: Status rewrite preserving quoting (TDD)

**Files:**
- Modify: `plugin/dashboard/serve.py`
- Create: `plugin/dashboard/tests/test_status_rewrite.py`

- [ ] **Step 1: Write the failing tests**

Create `plugin/dashboard/tests/test_status_rewrite.py`:

```python
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
    # blank line between status and tier is preserved
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
    # A `status:` line in the body should NOT be touched.
    src = dedent("""\
        ---
        status: interviewing
        ---

        Notes: status: was rejected at one point, then revived.
        """)
    out = rewrite_status(src, "applied")
    assert "status: applied" in out
    assert "status: was rejected at one point" in out
    # Sanity: only one `status: applied` (frontmatter), body kept as-is
    assert out.count("status: applied") == 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_status_rewrite.py -v`
Expected: All FAIL with `ImportError: cannot import name 'rewrite_status'`.

- [ ] **Step 3: Implement `rewrite_status` in `serve.py`**

Append to `plugin/dashboard/serve.py`:

```python
_STATUS_LINE_RE = re.compile(r"^(\s*status\s*:\s*)(\"[^\"]*\"|'[^']*'|[^\n]*)$", re.MULTILINE)


def rewrite_status(md: str, new_status: str) -> str:
    """Replace the `status:` value in the frontmatter, preserving quoting style.

    Raises ValueError if no frontmatter is present or no status line is found.
    Only the frontmatter block (between the first two `---` lines) is searched.
    """
    match = _FRONTMATTER_RE.match(md)
    if not match:
        raise ValueError("no frontmatter")
    fm_block = match.group(1)
    body = match.group(2)

    def _replace(m: re.Match[str]) -> str:
        prefix, current = m.group(1), m.group(2)
        if current.startswith('"') and current.endswith('"'):
            return f'{prefix}"{new_status}"'
        if current.startswith("'") and current.endswith("'"):
            return f"{prefix}'{new_status}'"
        return f"{prefix}{new_status}"

    new_block, count = _STATUS_LINE_RE.subn(_replace, fm_block, count=1)
    if count == 0:
        raise ValueError("no status line in frontmatter")

    return f"---\n{new_block}\n---\n{body}"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_status_rewrite.py -v`
Expected: All 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add plugin/dashboard/serve.py plugin/dashboard/tests/test_status_rewrite.py
git commit -m "feat(dashboard): rewrite_status preserves quoting + formatting (TDD)"
```

---

### Task A5: Atomic file write (TDD)

**Files:**
- Modify: `plugin/dashboard/serve.py`
- Create: `plugin/dashboard/tests/test_atomic_write.py`

- [ ] **Step 1: Write the failing tests**

Create `plugin/dashboard/tests/test_atomic_write.py`:

```python
"""Tests for atomic_write — write a file via tempfile + rename."""
from pathlib import Path

from serve import atomic_write


def test_writes_new_file(tmp_path: Path):
    target = tmp_path / "out.txt"
    atomic_write(target, "hello\n")
    assert target.read_text() == "hello\n"


def test_overwrites_existing_file(tmp_path: Path):
    target = tmp_path / "out.txt"
    target.write_text("old\n")
    atomic_write(target, "new\n")
    assert target.read_text() == "new\n"


def test_uses_same_directory_for_tempfile(tmp_path: Path):
    # rename is atomic only when source and target are on the same filesystem.
    # We approximate this by ensuring no leftover temp files in tmp_path after write.
    target = tmp_path / "out.txt"
    atomic_write(target, "data\n")
    tmp_files = [p for p in tmp_path.iterdir() if p.name != "out.txt"]
    assert tmp_files == [], f"leftover temp files: {tmp_files}"


def test_creates_parent_directory_if_missing(tmp_path: Path):
    target = tmp_path / "nested" / "out.txt"
    atomic_write(target, "x\n")
    assert target.read_text() == "x\n"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_atomic_write.py -v`
Expected: All FAIL with `ImportError`.

- [ ] **Step 3: Implement `atomic_write` in `serve.py`**

Append to `plugin/dashboard/serve.py`:

```python
import os
import tempfile
from pathlib import Path


def atomic_write(target: Path, content: str) -> None:
    """Write content to target atomically: write to temp file in same dir, then rename.

    Creates the target's parent directory if missing.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path_str = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=str(target.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path_str, target)
    except Exception:
        Path(tmp_path_str).unlink(missing_ok=True)
        raise
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_atomic_write.py -v`
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add plugin/dashboard/serve.py plugin/dashboard/tests/test_atomic_write.py
git commit -m "feat(dashboard): atomic_write helper (TDD)"
```

---

### Task A6: Company glob across flat + subfolder layouts (TDD)

**Files:**
- Modify: `plugin/dashboard/serve.py`
- Create: `plugin/dashboard/tests/test_glob_companies.py`

- [ ] **Step 1: Write the failing tests**

Create `plugin/dashboard/tests/test_glob_companies.py`:

```python
"""Tests for collect_companies — glob and parse all meta.md files into Position records."""
from pathlib import Path

from serve import collect_companies


def test_returns_one_record_per_meta_md(userdata: Path):
    positions = collect_companies(userdata)
    assert len(positions) == 3  # Plaid + Stripe×2


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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_glob_companies.py -v`
Expected: All FAIL with `ImportError`.

- [ ] **Step 3: Implement `collect_companies` in `serve.py`**

Append to `plugin/dashboard/serve.py`:

```python
from typing import Any


def collect_companies(userdata_root: Path) -> list[dict[str, Any]]:
    """Glob both flat and subfolder meta.md files; return one record per position."""
    companies_root = userdata_root / "companies"
    if not companies_root.is_dir():
        return []

    flat_files = list(companies_root.glob("*/meta.md"))
    sub_files = list(companies_root.glob("*/*/meta.md"))

    # Multi-role detection: a company is multi-role iff its companies/<Co>/ folder
    # has no flat meta.md but has 1+ subfolder meta.md files.
    multi_role_companies: set[str] = set()
    for sub_meta in sub_files:
        multi_role_companies.add(sub_meta.parent.parent.name)

    results: list[dict[str, Any]] = []

    for meta_path in flat_files:
        company_name = meta_path.parent.name
        fm, _ = parse_frontmatter(meta_path.read_text(encoding="utf-8"))
        results.append(_build_record(fm, company_name, folder_path=company_name, is_multi_role=False))

    for meta_path in sub_files:
        company_name = meta_path.parent.parent.name
        slug = meta_path.parent.name
        fm, _ = parse_frontmatter(meta_path.read_text(encoding="utf-8"))
        results.append(
            _build_record(
                fm,
                company_name,
                folder_path=f"{company_name}/{slug}",
                is_multi_role=True,
            )
        )

    return results


_OPTIONAL_FIELDS = ("score", "link", "date_added", "date_applied", "last_inbound", "monitoring")


def _build_record(
    fm: dict[str, str],
    company_name: str,
    *,
    folder_path: str,
    is_multi_role: bool,
) -> dict[str, Any]:
    position = fm.get("position", "")
    record: dict[str, Any] = {
        "company": fm.get("company", company_name),
        "position": position,
        "position_slug": position_slug(position),
        "tier": fm.get("tier", ""),
        "status": fm.get("status", ""),
        "folder_path": folder_path,
        "is_multi_role": is_multi_role,
    }
    for field in _OPTIONAL_FIELDS:
        if field in fm:
            record[field] = fm[field]
    return record
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_glob_companies.py -v`
Expected: All 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add plugin/dashboard/serve.py plugin/dashboard/tests/test_glob_companies.py
git commit -m "feat(dashboard): collect_companies handles flat + subfolder layouts (TDD)"
```

---

### Task A7: Latest daily-brief lookup (TDD)

**Files:**
- Modify: `plugin/dashboard/serve.py`
- Create: `plugin/dashboard/tests/test_latest_brief.py`

- [ ] **Step 1: Write the failing tests**

Create `plugin/dashboard/tests/test_latest_brief.py`:

```python
"""Tests for latest_brief — find the newest daily-brief-YYYY-MM-DD.md."""
from pathlib import Path

from serve import latest_brief


def test_returns_latest_by_filename_date(userdata: Path):
    # conftest writes daily-brief-2026-05-18.md
    out = latest_brief(userdata)
    assert out is not None
    assert out["date"] == "2026-05-18"
    assert out["markdown"].startswith("# Daily brief")


def test_picks_newest_when_multiple(userdata: Path):
    (userdata / "outputs" / "daily-brief-2026-05-10.md").write_text("# older\n")
    (userdata / "outputs" / "daily-brief-2026-05-20.md").write_text("# newest\n")
    out = latest_brief(userdata)
    assert out["date"] == "2026-05-20"
    assert "newest" in out["markdown"]


def test_returns_none_when_no_briefs(tmp_path: Path):
    (tmp_path / "outputs").mkdir()
    assert latest_brief(tmp_path) is None


def test_returns_none_when_outputs_dir_missing(tmp_path: Path):
    assert latest_brief(tmp_path) is None


def test_ignores_non_brief_files(userdata: Path):
    (userdata / "outputs" / "applications.md").write_text("# apps\n")
    (userdata / "outputs" / "daily-brief-bad.md").write_text("# bad name\n")
    out = latest_brief(userdata)
    assert out["date"] == "2026-05-18"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_latest_brief.py -v`
Expected: All FAIL with `ImportError`.

- [ ] **Step 3: Implement `latest_brief` in `serve.py`**

Append to `plugin/dashboard/serve.py`:

```python
_BRIEF_NAME_RE = re.compile(r"^daily-brief-(\d{4}-\d{2}-\d{2})\.md$")


def latest_brief(userdata_root: Path) -> dict[str, str] | None:
    """Return {date, markdown} for the most recent daily-brief, or None if absent."""
    outputs = userdata_root / "outputs"
    if not outputs.is_dir():
        return None
    candidates: list[tuple[str, Path]] = []
    for path in outputs.iterdir():
        m = _BRIEF_NAME_RE.match(path.name)
        if m:
            candidates.append((m.group(1), path))
    if not candidates:
        return None
    candidates.sort(key=lambda pair: pair[0], reverse=True)
    date, path = candidates[0]
    return {"date": date, "markdown": path.read_text(encoding="utf-8")}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_latest_brief.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add plugin/dashboard/serve.py plugin/dashboard/tests/test_latest_brief.py
git commit -m "feat(dashboard): latest_brief lookup (TDD)"
```

---

### Task A8: Strategy reader (TDD)

**Files:**
- Modify: `plugin/dashboard/serve.py`
- Create: `plugin/dashboard/tests/test_strategy.py`

- [ ] **Step 1: Write the failing tests**

Create `plugin/dashboard/tests/test_strategy.py`:

```python
"""Tests for read_strategy — pull target_offer_date and weekly_targets from strategy.md frontmatter."""
from pathlib import Path

from serve import read_strategy


def test_extracts_target_offer_date_and_weekly_targets(userdata: Path):
    s = read_strategy(userdata)
    assert s["target_offer_date"] == "2026-06-28"
    assert s["weekly_targets"] == {"outreach": 7, "applications": 3}


def test_returns_empty_dict_when_no_strategy_file(tmp_path: Path):
    assert read_strategy(tmp_path) == {}


def test_handles_missing_weekly_targets(tmp_path: Path):
    (tmp_path / "strategy.md").write_text("---\ntarget_offer_date: 2026-12-01\n---\n")
    s = read_strategy(tmp_path)
    assert s["target_offer_date"] == "2026-12-01"
    assert s["weekly_targets"] == {}
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_strategy.py -v`
Expected: All FAIL with `ImportError`.

- [ ] **Step 3: Implement `read_strategy` in `serve.py`**

Append to `plugin/dashboard/serve.py`:

```python
def read_strategy(userdata_root: Path) -> dict[str, Any]:
    """Read strategy.md frontmatter, returning {target_offer_date, weekly_targets}."""
    strategy_path = userdata_root / "strategy.md"
    if not strategy_path.is_file():
        return {}
    fm, _ = parse_frontmatter(strategy_path.read_text(encoding="utf-8"))
    weekly: dict[str, int] = {}
    for key, value in fm.items():
        if key.startswith("weekly_targets."):
            sub_key = key.split(".", 1)[1]
            try:
                weekly[sub_key] = int(value)
            except ValueError:
                continue
    out: dict[str, Any] = {"weekly_targets": weekly}
    if "target_offer_date" in fm:
        out["target_offer_date"] = fm["target_offer_date"]
    return out
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_strategy.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add plugin/dashboard/serve.py plugin/dashboard/tests/test_strategy.py
git commit -m "feat(dashboard): read_strategy helper (TDD)"
```

---

### Task A9: HTTP server with GET /api/state

**Files:**
- Modify: `plugin/dashboard/serve.py`
- Create: `plugin/dashboard/tests/test_http_state.py`

- [ ] **Step 1: Write the failing tests**

Create `plugin/dashboard/tests/test_http_state.py`:

```python
"""Tests for the HTTP layer — exercise the request handler via in-process invocation."""
from __future__ import annotations

import json
import threading
import urllib.request
from pathlib import Path
from typing import Iterator

import pytest

from serve import build_server


@pytest.fixture
def running_server(userdata: Path) -> Iterator[str]:
    """Start the server on a free port in a background thread; yield the base URL."""
    server, port = build_server(userdata_root=userdata, preferred_port=0, dist_dir=None)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://localhost:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def _get_json(url: str) -> dict:
    with urllib.request.urlopen(url) as r:
        return json.loads(r.read())


def test_state_endpoint_returns_companies(running_server: str):
    body = _get_json(f"{running_server}/api/state")
    companies = {p["company"] for p in body["companies"]}
    assert companies == {"Plaid", "Stripe"}


def test_state_endpoint_returns_strategy(running_server: str):
    body = _get_json(f"{running_server}/api/state")
    assert body["strategy"]["target_offer_date"] == "2026-06-28"
    assert body["strategy"]["weekly_targets"] == {"outreach": 7, "applications": 3}


def test_state_endpoint_returns_latest_brief(running_server: str):
    body = _get_json(f"{running_server}/api/state")
    assert body["latest_brief"]["date"] == "2026-05-18"


def test_state_endpoint_returns_null_brief_when_absent(running_server: str, userdata: Path):
    (userdata / "outputs" / "daily-brief-2026-05-18.md").unlink()
    body = _get_json(f"{running_server}/api/state")
    assert body["latest_brief"] is None


def test_state_endpoint_returns_userdata_root_absolute(running_server: str, userdata: Path):
    body = _get_json(f"{running_server}/api/state")
    assert body["userdata_root"] == str(userdata.resolve())
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_http_state.py -v`
Expected: All FAIL with `ImportError: cannot import name 'build_server'`.

- [ ] **Step 3: Implement `build_server` and the request handler in `serve.py`**

Append to `plugin/dashboard/serve.py`:

```python
import json as _json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from socketserver import TCPServer
from typing import Callable


def _make_handler(
    userdata_root: Path,
    dist_dir: Path | None,
) -> type[BaseHTTPRequestHandler]:
    """Build a request handler class closed over the userdata + dist paths."""

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            # Suppress default access log; tests want clean output.
            return

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/api/state":
                self._handle_state()
                return
            if dist_dir is not None:
                self._serve_static()
                return
            self._send_status(404, b"not found")

        def _handle_state(self) -> None:
            payload = {
                "companies": collect_companies(userdata_root),
                "strategy": read_strategy(userdata_root),
                "latest_brief": latest_brief(userdata_root),
                "userdata_root": str(userdata_root.resolve()),
            }
            self._send_json(200, payload)

        def _serve_static(self) -> None:
            # Map "/" to index.html; anything else to the literal path under dist_dir.
            assert dist_dir is not None
            rel = self.path.lstrip("/") or "index.html"
            file_path = (dist_dir / rel).resolve()
            try:
                file_path.relative_to(dist_dir.resolve())
            except ValueError:
                self._send_status(403, b"forbidden")
                return
            if not file_path.is_file():
                # SPA fallback: serve index.html for unknown routes
                file_path = dist_dir / "index.html"
                if not file_path.is_file():
                    self._send_status(404, b"not found")
                    return
            content = file_path.read_bytes()
            ctype = _guess_content_type(file_path.name)
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        def _send_json(self, status: int, payload: Any) -> None:
            body = _json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_status(self, status: int, body: bytes) -> None:
            self.send_response(status)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json_body(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b""
            return _json.loads(raw) if raw else {}

    return Handler


def _guess_content_type(name: str) -> str:
    if name.endswith(".html"):
        return "text/html; charset=utf-8"
    if name.endswith(".js"):
        return "application/javascript; charset=utf-8"
    if name.endswith(".css"):
        return "text/css; charset=utf-8"
    if name.endswith(".svg"):
        return "image/svg+xml"
    if name.endswith(".json"):
        return "application/json"
    return "application/octet-stream"


def build_server(
    userdata_root: Path,
    *,
    preferred_port: int,
    dist_dir: Path | None,
) -> tuple[TCPServer, int]:
    """Bind a ThreadingHTTPServer on preferred_port or next free port if preferred is busy.

    If preferred_port is 0, the OS picks any free port (used in tests).
    """
    handler_cls = _make_handler(userdata_root, dist_dir)
    if preferred_port == 0:
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler_cls)
        return server, server.server_address[1]

    last_err: OSError | None = None
    for port in range(preferred_port, preferred_port + 10):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), handler_cls)
            return server, port
        except OSError as e:
            last_err = e
            continue
    raise RuntimeError(f"no free port in {preferred_port}-{preferred_port+9}") from last_err
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_http_state.py -v`
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add plugin/dashboard/serve.py plugin/dashboard/tests/test_http_state.py
git commit -m "feat(dashboard): GET /api/state + build_server with port fallback (TDD)"
```

---

### Task A10: PATCH /api/positions/<folder_path>/status

**Files:**
- Modify: `plugin/dashboard/serve.py`
- Create: `plugin/dashboard/tests/test_http_status.py`

- [ ] **Step 1: Write the failing tests**

Create `plugin/dashboard/tests/test_http_status.py`:

```python
"""Tests for PATCH /api/positions/<folder_path>/status."""
from __future__ import annotations

import json
import threading
import urllib.request
from pathlib import Path
from typing import Iterator
from urllib.parse import quote

import pytest

from serve import build_server


@pytest.fixture
def running_server(userdata: Path) -> Iterator[tuple[str, Path]]:
    server, port = build_server(userdata_root=userdata, preferred_port=0, dist_dir=None)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://localhost:{port}", userdata
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def _patch(url: str, body: dict) -> int:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="PATCH",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def test_patches_flat_layout_company(running_server: tuple[str, Path]):
    base, root = running_server
    status = _patch(f"{base}/api/positions/Plaid/status", {"status": "rejected"})
    assert status == 200
    content = (root / "companies" / "Plaid" / "meta.md").read_text()
    assert "status: rejected" in content
    assert "company: Plaid" in content  # other fields untouched


def test_patches_subfolder_layout_company(running_server: tuple[str, Path]):
    base, root = running_server
    path = quote("Stripe/lead-pm-growth", safe="")
    status = _patch(f"{base}/api/positions/{path}/status", {"status": "interviewing"})
    assert status == 200
    content = (root / "companies" / "Stripe" / "lead-pm-growth" / "meta.md").read_text()
    assert "status: interviewing" in content


def test_returns_404_when_company_missing(running_server: tuple[str, Path]):
    base, _ = running_server
    assert _patch(f"{base}/api/positions/NonExistent/status", {"status": "applied"}) == 404


def test_returns_400_when_body_missing_status(running_server: tuple[str, Path]):
    base, _ = running_server
    assert _patch(f"{base}/api/positions/Plaid/status", {}) == 400


def test_rejects_path_traversal(running_server: tuple[str, Path]):
    base, _ = running_server
    # Encoded ../ — must not escape the companies dir.
    path = quote("../../etc", safe="")
    assert _patch(f"{base}/api/positions/{path}/status", {"status": "applied"}) == 400
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_http_status.py -v`
Expected: All FAIL — handler doesn't implement PATCH yet.

- [ ] **Step 3: Add PATCH handling to the request handler**

In `plugin/dashboard/serve.py`, find the `Handler` class. Add a `do_PATCH` method and a helper for path resolution. Modify `_make_handler` so the inner `Handler` class gets:

```python
        def do_PATCH(self) -> None:  # noqa: N802
            if self.path.startswith("/api/positions/") and self.path.endswith("/status"):
                self._handle_status_patch()
                return
            self._send_status(404, b"not found")

        def _handle_status_patch(self) -> None:
            folder_path = self.path[len("/api/positions/") : -len("/status")]
            meta_path = _resolve_meta_path(userdata_root, folder_path)
            if meta_path is None:
                self._send_status(400, b"invalid folder_path")
                return
            if not meta_path.is_file():
                self._send_status(404, b"company not found")
                return
            try:
                body = self._read_json_body()
            except _json.JSONDecodeError:
                self._send_status(400, b"invalid json")
                return
            new_status = body.get("status")
            if not isinstance(new_status, str) or not new_status:
                self._send_status(400, b"missing status")
                return
            try:
                new_md = rewrite_status(meta_path.read_text(encoding="utf-8"), new_status)
            except ValueError as e:
                self._send_status(409, str(e).encode())
                return
            atomic_write(meta_path, new_md)
            self._send_json(200, {"ok": True})
```

Also append (outside the `_make_handler` function) the path-resolution helper:

```python
from urllib.parse import unquote


def _resolve_meta_path(userdata_root: Path, folder_path: str) -> Path | None:
    """Resolve a folder_path from the URL to a meta.md path, refusing traversal."""
    decoded = unquote(folder_path)
    if not decoded or ".." in decoded.split("/") or decoded.startswith("/"):
        return None
    target = (userdata_root / "companies" / decoded / "meta.md").resolve()
    try:
        target.relative_to((userdata_root / "companies").resolve())
    except ValueError:
        return None
    return target
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_http_status.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add plugin/dashboard/serve.py plugin/dashboard/tests/test_http_status.py
git commit -m "feat(dashboard): PATCH /api/positions/.../status with path-traversal guard (TDD)"
```

---

### Task A11: POST /api/positions/<folder_path>/notes

**Files:**
- Modify: `plugin/dashboard/serve.py`
- Create: `plugin/dashboard/tests/test_http_notes.py`

- [ ] **Step 1: Write the failing tests**

Create `plugin/dashboard/tests/test_http_notes.py`:

```python
"""Tests for POST /api/positions/<folder_path>/notes."""
from __future__ import annotations

import json
import threading
import urllib.request
from pathlib import Path
from typing import Iterator

import pytest

from serve import build_server


@pytest.fixture
def running_server(userdata: Path) -> Iterator[tuple[str, Path]]:
    server, port = build_server(userdata_root=userdata, preferred_port=0, dist_dir=None)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://localhost:{port}", userdata
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def _post(url: str, body: dict) -> int:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


def test_creates_notes_md_on_first_write(running_server: tuple[str, Path]):
    base, root = running_server
    status = _post(f"{base}/api/positions/Plaid/notes", {"note": "Recruiter called."})
    assert status == 200
    notes_path = root / "companies" / "Plaid" / "notes.md"
    assert notes_path.is_file()
    content = notes_path.read_text()
    assert content.startswith("# Notes — Plaid Senior PM, Consumer Credit\n")
    assert "Recruiter called." in content
    # Heading format: ## YYYY-MM-DD HH:MM
    assert "\n## 2" in content  # starts with 2026-something


def test_appends_to_existing_notes_md(running_server: tuple[str, Path]):
    base, root = running_server
    _post(f"{base}/api/positions/Plaid/notes", {"note": "first"})
    _post(f"{base}/api/positions/Plaid/notes", {"note": "second"})
    content = (root / "companies" / "Plaid" / "notes.md").read_text()
    assert content.count("\n## 2") == 2
    assert "first" in content
    assert "second" in content


def test_writes_subfolder_layout(running_server: tuple[str, Path]):
    base, root = running_server
    from urllib.parse import quote
    path = quote("Stripe/lead-pm-growth", safe="")
    _post(f"{base}/api/positions/{path}/notes", {"note": "stripe note"})
    notes_path = root / "companies" / "Stripe" / "lead-pm-growth" / "notes.md"
    assert notes_path.is_file()
    assert "stripe note" in notes_path.read_text()


def test_returns_404_when_company_missing(running_server: tuple[str, Path]):
    base, _ = running_server
    assert _post(f"{base}/api/positions/NonExistent/notes", {"note": "x"}) == 404


def test_returns_400_when_note_missing(running_server: tuple[str, Path]):
    base, _ = running_server
    assert _post(f"{base}/api/positions/Plaid/notes", {}) == 400
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_http_notes.py -v`
Expected: All FAIL — handler doesn't implement notes POST yet.

- [ ] **Step 3: Add POST handling to the request handler**

In `plugin/dashboard/serve.py`'s `Handler` class, add `do_POST`:

```python
        def do_POST(self) -> None:  # noqa: N802
            if self.path.startswith("/api/positions/") and self.path.endswith("/notes"):
                self._handle_note_post()
                return
            self._send_status(404, b"not found")

        def _handle_note_post(self) -> None:
            folder_path = self.path[len("/api/positions/") : -len("/notes")]
            meta_path = _resolve_meta_path(userdata_root, folder_path)
            if meta_path is None:
                self._send_status(400, b"invalid folder_path")
                return
            if not meta_path.is_file():
                self._send_status(404, b"company not found")
                return
            try:
                body = self._read_json_body()
            except _json.JSONDecodeError:
                self._send_status(400, b"invalid json")
                return
            note = body.get("note")
            if not isinstance(note, str) or not note.strip():
                self._send_status(400, b"missing note")
                return
            fm, _ = parse_frontmatter(meta_path.read_text(encoding="utf-8"))
            company = fm.get("company", meta_path.parent.name)
            position = fm.get("position", "")
            append_note(meta_path.parent / "notes.md", company, position, note)
            self._send_json(200, {"ok": True})
```

Append the `append_note` helper at module scope:

```python
from datetime import datetime


def append_note(notes_path: Path, company: str, position: str, note: str) -> None:
    """Append a timestamped note to notes_path. Create with title heading on first write."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n## {timestamp}\n\n{note.strip()}\n"
    if not notes_path.exists():
        header = f"# Notes — {company} {position}\n".rstrip() + "\n"
        atomic_write(notes_path, header + entry)
        return
    atomic_write(notes_path, notes_path.read_text(encoding="utf-8") + entry)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_http_notes.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add plugin/dashboard/serve.py plugin/dashboard/tests/test_http_notes.py
git commit -m "feat(dashboard): POST /api/positions/.../notes appends to notes.md (TDD)"
```

---

### Task A12: POST /api/companies (with dedup + multi-role conflict)

**Files:**
- Modify: `plugin/dashboard/serve.py`
- Create: `plugin/dashboard/tests/test_http_new_company.py`

- [ ] **Step 1: Write the failing tests**

Create `plugin/dashboard/tests/test_http_new_company.py`:

```python
"""Tests for POST /api/companies."""
from __future__ import annotations

import json
import threading
import urllib.request
from pathlib import Path
from typing import Iterator

import pytest

from serve import build_server


@pytest.fixture
def running_server(userdata: Path) -> Iterator[tuple[str, Path]]:
    server, port = build_server(userdata_root=userdata, preferred_port=0, dist_dir=None)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://localhost:{port}", userdata
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def _post(url: str, body: dict) -> tuple[int, dict]:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_creates_new_company_flat_layout(running_server: tuple[str, Path]):
    base, root = running_server
    status, body = _post(f"{base}/api/companies", {
        "company": "Lendable",
        "position": "Senior PM, Underwriting",
        "tier": "P1",
        "link": "https://example.com/lendable",
        "status": "discovered",
    })
    assert status == 201
    assert body["folder_path"] == "Lendable"
    meta = (root / "companies" / "Lendable" / "meta.md").read_text()
    assert "company: Lendable" in meta
    assert "position: Senior PM, Underwriting" in meta
    assert "tier: P1" in meta
    assert "status: discovered" in meta
    assert "link: https://example.com/lendable" in meta
    assert "score: 0" in meta
    assert "date_added: 2" in meta  # today's year starts with 2


def test_rejects_duplicate_company_position(running_server: tuple[str, Path]):
    base, _ = running_server
    status, body = _post(f"{base}/api/companies", {
        "company": "Plaid",
        "position": "Senior PM, Consumer Credit",
        "tier": "P0",
        "link": "x",
        "status": "discovered",
    })
    assert status == 409
    assert "exists" in body["error"].lower() or "duplicate" in body["error"].lower()


def test_rejects_second_role_on_flat_layout_company(running_server: tuple[str, Path]):
    # Plaid is single-role (flat layout). Adding a SECOND position to Plaid
    # must fail with a migration-guidance message — the server does not
    # auto-migrate flat → subfolder.
    base, _ = running_server
    status, body = _post(f"{base}/api/companies", {
        "company": "Plaid",
        "position": "Lead PM, Identity",
        "tier": "P1",
        "link": "x",
        "status": "discovered",
    })
    assert status == 409
    assert "multi-role" in body["error"].lower() or "/evaluate-position" in body["error"]


def test_allows_third_role_on_existing_multi_role_company(running_server: tuple[str, Path]):
    # Stripe already has 2 roles in subfolder layout; adding a 3rd is fine.
    base, root = running_server
    status, body = _post(f"{base}/api/companies", {
        "company": "Stripe",
        "position": "Group PM, Atlas",
        "tier": "P1",
        "link": "x",
        "status": "discovered",
    })
    assert status == 201
    assert body["folder_path"] == "Stripe/group-pm-atlas"
    assert (root / "companies" / "Stripe" / "group-pm-atlas" / "meta.md").is_file()


def test_rejects_missing_required_fields(running_server: tuple[str, Path]):
    base, _ = running_server
    status, _ = _post(f"{base}/api/companies", {"company": "X"})
    assert status == 400
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_http_new_company.py -v`
Expected: All FAIL.

- [ ] **Step 3: Implement the new-company endpoint**

In `plugin/dashboard/serve.py`'s `Handler.do_POST` method, add a branch for `/api/companies`:

```python
        def do_POST(self) -> None:  # noqa: N802
            if self.path == "/api/companies":
                self._handle_new_company()
                return
            if self.path.startswith("/api/positions/") and self.path.endswith("/notes"):
                self._handle_note_post()
                return
            self._send_status(404, b"not found")

        def _handle_new_company(self) -> None:
            try:
                body = self._read_json_body()
            except _json.JSONDecodeError:
                self._send_status(400, b"invalid json")
                return
            required = ("company", "position", "tier", "link", "status")
            if not all(isinstance(body.get(k), str) and body.get(k) for k in required):
                self._send_status(400, b"missing required field")
                return
            try:
                folder_path = create_company_scaffold(
                    userdata_root,
                    company=body["company"],
                    position=body["position"],
                    tier=body["tier"],
                    link=body["link"],
                    status=body["status"],
                )
            except CompanyExistsError as e:
                self._send_json(409, {"error": str(e)})
                return
            except MultiRoleMigrationError as e:
                self._send_json(409, {"error": str(e)})
                return
            self._send_json(201, {"folder_path": folder_path})
```

Append the helpers at module scope:

```python
class CompanyExistsError(Exception):
    """Raised when (company, position) already exists."""


class MultiRoleMigrationError(Exception):
    """Raised when adding a 2nd position to a flat-layout company."""


def create_company_scaffold(
    userdata_root: Path,
    *,
    company: str,
    position: str,
    tier: str,
    link: str,
    status: str,
) -> str:
    """Create a new company/position folder + scaffolded meta.md. Returns folder_path."""
    companies_root = userdata_root / "companies"
    companies_root.mkdir(parents=True, exist_ok=True)

    co_folder = companies_root / company
    slug = position_slug(position)
    existing = collect_companies(userdata_root)
    existing_for_company = [p for p in existing if p["company"] == company]

    # Duplicate (company, position) check
    for p in existing_for_company:
        if p["position"] == position:
            raise CompanyExistsError(f"{company} / {position} already exists")

    is_existing_flat = (
        co_folder.is_dir()
        and (co_folder / "meta.md").is_file()
    )

    if is_existing_flat:
        raise MultiRoleMigrationError(
            f"{company} is single-role (flat layout). Multi-role companies need the "
            "subfolder layout. Run `/evaluate-position` for this new role — it "
            "handles the migration."
        )

    is_existing_multi = any(p["is_multi_role"] for p in existing_for_company)
    if is_existing_multi:
        target_dir = co_folder / slug
        folder_path = f"{company}/{slug}"
    else:
        # Brand-new company, default to flat layout
        target_dir = co_folder
        folder_path = company

    today = datetime.now().strftime("%Y-%m-%d")
    meta_md = (
        "---\n"
        f"company: {company}\n"
        f"status: {status}\n"
        f"tier: {tier}\n"
        "score: 0\n"
        f"position: {position}\n"
        f"link: {link}\n"
        f"date_added: {today}\n"
        "---\n"
        "\n"
        f"# {company}\n"
        "\n"
        f"(Scaffolded from dashboard on {today}. Run /evaluate-position for full scoring + research brief.)\n"
    )

    target_dir.mkdir(parents=True, exist_ok=True)
    atomic_write(target_dir / "meta.md", meta_md)
    return folder_path
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd plugin/dashboard && python3 -m pytest tests/test_http_new_company.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 5: Run the full suite**

Run: `cd plugin/dashboard && python3 -m pytest -v`
Expected: All tests PASS across all files.

- [ ] **Step 6: Commit**

```bash
git add plugin/dashboard/serve.py plugin/dashboard/tests/test_http_new_company.py
git commit -m "feat(dashboard): POST /api/companies with dedup + multi-role guard (TDD)"
```

---

### Task A13: CLI entry point with port + browser-open + SIGINT

**Files:**
- Modify: `plugin/dashboard/serve.py`

- [ ] **Step 1: Append `main()` to `serve.py`**

```python
import argparse
import signal
import sys
import webbrowser


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pm-dashboard")
    parser.add_argument("--userdata", required=True, type=Path,
                        help="Path to the workspace's userdata/ directory")
    parser.add_argument("--dist", default=None, type=Path,
                        help="Path to the built dashboard dist/ (defaults to ./dist relative to this file)")
    parser.add_argument("--port", default=7890, type=int)
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args(argv)

    userdata_root = args.userdata.expanduser().resolve()
    if not userdata_root.is_dir():
        print(f"error: userdata directory not found: {userdata_root}", file=sys.stderr)
        return 1

    dist_dir = args.dist or (Path(__file__).parent / "dist")
    dist_dir = dist_dir.expanduser().resolve()
    if not dist_dir.is_dir():
        print(
            f"error: dashboard bundle not found at {dist_dir}.\n"
            "If you're a contributor, build it first: cd plugin/dashboard && npm install && npm run build",
            file=sys.stderr,
        )
        return 1

    try:
        server, port = build_server(
            userdata_root=userdata_root,
            preferred_port=args.port,
            dist_dir=dist_dir,
        )
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    url = f"http://localhost:{port}"
    print(f"pm-job-search dashboard: {url}", flush=True)
    print("Press ctrl-C to stop.", flush=True)

    if not args.no_open:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    def _handle_sigint(_signum: int, _frame: Any) -> None:
        print("\nshutting down...", flush=True)
        server.shutdown()

    signal.signal(signal.SIGINT, _handle_sigint)
    try:
        server.serve_forever()
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Smoke-test the CLI manually**

Run: `cd plugin/dashboard && python3 serve.py --userdata ../../userdata/examples/maya --no-open --port 7890`
Expected: Prints `pm-job-search dashboard: http://localhost:7890` and waits. Ctrl-C exits cleanly with `shutting down...`.

If `plugin/dashboard/dist/` doesn't exist yet (Slice B hasn't built it), the smoke test will exit 1 with the missing-bundle error. That's correct behaviour — re-run after Slice B / Slice F has produced `dist/`.

- [ ] **Step 3: Commit**

```bash
git add plugin/dashboard/serve.py
git commit -m "feat(dashboard): main() entry point with port fallback + SIGINT cleanup"
```

---

## Slice B — Vite + Mantine app shell

### Task B1: package.json + npm install

**Files:**
- Create: `plugin/dashboard/package.json`
- Create: `plugin/dashboard/.gitignore`

- [ ] **Step 1: Write `plugin/dashboard/package.json`**

```json
{
  "name": "pm-job-search-dashboard",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@mantine/core": "^7.13.0",
    "@mantine/hooks": "^7.13.0",
    "@tabler/icons-react": "^3.21.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-markdown": "^9.0.1",
    "remark-gfm": "^4.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.3",
    "typescript": "^5.6.3",
    "vite": "^5.4.10"
  }
}
```

- [ ] **Step 2: Write `plugin/dashboard/.gitignore`**

```
node_modules/
*.log
.DS_Store
```

Note: `dist/` is intentionally NOT ignored — it must be committed.

- [ ] **Step 3: Run npm install**

Run: `cd plugin/dashboard && npm install`
Expected: `node_modules/` and `package-lock.json` appear; no errors.

- [ ] **Step 4: Commit**

```bash
git add plugin/dashboard/package.json plugin/dashboard/package-lock.json plugin/dashboard/.gitignore
git commit -m "feat(dashboard): package.json with Mantine + Vite + React"
```

---

### Task B2: vite.config.ts + tsconfig.json + index.html

**Files:**
- Create: `plugin/dashboard/vite.config.ts`
- Create: `plugin/dashboard/tsconfig.json`
- Create: `plugin/dashboard/tsconfig.node.json`
- Create: `plugin/dashboard/index.html`

- [ ] **Step 1: Write `plugin/dashboard/vite.config.ts`**

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": "http://localhost:7890",
    },
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
    target: "es2020",
  },
});
```

- [ ] **Step 2: Write `plugin/dashboard/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

- [ ] **Step 3: Write `plugin/dashboard/tsconfig.node.json`**

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true,
    "strict": true
  },
  "include": ["vite.config.ts"]
}
```

- [ ] **Step 4: Write `plugin/dashboard/index.html`**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>pm-job-search dashboard</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

- [ ] **Step 5: Commit**

```bash
git add plugin/dashboard/vite.config.ts plugin/dashboard/tsconfig.json plugin/dashboard/tsconfig.node.json plugin/dashboard/index.html
git commit -m "feat(dashboard): vite + tsconfig + index.html"
```

---

### Task B3: Types matching the API contract

**Files:**
- Create: `plugin/dashboard/src/types.ts`

- [ ] **Step 1: Write `plugin/dashboard/src/types.ts`**

```typescript
export type Status =
  | "discovered"
  | "applied"
  | "interviewing"
  | "offer-received"
  | "rejected"
  | "withdrew"
  | "paused";

export type Tier = "P0" | "P1" | "P2" | "P3";

export interface Position {
  company: string;
  position: string;
  position_slug: string;
  tier: Tier | string;
  status: Status | string;
  folder_path: string;
  is_multi_role: boolean;
  score?: string;
  link?: string;
  date_added?: string;
  date_applied?: string;
  last_inbound?: string;
  monitoring?: string;
}

export interface WeeklyTargets {
  [key: string]: number;
}

export interface Strategy {
  target_offer_date?: string;
  weekly_targets: WeeklyTargets;
}

export interface DailyBrief {
  date: string;
  markdown: string;
}

export interface DashboardState {
  companies: Position[];
  strategy: Strategy;
  latest_brief: DailyBrief | null;
  userdata_root: string;
}

export interface NewCompanyPayload {
  company: string;
  position: string;
  tier: string;
  link: string;
  status: string;
}
```

- [ ] **Step 2: Commit**

```bash
git add plugin/dashboard/src/types.ts
git commit -m "feat(dashboard): API contract types"
```

---

### Task B4: Typed fetch wrappers

**Files:**
- Create: `plugin/dashboard/src/api.ts`

- [ ] **Step 1: Write `plugin/dashboard/src/api.ts`**

```typescript
import type { DashboardState, NewCompanyPayload } from "./types";

async function jsonOrThrow<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = "";
    try {
      const body = await res.json();
      detail = typeof body?.error === "string" ? body.error : "";
    } catch {
      detail = await res.text().catch(() => "");
    }
    throw new ApiError(res.status, detail || res.statusText);
  }
  return res.json();
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

export async function fetchState(): Promise<DashboardState> {
  const res = await fetch("/api/state");
  return jsonOrThrow<DashboardState>(res);
}

export async function patchStatus(folderPath: string, status: string): Promise<void> {
  const res = await fetch(`/api/positions/${encodeURIComponent(folderPath)}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  await jsonOrThrow<{ ok: true }>(res);
}

export async function postNote(folderPath: string, note: string): Promise<void> {
  const res = await fetch(`/api/positions/${encodeURIComponent(folderPath)}/notes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ note }),
  });
  await jsonOrThrow<{ ok: true }>(res);
}

export async function postCompany(payload: NewCompanyPayload): Promise<{ folder_path: string }> {
  const res = await fetch("/api/companies", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return jsonOrThrow<{ folder_path: string }>(res);
}
```

- [ ] **Step 2: Commit**

```bash
git add plugin/dashboard/src/api.ts
git commit -m "feat(dashboard): typed fetch wrappers for the REST API"
```

---

### Task B5: main.tsx — MantineProvider, dark scheme

**Files:**
- Create: `plugin/dashboard/src/main.tsx`

- [ ] **Step 1: Write `plugin/dashboard/src/main.tsx`**

```typescript
import "@mantine/core/styles.css";

import { MantineProvider, createTheme } from "@mantine/core";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { App } from "./App";

const theme = createTheme({});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MantineProvider theme={theme} defaultColorScheme="dark">
      <App />
    </MantineProvider>
  </StrictMode>,
);
```

- [ ] **Step 2: Commit**

```bash
git add plugin/dashboard/src/main.tsx
git commit -m "feat(dashboard): main.tsx with Mantine provider, dark scheme"
```

---

### Task B6: App.tsx — three-zone shell with data fetch

**Files:**
- Create: `plugin/dashboard/src/App.tsx`
- Create: `plugin/dashboard/src/components/PipelineStats.tsx` (placeholder)
- Create: `plugin/dashboard/src/components/ApplicationsTable.tsx` (placeholder)
- Create: `plugin/dashboard/src/components/TodaySection.tsx` (placeholder)

- [ ] **Step 1: Write placeholder components**

`plugin/dashboard/src/components/PipelineStats.tsx`:

```typescript
import { Paper, Text } from "@mantine/core";
import type { Position, Strategy } from "../types";

interface Props {
  companies: Position[];
  strategy: Strategy;
}

export function PipelineStats({ companies, strategy: _strategy }: Props) {
  return (
    <Paper p="md" withBorder>
      <Text>PipelineStats placeholder — {companies.length} companies</Text>
    </Paper>
  );
}
```

`plugin/dashboard/src/components/ApplicationsTable.tsx`:

```typescript
import { Paper, Text } from "@mantine/core";
import type { Position } from "../types";

interface Props {
  companies: Position[];
  userdataRoot: string;
  onChange: () => void;
}

export function ApplicationsTable({ companies, userdataRoot: _userdataRoot, onChange: _onChange }: Props) {
  return (
    <Paper p="md" withBorder>
      <Text>ApplicationsTable placeholder — {companies.length} positions</Text>
    </Paper>
  );
}
```

`plugin/dashboard/src/components/TodaySection.tsx`:

```typescript
import { Paper, Text } from "@mantine/core";
import type { DailyBrief } from "../types";

interface Props {
  brief: DailyBrief | null;
}

export function TodaySection({ brief }: Props) {
  return (
    <Paper p="md" withBorder>
      <Text>TodaySection placeholder — brief {brief ? brief.date : "absent"}</Text>
    </Paper>
  );
}
```

- [ ] **Step 2: Write `plugin/dashboard/src/App.tsx`**

```typescript
import { Alert, Container, Loader, Stack } from "@mantine/core";
import { useCallback, useEffect, useState } from "react";

import { fetchState } from "./api";
import { ApplicationsTable } from "./components/ApplicationsTable";
import { PipelineStats } from "./components/PipelineStats";
import { TodaySection } from "./components/TodaySection";
import type { DashboardState } from "./types";

export function App() {
  const [state, setState] = useState<DashboardState | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const next = await fetchState();
      setState(next);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "unknown error");
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  if (error) {
    return (
      <Container size="lg" py="md">
        <Alert color="red" title="Failed to load dashboard state">{error}</Alert>
      </Container>
    );
  }
  if (!state) {
    return (
      <Container size="lg" py="md">
        <Loader />
      </Container>
    );
  }

  return (
    <Container size="lg" py="md">
      <Stack gap="md">
        <PipelineStats companies={state.companies} strategy={state.strategy} />
        <ApplicationsTable
          companies={state.companies}
          userdataRoot={state.userdata_root}
          onChange={refresh}
        />
        <TodaySection brief={state.latest_brief} />
      </Stack>
    </Container>
  );
}
```

- [ ] **Step 3: Verify the shell builds**

Run: `cd plugin/dashboard && npm run build`
Expected: TypeScript compiles, Vite produces `dist/index.html` + `dist/assets/`. No errors.

- [ ] **Step 4: Commit**

```bash
git add plugin/dashboard/src/
git commit -m "feat(dashboard): three-zone shell with placeholder components + data fetch"
```

---

## Slice C — Table + writes UI

### Task C1: ApplicationsTable — grouped accordion with toggle

**Files:**
- Modify: `plugin/dashboard/src/components/ApplicationsTable.tsx`
- Create: `plugin/dashboard/src/components/StatusSelect.tsx`
- Create: `plugin/dashboard/src/components/NoteDrawer.tsx`
- Create: `plugin/dashboard/src/components/NewCompanyModal.tsx`

This task wires the structural skeleton — segmented control, accordion groups, and table rows. The interactive cells (StatusSelect, action icons) get filled in via tasks C2–C4 against this same file.

- [ ] **Step 1: Write `plugin/dashboard/src/components/StatusSelect.tsx`** (used in C2 but co-created here for type-import simplicity)

```typescript
import { Select } from "@mantine/core";
import { useState } from "react";

import { patchStatus } from "../api";

const STATUS_OPTIONS = [
  "discovered",
  "applied",
  "interviewing",
  "offer-received",
  "rejected",
  "withdrew",
  "paused",
];

interface Props {
  folderPath: string;
  current: string;
  onChange: () => void;
}

export function StatusSelect({ folderPath, current, onChange }: Props) {
  const [saving, setSaving] = useState(false);
  const [value, setValue] = useState(current);

  return (
    <Select
      size="xs"
      data={STATUS_OPTIONS}
      value={value}
      disabled={saving}
      onChange={async (next) => {
        if (!next || next === value) return;
        setSaving(true);
        setValue(next);
        try {
          await patchStatus(folderPath, next);
          onChange();
        } catch (e) {
          setValue(current);
          alert(`Failed to update status: ${e instanceof Error ? e.message : String(e)}`);
        } finally {
          setSaving(false);
        }
      }}
    />
  );
}
```

- [ ] **Step 2: Write `plugin/dashboard/src/components/NoteDrawer.tsx`**

```typescript
import { Button, Drawer, Stack, Text, Textarea } from "@mantine/core";
import { useState } from "react";

import { postNote } from "../api";

interface Props {
  opened: boolean;
  onClose: () => void;
  folderPath: string;
  company: string;
  position: string;
}

export function NoteDrawer({ opened, onClose, folderPath, company, position }: Props) {
  const [note, setNote] = useState("");
  const [saving, setSaving] = useState(false);

  const submit = async () => {
    if (!note.trim()) return;
    setSaving(true);
    try {
      await postNote(folderPath, note);
      setNote("");
      onClose();
    } catch (e) {
      alert(`Failed to add note: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <Drawer
      opened={opened}
      onClose={onClose}
      title={`Note — ${company} · ${position}`}
      position="right"
      size="md"
    >
      <Stack>
        <Text size="sm" c="dimmed">
          Appended to notes.md alongside this position's meta.md with a timestamp.
        </Text>
        <Textarea
          autosize
          minRows={6}
          placeholder="What happened?"
          value={note}
          onChange={(e) => setNote(e.currentTarget.value)}
        />
        <Button loading={saving} onClick={submit}>Save note</Button>
      </Stack>
    </Drawer>
  );
}
```

- [ ] **Step 3: Write `plugin/dashboard/src/components/NewCompanyModal.tsx`**

```typescript
import { Alert, Button, Modal, Select, Stack, TextInput } from "@mantine/core";
import { useState } from "react";

import { ApiError, postCompany } from "../api";

const STATUS_OPTIONS = [
  "discovered",
  "applied",
  "interviewing",
];

const TIER_OPTIONS = ["P0", "P1", "P2", "P3"];

interface Props {
  opened: boolean;
  onClose: () => void;
  onCreated: () => void;
}

export function NewCompanyModal({ opened, onClose, onCreated }: Props) {
  const [company, setCompany] = useState("");
  const [position, setPosition] = useState("");
  const [tier, setTier] = useState<string>("P1");
  const [link, setLink] = useState("");
  const [status, setStatus] = useState<string>("discovered");
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  const reset = () => {
    setCompany("");
    setPosition("");
    setTier("P1");
    setLink("");
    setStatus("discovered");
    setError(null);
  };

  const submit = async () => {
    setError(null);
    if (!company.trim() || !position.trim() || !link.trim()) {
      setError("Company, position, and link are required.");
      return;
    }
    setSaving(true);
    try {
      await postCompany({ company, position, tier, link, status });
      reset();
      onCreated();
      onClose();
    } catch (e) {
      if (e instanceof ApiError && e.status === 409) {
        setError(e.message);
      } else {
        setError(e instanceof Error ? e.message : "Failed to create company");
      }
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal opened={opened} onClose={onClose} title="Add company" centered>
      <Stack>
        <TextInput label="Company" value={company} onChange={(e) => setCompany(e.currentTarget.value)} required />
        <TextInput label="Position" value={position} onChange={(e) => setPosition(e.currentTarget.value)} required />
        <Select label="Tier" data={TIER_OPTIONS} value={tier} onChange={(v) => v && setTier(v)} />
        <TextInput label="Link" value={link} onChange={(e) => setLink(e.currentTarget.value)} required />
        <Select label="Status" data={STATUS_OPTIONS} value={status} onChange={(v) => v && setStatus(v)} />
        {error && <Alert color="red">{error}</Alert>}
        <Button loading={saving} onClick={submit}>Create</Button>
      </Stack>
    </Modal>
  );
}
```

- [ ] **Step 4: Rewrite `plugin/dashboard/src/components/ApplicationsTable.tsx`**

```typescript
import {
  Accordion,
  ActionIcon,
  Badge,
  Button,
  Group,
  SegmentedControl,
  Stack,
  Table,
  Text,
} from "@mantine/core";
import { IconCopy, IconExternalLink, IconNote, IconPlus } from "@tabler/icons-react";
import { useMemo, useState } from "react";

import type { Position } from "../types";
import { NewCompanyModal } from "./NewCompanyModal";
import { NoteDrawer } from "./NoteDrawer";
import { StatusSelect } from "./StatusSelect";

type GroupKey = "Status" | "Tier";

interface Props {
  companies: Position[];
  userdataRoot: string;
  onChange: () => void;
}

const TIER_COLORS: Record<string, string> = {
  P0: "red",
  P1: "orange",
  P2: "gray",
  P3: "gray",
};

export function ApplicationsTable({ companies, userdataRoot, onChange }: Props) {
  const [groupBy, setGroupBy] = useState<GroupKey>("Status");
  const [modalOpen, setModalOpen] = useState(false);
  const [notePosition, setNotePosition] = useState<Position | null>(null);

  const groups = useMemo(() => buildGroups(companies, groupBy), [companies, groupBy]);

  return (
    <Stack gap="md">
      <Group justify="space-between">
        <SegmentedControl
          data={["Status", "Tier"]}
          value={groupBy}
          onChange={(v) => setGroupBy(v as GroupKey)}
        />
        <Button leftSection={<IconPlus size={16} />} onClick={() => setModalOpen(true)}>
          New company
        </Button>
      </Group>

      <Accordion multiple defaultValue={groups.map((g) => g.key)}>
        {groups.map((group) => (
          <Accordion.Item key={group.key} value={group.key}>
            <Accordion.Control>
              <Group gap="sm">
                <Text fw={600}>{group.label}</Text>
                <Badge variant="light">{group.rows.length}</Badge>
              </Group>
            </Accordion.Control>
            <Accordion.Panel>
              <Table striped highlightOnHover verticalSpacing="xs">
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Tier</Table.Th>
                    <Table.Th>Company</Table.Th>
                    <Table.Th>Position</Table.Th>
                    <Table.Th>Status</Table.Th>
                    <Table.Th>Last activity</Table.Th>
                    <Table.Th />
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {group.rows.map((p) => (
                    <Table.Tr key={p.folder_path}>
                      <Table.Td>
                        <Badge color={TIER_COLORS[p.tier] ?? "gray"}>{p.tier}</Badge>
                      </Table.Td>
                      <Table.Td>
                        <Text fw={600}>{p.company}</Text>
                      </Table.Td>
                      <Table.Td>{p.position}</Table.Td>
                      <Table.Td>
                        <StatusSelect
                          folderPath={p.folder_path}
                          current={p.status}
                          onChange={onChange}
                        />
                      </Table.Td>
                      <Table.Td>
                        <Text size="xs" c="dimmed">{relativeDate(p.last_inbound ?? p.date_applied ?? p.date_added)}</Text>
                      </Table.Td>
                      <Table.Td>
                        <Group gap={4}>
                          <ActionIcon variant="subtle" aria-label="Add note" onClick={() => setNotePosition(p)}>
                            <IconNote size={16} />
                          </ActionIcon>
                          <ActionIcon
                            variant="subtle"
                            component="a"
                            href={`vscode://file/${absolutePath(userdataRoot, p.folder_path)}`}
                            aria-label="Open in VS Code"
                            title="Open in VS Code"
                          >
                            <IconExternalLink size={16} />
                          </ActionIcon>
                          <ActionIcon
                            variant="subtle"
                            aria-label="Copy meta.md path"
                            title="Copy meta.md path"
                            onClick={() => {
                              void navigator.clipboard.writeText(absolutePath(userdataRoot, p.folder_path));
                            }}
                          >
                            <IconCopy size={16} />
                          </ActionIcon>
                        </Group>
                      </Table.Td>
                    </Table.Tr>
                  ))}
                </Table.Tbody>
              </Table>
            </Accordion.Panel>
          </Accordion.Item>
        ))}
      </Accordion>

      <NewCompanyModal
        opened={modalOpen}
        onClose={() => setModalOpen(false)}
        onCreated={onChange}
      />
      <NoteDrawer
        opened={notePosition !== null}
        onClose={() => setNotePosition(null)}
        folderPath={notePosition?.folder_path ?? ""}
        company={notePosition?.company ?? ""}
        position={notePosition?.position ?? ""}
      />
    </Stack>
  );
}

interface GroupBucket {
  key: string;
  label: string;
  rows: Position[];
}

const STATUS_ORDER = [
  "interviewing",
  "applied",
  "discovered",
  "offer-received",
  "paused",
  "withdrew",
  "rejected",
];
const TIER_ORDER = ["P0", "P1", "P2", "P3"];

function buildGroups(rows: Position[], groupBy: GroupKey): GroupBucket[] {
  const buckets = new Map<string, Position[]>();
  for (const row of rows) {
    const key = groupBy === "Status" ? row.status : row.tier;
    if (!buckets.has(key)) buckets.set(key, []);
    buckets.get(key)!.push(row);
  }
  const order = groupBy === "Status" ? STATUS_ORDER : TIER_ORDER;
  const ordered: GroupBucket[] = [];
  for (const key of order) {
    if (buckets.has(key)) {
      ordered.push({ key, label: key, rows: buckets.get(key)! });
      buckets.delete(key);
    }
  }
  // Anything else (unknown status/tier) appended
  for (const [key, value] of buckets.entries()) {
    ordered.push({ key, label: key, rows: value });
  }
  return ordered;
}

function relativeDate(iso: string | undefined): string {
  if (!iso) return "—";
  const then = Date.parse(iso);
  if (Number.isNaN(then)) return iso;
  const days = Math.floor((Date.now() - then) / (24 * 60 * 60 * 1000));
  if (days < 1) return "today";
  if (days < 2) return "1d";
  if (days < 7) return `${days}d`;
  if (days < 14) return "1w";
  if (days < 60) return `${Math.floor(days / 7)}w`;
  return `${Math.floor(days / 30)}mo`;
}

function absolutePath(userdataRoot: string, folderPath: string): string {
  // userdataRoot comes from /api/state and is the server-resolved absolute path
  // to userdata/. vscode://file/ requires absolute paths to open files reliably.
  return `${userdataRoot}/companies/${folderPath}/meta.md`;
}
```

- [ ] **Step 5: Verify the build still passes**

Run: `cd plugin/dashboard && npm run build`
Expected: TypeScript compiles cleanly, Vite produces `dist/`.

- [ ] **Step 6: Commit**

```bash
git add plugin/dashboard/src/components/
git commit -m "feat(dashboard): table grouping + status select + note drawer + new-company modal"
```

---

## Slice D — Top + bottom zones

### Task D1: PipelineStats — counts + weekly progress + countdown

**Files:**
- Modify: `plugin/dashboard/src/components/PipelineStats.tsx`

- [ ] **Step 1: Rewrite `plugin/dashboard/src/components/PipelineStats.tsx`**

```typescript
import { Group, Paper, Progress, Stack, Text } from "@mantine/core";
import { useMemo } from "react";

import type { Position, Strategy } from "../types";

interface Props {
  companies: Position[];
  strategy: Strategy;
}

const ACTIVE_STATUSES = ["interviewing", "applied", "discovered"];

export function PipelineStats({ companies, strategy }: Props) {
  const counts = useMemo(() => {
    const out = new Map<string, number>();
    for (const status of ACTIVE_STATUSES) out.set(status, 0);
    for (const p of companies) {
      if (out.has(p.status)) out.set(p.status, out.get(p.status)! + 1);
    }
    return out;
  }, [companies]);

  const weeklyBar = useMemo(() => buildWeeklyBar(companies, strategy), [companies, strategy]);
  const countdown = useMemo(() => buildCountdown(strategy.target_offer_date), [strategy.target_offer_date]);

  return (
    <Paper p="md" withBorder>
      <Group justify="space-between" wrap="wrap" gap="xl">
        <Group gap="xl">
          {ACTIVE_STATUSES.map((status) => (
            <Stack gap={2} key={status}>
              <Text fz="xl" fw={700}>{counts.get(status) ?? 0}</Text>
              <Text fz="xs" c="dimmed" tt="uppercase">{status}</Text>
            </Stack>
          ))}
        </Group>
        <Group gap="xl">
          {weeklyBar && (
            <Stack gap={4} w={160}>
              <Text fz="xs" c="dimmed" tt="uppercase">{weeklyBar.label} this week</Text>
              <Text fz="lg" fw={600}>{weeklyBar.count} / {weeklyBar.target}</Text>
              <Progress value={Math.min(100, (weeklyBar.count / weeklyBar.target) * 100)} />
            </Stack>
          )}
          {countdown && (
            <Stack gap={2}>
              <Text fz="xl" fw={700}>{countdown.days}d</Text>
              <Text fz="xs" c="dimmed" tt="uppercase">to target offer</Text>
              <Text fz="xs" c="dimmed">{countdown.date}</Text>
            </Stack>
          )}
        </Group>
      </Group>
    </Paper>
  );
}

interface WeeklyBar {
  label: string;
  count: number;
  target: number;
}

function buildWeeklyBar(companies: Position[], strategy: Strategy): WeeklyBar | null {
  const targets = strategy.weekly_targets;
  if (!targets || Object.keys(targets).length === 0) return null;

  // Largest target wins the bar slot
  const [label, target] = Object.entries(targets).reduce((best, cur) =>
    cur[1] > best[1] ? cur : best,
  );

  const dateField = label === "applications" ? "date_applied" : "date_added";
  const start = startOfIsoWeek(new Date());
  const count = companies.filter((p) => {
    const value = p[dateField as keyof Position] as string | undefined;
    if (!value) return false;
    const t = Date.parse(value);
    return !Number.isNaN(t) && t >= start.getTime();
  }).length;

  return { label, count, target };
}

function buildCountdown(targetDate: string | undefined): { days: number; date: string } | null {
  if (!targetDate) return null;
  const t = Date.parse(targetDate);
  if (Number.isNaN(t)) return null;
  const days = Math.max(0, Math.ceil((t - Date.now()) / (24 * 60 * 60 * 1000)));
  return { days, date: targetDate };
}

function startOfIsoWeek(now: Date): Date {
  // ISO weeks start on Monday
  const d = new Date(now);
  const day = d.getDay() || 7; // Sun=0 -> 7
  d.setHours(0, 0, 0, 0);
  d.setDate(d.getDate() - (day - 1));
  return d;
}
```

- [ ] **Step 2: Build and verify**

Run: `cd plugin/dashboard && npm run build`
Expected: Compiles cleanly.

- [ ] **Step 3: Commit**

```bash
git add plugin/dashboard/src/components/PipelineStats.tsx
git commit -m "feat(dashboard): PipelineStats with counts + weekly bar + offer countdown"
```

---

### Task D2: TodaySection — markdown render + stale + empty states

**Files:**
- Modify: `plugin/dashboard/src/components/TodaySection.tsx`

- [ ] **Step 1: Rewrite `plugin/dashboard/src/components/TodaySection.tsx`**

```typescript
import { Alert, Paper, Stack, Text, TypographyStylesProvider } from "@mantine/core";
import { useMemo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type { DailyBrief } from "../types";

interface Props {
  brief: DailyBrief | null;
}

export function TodaySection({ brief }: Props) {
  const today = useMemo(() => new Date().toISOString().slice(0, 10), []);
  const isStale = brief !== null && brief.date < today;

  if (brief === null) {
    return (
      <Paper p="md" withBorder>
        <Text c="dimmed">No daily brief yet — run <Text component="code">/today</Text>.</Text>
      </Paper>
    );
  }

  return (
    <Paper p="md" withBorder>
      <Stack gap="sm">
        <Text fz="sm" c="dimmed" tt="uppercase">
          Today — from daily-brief-{brief.date}.md
        </Text>
        {isStale && (
          <Alert color="yellow">
            Last brief from {brief.date} — run <Text component="code">/today</Text> to refresh.
          </Alert>
        )}
        <TypographyStylesProvider>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{brief.markdown}</ReactMarkdown>
        </TypographyStylesProvider>
      </Stack>
    </Paper>
  );
}
```

- [ ] **Step 2: Build and verify**

Run: `cd plugin/dashboard && npm run build`
Expected: Compiles cleanly.

- [ ] **Step 3: Commit**

```bash
git add plugin/dashboard/src/components/TodaySection.tsx
git commit -m "feat(dashboard): TodaySection renders brief markdown + stale alert + empty state"
```

---

## Slice E — /dashboard SKILL.md

### Task E1: Write the skill spec

**Files:**
- Create: `plugin/skills/dashboard/SKILL.md`

- [ ] **Step 1: Inspect existing skill format**

Run: `ls plugin/skills/ && head -40 plugin/skills/today/SKILL.md`
Expected: lists the existing skills + shows the SKILL.md frontmatter convention.

- [ ] **Step 2: Write `plugin/skills/dashboard/SKILL.md`**

```markdown
---
name: dashboard
description: This skill should be used when the user asks to "/dashboard", "open the dashboard", "show me my pipeline visually", "launch the dashboard", or wants a browser-based view of their job-search pipeline. Launches a local Python server that serves a React + Mantine SPA reading from `userdata/companies/*/meta.md`, `userdata/strategy.md`, and the latest `userdata/outputs/daily-brief-*.md`. Supports inline status changes, timestamped notes per company, and scaffolding a new company entry. The dashboard reads and writes the same md files all other skills use — markdown remains the source of truth.
---

# /dashboard

Launches the pm-job-search visual dashboard.

## What it does

1. Starts a local Python server (`plugin/dashboard/serve.py`) on port 7890 (or the next free port up to 7900).
2. Opens the user's default browser to `http://localhost:<port>`.
3. Prints the URL to chat so the user can copy it if auto-open fails.
4. Waits in the foreground until the user hits ctrl-C.

The dashboard provides:
- A top status bar showing pipeline counts, weekly progress vs `strategy.md` targets, and days-to-target-offer countdown.
- A grouped applications table (toggle Status / Tier) with inline status dropdowns and per-row "add note" / "open in editor" actions.
- A "+ New company" button that scaffolds a folder + `meta.md` for a fresh company-position pair.
- A bottom panel rendering the latest `daily-brief-*.md` (with a stale-brief banner when older than today).

## When to invoke

- User types `/dashboard`.
- User asks to "open the dashboard", "show me my pipeline", "launch the visual view".
- User wants to do bulk pipeline maintenance (status sweeps, quick notes against several companies).

## How to invoke

The skill runs one shell command:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/dashboard/serve.py" --userdata "$(pwd)/userdata"
```

`${CLAUDE_PLUGIN_ROOT}` resolves to the plugin install directory. `$(pwd)` resolves to the user's workspace root (the dir containing `userdata/`).

If the user is running this from somewhere other than their workspace root, ask for the workspace path and pass it explicitly: `--userdata <path>/userdata`.

## Failure modes and what to do

- **Bundle missing** (`error: dashboard bundle not found`). The plugin's `dist/` is not committed or got deleted. Tell the user to reinstall the plugin; this should not happen in a clean install.
- **Port range exhausted** (`error: no free port in 7890-7899`). Something else is using all ten ports. Suggest `--port 7900` (or higher) explicitly.
- **userdata not found**. The user is in the wrong directory. Ask for the workspace path.

## What this skill does NOT do

- Does not modify md files itself — all writes go through the dashboard's REST API, which uses atomic file writes.
- Does not run `/today`, `/evaluate-position`, or any other skill. The dashboard renders the latest brief; it doesn't recompute it.
- Does not handle authentication, multi-user, or remote access. Local-only.
- Does not add Python dependencies. Server uses stdlib only.

## Tone

Match plugin/TONE.md: low-effort, terse, no marketing voice. When announcing the URL, say it once and stop talking.
```

- [ ] **Step 3: Commit**

```bash
git add plugin/skills/dashboard/SKILL.md
git commit -m "feat(dashboard): /dashboard skill spec"
```

---

## Slice F — Docs, privacy, CI, build, commit dist/

### Task F1: Build dist/ and commit it

**Files:**
- Create: `plugin/dashboard/dist/` (committed Vite build output)

- [ ] **Step 1: Verify all prior slices are merged**

Run: `git log --oneline -20`
Expected: commits from Slices A, B, C, D, E are all present.

- [ ] **Step 2: Run the build**

Run: `cd plugin/dashboard && npm install && npm run build`
Expected: `dist/index.html` + `dist/assets/*.js` + `dist/assets/*.css` produced; no errors.

- [ ] **Step 3: Inspect bundle size**

Run: `du -sh plugin/dashboard/dist/`
Expected: under 2MB uncompressed (~500KB gzipped). If materially larger, note it for follow-up but do not block the commit.

- [ ] **Step 4: Commit the bundle**

```bash
git add plugin/dashboard/dist/
git commit -m "feat(dashboard): commit Vite-built bundle to dist/"
```

---

### Task F2: README + plugin/README updates

**Files:**
- Modify: `README.md`
- Modify: `plugin/README.md`

- [ ] **Step 1: Inspect existing skills table**

Run: `grep -n -A 3 -B 1 "today" README.md plugin/README.md | head -40`
Expected: locates the skills table or list in both READMEs.

- [ ] **Step 2: Add `/dashboard` to the skills list/table in both files**

In each README, find the section that lists skills (e.g. a table or bullet list including `/today`, `/evaluate-position`, etc.). Add a row/bullet:

```
| `/dashboard` | Visual dashboard — pipeline view, inline status changes, quick notes, new-company scaffold. |
```

(Adapt the syntax to whatever table format the existing README uses.)

- [ ] **Step 3: Add a "Visual dashboard" sub-section under "How it works" in both READMEs**

```markdown
### Visual dashboard

Run `/dashboard` to open a browser view of your pipeline. The dashboard reads
the same md files all other skills use (`userdata/companies/*/meta.md`,
`userdata/strategy.md`, latest `userdata/outputs/daily-brief-*.md`) and can
write three things back: status changes, timestamped notes (`notes.md` per
company), and scaffolded `meta.md` for a brand-new company-position pair.

Built with React + Mantine. The bundle is pre-built and committed — you
install zero additional dependencies. Stops on ctrl-C.
```

- [ ] **Step 4: Commit**

```bash
git add README.md plugin/README.md
git commit -m "docs: README mentions /dashboard skill + visual dashboard section"
```

---

### Task F3: CONTRIBUTING.md — modifying the dashboard

**Files:**
- Modify: `CONTRIBUTING.md`

- [ ] **Step 1: Add a "Modifying the dashboard" section**

Append the following section to `CONTRIBUTING.md` (place it before the "Commit conventions" section if one exists):

```markdown
## Modifying the dashboard

The visual dashboard at `plugin/dashboard/` is a React + Mantine + Vite app. Its
built output (`plugin/dashboard/dist/`) is **committed** to this repo so plugin
users install zero JS dependencies. When you modify dashboard source, you MUST
rebuild and commit `dist/` in the same PR.

```bash
cd plugin/dashboard
npm install            # one-time per fresh checkout
npm run build          # produces dist/
cd ../..
git add plugin/dashboard/src/ plugin/dashboard/dist/
git commit -m "feat(dashboard): <what you changed>"
```

Contributors need Node 20+ (any modern LTS). The `dashboard-build-check` CI
workflow will fail if `dist/` is out of date relative to `src/`.

### Running the Python tests

```bash
cd plugin/dashboard
pip install -r requirements-dev.txt  # one-time, in a venv if you prefer
python3 -m pytest -v
```

### Running the dashboard locally

```bash
python3 plugin/dashboard/serve.py --userdata <path-to-userdata>
```
```

- [ ] **Step 2: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "docs: CONTRIBUTING — modifying the dashboard"
```

---

### Task F4: .gitignore + plugin/TONE.md

**Files:**
- Modify: `.gitignore`
- Modify: `plugin/TONE.md`

- [ ] **Step 1: Confirm `.gitignore` already excludes node_modules**

Run: `grep -n node_modules .gitignore`
Expected: matches at least one line, OR no output (we'll add it).

If `node_modules/` is not in the root `.gitignore`, append:

```
# Dashboard build deps
plugin/dashboard/node_modules/
```

(The per-dir `plugin/dashboard/.gitignore` already covers this for that directory specifically, but a root entry is belt-and-braces.)

Also confirm `dist/` is NOT in any `.gitignore`:

Run: `grep -rn "dist" .gitignore plugin/.gitignore plugin/dashboard/.gitignore 2>/dev/null`
Expected: no matches. If any match, remove the line — `dist/` MUST be committed.

- [ ] **Step 2: Add a dashboard note to `plugin/TONE.md`**

Append the following bullet to TONE.md (under whatever the UI / aesthetic section is, or append a new short section at the end):

```markdown
## Dashboard

The visual dashboard at `plugin/dashboard/` uses Mantine v7 component defaults.
No custom theming beyond dark scheme, no new design tokens, no wrapper
components. The low-friction principle that makes the markdown-first workflow
work also applies to the dashboard's visual layer — use library primitives
straight off the shelf so the entire surface stays small and obvious.
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore plugin/TONE.md
git commit -m "docs: .gitignore + TONE.md cover dashboard"
```

---

### Task F5: CI workflow — dashboard-build-check

**Files:**
- Create: `.github/workflows/dashboard-build-check.yml`

- [ ] **Step 1: Inspect existing privacy-check workflow for style**

Run: `cat .github/workflows/privacy-check.yml`
Expected: shows the existing workflow's `on:` and `jobs:` syntax we should mirror.

- [ ] **Step 2: Write `.github/workflows/dashboard-build-check.yml`**

```yaml
name: dashboard-build-check

on:
  pull_request:
    paths:
      - 'plugin/dashboard/**'
  push:
    branches: [main]
    paths:
      - 'plugin/dashboard/**'

jobs:
  verify-dist:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: plugin/dashboard/package-lock.json
      - name: Install dashboard dependencies
        working-directory: plugin/dashboard
        run: npm ci
      - name: Build dashboard
        working-directory: plugin/dashboard
        run: npm run build
      - name: Verify dist/ matches committed bundle
        run: |
          if ! git diff --quiet -- plugin/dashboard/dist/; then
            echo "::error::plugin/dashboard/dist/ is out of date. Rebuild and commit."
            git diff --stat -- plugin/dashboard/dist/
            exit 1
          fi
      - name: Verify dashboard tests
        working-directory: plugin/dashboard
        run: |
          pip install -r requirements-dev.txt
          python3 -m pytest -v
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/dashboard-build-check.yml
git commit -m "ci: dashboard-build-check verifies dist/ + runs python tests"
```

---

### Task F6: README for plugin/dashboard

**Files:**
- Create: `plugin/dashboard/README.md`

- [ ] **Step 1: Write `plugin/dashboard/README.md`**

```markdown
# pm-job-search dashboard

React + Mantine SPA served by a Python stdlib HTTP server. Launched via the
`/dashboard` skill in the parent plugin.

- **Spec:** [docs/superpowers/specs/2026-05-18-dashboard-design.md](../../docs/superpowers/specs/2026-05-18-dashboard-design.md)
- **Rebuild:** `cd plugin/dashboard && npm install && npm run build` (then commit `dist/`)
- **Test (Python):** `python3 -m pytest -v`
- **Run locally:** `python3 serve.py --userdata <path-to-userdata>`

Users do not need to run any of the above. The committed `dist/` bundle and
the stdlib-only Python server are everything required at install time.
```

- [ ] **Step 2: Commit**

```bash
git add plugin/dashboard/README.md
git commit -m "docs: plugin/dashboard/README points at spec + rebuild commands"
```

---

### Task F7: Privacy scan + end-to-end verification

**Files:** (no file changes — verification only)

- [ ] **Step 1: Run the privacy scan on all new dashboard files**

Extract the blocklist pattern from `.github/workflows/privacy-check.yml` (look for the `PATTERN=` line) and run `rg -i "$PATTERN"` against the new dashboard files:

```bash
PATTERN=$(awk -F"'" '/PATTERN=/ {print $2; exit}' .github/workflows/privacy-check.yml)
rg -i "$PATTERN" plugin/dashboard/ plugin/skills/dashboard/ .github/workflows/dashboard-build-check.yml
```

Expected: zero hits (rg exits non-zero with no matches, which is what we want here — wrap with `|| echo clean` if you want a positive signal). If any hit appears, fix the offending file before proceeding.

- [ ] **Step 2: Run full Python test suite**

Run: `cd plugin/dashboard && python3 -m pytest -v`
Expected: all tests pass.

- [ ] **Step 3: Cold-start launch against Maya's example install**

Run: `python3 plugin/dashboard/serve.py --userdata userdata/examples/maya --no-open --port 7890`
Expected: prints URL, server runs. In another terminal, `curl http://localhost:7890/api/state | head -c 200` returns JSON starting with `{"companies":`. Ctrl-C the server.

- [ ] **Step 4: Exercise the writes manually**

Pick one company from Maya's install (e.g. Plaid):

```bash
# Status change
curl -X PATCH http://localhost:7890/api/positions/Plaid/status \
  -H 'Content-Type: application/json' \
  -d '{"status":"rejected"}'
# Expect: {"ok":true}
cat userdata/examples/maya/companies/Plaid/meta.md  # status: rejected, other fields untouched

# Note append
curl -X POST http://localhost:7890/api/positions/Plaid/notes \
  -H 'Content-Type: application/json' \
  -d '{"note":"Verification test from F7"}'
# Expect: {"ok":true}
cat userdata/examples/maya/companies/Plaid/notes.md  # heading + timestamped entry

# New company (unique)
curl -X POST http://localhost:7890/api/companies \
  -H 'Content-Type: application/json' \
  -d '{"company":"Lendable","position":"Senior PM, Underwriting","tier":"P1","link":"https://example.com/lendable","status":"discovered"}'
# Expect: {"folder_path":"Lendable"}
ls userdata/examples/maya/companies/Lendable/

# Conflict (duplicate)
curl -X POST http://localhost:7890/api/companies \
  -H 'Content-Type: application/json' \
  -d '{"company":"Plaid","position":"Senior PM, Consumer Credit","tier":"P0","link":"x","status":"discovered"}'
# Expect: HTTP 409, body {"error":"Plaid / Senior PM, Consumer Credit already exists"}
```

- [ ] **Step 5: Revert verification edits to Maya's install**

Run:

```bash
git checkout userdata/examples/maya/
rm -rf userdata/examples/maya/companies/Lendable/
```

(Maya is a committed example install; verification writes must not be left behind.)

- [ ] **Step 6: Smoke-test the browser UI**

Run: `python3 plugin/dashboard/serve.py --userdata userdata/examples/maya`
Expected: browser opens. Verify visually:
- Three zones render (top stats, grouped table, bottom brief panel).
- Status toggle works (Status / Tier).
- Status dropdown changes a row's status and persists across reload.
- Add-note drawer opens and saves.
- "+ New company" modal opens and rejects a duplicate.

Then revert any test writes (`git checkout userdata/examples/maya/`) and ctrl-C the server.

- [ ] **Step 7: Final commit (only if anything was fixed during verification)**

If steps 1-6 surfaced bugs, fix them and commit. If everything passed clean, no commit needed.

```bash
# Only if needed:
git add <files>
git commit -m "fix(dashboard): <verification-driven fix>"
```

---

## Self-review (run after all slices complete)

Before claiming the plan executed successfully, the operator MUST:

1. Re-read the spec at [docs/superpowers/specs/2026-05-18-dashboard-design.md](../specs/2026-05-18-dashboard-design.md) and confirm every numbered verification item passes.
2. Confirm `git log --oneline` for the branch shows commits matching the slice boundaries above (no half-finished slices, no orphan changes).
3. Confirm `git diff main --stat` shows ONLY files listed in the spec's "Files to be created or modified" section.
4. Confirm the privacy-check and dashboard-build-check CI workflows pass on the branch.
5. Invoke `superpowers:verification-before-completion` to gate the merge claim.
