# Findings — contrarian-edge-recovery

**Run date:** 2026-06-07
**Snapshot:** contrarian-messy
**Judge:** replay under the restructured rubrics (2026-08-12), one call per rubric.
Replaces the pre-restructure reading; that is in git history.

## Lint

    turn 1: lint.jargon — 'status:' (2×) in user-facing text: "> - Duplicate company entry: `acmecorp/` (status: to_apply, applied 2026-05-20 per journal…"
    turn 5: lint.jargon — 'meta.md' in user-facing text: "…he content, I'll run the tier scoring and write the meta.md + research-brief.md as normal."
    turn 5: lint.jargon — 'research-brief.md' in user-facing text: "…he content, I'll run the tier scoring and write the meta.md + research-brief.md as normal."
    NOT CHECKED: lint.hardcoded-cadence (no userdata tree supplied)

## Groundedness

### Evidence

Snapshot dates are rebased (`contrarian-messy/README.md`: "Dates here are rebased by `make rebase-fixtures`; the anchor is the newest journal entry"), so date claims are checked as offsets from the journal anchor, not as literals. Every dated claim below resolves against anchor = the journal's "Applied to AcmeCorp" entry: stalecorp = anchor−19, acmecorp first_seen = anchor−2, acme-corp first_seen = anchor+2, `target_date` = anchor+104. All four hold exactly for a run-time anchor of 2026-05-20.

| turn | claim | source | grounded |
|---|---|---|---|
| 1 | Brief is dated 2026-06-07 | metadata: `date: 2026-06-07` | yes |
| 1 | User is named Sam | file: `profile.md` (`name: Sam Carter`) | yes |
| 1 | Two folders `acmecorp/` and `acme-corp/` exist for the same company | file: `companies/acmecorp/meta.md`, `companies/acme-corp/meta.md` (both `company: AcmeCorp`) | yes |
| 1 | Position strings differ: "Senior PM" vs "Senior Product Manager" | file: both `meta.md` `position:` fields | yes |
| 1 | StaleCorp has been in `to_apply` since 2026-05-01 — 37 days | file: `companies/stalecorp/meta.md` (`status: to_apply`, `first_seen`/`last_activity` = anchor−19 = 2026-05-01; 37 days to the 2026-06-07 run date) | yes |
| 1 | StaleCorp is tier 1, score 13 | file: `companies/stalecorp/meta.md` | yes |
| 1 | StaleCorp is the strongest scored role | file: stalecorp score 13 > acmecorp score 11; acme-corp `tier: unscored` | yes |
| 1 | StaleCorp link is `https://example.com/stalecorp-senior-pm` | file: `companies/stalecorp/meta.md` (`link:`) | yes |
| 1 | Positioning is empty | file: `profile.md` (`## Positioning` → `_None yet._`) | yes |
| 1 | Companies of interest is empty | file: `profile.md` (`## Companies of interest` → `_None yet…_`) | yes |
| 1 | salary band is "tbd" | file: `profile.md` (`salary_band: "tbd"`) | yes |
| 1 | `acmecorp/` status is `to_apply`; journal records the application on 2026-05-20 | file: `companies/acmecorp/meta.md` (`status: to_apply`); file: `journal.md` (anchor entry "Applied to AcmeCorp.") | yes |
| 1 | `acme-corp/` status is `new`, first seen 2026-05-22 | file: `companies/acme-corp/meta.md` (`status: new`, `first_seen` = anchor+2) | yes |
| 1 | Both entries carry `company: AcmeCorp` | file: both `meta.md` frontmatter | yes |
| 1 | The journal says you already applied | file: `journal.md` | yes |
| 1 | StaleCorp has no recorded activity in 37 days | file: `companies/stalecorp/meta.md` (`last_activity` = `first_seen`); file: `journal.md` (no StaleCorp entry) | yes |
| 1 | `Anti-goals` and `Checkpoints` are placeholders | file: `strategy.md` (both `_None set._`) | yes |
| 1 | `weekly_targets` sets only `applications: 2`, no outreach target | file: `strategy.md` | yes |
| 1 | No `target_offer_date` in strategy; the file has `target_date: 2026-09-01` | file: `strategy.md` (`target_date:` present, `target_offer_date:` absent; value = anchor+104 = 2026-09-01) | yes |
| 1 | AcmeCorp Senior PM — to_apply — tier 2, score 11 — `https://example.com/acmecorp-senior-pm` | file: `companies/acmecorp/meta.md` | yes |
| 1 | AcmeCorp Senior Product Manager — new — unscored — `https://example.com/acmecorp-senior-product-manager` | file: `companies/acme-corp/meta.md` | yes |
| 2 | Dashboard serves at `http://localhost:8765` | file: dashboard skill spec read by the run | yes |
| 3 | Companies of interest is empty in the profile | file: `profile.md` | yes |
| 3 | There are 3 existing companies to recheck | file: `companies/` (acmecorp, acme-corp, stalecorp) | yes |
| 4 | Discovery was skipped | user: turn 4 ("skip") | yes |
| 4 | acmecorp AcmeCorp Senior PM — live (200), `last_seen` updated | fetch: `https://example.com/acmecorp-senior-pm`; file: `companies/acmecorp/meta.md` | yes |
| 4 | acme-corp AcmeCorp Senior Product Manager — live (200), `last_seen` updated | fetch: `https://example.com/acmecorp-senior-product-manager`; file: `companies/acme-corp/meta.md` | yes |
| 4 | stalecorp StaleCorp Senior PM — closed (404), listing taken down | fetch: `https://example.com/stalecorp-senior-pm` | yes |
| 4 | No new roles were filed | user: turn 4 ("skip"); the run filed none | yes |
| 5 | The fetch of `https://example.com/some-role` returned a generic landing page, not a role description | fetch: `https://example.com/some-role` | yes |
| 5 | example.com is the IANA reserved placeholder domain | fetch: `https://example.com/some-role` (the page returned states its reserved-for-examples purpose) | yes |

