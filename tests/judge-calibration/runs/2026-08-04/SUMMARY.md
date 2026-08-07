# Test run — 2026-08-04

Verifying v0.4.0 (working tree at `c32040d`) — staged run, journey 1 of a possible 4.

**Code under test:** `<workspace>/plugin`, NOT the installed
plugin (which is a stale `0.3.0-beta.5` June snapshot lacking `cv-extraction.md`).
Orchestrated manually so `${CLAUDE_PLUGIN_ROOT}` resolves to the working tree; the
marketplace-registration route in the handoff was not needed and was not used.

| Journey | Verdict | Hard | Spec gaps | Soft | Critiques |
|---|---|---|---|---|---|
| cold-start-cv | PASS | PASS | 14/14 req | 0 | 3 |
| cold-start | PASS (with 1 finding) | 1 finding | 17/17 req in scope | 2 | — |
| active-loop | not run | — | — | — | — |
| edge-recovery | not run | — | — | — | — |

`cold-start` completed `/setup` (no-CV path) and a full live `/job-search` sweep:
51 candidates discovered across 10 site-scoped queries, 25 fetchable and scored,
25 filed across 21 companies. `/dashboard` and `/today` were not re-run — `/today`
against a freshly written profile was verified independently as handoff check §4.7.

The sweep turn suffered two infrastructure failures (API connection drop, then a
600s stall watchdog once the agent's context held the whole conversation plus all
candidate data). Neither is a plugin fault. Filing was completed by a fresh
narrowly-scoped agent using the scoring output already produced.

Findings from `cold-start`:

- **Invented attribution (real).** The user gave an employer for proof point 1 only.
  The Mode A draft anchored BOTH proof points to "Current fintech (Series B)",
  fabricating the employer for #2. Same fabrication class the state guardrails target.
- **Locked-wording paraphrase (fidelity).** Turn 1 rewrote the `cv-extraction.md`
  drop prompt and invented a "no CV" escape the locked wording does not offer.
  Plausibly sub-agent drift rather than a code defect — the harness documents
  sub-agent fidelity drift as a known limitation.
- **Third-person drift in drafts (soft, recurring).** Both journeys produced
  positioning copy in the third person about the user ("reads her own data",
  "Currently owns growth pricing"), which also assumes the user's pronouns. The CV
  and the user's own input are first person.

Confirmed working in `cold-start` that nothing had tested before:

- `/job-search` Phase 0 step C **case 1** — heading absent → asked once, verbatim,
  and wrote `## Companies of interest` to `profile.md` in the documented bullet
  shape. This is the migration that moved the question out of `/setup`.
- `/setup` never asked about companies of interest.
- Steps 5, 7 and 8 stayed option-based selects with no CV present.
- Timezone override applied (`Europe/London` over the detected `<host-timezone>`).
- Two proof points requested as 3-5 did NOT get padded with an invented third.
- A banned superlative in the user's own words ("Depth") was stripped from the draft.
- The snapshot `.gitkeep` fix works — reset left `git status` clean.

See per-journey `.judge.md` files for details.

## Manual checks (release handoff §4.7-§4.9)

| Check | Result |
|---|---|
| §4.7 CV path downstream (`/today` reads CV-derived profile) | PASS |
| §4.8 `/setup` re-run mode | FAIL — one self-contradiction, two ambiguities |
| §4.9 static checks (4 greps) | PASS |
| pytest suite (120 tests) | PASS |
| Privacy gate | PASS — zero hits |
| `${CLAUDE_PLUGIN_ROOT}` path resolution (30 paths) | PASS |
| Template placeholder / Maya-example key parity | PASS |

## Files in this run

- `maya-cold-start-cv.md` (transcript, 13 turns of a 24-turn budget)
- `maya-cold-start-cv.judge.md` (findings + orchestrator addendum covering §4.7/§4.8)

## Candidate memory entries

Patterns worth promoting into `plugin/memory.md` if they reflect a real lesson
rather than a one-off:

- **2026-08-04** — Re-run mode contradicts itself on whether the tier rubric is in scope
  - Journey: manual check §4.8 (no journey covers re-run mode)
  - Surfaced in: this test run
  - Watch for: instructions that describe the same loop twice in different sections;
    `setup/SKILL.md:270` and `:276` disagree and are six lines apart. Found by executing
    the skill, not by reading the diff — the same detection method that caught the four
    Important defects during the v0.4.0 build review.

- **2026-08-04** — Synthetic personas can import real personal data from the environment
  - Journey: cold-start-cv
  - Surfaced in: this test run
  - Watch for: `simulator-prompt.md` forbids inventing facts but not importing real ones.
    In one run, the simulator pulled a real email address out of the host environment
    into the transcript before it was caught and corrected. Any run can silently write
    real PII into `userdata/test-runs/`.

- **2026-08-04** — Persona proof-point list narrower than the CV fixture causes false FAILs
  - Journey: cold-start-cv
  - Surfaced in: this test run
  - Watch for: `personas/maya.md` lists 2 proof points; `empty-with-cv/cv.md` carries 6.
    A simulator obeying "do not invent facts" disowns legitimate CV content, which reads
    as the plugin having fabricated it.

## Live-sweep findings (`/job-search`, first real run of this code)

Working, verified on disk:

- 25/25 filed `meta.md` carry a real `http(s)` `link:` — no placeholders
- 25/25 carry every required key; `status: new`; zero forbidden drift keys
- `applications.md` Link column populated with real URLs; chat rows render the URL inline
- Multi-role companies correctly used role-slug subfolders (FINN, Mercury, Plaid, Remote)
- Anti-fabrication held under pressure: unfetchable postings were NOT scored or filed.
  The Plaid Lever posting returned HTTP 403; the scorer checked Lever's public API,
  found the board dead, and recorded "not scored to avoid fabrication" with null
  scores. A Hopper posting was checked against Ashby's API, found absent, and dropped.
  Title drift was reported honestly (PawaPay, Fresha) rather than silently accepted.
- Companies-of-interest seeding demonstrably worked: Lendable — one of the four
  seeded companies — produced the top-scoring role of the run (P0, 14).

New findings:

- **Company folder names carry spaces and parentheses** — `Bitpanda Technology
  Solutions`, `Lead (Lead Bank)`, `Remote (remote.com)`. Every shell path touching
  these must be quoted, and the parenthetical forms are scorer disambiguation rather
  than clean company names. `dedup-normalization.md` governs name normalisation for
  dedup; it does not appear to constrain the on-disk folder name. Worth a rule.
- **Discovery surfaces a high proportion of dead postings.** Of 51 candidates, 26
  could not be fetched — 403s, 404s, and postings verified as removed via the ATS's
  own public API. `site:`-scoped WebSearch returns stale index entries. The SKILL.md
  treats Playwright link-liveness verification as optional; on this evidence it is
  closer to load-bearing. The scoring pass absorbed the cost by verifying against
  Ashby/Greenhouse/Lever APIs, which is why nothing bad was filed — but that is the
  scorer compensating for Discovery.
