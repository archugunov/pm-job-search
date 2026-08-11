# Findings — maya-cold-start

**Run date:** 2026-06-04
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
| 1 | The setup flow consists of "Twelve quick questions" | file: the `/pm-job-search:setup` instructions the run is executing | yes |
| 1 | The answers are not locked in and setup can be rerun | file: the `/pm-job-search:setup` instructions the run is executing | yes |
| 4 | The user's timezone is `Europe/London` | user: turn 4 ("London, UK"), offered for confirmation rather than asserted | yes |
| 9 | `/pm-job-search:setup --refresh` resumes where the user left off | file: the `/pm-job-search:setup` instructions the run is executing | yes |
| 9 | The roles question is question 7 of the flow ("Q7:") | file: the `/pm-job-search:setup` question sequence (consistent with the six prior numbered asks; the turn-4 timezone check is a confirmation, not a numbered question) | yes |

No other assistant content in turns 1-10 asserts anything checkable: the location options in turn 7, the A/B/C positioning options in turn 8, and the example senior-PM titles in turn 9 are offers and generic role vocabulary naming no specific entity, so they are not claims and are deliberately kept out of the table.

### Findings

No findings.

### Verdict

**PASS** — every claim in the transcript traces to the user's own earlier answers or to the setup instructions the run was executing; the transcript never names a company, pipeline item, file's contents, date, or number that no source in the run supplied.

## Coherence

### Findings

- **turn 9:** "Q7: What roles are you targeting?" — Rule 1 / Rule 5: a question-numbering scheme appears for the first time at turn 9 after eight unlabelled questions ("What's your name?", "Where are you based?", "What's the best email for you?"), so the user is left holding a label that points at a sequence they have never been shown and cannot map onto the "Twelve quick questions" promised in turn 1.

### Verdict

**PASS** — The conversation runs as one clean linear thread: each question follows from the last, the timezone guess is derived from the city the user just gave, the skip at turn 8 is acknowledged before moving on, and the only blemish is a single stray question label the user can roughly infer past.

## Conformance

### Findings