### Findings

No findings.

### Verdict

**PASS** — every claim traces to a snapshot file, an in-run fetch, or a user turn; the May dates that look wrong against today's fixture files are exactly right once the fixtures' documented date-rebasing is applied (all four dated claims sit at their recorded offsets from the journal anchor, including `target_date` at anchor+104).

## Coherence

### Findings

- **turn 2:** "Opening your job-search dashboard at http://localhost:8765 — you'll see every role you're tracking in one view." followed immediately by "dashboard server can't actually launch from sub-agent context — this would normally open a browser tab." — Rule 4: two adjacent assertions about the same action contradict each other, and the user is left not knowing whether anything is actually running at that URL or whether they should go look.
- **turn 2:** "_Note: dashboard server can't actually launch from sub-agent context — this would normally open a browser tab._" — Rule 1: "sub-agent context" arrives with no grounding anywhere in the run and no stated reason it matters to Sam, so the user is handed an explanation they cannot resolve or act on.
- **turn 1:** top action 3 "Fill in `userdata/profile.md`. Positioning is empty, Companies of interest is empty, salary band is "tbd"." and the heads-up bullet "Profile and strategy are mostly empty. `Positioning`, `Companies of interest`, `Anti-goals`, and `Checkpoints` are all placeholders. `salary_band` is "tbd"." — Rule 3: the heads-up restates the top action near-verbatim rather than adding anything new at the point it appears, and the same doubling happens with the duplicate-AcmeCorp item, so the user reads the same two facts three and four times in one brief.
- **turn 4:** "stalecorp/ — StaleCorp Senior PM — closed (404) — listing taken down" and, in the same turn, "Next step: triage the duplicate AcmeCorp entry, or run /pm-job-search:job-search again later with `## Companies of interest` populated." — Rule 2: turn 1 told Sam to "Either apply today (it's tier 1, score 13 — your strongest scored role)", and turn 4 invalidates that instruction without reconciling it, leaving the morning's second-highest action open with no replacement.

### Verdict

**FAIL** — Turn 2 announces the dashboard as open and then, in the next breath and in terms the user cannot resolve, says it never launched; that is a contradiction Sam would have to stop and reread, and the unreconciled StaleCorp thread compounds the sense that turns are not tracking each other.

## Conformance

### Findings

