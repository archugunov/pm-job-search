# Findings — maya-cold-start

**Run date:** 2026-08-07
**Snapshot:** empty
**Judge:** replay under the restructured rubrics (2026-08-12), one call per rubric.
Replaces the pre-restructure reading; that is in git history.

## Lint

    No lint findings.
    NOT CHECKED: lint.hardcoded-cadence (no userdata tree supplied)

## Groundedness

### Evidence

| turn | claim | source | grounded |
|---|---|---|---|
| 1 | `userdata/` has been created | file: `userdata/` (created by this run; snapshot was empty) | yes |
| 1 | A CV is accepted at `cv.md`, `cv.txt`, or `cv.pdf` in that folder | file: setup SKILL.md executed this run | yes |
| 2 | No CV is available, so the long path applies | user: turn 2 | yes |
| 2 | Onboarding is nine steps | file: setup SKILL.md executed this run | yes |
| 2 | Nothing is locked in; the flow can be rerun | file: setup SKILL.md executed this run | yes |
| 7 | The user's timezone is `Europe/London` | user: turn 5 (`London, UK`), offered for confirmation and override rather than asserted | yes |
| 11 | Positioning can be filled in later | file: setup SKILL.md executed this run | yes |
| 11 | `/pm-job-search:setup --refresh` resumes where the user left off | file: setup SKILL.md executed this run | yes |
| 11 | London is the on-site option offered | user: turn 5 | yes |

Excluded as non-claims: the illustrative role titles in turn 8, industry examples in turn 9, the two positioning options in turn 10, and the salary-format examples in turn 12 — generic illustrations naming no entity in the user's world, plus the assistant's questions and framing throughout.

### Findings

No findings.

### Verdict

**PASS** — every factual claim in the transcript traces to the user's own earlier answers or to files this run created or executed against, with no company, number, date, or file content asserted from outside the run.

## Coherence

### Findings

- **turn 10:** "A. Write it now — you paste 1-3 sentences about yourself, I draft positioning, proof points and a moat from it." — Rule 1: "positioning" is defined in the preceding line ("who you are and what you're best at") but "proof points" and "moat" arrive undefined, so the user weighing option A is left holding two plugin terms they cannot evaluate; mitigated by the fact that the A/B choice itself (write now vs. fill in later) is legible without them.

### Verdict

**PASS** — The onboarding runs as one clean thread with each question grounded in the answer before it (timezone inferred from "London, UK", location options naming London, the fill-in-later path tied back to a rerunnable command), and the single ungrounded moment is a pair of terms inside an option whose actual decision axis is stated plainly, not a jump or contradiction the user would have to stop and reread.

## Conformance

### Findings

