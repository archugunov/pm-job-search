---
name: sweep-smoke
persona: maya
snapshot: empty
max_turns: 16
---

## Goal

The standalone `job-sweep` plugin, end to end: three-question onboarding, a first
sweep, then a second sweep that must suppress everything the first one showed.
The suppression is the point — it is the single feature separating this from a
novelty.

## Opening message

`/job-sweep:sweep`

## Mid-journey instructions to the simulator

1. When the first run offers "drop a CV or answer three questions", choose the
   three questions — this journey covers the no-CV path deliberately.
2. Answer the three in persona: senior-PM titles, fintech / consumer credit,
   London hybrid or EMEA remote.
3. After the first sweep prints its summary, send exactly: `/job-sweep:sweep`
4. After the second sweep's summary, acknowledge briefly and stop.

## Termination

Stop when the SECOND sweep has printed a summary AND the simulator has
acknowledged it.

## Spec criteria (judge checks)

Each criterion is tagged `[required]` (must be exercised AND pass) or `[opportunistic]` (advisory). See `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/rubrics/conformance.md` for verdict aggregation rules.

- **[required]** First run created `job-sweep/` and wrote `job-sweep/profile.md` with `target_titles`, `target_industries` and `geography`
- **[required]** The three questions were asked one per message, not bundled
- **[required]** Nothing was written outside `job-sweep/` — no `userdata/`, no company folder, no `meta.md`
- **[required]** The sweep never scored a tier, never assigned a status, and never claimed to track an application
- **[required]** Every role shown carries a real URL that appeared in a search result — no invented companies, roles or links
- **[required]** `job-sweep/seen-roles.jsonl` exists after run one, one JSON object per line, each with exactly `company_key`, `strict_key`, `base_key`, `url_key`, `raw_title`, `first_surfaced`
- **[required]** The second run did NOT re-ask onboarding — `profile.md` existed, so it swept directly
- **[required]** The second run suppressed the roles shown in run one; any role appearing in both runs' output files is a failure unless it is under "Possible repeats"
- **[required]** The second run's chat summary stated how many already-seen roles were suppressed
- **[required]** Roles were bucketed strong / possible / edge, with no weighted score or tier notation anywhere
- **[required]** The run closed with exactly one line pointing at the full plugin — not repeated mid-run
- **[opportunistic]** A posting verified as closed was dropped rather than shown

## Note on running this journey

This journey exercises the `job-sweep` plugin at `plugin-sweep/`, not the full
plugin at `plugin/`. The harness inlines `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md`
per Phase 3 — for this journey that resolves to
`plugin-sweep/skills/sweep/SKILL.md`. If the orchestrator is the installed
pm-job-search plugin, it will not find that path; run this journey against the
working tree, resolving `${CLAUDE_PLUGIN_ROOT}` to `plugin-sweep/`.
