# Findings — maya-cold-start-cv

**Run date:** 2026-08-04
**Snapshot:** empty-with-cv

## Verdict

**Overall: PASS**

- Hard violations: PASS
- Spec gaps: PASS
- Soft issues: 0 (advisory)
- Open critiques: 3 (advisory)

## Hard violations (lint checklist)

No hard violations found. The SCHEMA VALIDATION block scopes to `meta.md` files in `userdata/companies/`, none of which exist in this journey (it stops after `/setup`, before any company is filed) — "not applicable," so no Rule 7 findings apply.

## Soft issues (TONE voice + UX)

No soft issues found. Every locked-wording prompt in the transcript (Turn 1 opening line, Turn 2 facts confirmation, Turn 3/4 evidence-line asks, Turn 6 geography ask, Turn 7 salary ask, Turn 8 timeline ask, Turn 9 hard-filters ask, Turn 10 CLAUDE.md guard, Turn 11 closing summary + positioning offer, Turn 12 automation offer) matches `plugin/skills/setup/SKILL.md`'s verbatim wording, and the drafted positioning/proof-points/moat in Turn 5 contain no banned superlatives, clichés, or invented numbers.

## Spec gaps

### Required (14/14 in scope passed)

- **Cross-journey 1 — End-of-run nudge:** PASS — Turn 13: "Setup done. Run `/pm-job-search:job-search` to seed your applications list — or `/pm-job-search:today` right now if you'd rather see a daily brief first." This is the exact state-aware nudge `references/recommended-flow.md` prescribes for "profile.md just written, no companies in userdata/companies/," not a generic parrot of the full canonical order.
- **Cross-journey 2 — No prior-state leak in messaging:** NOT EXERCISED — this is a fresh-install run with no prior state; no assistant turn references "since last time" or a previous run, so the precondition was never met.
- **Cross-journey 3 — No dead ends:** PASS — Turn 13 closes with two concrete next-action options; the transcript does not end mid-prompt.
- **Cross-journey 4 — Profile + strategy not silently overwritten:** PASS — Turn 11 names both writes and describes their contents.
- **Cross-journey 5 — JD link present in three places:** NOT EXERCISED — `/job-search` did not run; the journey is scoped to stop after `/setup`.
- **CV detected without asking to drop one:** PASS — Turn 1: "Got your CV — I'll fill in what I can and you just correct me."
- **Facts as a single confirmation line:** PASS — Turn 2 presents name, city, email and LinkedIn on one line with one ask.
- **Corrected email applied without re-asking the whole line:** PASS — Turn 3: "Email updated to maya.patel.pm@example.com." then proceeds directly to target titles.
- **Target titles as multi-select with evidence line:** PASS — Turn 3 carries "from Senior PM at Brightline Credit, Lead PM at Lumio, Lead PM at NorthLoop".
- **Target industries as multi-select with evidence line:** PASS — Turn 4 carries the per-employer evidence line.
- **Deselected title absent, user-added title present in profile.md:** PASS — `profile.md` line 21 reads `target_titles: [Lead PM, Head of Product, Director of Product]`; Senior PM and Group Product Manager absent, Director of Product present.
- **No standalone name/city/email questions when CV supplied them:** PASS — no such turns exist.
- **Nothing invented to fill a profile.md field:** PASS — all six proof points trace to the CV fixture; every non-extractable field was asked, per `cv-extraction.md`.
- **`/setup` did NOT ask about companies of interest:** PASS — absent from the transcript.
- **profile.md frontmatter key/type parity with `examples/maya/profile.md`:** PASS — identical key set and matching YAML types; only inline-vs-block list formatting differs, which the criterion explicitly permits.
- **Salary was the only step with no option set at all:** PASS, with a criterion-drafting note. The user took Step 5's geography "Other" escape, which is by-design per `setup/SKILL.md` Step 5. The criterion's exception list ("Steps 2, 3 and 8") omits Step 5 — an incomplete criterion, not a code regression. Correct the exception list rather than the code.

### Opportunistic (1/1 in scope passed)

- **Positioning draft (Mode B) ran without re-prompting for a CV:** PASS — Turn 5 goes straight into the CV-derived draft.

## Open critique

- Evidence-line ordering is inconsistent between the two Tier-2 inference asks: Turn 3 lists roles oldest-to-newest, Turn 4 newest-to-oldest. Harmless, but reads as careless when skimmed back-to-back.
- Turn 10 opens with a passive status recap before pivoting to an active y/n gate in the same message; a skimming user could read the turn as an FYI rather than a question.
- The Turn 5 positioning draft is by far the densest turn — two paragraphs, six bullets and a moat line, all behind one edit/accept/discard decision. Spec-compliant, but a marked step up in cognitive load.

---

## Orchestrator addendum — findings outside the judge's scope

These come from the two manual checks the release handoff mandates (§4.7, §4.8),
which sit outside the judged transcript.

### §4.7 — CV path downstream (PASS)

`/today` read the CV-derived `profile.md` and `strategy.md` with no parse failure,
no missing key and no malformed YAML. Heads-up rendered above Pipeline state, the
first-run input prompt was correctly suppressed, and no hardcoded founder-outreach
number appeared. This closes the gap the handoff flagged as entirely unproven.

Two spec gaps in `/today` surfaced by the same run, both minor:

- The weekly-target action ("Send 12 more applications this week (0/12)") fires on a
  literally empty pipeline, before `/job-search` has ever run. The SKILL.md gates this
  only on "a target is set", not on the pipeline existing.
- No tie-break is defined when `warm_outreach` and `applications` are both at a 100%
  relative gap, and nothing defines what Pipeline state should render when zero
  `meta.md` files exist. Both were resolved by the agent's judgement, not by the spec.

### §4.8 — `/setup` re-run mode (FAIL — one real defect)

The re-run entry path works: it enters re-run mode correctly, does not re-read the
CV, never asks about companies of interest, and modified no file during inspection
(verified by checksum before and after).

**Defect — self-contradiction on the tier rubric.** `setup/SKILL.md` line 270 states
the re-run mode "does NOT include the tier rubric either", while line 276 instructs
the re-run loop to "iterate fields in the same order as the fresh walk (Steps 1-8 +
tier rubric)". The two are six lines apart and cannot both be executed. An
implementer must guess. This is in shipped v0.4.0 code.

Two further ambiguities in the same section, both unresolved by the text:

- The re-run loop has no locked user-facing wording, unlike Steps 1-8, despite
  `TONE.md` mandating verbatim prompts. The agent had to author its own opening line.
- "Field" granularity is undefined for Step 1, which bundles five values. Re-run may
  mean one combined keep/update/skip or five separate ones; both readings are
  defensible and they produce materially different flows.

### Harness defects (not plugin defects)

- `personas/maya.md` `journey_fit` omits `cold-start-cv`, though that journey declares
  `persona: maya`. A `--persona maya` invocation would silently skip it.
- `simulator-prompt.md` forbids *inventing* facts but never forbids importing *real*
  data from the agent's environment. The simulator injected a real personal email
  address into this run before being corrected. A synthetic-persona harness should
  forbid real personal data explicitly.
- `personas/maya.md` lists only "2 strong proof points you lean on" while the
  `empty-with-cv` CV fixture carries six. A simulator obeying rule 2 disowns
  CV-derived content as invented — it did exactly that here, and would have produced
  a false FAIL on the "nothing was invented" criterion had it not been corrected.
- `tests/snapshots/contrarian-messy/` newest date is 2026-05-22, eleven weeks stale.
  Re-date before running `edge-recovery`.
