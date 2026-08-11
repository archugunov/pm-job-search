# Rubric: Conformance

Did the product do what its own spec says. Not whether the output was good —
whether it matched the contract the skill documents for itself.

These criteria apply to every journey. The journey file's own `## Spec criteria` section adds journey-specific items on top.

## Required vs opportunistic convention

Every criterion in this rubric and in every journey file is annotated with one of three tags:

- **`[deterministic]`** — not yours. A script decides it, or nothing does yet. Skip it entirely: do not report it, do not mark it NOT EXERCISED, do not mention it in your findings. A criterion about the contents of a file that was never rendered in chat is structurally unassessable from a transcript, and guessing at it produces a confident finding with no evidence behind it.
- **`[required]`** — must be exercised AND pass for the journey to PASS verdict. If a required criterion is "not exercised" when it was in scope (its preconditions were met), the journey's spec-gaps verdict is FAIL.
- **`[opportunistic]`** — nice to have. Can be "not exercised" or "fail" without affecting the verdict. Surfaced for awareness but never blocks a release.

Some criteria are conditional — they only apply when a specific skill ran or a specific state was reached. Each conditional criterion has an `Applies when:` line. If the precondition wasn't met, the criterion drops to "not exercised" and the [required] tag doesn't trigger a fail.

## Cross-journey criteria

1. **[required] End-of-run nudge.** The final skill in the journey closes with a context-aware next-step nudge derived from `${CLAUDE_PLUGIN_ROOT}/references/recommended-flow.md`. Not a generic parrot of the canonical order — a state-aware suggestion.
   *Applies when:* the journey reached termination (transcript didn't max-out turns).

2. **[required] No prior-state leak in messaging.** Skill outputs that mention "since last time" or "your previous run" must correspond to actual prior state (file existing, journal entry present).
   *Applies when:* any skill in the journey wrote messaging referencing past activity.

3. **[required] No dead ends.** Every skill terminates with one of: a clear next action, an offered skip, or a "you're done" acknowledgement. No transcript should end mid-prompt awaiting input the journey didn't provide.
   *Applies when:* always.

4. **[required] Profile + strategy not silently overwritten.** If a skill writes to `userdata/profile.md` or `userdata/strategy.md`, the transcript must show a confirmation message naming what changed.
   *Applies when:* a skill in the journey wrote to one of those files.

5. **[required] JD link present in the chat row.** New roles surfaced in chat render the live JD URL in the row (e.g. `- Plaid — Senior PM — to apply — https://...`). The file-side halves of this check (meta.md `link:`, research-brief Source line, and their equality) are decided by `scripts/validate_userdata.py` and are not yours to judge — assess only what the chat row shows.
   *Applies when:* `/job-search` or `/evaluate-position` ran in the journey AND surfaced at least one new role in chat.

## How to report findings under this rubric

For each criterion: name the criterion number (1-5), state `PASS`, `FAIL`, or `NOT EXERCISED`, and provide evidence — a quote when PASS or FAIL, a one-line reason ("`/job-search` did not run") when NOT EXERCISED.

When in doubt about scope, prefer `NOT EXERCISED` over `FAIL`. Verdict aggregation only penalises [required] criteria that were in scope.

## Verdict

Zero tolerance on `[required]` criteria that were in scope: **PASS** only if
every one of them passed. A `[required]` criterion that should have been in
scope but was never exercised — the journey was meant to reach `/job-search`
and didn't — is a **FAIL**, not a skip. `[opportunistic]` criteria never
affect the verdict.

## Worked examples

**Violation — the skill wrote a file and said nothing.**
`/job-search` appends `## Companies of interest` to `profile.md`, verified on
disk, and no chat line mentions it. Criterion 4 exists because a silent write
to a user's own file is indistinguishable from data loss when they next open
it. The write succeeding is not the criterion; the confirmation is.

**Violation — a required criterion that never got its chance.**
The journey was meant to reach `/job-search` and terminated during `/setup`, so
criterion 5 (JD link in the chat row) was never exercised. That is a FAIL, not
a NOT EXERCISED: the precondition should have been met, and reporting it as
out-of-scope would hide a journey that didn't finish.

**Not a violation — a criterion whose precondition genuinely never held.**
`/job-search` was not part of this journey at all, so criterion 5 is NOT
EXERCISED and does not count against the verdict. The distinction from the case
above is whether the journey was *supposed* to get there.

**Not a violation — the right thing done in the wrong words.**
Criterion 1 asks for a context-aware next-step nudge. A nudge that names the
user's actual state in plain language passes even if it doesn't match the
phrasing in `recommended-flow.md`. Conformance is about the contract, not the
wording — wording belongs to tone.
