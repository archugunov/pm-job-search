from pathlib import Path
from textwrap import dedent

import pytest

from lint_transcript import (
    Finding,
    lint_transcript,
    mask_shell_spans,
    parse_turns,
    snapshot_has_prior_state,
    snapshot_name,
    _quote,
)

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugin"
RUNS = ROOT / "tests" / "judge-calibration" / "runs"
SNAPSHOTS = ROOT / "tests" / "snapshots"


def transcript(*turns: tuple[str, str], snapshot: str = "empty") -> str:
    """Build a transcript from (role, body) pairs, numbered from 1."""
    head = f"# Transcript — test\n\n**Snapshot:** {snapshot}\n\n---\n"
    return head + "".join(
        f"\n## Turn {i} — {role}\n\n{body}\n"
        for i, (role, body) in enumerate(turns, start=1)
    )


def rules(findings: list[Finding]) -> list[tuple[int, str]]:
    return [(f.turn, f.rule) for f in findings]


def lint(text, snapshot=None, userdata=None):
    return lint_transcript(text, PLUGIN, snapshot, userdata)[0]


# --- parsing -----------------------------------------------------------------

def test_parse_turns_splits_on_header():
    turns = parse_turns(transcript(("USER", "hi"), ("ASSISTANT", "hello")))
    assert [(t.number, t.role) for t in turns] == [(1, "USER"), (2, "ASSISTANT")]
    assert turns[1].body.strip() == "hello"


def test_metadata_block_is_not_a_turn():
    """Everything before the first turn header is run metadata and must never
    be linted — it legitimately contains snapshot names and file paths."""
    text = "# Transcript\n\n**Snapshot:** empty\n\nmeta.md P0 status:\n"
    assert parse_turns(text) == []
    assert lint(text, snapshot=SNAPSHOTS / "empty") == []


def test_user_turns_are_never_linted():
    text = transcript(("USER", "what is meta.md and P0?"))
    assert lint(text, snapshot=SNAPSHOTS / "empty") == []


@pytest.mark.parametrize("header,expected", [
    ("**Snapshot:** empty", "empty"),
    ("**Snapshot:** maya-active (after Phase 2 backfill fix)", "maya-active"),
    ("**Snapshot:** diego-reflection (after Phase 2 backfill — added entries)",
     "diego-reflection"),
])
def test_snapshot_name_strips_parenthetical(header, expected):
    assert snapshot_name(f"# T\n\n{header}\n") == expected


def test_snapshot_name_absent():
    assert snapshot_name("# T\n\nno header here\n") is None


# --- lint.fenced-summary -----------------------------------------------------

def test_bare_fence_in_chat_is_flagged():
    text = transcript(("ASSISTANT", "Here's your week:\n\n```\nMon: apply\n```"))
    assert rules(lint(text)) == [(1, "lint.fenced-summary")]


def test_language_tagged_fence_is_allowed():
    text = transcript(("ASSISTANT", "```json\n{\"a\": 1}\n```"))
    assert lint(text) == []


def test_shell_command_in_bare_fence_is_allowed():
    """The one fenced block in the whole frozen corpus is this case."""
    text = transcript(("ASSISTANT",
                       '```\npython3 "${CLAUDE_PLUGIN_ROOT}/dashboard/serve.py"\n```'))
    assert lint(text) == []


def test_unterminated_fence_does_not_swallow_later_turns():
    text = transcript(("ASSISTANT", "```\nMon: apply"), ("ASSISTANT", "meta.md"))
    assert rules(lint(text)) == [(1, "lint.fenced-summary"), (2, "lint.jargon")]


# --- lint.unresolved-ref -----------------------------------------------------

def test_real_skill_reference_resolves():
    assert lint(transcript(("ASSISTANT", "Run /pm-job-search:today next."))) == []


def test_missing_skill_reference_is_flagged():
    found = lint(transcript(("ASSISTANT", "Run /pm-job-search:nonesuch next.")))
    assert rules(found) == [(1, "lint.unresolved-ref")]
    assert "nonesuch" in found[0].detail


def test_missing_plugin_root_path_is_flagged():
    """The literal `CLAUDE_PLUGIN_ROOT` also trips the jargon ban here, which
    is correct — both findings are real, so assert on this rule only."""
    text = transcript(("ASSISTANT", "See ${CLAUDE_PLUGIN_ROOT}/nope/missing.md."))
    refs = [f for f in lint(text) if f.rule == "lint.unresolved-ref"]
    assert len(refs) == 1 and "nope/missing.md" in refs[0].detail


def test_plugin_root_path_trailing_punctuation_is_stripped():
    """'…/dashboard/serve.py.' at the end of a sentence must still resolve."""
    text = transcript(("ASSISTANT", "Run ${CLAUDE_PLUGIN_ROOT}/dashboard/serve.py."))
    assert [f for f in lint(text) if f.rule == "lint.unresolved-ref"] == []