- **Criterion 1 — end-of-run nudge — FAIL.** turn 9: "Fill in later — `/pm-job-search:setup --refresh` picks up where you leave it." is a mid-flow aside, not a close; the run ends at "## Loop terminated / Transcript stopped at turn 10", so the journey never reached the termination it was designed to reach and no final skill ever produced a state-aware next-step nudge.
- **Criterion 2 — no prior-state leak — NOT EXERCISED.** No skill in the nine assistant turns wrote messaging referencing past activity; turn 9's "picks up where you leave it" points forward, not back.
- **Criterion 3 — no dead ends — NOT EXERCISED.** No skill reached a terminating message at all — the run was cut mid-`/setup` by the harness ("Transcript stopped at turn 10 to verify the judge mechanism"), so terminal behaviour was never observable; the non-termination itself is charged under criterion 1.
- **Criterion 4 — profile + strategy not silently overwritten — NOT EXERCISED.** `/setup` never reached its write step; no turn mentions writing `profile.md` or `strategy.md`.
- **Criterion 5 — JD link present in the chat row — FAIL.** The journey was designed to reach `/job-search` (mid-journey instruction 2: "send: `/pm-job-search:job-search`") and never did — "full /setup wrap, /job-search, /dashboard, /today were NOT exercised" — so a required criterion that should have been in scope never got its chance.
- **Spec — `/setup` precreated `userdata/` (or confirmed it existed) before the CV prompt — FAIL.** turn 8: "- A. Drop your CV (recommended)" is issued with no preceding line anywhere in turns 1-8 confirming `userdata/` was created or already present, on a `snapshot: empty` run where it could not have existed.
- **Spec — one residence question and one distinct geography question — PASS.** turn 3: "Where are you based? City + country works (e.g. London, UK)." and turn 7: "Where are you looking? / 1. On-site in London / 2. Remote / 3. Both" are distinct, non-redundant asks.
- **Spec — `/setup` did NOT ask about companies of interest — NOT EXERCISED.** No such ask appears in the nine turns that ran, but `/setup` was cut off at "Q7: What roles are you targeting?", before the steps where the ask could have surfaced.
- **Spec — `/job-search` asked companies-of-interest on first run and wrote `## Companies of interest` — FAIL.** "`/job-search` ... were NOT exercised" — the journey was supposed to run `/job-search` after `/setup` wrapped and never reached it.
- **Spec — `/setup` did NOT show the weekly-reflection nudge — NOT EXERCISED.** `/setup` never reached its closing sequence, which is where the nudge would have appeared.
- **Spec — `/setup`'s automation prompt was 2-step (y/n, then time) — FAIL.** The run stopped at turn 9's "Q7: What roles are you targeting?", so the automation prompt — a documented later step of `/setup` the journey was meant to walk — was never issued.
- **Spec — `/job-search` auto-filed at least one role with `status: new` — FAIL.** "full /setup wrap, /job-search, /dashboard, /today were NOT exercised"; the journey was designed to file roles and did not.
- **Spec — chat rendering of the application row included the URL inline — FAIL.** No role row was ever rendered; the transcript ends at turn 10's "Head of Product, Lead PM, Senior PM" with `/job-search` unreached.
- **Spec — `/today`'s first run skipped the input-loop prompt — FAIL.** "`/today` were NOT exercised" — the journey's termination condition was `/today`'s brief printing, and it never ran.
- **Spec — `/today`'s brief rendered Heads-up above Pipeline state — FAIL.** No brief was produced; the journey terminated at turn 10 without reaching `/today`.
- **Spec — `/today` did NOT include a hardcoded founder-outreach number — FAIL.** `/today` never ran, so a required criterion the journey was built to exercise went unexercised.
- **Spec — each skill's closing message included a context-aware next-step nudge — FAIL.** No skill in the transcript produced a closing message at all; turn 9 ends with "Q7: What roles are you targeting? ... List as many as you'd take, comma-separated." and the run stops.
- **Spec — with no CV, `/setup` still walked all nine steps and never claimed to have read a CV — FAIL.** `/setup` reached only "Q7: What roles are you targeting?" before "## Loop terminated"; the nine-step walk was not completed (it did correctly avoid claiming to have read a CV, accepting "C" at turn 9 with "Fill in later").
- **Spec — timeline offered as a bucket choice, and `strategy.md` holds a concrete `YYYY-MM-DD` — FAIL.** The timeline step was never reached — the last assistant turn is turn 9's roles question — so a required step the journey was meant to exercise never ran.
- **Spec — hard filters offered as a multi-select — FAIL.** The hard-filters step was never reached; the transcript ends at turn 10 with `/setup` still at the roles question.
- **Spec — with no CV, Steps 5, 7 and 8 still option-based selects — FAIL.** Step 5 passed (turn 7: "1. On-site in London / 2. Remote / 3. Both / 4. Other (free text)"), but Steps 7 and 8 were never reached, so the pick-not-write shape was only one-third demonstrated.

### Verdict

**FAIL** — the run stopped nine assistant turns in, at `/setup`'s roles question, so fifteen `[required]` criteria the journey was explicitly designed to exercise (the `/setup` tail, `/job-search`, and all of `/today`) never got their chance, and conformance is zero-tolerance.

## Tone

### Findings

- **turn 9:** "Q7: What roles are you targeting?" — internal question numbering leaked into user-facing copy; the user never saw Q1-Q6 labelled, so the label is the assistant narrating its own script rather than speaking plainly.
- **turn 1:** "Twelve quick questions — none of it locked in, you can rerun anytime. Ready?" — a preamble turn that spends a full round trip gating on consent the user already gave by invoking the command; defaults beat prompts here.

### Verdict

**PASS** — the voice is consistently direct, contracted and skip-friendly ("Where are you based?", "LinkedIn URL? Or skip.", timezone inferred then confirmed); the stray `Q7:` label and the opening "Ready?" gate are nitpicks a user would shrug past, not a moment where the product sounds like something else.

## Verdict

    Lint:          PASS
    Groundedness:  PASS
    Coherence:     PASS
    Conformance:   FAIL (15)
    Tone:          PASS

    Gate: Lint AND Groundedness AND Conformance

**Overall: FAIL**
