#!/usr/bin/env python3
"""Deterministic lint over a journey transcript.

Single source of truth for the mechanically-checkable half of what used to be
rubrics/lint-checklist.md. Called three ways:
  * test-personas Phase 3.5 — over the transcript a journey just produced
  * CI (tests/test_lint_transcript.py) — over each frozen corpus transcript
  * by hand: python3 scripts/lint_transcript.py <transcript.md>

Its output reaches the judge as an authoritative block, same contract as the
schema validator: a lint finding is a fact, not something to re-litigate from
the transcript. So a false finding is worse than a missing one — every rule
here is deliberately narrow, and anything needing judgement stayed with the
judge (old Rule 2, "two unrelated asks", lives in rubrics/tone.md as Rule A).

Rules, and what each needs:
  lint.fenced-summary      transcript only
  lint.unresolved-ref      transcript + plugin/ tree
  lint.jargon              transcript only
  lint.prior-state-prompt  transcript + the snapshot the run started from
  lint.hardcoded-cadence   transcript + the userdata/ tree the run produced

Rules whose input is missing are reported as NOT CHECKED rather than silently
passing — a clean run must not be mistaken for full coverage.

Stdlib only, no deps. Exit 0 = clean, 1 = findings, 2 = usage error.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import namedtuple
from pathlib import Path

Finding = namedtuple("Finding", ["turn", "rule", "detail"])

TURN_RE = re.compile(r"^## Turn (\d+) — (USER|ASSISTANT)\s*$", re.MULTILINE)
SNAPSHOT_RE = re.compile(r"^\*\*Snapshot:\*\*\s*(.+?)\s*$", re.MULTILINE)
FENCE_RE = re.compile(r"^```(.*)$")

# A fenced block is allowed when it carries a real language tag, or when its
# first non-blank line reads as a shell command the user is meant to run. The
# violation this rule targets is a summary rendered to chat inside a bare
# fence. Corpus evidence: across 15 transcripts there is exactly one fenced
# block in an assistant turn, and it is the allowed dashboard launch command.
PROSE_INFO = {"", "text", "txt", "markdown", "md"}
SHELL_START_RE = re.compile(
    r"^\s*(?:\$\s*)?(?:python3?|pip3?|npm|npx|node|git|cd|ls|cat|make|curl"
    r"|open|sh|bash|zsh|chmod|mkdir|mv|cp|rm|echo|export|\./)\b"
)

SKILL_REF_RE = re.compile(r"/pm-job-search:([A-Za-z0-9_-]+)")
ROOT_REF_RE = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9_./-]+)")

# Flat ban, not "jargon without explanation". The largest measured source of
# judge disagreement in the corpus was three findings arguing about whether
# `meta.md` / `status: new` / `tier: unscored` counted as explained. As a flat
# ban that argument cannot occur, and it is the better product rule anyway.
JARGON = [
    ("frontmatter", re.compile(r"\bfrontmatter\b", re.IGNORECASE)),
    ("tier_weights", re.compile(r"\btier_weights\b")),
    ("tier_thresholds", re.compile(r"\btier_thresholds\b")),
    ("meta.md", re.compile(r"\bmeta\.md\b")),
    ("research-brief.md", re.compile(r"\bresearch-brief\.md\b")),
    ("P0/P1/P2", re.compile(r"\bP[012]\b")),
    ("status:", re.compile(r"\bstatus:")),
    ("tier:", re.compile(r"\btier:")),
    ("CLAUDE_PLUGIN_ROOT", re.compile(r"CLAUDE_PLUGIN_ROOT")),
]

PRIOR_STATE_RE = re.compile(
    r"since (?:the )?last time|since we last|since your last|since you last"
    r"|anything (?:that(?:'s| has)? )?moved|last time you|previous run"
    r"|your last run|catch me up on",
    re.IGNORECASE,
)

CADENCE_RE = re.compile(
    r"\b(\d+)\s+(applications?|outreaches?|messages?|founders?|roles?|threads?)\b",
    re.IGNORECASE,
)
CLOCK_RE = re.compile(r"\bevery\s+(\d{1,2})\s*(?:am|pm)\b", re.IGNORECASE)

Turn = namedtuple("Turn", ["number", "role", "body"])


def parse_turns(text: str) -> list[Turn]:
    """Split a transcript into turns. Anything before the first turn header
    (the run metadata block) is not a turn and is never linted."""
    marks = list(TURN_RE.finditer(text))
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out.append(Turn(int(m.group(1)), m.group(2), text[m.end():end]))
    return out


def fenced_blocks(body: str) -> list[tuple[str, str]]:
    """(info string, content) for each fenced block. An unterminated fence
    runs to the end of the turn rather than swallowing the rest of the file."""
    out, info, buf, inside = [], None, [], False
    for line in body.splitlines():
        m = FENCE_RE.match(line)
        if m and not inside:
            inside, info, buf = True, m.group(1).strip(), []
        elif m and inside:
            out.append((info or "", "\n".join(buf)))
            inside = False
        elif inside:
            buf.append(line)
    if inside:
        out.append((info or "", "\n".join(buf)))
    return out


def strip_fences(body: str) -> str:
    out, inside = [], False
    for line in body.splitlines():
        if FENCE_RE.match(line):
            inside = not inside
            continue
        if not inside:
            out.append(line)
    return "\n".join(out)


INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")


def mask_shell_spans(text: str) -> str:
    """Blank out inline `code` spans that read as shell commands, preserving
    length so match offsets still index the original text. A command the user
    is meant to type is not jargon — `python3 ${CLAUDE_PLUGIN_ROOT}/…` in
    2026-07-11 turn 22 is the case this exists for, and the judge that read it
    agreed it was allowed."""
    return INLINE_CODE_RE.sub(
        lambda m: "`" + " " * len(m.group(1)) + "`"
        if SHELL_START_RE.match(m.group(1)) else m.group(0),
        text,
    )


def _quote(text: str, match_start: int, width: int = 90) -> str:
    """The line the match sits on, windowed around the match. Centring matters:
    long assistant lines routinely push the offending term past a plain
    left-anchored truncation, leaving a finding whose quote doesn't show the
    thing it is complaining about."""
    start = text.rfind("\n", 0, match_start) + 1
    end = text.find("\n", match_start)
    if end == -1:
        end = len(text)
    line, off = text[start:end], match_start - start
    if len(line) > width:
        lo = max(0, off - width // 2)
        hi = min(len(line), lo + width)
        lo = max(0, hi - width)
        line = ("…" if lo > 0 else "") + line[lo:hi] + ("…" if hi < len(line) else "")
    return re.sub(r"\s+", " ", line).strip()


def check_fenced_summary(turns: list[Turn]) -> list[Finding]:
    out = []
    for t in turns:
        if t.role != "ASSISTANT":
            continue
        for info, content in fenced_blocks(t.body):
            if info.lower() not in PROSE_INFO:
                continue  # a real language tag — file content or code
            first = next((ln for ln in content.splitlines() if ln.strip()), "")
            if SHELL_START_RE.match(first):
                continue  # shell command the user is meant to run
            out.append(Finding(t.number, "lint.fenced-summary",
                               f"bare fenced block in chat: \"{_quote(first, 0)}\""))
    return out


def check_unresolved_refs(turns: list[Turn], plugin: Path) -> list[Finding]:
    out = []
    for t in turns:
        if t.role != "ASSISTANT":
            continue
        for m in SKILL_REF_RE.finditer(t.body):
            if not (plugin / "skills" / m.group(1)).is_dir():
                out.append(Finding(t.number, "lint.unresolved-ref",
                                   f"/pm-job-search:{m.group(1)} — no such skill"))
        for m in ROOT_REF_RE.finditer(t.body):
            rel = m.group(1).rstrip(".,;:!?)\"'`")
            if not (plugin / rel).exists():
                out.append(Finding(t.number, "lint.unresolved-ref",
                                   f"${{CLAUDE_PLUGIN_ROOT}}/{rel} — no such file"))
    return out


def check_jargon(turns: list[Turn]) -> list[Finding]:
    out = []
    for t in turns:
        if t.role != "ASSISTANT":
            continue
        prose = strip_fences(t.body)
        masked = mask_shell_spans(prose)
        for label, rx in JARGON:
            hits = list(rx.finditer(masked))
            if not hits:
                continue
            times = f" ({len(hits)}×)" if len(hits) > 1 else ""
            out.append(Finding(t.number, "lint.jargon",
                               f"'{label}'{times} in user-facing text: "
                               f"\"{_quote(prose, hits[0].start())}\""))
    return out


def snapshot_has_prior_state(snapshot: Path) -> bool:
    """Prior state = something a 'since last time' prompt could refer to: a
    dated journal entry, or any tracked company."""
    journal = snapshot / "journal.md"
    if journal.exists() and re.search(r"^## \d{4}-\d{2}-\d{2}", journal.read_text(),
                                      re.MULTILINE):
        return True
    companies = snapshot / "companies"
    if not companies.is_dir():
        return False
    return any(companies.glob("*/meta.md")) or any(companies.glob("*/*/meta.md"))


def check_prior_state_prompt(turns: list[Turn], snapshot: Path) -> list[Finding]:
    if snapshot_has_prior_state(snapshot):
        return []
    out = []
    for t in turns:
        if t.role != "ASSISTANT":
            continue
        prose = strip_fences(t.body)
        m = PRIOR_STATE_RE.search(prose)
        if m:
            out.append(Finding(t.number, "lint.prior-state-prompt",
                               f"prior-state prompt with no prior state "
                               f"(snapshot '{snapshot.name}'): "
                               f"\"{_quote(prose, m.start())}\""))
    return out


def _numbers_in(path: Path) -> set[str]:
    return set(re.findall(r"\b\d+\b", path.read_text())) if path.exists() else set()


def check_hardcoded_cadence(turns: list[Turn], userdata: Path) -> list[Finding]:
    """A cadence number is fine when it traces to the user's own plan. Allowed
    if it appears anywhere in strategy.md or profile.md — deliberately loose,
    because a false finding here costs more than a missed one."""
    allowed = _numbers_in(userdata / "strategy.md") | _numbers_in(userdata / "profile.md")
    out = []
    for t in turns:
        if t.role != "ASSISTANT":
            continue
        prose = mask_shell_spans(strip_fences(t.body))
        for m in CADENCE_RE.finditer(prose):
            if m.group(1) in allowed:
                continue
            out.append(Finding(t.number, "lint.hardcoded-cadence",
                               f"'{m.group(1)} {m.group(2)}' not in strategy.md "
                               f"or profile.md: \"{_quote(prose, m.start())}\""))
        for m in CLOCK_RE.finditer(prose):
            out.append(Finding(t.number, "lint.hardcoded-cadence",
                               f"hardcoded time of day: \"{_quote(prose, m.start())}\""))
    return out


def snapshot_name(text: str) -> str | None:
    """The '**Snapshot:** name' header, minus any parenthetical note — several
    corpus transcripts write 'maya-active (after Phase 2 backfill fix)'."""
    m = SNAPSHOT_RE.search(text)
    if not m:
        return None
    return re.sub(r"\s*\(.*\)\s*$", "", m.group(1)).strip() or None


def lint_transcript(text: str, plugin: Path, snapshot: Path | None = None,
                    userdata: Path | None = None) -> tuple[list[Finding], list[str]]:
    """Returns (findings, names of rules that could not be checked)."""
    turns = parse_turns(text)
    findings = (check_fenced_summary(turns)
                + check_unresolved_refs(turns, plugin)
                + check_jargon(turns))
    skipped = []
    if snapshot is not None:
        findings += check_prior_state_prompt(turns, snapshot)
    else:
        skipped.append("lint.prior-state-prompt (no snapshot supplied)")
    if userdata is not None:
        findings += check_hardcoded_cadence(turns, userdata)
    else:
        skipped.append("lint.hardcoded-cadence (no userdata tree supplied)")
    findings.sort(key=lambda f: (f.turn, f.rule, f.detail))
    return findings, skipped


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.splitlines()[0])
    ap.add_argument("transcript")
    ap.add_argument("--plugin", default=str(root / "plugin"),
                    help="plugin/ tree used to resolve skill and file references")
    ap.add_argument("--snapshots", default=str(root / "tests" / "snapshots"),
                    help="directory of snapshot fixtures; the transcript's "
                         "'**Snapshot:**' header selects one")
    ap.add_argument("--snapshot", default=None,
                    help="explicit snapshot directory, overriding the header")
    ap.add_argument("--userdata", default=None,
                    help="userdata/ tree the run produced (enables cadence check)")
    try:
        args = ap.parse_args(argv[1:])
    except SystemExit:
        return 2

    tpath = Path(args.transcript)
    if not tpath.is_file():
        print(f"usage: lint_transcript.py <transcript.md>  (no such file: {tpath})",
              file=sys.stderr)
        return 2
    text = tpath.read_text()

    if args.snapshot:
        snapshot = Path(args.snapshot)
    else:
        name = snapshot_name(text)
        cand = Path(args.snapshots) / name if name else None
        snapshot = cand if cand and cand.is_dir() else None
    userdata = Path(args.userdata) if args.userdata else None
    if userdata is not None and not userdata.is_dir():
        print(f"usage: --userdata is not a directory: {userdata}", file=sys.stderr)
        return 2

    findings, skipped = lint_transcript(text, Path(args.plugin), snapshot, userdata)
    for f in findings:
        print(f"turn {f.turn}: {f.rule} — {f.detail}")
    if not findings:
        print("No lint findings.")
    for s in skipped:
        print(f"NOT CHECKED: {s}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
