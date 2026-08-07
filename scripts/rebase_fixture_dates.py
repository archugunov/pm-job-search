#!/usr/bin/env python3
"""Shift a test snapshot's dates forward so its date-gated paths stay reachable.

The skills read the real wall clock — `/today` gates output on "within 7 days",
"more than 14 days ago", the current ISO week and the prior ISO week. A snapshot
frozen in May therefore stops exercising those branches: some can never fire and
others always fire, and a journey that cannot distinguish a real regression from
fixture rot has stopped being a test.

So the data moves, not the assertions.

    python3 scripts/rebase_fixture_dates.py maya-active
    python3 scripts/rebase_fixture_dates.py all --as-of 2026-08-07
    python3 scripts/rebase_fixture_dates.py all --dry-run

Two properties matter and both come from shifting every date by one constant:

  * A *uniform* shift preserves every interval. "Applied 26 days ago" stays 26
    days ago, so a `> 14 days` gate lands on the same side it always did.
  * A shift that is a whole number of *weeks* additionally preserves weekday
    alignment. ISO-week gates ("this week", "the prior week") keep exercising the
    same branch instead of drifting onto a different day of the week.

The anchor is the newest date in the snapshot that is not forward-looking.
Forward-looking fields (`target_offer_date`, `checkpoints[].date`) describe the
future and would drag the anchor past the snapshot's real "as of" moment — Maya's
`target_offer_date` sits months ahead of her newest activity. They are still
shifted; they just do not get a vote on how far.

Nothing is committed. Review with `git diff` and commit separately.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SNAPSHOT_ROOT = REPO_ROOT / "tests" / "snapshots"

DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")

# Anchor detection uses a whitelist, not a blacklist. Trying to exclude
# forward-looking dates turned out to be unreliable: a snapshot carried a
# commented-out template example (`#   - date: …`), another used `target_date:`
# rather than `target_offer_date:`, and READMEs mention target dates in prose.
# Any one of those drags the anchor into the future and the shift comes out
# short. So instead: anchor only on the fields that actually record something
# having happened — the same fields `/today`'s gates read.
ACTIVITY_FIELD_RE = re.compile(
    r"^\s*(?:date_added|date_applied|last_inbound|last_practised)\s*:\s*(\d{4}-\d{2}-\d{2})",
    re.MULTILINE,
)

# Journal entries: `## 2026-05-18`.
JOURNAL_HEADING_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)

# Files whose names embed the date they were produced.
DATED_FILENAME_RE = re.compile(
    r"(?:interview-prep|interview-debrief|daily-brief|offer-evaluation)-(\d{4}-\d{2}-\d{2})"
)

# Bare-date marker files (`.last-weekly-reflection` holds one ISO date).
BARE_DATE_FILES = {".last-weekly-reflection"}

# How many whole weeks BEFORE today each snapshot's newest activity should land.
#
# 0 means "inside the last seven days", which is what most journeys want — Maya's
# `active-loop` needs a `last_inbound` within 7 days for the active-thread trigger
# to fire at all.
#
# `diego-reflection` is the exception and needs 1. Its whole purpose is the
# weekly-reflection nudge, which requires at least one journal entry from the
# PRIOR ISO week. Landing its newest entry inside the current week puts every
# entry in the current week and the nudge silently never fires — which is exactly
# the bug commit ffd8cbf's backfill was written to fix, so re-introducing it via
# the rebase would be a quiet regression in the fixture rather than the code.
LANDING_WEEKS_BEFORE_TODAY = {
    "diego-reflection": 1,
}

# "**Window:** 2026-05-04 to 2026-05-10 (ISO week 19)." — the label is derived
# from the dates, so it has to be recomputed rather than shifted.
ISO_WEEK_RE = re.compile(r"\(ISO week (\d+)\)")

SKIP_DIRS = {".git"}
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".mp4", ".ico"}


def iter_files(root: pathlib.Path):
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in BINARY_SUFFIXES:
            continue
        yield p


def read(p: pathlib.Path) -> str | None:
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def parse(y: str, m: str, d: str) -> dt.date | None:
    try:
        return dt.date(int(y), int(m), int(d))
    except ValueError:
        return None


def find_anchor(root: pathlib.Path) -> tuple[dt.date | None, pathlib.Path | None]:
    """Newest date recording something that HAPPENED, and where it was found.

    Deliberately ignores target dates, checkpoints and prose — see the note on
    ACTIVITY_FIELD_RE. Returns (None, None) for a snapshot with no activity.
    """
    best: dt.date | None = None
    best_file: pathlib.Path | None = None

    def consider(raw: str, p: pathlib.Path) -> None:
        nonlocal best, best_file
        try:
            date = dt.date.fromisoformat(raw)
        except ValueError:
            return
        if best is None or date > best:
            best, best_file = date, p

    for p in iter_files(root):
        for m in DATED_FILENAME_RE.finditer(p.name):
            consider(m.group(1), p)

        text = read(p)
        if text is None:
            continue

        if p.name in BARE_DATE_FILES:
            consider(text.strip(), p)
            continue

        for m in ACTIVITY_FIELD_RE.finditer(text):
            consider(m.group(1), p)
        for m in JOURNAL_HEADING_RE.finditer(text):
            consider(m.group(1), p)

    return best, best_file


def shift_text(text: str, delta: dt.timedelta) -> str:
    def repl(m: re.Match) -> str:
        date = parse(*m.groups())
        return m.group(0) if date is None else (date + delta).isoformat()

    shifted = DATE_RE.sub(repl, text)

    # Recompute "(ISO week N)" from the first date on the same line, since the
    # label is derived from the window rather than being a date itself.
    out = []
    for line in shifted.split("\n"):
        if ISO_WEEK_RE.search(line):
            first = DATE_RE.search(line)
            if first:
                date = parse(*first.groups())
                if date:
                    week = date.isocalendar()[1]
                    line = ISO_WEEK_RE.sub(f"(ISO week {week})", line)
        out.append(line)
    return "\n".join(out)


def shift_name(name: str, delta: dt.timedelta) -> str:
    def repl(m: re.Match) -> str:
        date = parse(*m.groups())
        return m.group(0) if date is None else (date + delta).isoformat()

    return DATE_RE.sub(repl, name)


def rebase(snapshot: str, as_of: dt.date, dry_run: bool) -> int:
    root = SNAPSHOT_ROOT / snapshot
    if not root.is_dir():
        print(f"error: no snapshot at {root}", file=sys.stderr)
        return 1

    anchor, anchor_file = find_anchor(root)
    if anchor is None:
        print(f"{snapshot}: no dates — nothing to rebase")
        return 0

    landing = LANDING_WEEKS_BEFORE_TODAY.get(snapshot, 0)
    weeks = (as_of - anchor).days // 7 - landing
    if weeks <= 0:
        print(f"{snapshot}: anchor {anchor} is already within {landing + 1}w of {as_of} — fresh")
        return 0

    delta = dt.timedelta(weeks=weeks)
    where = anchor_file.relative_to(root) if anchor_file else "?"
    note = f", landing {landing}w back" if landing else ""
    print(f"{snapshot}: anchor {anchor} ({where}) → +{weeks}w = {anchor + delta}{note}")

    renames: list[tuple[pathlib.Path, pathlib.Path]] = []
    edits = 0

    for p in iter_files(root):
        text = read(p)
        if text is not None:
            shifted = shift_text(text, delta)
            if shifted != text:
                edits += 1
                if not dry_run:
                    p.write_text(shifted, encoding="utf-8")

        new_name = shift_name(p.name, delta)
        if new_name != p.name:
            renames.append((p, p.with_name(new_name)))

    for old, new in renames:
        print(f"  rename {old.relative_to(root)} → {new.name}")
        if not dry_run:
            old.rename(new)

    verb = "would edit" if dry_run else "edited"
    print(f"  {verb} {edits} file(s), {len(renames)} rename(s)")
    return 0


def freshness(as_of: dt.date) -> int:
    """Read-only staleness report. Used by `make check-fixture-freshness`."""
    stale = False
    for root in sorted(SNAPSHOT_ROOT.iterdir()):
        if not root.is_dir():
            continue
        anchor, _ = find_anchor(root)
        if anchor is None:
            print(f"  {root.name:<20} no dates")
            continue
        weeks = (as_of - anchor).days // 7
        flag = "" if weeks <= 1 else "   <-- stale"
        if weeks > 1:
            stale = True
        print(f"  {root.name:<20} anchor {anchor}  ({weeks}w behind){flag}")
    if stale:
        print("\nRebase before running date-gated journeys:  make rebase-fixtures")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("snapshot", help="snapshot name, 'all', or 'check' for a report")
    ap.add_argument("--as-of", help="target date (default: today)")
    ap.add_argument("--dry-run", action="store_true", help="print without writing")
    args = ap.parse_args()

    as_of = dt.date.today()
    if args.as_of:
        try:
            as_of = dt.date.fromisoformat(args.as_of)
        except ValueError:
            print(f"error: --as-of must be YYYY-MM-DD, got {args.as_of!r}", file=sys.stderr)
            return 1

    if args.snapshot == "check":
        return freshness(as_of)

    if args.snapshot == "all":
        rc = 0
        for root in sorted(SNAPSHOT_ROOT.iterdir()):
            if root.is_dir():
                rc |= rebase(root.name, as_of, args.dry_run)
        return rc

    return rebase(args.snapshot, as_of, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