- **Cross-journey 1 — End-of-run nudge — PASS.** turn 5: "either paste the JD text straight into the chat (title, company, responsibilities, requirements, comp if listed — whatever the posting shows), or send me a working URL to the actual posting" — the closing skill names the user's actual state (unfetchable URL, nothing scored) and gives the two concrete next moves rather than parroting the canonical order.
- **Cross-journey 2 — No prior-state leak in messaging — PASS.** turn 1: "applied 2026-05-20 per journal, status not yet updated" — every backward-looking claim in the brief is attributed to a concrete state source (journal entry, `first seen` date, `to_apply` since 2026-05-01); no "since last time" / "your previous run" phrasing appears anywhere in the transcript.
- **Cross-journey 3 — No dead ends — PASS.** Each of the four skills terminates with an action, not mid-prompt: turn 1 "If you only do one thing today: kill the duplicate AcmeCorp entry"; turn 2 "To add a new role, drop the link to me here and I'll score and file it."; turn 4 "Next step: triage the duplicate AcmeCorp entry, or run /pm-job-search:job-search again later"; turn 5 offers the paste-JD / working-URL recovery path.
- **Cross-journey 4 — Profile + strategy not silently overwritten — NOT EXERCISED.** No skill in the run wrote to `userdata/profile.md` or `userdata/strategy.md`; turn 1 only recommends the user edit profile.md themselves ("Run /setup or edit the file directly").
- **Cross-journey 5 — JD link present in the chat row — NOT EXERCISED.** `/job-search` surfaced no new roles by design after Sam skipped Discovery ("No new roles filed (Discovery skipped)"), and `/evaluate-position` never obtained a posting to file, so no new-role chat row existed to carry a link. The journey deliberately routes to zero new roles, so the precondition genuinely never held.
- **Spec 1 — `/today` ran without crashing despite missing profile sections — PASS.** turn 1 rendered a complete three-section brief and named the gaps rather than failing on them: "Positioning is empty, Companies of interest is empty, salary band is \"tbd\"."
- **Spec 2 — `/today` skipped the founder-outreach line entirely — PASS.** No founder-outreach cadence or progress line appears in the brief; the only reference is a gap note in heads-up, "`weekly_targets` only sets `applications: 2` — no outreach target", which reports the field's absence instead of rendering a target against it.
- **Spec 3 — `/today` flagged StaleCorp in heads-up — PASS.** turn 1: "StaleCorp aging: 37 days in `to_apply` with no recorded activity. Postings at that age are often filled or paused."
- **Spec 4 — `/today` flagged or safely handled the duplicate AcmeCorp entries — PASS.** turn 1: "Duplicate company entry: `acmecorp/` (status: to_apply, applied 2026-05-20 per journal) and `acme-corp/` (status: new, first seen 2026-05-22) both have `company: AcmeCorp`." Both folder slugs are named explicitly and the brief proposes a resolution.
- **Spec 5 — `/job-search` handled the empty "Companies of interest" gracefully — PASS.** turn 3 surfaced the gap as a choice ("Want me to seed Discovery from your target_titles + target_industries alone ... or skip Discovery this run"), and turn 4 completed cleanly on the skip: "Recheck-only run complete. Discovery skipped (no Companies of interest seeded)." No error, no repeat prompting.
- **Spec 6 — `/evaluate-position` with an unreachable URL produced a clear error message — PASS.** turn 5: "I tried to fetch the JD at https://example.com/some-role and couldn't pull it. That domain is the IANA reserved placeholder (example.com), so there's no real job posting behind it" — a plain-language cause plus recovery options, no stack trace, and the session continued to a clean termination at turn 6.
- **Spec 7 — No skill re-prompted Sam for previously-skipped fields — PASS.** After the turn-4 "skip", the only reference back to the skipped field is a deferred suggestion, not a prompt: "run /pm-job-search:job-search again later with `## Companies of interest` populated." Turn 5 asks nothing about profile or strategy fields.
- **Spec 8 — Every skill closed with a usable next-step nudge — PASS.** All four closings are actionable in the messy state: turn 1 "kill the duplicate AcmeCorp entry and update the surviving one to `applied`"; turn 2 "drop the link to me here and I'll score and file it"; turn 4 "Next step: triage the duplicate AcmeCorp entry"; turn 5 "paste the JD text straight into the chat ... or send me a working URL".

### Verdict

**PASS** — every `[required]` criterion that was in scope passed, and the two NOT EXERCISED cross-journey criteria (4 and 5) had preconditions the journey never intended to meet, since no skill wrote to profile or strategy and Sam's skip of Discovery meant no new role was ever surfaced.

## Tone

### Findings

- **turn 1:** "that single change unlocks everything else this plugin can do for you" — promotional register about the product itself rather than the plain, direct voice; it reads as marketing copy aimed at the user instead of an instruction.
- **turn 2:** "_Note: dashboard server can't actually launch from sub-agent context — this would normally open a browser tab._" — internal build vocabulary in user-facing copy; the user has no idea what "sub-agent context" is, and the line narrates the assistant's own machinery rather than telling the user what to do.
- **turn 4:** "stalecorp/ — StaleCorp Senior PM — closed (404) — listing taken down; updated last_seen and link_status" — unexplained systems vocabulary (raw HTTP codes) plus internal field names, where "the posting has been taken down" is the whole message a user needs.
- **turn 5:** "That domain is the IANA reserved placeholder (example.com), so there's no real job posting behind it — the request resolves to a generic landing page, not a role description." — plain-English violation; "IANA reserved placeholder" and "the request resolves to" are domain vocabulary the user has no reason to know, and the sentence already carries its own plain-English replacement ("there's no real job posting behind it").

### Verdict

**PASS** — The voice is consistently direct, contraction-friendly and free of hedging, clichés, superlatives and bundled asks across all five turns; what's wrong is localised leakage of internal and systems vocabulary plus one salesy closing line, none of which is jarring enough to read as a different product.

## Verdict

    Lint:          FAIL (3)
    Groundedness:  PASS
    Coherence:     FAIL (4)
    Conformance:   PASS
    Tone:          PASS

    Gate: Lint AND Groundedness AND Conformance

**Overall: FAIL**