# --- lint.jargon -------------------------------------------------------------

@pytest.mark.parametrize("term", [
    "frontmatter", "tier_weights", "tier_thresholds", "meta.md",
    "research-brief.md", "CLAUDE_PLUGIN_ROOT",
])
def test_banned_terms_are_flagged(term):
    assert rules(lint(transcript(("ASSISTANT", f"I wrote the {term} for you.")))) \
        == [(1, "lint.jargon")]


@pytest.mark.parametrize("text", ["two P0 roles", "a P1 thread", "the P2 bucket"])
def test_tier_codes_are_flagged(text):
    assert rules(lint(transcript(("ASSISTANT", text)))) == [(1, "lint.jargon")]


def test_yaml_key_forms_are_flagged():
    text = transcript(("ASSISTANT", "Filed 3 roles, all `status: new`, `tier: unscored`."))
    assert rules(lint(text)) == [(1, "lint.jargon"), (1, "lint.jargon")]


def test_jargon_is_reported_once_per_turn_per_term_with_a_count():
    text = transcript(("ASSISTANT", "P0 here, P0 there, and another P0."))
    found = lint(text)
    assert len(found) == 1 and "(3×)" in found[0].detail


def test_prose_word_tier_is_not_flagged():
    """'Tier' as a column header or plain word is fine — only the YAML key
    form leaks. This is the distinction the 2026-07-11 judge got right."""
    assert lint(transcript(("ASSISTANT", "The Tier column shows how they rank."))) == []


def test_jargon_inside_a_fenced_block_is_not_flagged():
    text = transcript(("ASSISTANT", "Your file:\n\n```yaml\nstatus: new\n```"))
    assert lint(text) == []


def test_shell_command_in_inline_code_is_not_jargon():
    """Regression: `python3 ${CLAUDE_PLUGIN_ROOT}/…` is a command the user is
    meant to type, and the judge that read 2026-07-11 turn 22 agreed it was
    allowed. Masking it must not disturb the rest of the line."""
    text = transcript(("ASSISTANT",
                       "Run `python3 ${CLAUDE_PLUGIN_ROOT}/dashboard/serve.py` to start."))
    assert lint(text) == []


def test_masking_preserves_length_so_quotes_stay_aligned():
    src = "Run `python3 x` then meta.md"
    masked = mask_shell_spans(src)
    assert len(masked) == len(src)
    assert masked.index("meta.md") == src.index("meta.md")


def test_non_shell_inline_code_is_still_scanned():
    text = transcript(("ASSISTANT", "It lives in `meta.md` under your company folder."))
    assert rules(lint(text)) == [(1, "lint.jargon")]


# --- quoting -----------------------------------------------------------------

def test_quote_centres_on_the_match_not_the_line_start():
    """Regression: long assistant lines pushed the offending term past a
    left-anchored truncation, leaving a quote that didn't show the term."""
    line = "x" * 200 + " meta.md " + "y" * 200
    text = transcript(("ASSISTANT", line))
    detail = lint(text)[0].detail
    assert "meta.md" in detail


def test_quote_marks_both_elisions():
    text = "a" * 300 + "NEEDLE" + "b" * 300
    q = _quote(text, text.index("NEEDLE"))
    assert q.startswith("…") and q.endswith("…") and "NEEDLE" in q


# --- lint.prior-state-prompt -------------------------------------------------

def test_prior_state_prompt_flagged_when_snapshot_empty():
    text = transcript(("ASSISTANT", "Anything moved since last time?"))
    found = lint(text, snapshot=SNAPSHOTS / "empty")
    assert rules(found) == [(1, "lint.prior-state-prompt")]


def test_prior_state_prompt_allowed_when_journal_has_entries():
    text = transcript(("ASSISTANT", "Anything moved since last time?"),
                      snapshot="diego-reflection")
    assert lint(text, snapshot=SNAPSHOTS / "diego-reflection") == []


def test_prior_state_rule_is_skipped_without_a_snapshot():
    text = transcript(("ASSISTANT", "Anything moved since last time?"))
    findings, skipped = lint_transcript(text, PLUGIN, None, None)
    assert findings == []
    assert any("prior-state" in s for s in skipped)


def test_snapshot_prior_state_detection(tmp_path):
    assert snapshot_has_prior_state(tmp_path) is False
    (tmp_path / "journal.md").write_text("# Journal\n\nno dated entries\n")
    assert snapshot_has_prior_state(tmp_path) is False
    (tmp_path / "journal.md").write_text("# Journal\n\n## 2026-08-05\n- Applied.\n")
    assert snapshot_has_prior_state(tmp_path) is True


