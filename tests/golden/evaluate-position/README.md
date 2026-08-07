# Golden set — /evaluate-position

12 synthetic JDs with frozen labels (`cases/*.json`), scored against the
frozen rubric in `profile.md` (a copy of the maya-active snapshot's —
never rebased, never edited without re-deriving every label).

Two layers:

**CI ($0, every push):** `tests/test_golden_cases.py` re-checks each
label's arithmetic against the frozen thresholds. Catches label typos and
silent profile edits. No LLM involved.

**Release time (LLM, run with the 3 release-gate journeys):**

1. In a fresh Claude Code session at the repo root, prompt:

   > For each JSON file in tests/golden/evaluate-position/cases/, run the
   > /pm-job-search:evaluate-position scoring procedure from
   > plugin/skills/evaluate-position/SKILL.md on the case's "jd" text,
   > using tests/golden/evaluate-position/profile.md as the profile.
   > Do NOT write to userdata/ and do NOT ask interactive questions —
   > where the skill would ask, take the default. Collect results as a
   > JSON array of {"id", "tier", "score", "matched_filter"} — tier
   > "filtered" with the matched hard_filter string when the hard-filter
   > gate fires, otherwise the P0/P1/P2 tier and final score. Write it to
   > tests/golden/evaluate-position/results-<YYYY-MM-DD>.json.

2. Grade: `python3 tests/golden/evaluate-position/grade.py tests/golden/evaluate-position/results-<date>.json`
3. Gate: exit 0 required before tagging a release. On FAIL, the per-case
   table shows which JD drifted; check the skill's scoring section first,
   the label second (labels lose only if the rubric strings genuinely
   support the new reading — then fix the label AND say so in the commit).

`results-*.json` files are throwaway run artifacts — gitignored, not part
of the set. Provenance of labels: `author-derived-v1` (derived by hand
from the rubric strings). Upgrade path: replace individual labels after
adjudicated disagreement, bumping provenance.