- **Cross-journey 1 (end-of-run nudge) — FAIL.** turn 12: "What salary band are you aiming for? Whatever shape works — '£90-110K' or '$190-230K base + equity', or skip if you'd rather not anchor a number yet." — this is the last assistant output in the transcript; the journey was scripted to run through `/job-search`, `/dashboard` and `/today` and terminate on the brief, so the end-of-run nudge was in scope and was never produced.
- **Cross-journey 2 (no prior-state leak) — NOT EXERCISED.** No skill output in the run references past activity ("since last time", "your previous run").
- **Cross-journey 3 (no dead ends) — FAIL.** turn 13: "£90-110K for an IC role, £115-140K if it's proper leadership scope." — the user answered turn 12's prompt and the transcript stops there; `/setup` never terminated with a next action, an offered skip, or a "you're done" acknowledgement.
- **Cross-journey 4 (profile + strategy not silently overwritten) — NOT EXERCISED.** `/setup` stopped at the salary question, before any write to `profile.md` or `strategy.md`, so no write occurred that would need a confirmation message.
- **Cross-journey 5 (JD link present in the chat row) — FAIL.** turn 12: "What salary band are you aiming for? ..." — the run ended inside `/setup`; the journey's scripted step 2 was `/pm-job-search:job-search`, so a new-role chat row was in scope and never rendered.
- **Spec: `/setup` precreated `userdata/` before the CV prompt — PASS.** turn 1: "I've created `userdata/` for you — drop your CV there as cv.md, cv.txt, or cv.pdf. Say 'ready' when it's in."
- **Spec: one residence question and one geography question, distinct — PASS.** turn 4: "Where are you based? City + country works (e.g. London, UK)." and turn 11: "Where are you looking? - On-site in London - Remote - Both - Other (free text)" — two separate asks, not redundant.
- **Spec: `/setup` did NOT ask about companies of interest — PASS.** turn 9: "What industries are you looking at? E.g. healthcare, climate tech, education, enterprise SaaS. Comma-separated." — the targeting block asks roles then industries and moves on; no companies-of-interest ask appears anywhere in the run.
- **Spec: `/job-search` asked companies-of-interest on first run and wrote `## Companies of interest` to `profile.md` — FAIL.** turn 12: "What salary band are you aiming for? ..." is the final assistant turn; `/job-search` was the journey's next scripted step and never ran.
- **Spec: `/setup` did NOT show the weekly-reflection nudge — NOT EXERCISED.** `/setup` never reached its closing block, where that nudge would have appeared.
- **Spec: `/setup`'s automation prompt was 2-step — FAIL.** The run stopped at the salary question (turn 12), so the automation prompt — a later step of `/setup` the journey was meant to walk — was never rendered.
- **Spec: `/job-search` auto-filed at least one role with `status: new` — FAIL.** `/job-search` never ran; the transcript ends inside `/setup` at turn 13.
- **Spec: the chat rendering of the application row included the URL inline — FAIL.** No application row was ever rendered, because `/job-search` never ran.
- **Spec: `/today`'s first run skipped the input-loop prompt — NOT EXERCISED.** `/today` never ran, so no input-loop prompt could appear.
- **Spec: `/today`'s brief rendered Heads-up above Pipeline state — FAIL.** turn 12: "What salary band are you aiming for? ..." — the journey's scripted step 5 was `/pm-job-search:today` and no brief was ever printed.
- **Spec: `/today` did NOT include a hardcoded founder-outreach number — NOT EXERCISED.** `/today` never ran, so no brief content exists to inspect.
- **Spec: each skill's closing message included a context-aware next-step nudge — FAIL.** No skill in the run reached a closing message; `/setup` is still mid-questionnaire at turn 12 and the transcript ends.
- **Spec: with no CV, `/setup` still walked all nine steps and never claimed to have read a CV — FAIL.** turn 2: "No CV — we'll do it the long way then. Same questions, you just type more." — the no-CV acknowledgement is clean, but only Steps 1-6 (name through salary) were walked; Steps 7-9 never ran.
- **Spec: `/setup` offered timeline as a bucket choice and `strategy.md` holds a concrete date — FAIL.** The timeline step was never reached; the last question asked was salary (turn 12).
- **Spec: `/setup` offered hard filters as a multi-select — FAIL.** The hard-filters step was never reached.
- **Spec: with no CV, Steps 5, 7 and 8 were still option-based selects — FAIL.** turn 11: "Where are you looking? - On-site in London - Remote - Both - Other (free text)" shows Step 5 held the pick-not-write shape, but Steps 7 and 8 never ran, so the criterion is only one-third satisfied.

### Verdict

**FAIL** — 13 in-scope `[required]` criteria failed: the run aborted inside `/setup` at the salary question, so `/setup` never closed and the journey's three remaining skills (`/job-search`, `/dashboard`, `/today`) never ran, leaving every criterion downstream of Step 6 unmet rather than out of scope.

## Tone

### Findings

- **turn 2:** "OK, let's get you set up. Nine quick steps — none of it's locked in, you can rerun anytime. Ready?" — violates low-effort-first (defaults > prompts): the user already said "go ahead without it", so the extra "Ready?" gate burns a full round-trip on a confirmation the previous answer already gave.

### Verdict

**PASS** — the voice is consistently plain, terse and direct across all twelve turns (single asks, auto-detected timezone confirmed rather than asked, skip offered on every optional field, no hedging or motivational register), and the one nitpick is a redundant confirmation prompt no real user would read as an off voice.

## Verdict

    Lint:          PASS
    Groundedness:  PASS
    Coherence:     PASS
    Conformance:   FAIL (13)
    Tone:          PASS

    Gate: Lint AND Groundedness AND Conformance

**Overall: FAIL**