def test_prior_state_from_nested_company_folder(tmp_path):
    """Roles can live at companies/<Co>/meta.md or companies/<Co>/<role>/meta.md."""
    nested = tmp_path / "companies" / "Plaid" / "senior-pm"
    nested.mkdir(parents=True)
    (nested / "meta.md").write_text("---\ncompany: Plaid\n---\n")
    assert snapshot_has_prior_state(tmp_path) is True


# --- lint.hardcoded-cadence --------------------------------------------------

def test_cadence_number_absent_from_strategy_is_flagged(tmp_path):
    (tmp_path / "strategy.md").write_text("---\nweekly_targets:\n  applications: 3\n---\n")
    text = transcript(("ASSISTANT", "DM 10 founders this week."))
    assert rules(lint(text, userdata=tmp_path)) == [(1, "lint.hardcoded-cadence")]


def test_cadence_number_present_in_strategy_is_allowed(tmp_path):
    (tmp_path / "strategy.md").write_text("---\nweekly_targets:\n  applications: 8\n---\n")
    text = transcript(("ASSISTANT", "That's 8 applications a week."))
    assert lint(text, userdata=tmp_path) == []


def test_hardcoded_time_of_day_is_always_flagged(tmp_path):
    (tmp_path / "strategy.md").write_text("---\nweekly_targets:\n  applications: 9\n---\n")
    text = transcript(("ASSISTANT", "I'll nudge you every 9am."))
    assert rules(lint(text, userdata=tmp_path)) == [(1, "lint.hardcoded-cadence")]


def test_cadence_rule_is_skipped_without_a_userdata_tree():
    text = transcript(("ASSISTANT", "DM 10 founders this week."))
    findings, skipped = lint_transcript(text, PLUGIN, None, None)
    assert findings == []
    assert any("cadence" in s for s in skipped)


# --- frozen corpus baseline --------------------------------------------------
#
# Asserted as (path, turn, rule) triples rather than exact detail strings, so
# the baseline survives quote-formatting changes but still fails on any change
# to what the rules actually catch. Regenerate deliberately, never reflexively.

CORPUS_BASELINE = {
    ("2026-06-07/contrarian-edge-recovery.md", 1, "lint.jargon"),
    ("2026-06-07/contrarian-edge-recovery.md", 5, "lint.jargon"),
    ("2026-06-07/diego-reflection.md", 2, "lint.jargon"),
    ("2026-06-07/maya-active-loop.md", 3, "lint.jargon"),
    ("2026-06-07/maya-cold-start.md", 17, "lint.jargon"),
    ("2026-07-11/diego-reflection.md", 3, "lint.jargon"),
    ("2026-07-11/diego-reflection.md", 4, "lint.jargon"),
    ("2026-07-11/maya-cold-start.md", 17, "lint.jargon"),
    ("2026-07-11/maya-cold-start.md", 23, "lint.jargon"),
    ("2026-08-10/maya-cold-start.md", 16, "lint.jargon"),
    ("2026-08-10/maya-cold-start.md", 20, "lint.jargon"),
    ("2026-08-10/maya-cold-start.md", 21, "lint.jargon"),
    ("2026-08-10/maya-cold-start.md", 23, "lint.jargon"),
}


def corpus_transcripts() -> list[Path]:
    return sorted(p for p in RUNS.rglob("*.md")
                  if ".judge" not in p.name and p.name != "SUMMARY.md")


def test_corpus_transcripts_are_discovered():
    assert len(corpus_transcripts()) >= 12


def test_frozen_corpus_matches_baseline():
    actual = set()
    for p in corpus_transcripts():
        text = p.read_text()
        name = snapshot_name(text)
        snap = SNAPSHOTS / name if name and (SNAPSHOTS / name).is_dir() else None
        for f in lint_transcript(text, PLUGIN, snap, None)[0]:
            actual.add((p.relative_to(RUNS).as_posix(), f.turn, f.rule))
    assert actual == CORPUS_BASELINE


def test_corpus_has_no_unresolved_references():
    """Every skill and plugin-root path the corpus mentions still resolves.
    This is the rule that would catch a skill rename breaking user-facing copy."""
    for p in corpus_transcripts():
        found = lint_transcript(p.read_text(), PLUGIN, None, None)[0]
        assert [f for f in found if f.rule == "lint.unresolved-ref"] == [], p.name


def test_august_run_pins_the_judge_disagreement():
    """The 4:1 split between the two 2026-08-10 judge readings was entirely
    about `meta.md` / `status: new` / `tier: unscored`. Those are now decided
    deterministically — this test is the reason the rule was extracted."""
    p = RUNS / "2026-08-10" / "maya-cold-start.md"
    found = lint_transcript(p.read_text(), PLUGIN, SNAPSHOTS / "empty", None)[0]
    turns = {f.turn for f in found if f.rule == "lint.jargon"}
    assert {20, 21} <= turns
