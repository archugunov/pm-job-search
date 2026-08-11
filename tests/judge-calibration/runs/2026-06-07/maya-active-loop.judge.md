# Findings — maya-active-loop

**Run date:** 2026-06-07
**Snapshot:** maya-active
**Judge:** replay under the restructured rubrics (2026-08-12), one call per rubric.
Replaces the pre-restructure reading; that is in git history.

## Lint

    turn 3: lint.jargon — 'meta.md' in user-facing text: "…k the company row in the dashboard and add this note directly — same `meta.md` underneath."
    NOT CHECKED: lint.hardcoded-cadence (no userdata tree supplied)

## Groundedness

### Evidence

| turn | claim | source | grounded |
|---|---|---|---|
| 1 | 2 new roles filed, both tier-1 | file: `userdata/companies/*/meta.md` (written this run) | yes |
| 1 | Plaid — Lead PM, Risk, at `https://example.com/plaid-lead-pm-risk` | fetch: /job-search discovery, filed this run | yes |
| 1 | Atom Bank — Senior PM, Mortgages, at `https://example.com/atom-senior-pm-mortgages` | fetch: /job-search discovery, filed this run | yes |
| 2 | Three Plaid roles exist: Lead PM Risk; Senior PM, Consumer Credit; Senior PM, Growth Loops | file: role filed turn 1 + `companies/Plaid/senior-pm-consumer-credit/meta.md`, `companies/Plaid/senior-pm-growth-loops/meta.md` | yes |
| 3 | Plaid → Senior PM, Consumer Credit → `to_apply` | user: turn 3 + file: `companies/Plaid/senior-pm-consumer-credit/meta.md` (written this run) | yes |
| 3 | The dashboard row writes the same `meta.md` underneath | file: `companies/Plaid/senior-pm-consumer-credit/meta.md` | yes |
| 4 | The CV's strongest underwriting/credit signals are split across two threads | file: `userdata/cv.md` | yes |
| 4 | Thread one is "the SMB lending feature at your current fintech (clear B2B2C credit decisioning angle)" | none | NO |
| 4 | Thread two is "the consumer onboarding work that touched KYC/risk earlier in your career" | none | NO |
| 4 | Plaid's Senior PM Consumer Credit seat sits closer to the consumer side of the credit stack | file: `companies/Plaid/senior-pm-consumer-credit/research-brief.md` | yes |
| 6 | Tailored CV saved to `userdata/companies/Plaid/senior-pm-consumer-credit/cv-2026-06-07.md` | file: written this run | yes |
| 6 | Maya has underwriting depth at Brightline | file: `userdata/cv.md` | yes |
| 6 | The underwriting thread being led with is the Brightline one | user: turn 5 ("the SMB lending underwriting story") + turn 4's own placement of it at the current fintech | NO |
| 6 | Plaid Consumer Credit does thin-file decisioning work | file: `companies/Plaid/senior-pm-consumer-credit/research-brief.md` | yes |
| 6 | Reframe used: "Not a process PM — a PM who writes specs, runs the SQL, and sits close to risk" | file: `userdata/profile.md` (What NOT to Frame As; Positioning; Moat) + `userdata/cv.md` (Head of Risk co-ownership) | yes |
| 6 | Headline proof: 12% decline-rate cut on thin-file applicants, Q2–Q3 2025, via cashflow-based secondary check | user: turn 6 | yes |
| 6 | Pricing experiment programme is from NorthLoop and is the current seat | file: `userdata/cv.md` | yes |
| 6 | Activation experimentation programme is from Lumio | file: `userdata/cv.md` | yes |
| 6 | Plaid will need onboarding work | file: `companies/Plaid/senior-pm-consumer-credit/research-brief.md` | yes |
| 6 | The CV contains an APM mentorship line (dropped) | file: `userdata/cv.md` | yes |
| 6 | The CV contains a CEO-cited shipping-cadence framing (dropped) | file: `userdata/cv.md` | yes |
| 6 | This is a senior IC seat on an 18-person bet | file: `companies/Plaid/senior-pm-consumer-credit/research-brief.md` | yes |
| 8 | Prep doc saved as `userdata/companies/Plaid/senior-pm-consumer-credit/interview-prep-2026-06-07.md` | file: written this run | yes |
| 8 | 4 stories pulled, adapted for a Plaid hiring-manager round | user: turn 8 + file: `userdata/stories/*.md` | yes |
| 8 | Underwriting zero-to-one anchors to the thin-file segment | file: `userdata/stories/underwriting-zero-to-one.md` | yes |
| 8 | Bureau-integration reuse is an anchor for Plaid | file: `userdata/cv.md` + `companies/Plaid/senior-pm-consumer-credit/research-brief.md` | yes |
| 8 | Consumer credit onboarding pivot has a first-loan UX angle | file: `companies/Plaid/senior-pm-consumer-credit/research-brief.md` | yes |
| 8 | In that story Maya killed a track and re-scoped | file: `userdata/stories/consumer-credit-onboarding-pivot.md` | yes |
| 8 | Payments pricing experiment is the closest analogue to Plaid's risk-pricing trade-offs | file: `userdata/stories/payments-pricing-experiment.md` + research-brief | yes |
| 8 | A Capital Markets question exists for Plaid | file: `companies/Plaid/senior-pm-consumer-credit/research-brief.md` | yes |
| 8 | Risk team dissent carries a disagree-and-commit signal | file: `userdata/stories/risk-team-dissent.md` | yes |
| 8 | Plaid Consumer Credit is a founder-close pod | file: `companies/Plaid/senior-pm-consumer-credit/research-brief.md` | yes |

### Findings

- **turn 4:** "the SMB lending feature at your current fintech (clear B2B2C credit decisioning angle)" — no file read this run places any SMB lending work in Maya's history; `cv.md` and `profile.md` describe the current seat as Lead PM, Growth Pricing at NorthLoop on a consumer BNPL card, and the only "SMB Lending" in the workspace is the iwoca *role she applied to*, so this invents a career thread and then builds the whole CV on it.
- **turn 4:** "the consumer onboarding work that touched KYC/risk earlier in your career" — presented as read out of the CV ("Looking at your CV"), but `cv.md` contains no consumer onboarding or KYC work at any point in the timeline; characterising CV contents that the file does not hold is ungrounded regardless of whether a similar theme appears in an unread story file.
- **turn 6:** "Positioning angle: underwriting depth at Brightline reframed as the direct analogue to Plaid Consumer Credit's thin-file decisioning work" — turn 4 located the underwriting thread the user selected at "your current fintech" and turn 6 relocates the same thread to Brightline, an inexact restatement of the assistant's own earlier claim that leaves the user holding two incompatible employer attributions for the story now headlining her CV.

### Verdict

**FAIL** — three ungrounded rows, and the first of them is load-bearing: the CV, its headline positioning, and the downstream prep doc are all built on an SMB lending thread that no file, fetch, or user turn supplied.

## Coherence

### Findings

- **turn 2:** "Which Plaid role do you want to mark as to-apply? 1. Lead PM, Risk 2. Senior PM, Consumer Credit 3. Senior PM, Growth Loops" — turn 1 announced only one Plaid role ("Filed 2 new roles: 2 tier-1. - Plaid — Lead PM, Risk"), so two of the three options arrive with no bridging line saying they are roles already tracked rather than part of this sweep; the user is left to work out where Consumer Credit and Growth Loops came from (rule 1).
- **turn 3:** "Tip: you can also click the company row in the dashboard and add this note directly — same `meta.md` underneath." — the user marked a status, not a note, so "this note" has no antecedent anywhere in the conversation and the user is left holding a tip about an action they never took (rule 1).
- **turn 3:** "you can also click the company row in the dashboard" — turn 1 already offered the same dashboard route ("Open the dashboard to triage — or say `mark <Company> to apply`") and the user answered by choosing the chat path, so re-pitching the dashboard one turn later reads as not having tracked the choice they just made (rule 3).
- **turn 8:** "Payments pricing experiment — closest analogue to Plaid's risk-pricing trade-offs, opens the Capital Markets question naturally" — "the Capital Markets question" is given a definite article as if previously established, but it appears nowhere earlier in the run; the user cannot tell which question is meant or why this story opens it (rule 1).
- **turn 8:** "Risk team dissent — disagree-and-commit signal for a founder-close pod" — the user specified "hiring manager" one turn earlier, and "founder-close pod" is both undefined and pointed at a different round shape than the one they asked to prep for (rule 1).

### Verdict

**PASS** — the search → mark → tailor → prep arc holds turn to turn and each user reply lands on what was actually asked; the frictions are small local ones (a role list that widens without a bridge, one stale dashboard nudge, two unexplained terms in the closing summary) rather than a moment the user would have to stop and reread.

## Conformance

### Findings

No findings.

Per-criterion report:

**Cross-journey criteria**

- **Criterion 1 — End-of-run nudge: PASS.** turn 8: "Practise with `pm-job-search:interviewer-simulator` (mock round) — or open the doc and rehearse out loud first. Debrief after with `/pm-job-search:interview-analysis`." — state-aware, names the just-saved prep doc's natural next moves rather than parroting the canonical order.
- **Criterion 2 — No prior-state leak in messaging: NOT EXERCISED.** No skill output referenced "since last time", a previous run, or past activity; references to Brightline/NorthLoop/Lumio are CV content, not prior-run state.
- **Criterion 3 — No dead ends: PASS.** Each skill closes with a next action — turn 1: "Open the dashboard to triage — or say `mark <Company> to apply` and I'll update it."; turn 6: "Next: want me to draft a short cover note, or move on to interview-prep?"; turn 8: "Practise with `pm-job-search:interviewer-simulator` (mock round)". No turn ends awaiting input the journey didn't provide.
- **Criterion 4 — Profile + strategy not silently overwritten: NOT EXERCISED.** The transcript shows no skill writing to `userdata/profile.md` or `userdata/strategy.md`; the precondition is unverifiable from chat, so scope is not asserted.
- **Criterion 5 — JD link present in the chat row: PASS.** turn 1: "- Plaid — Lead PM, Risk — to triage — https://example.com/plaid-lead-pm-risk" and "- Atom Bank — Senior PM, Mortgages — to triage — https://example.com/atom-senior-pm-mortgages" — both new roles render the live JD URL in the row.

**Journey spec criteria (active-loop)**

- **`/job-search` run summary uses plain prose: PASS.** turn 1: "Filed 2 new roles: 2 tier-1." followed by two plain bullets — no fenced dump.
- **`/job-search` tier counts bucketed: PASS.** turn 1: "Filed 2 new roles: 2 tier-1."
- **Dashboard nudge on status change, at most once per session: PASS.** turn 3: "Tip: you can also click the company row in the dashboard and add this note directly — same `meta.md` underneath." — fires once, on the only status change, and never repeats.
- **`/apply` did not exceed 5 questions: PASS.** Two questions asked — turn 4: "do you want the CV to lead with the SMB lending work ... or reframe the consumer onboarding/risk work as the headline"; turn 5: "What's the single most defensible quantitative outcome from the SMB underwriting work you'd want headlined at the top of the CV".
- **`/apply` chat summary uses plain prose + bulleted recap: PASS.** turn 6: "Drafted your tailored CV for Plaid — Senior PM, Consumer Credit and saved it to `userdata/companies/Plaid/senior-pm-consumer-credit/cv-2026-06-07.md`." followed by a "What I leaned on:" bullet list — no fenced key:value dump.
- **`/apply` summary cites positioning angle + proof points: PASS.** turn 6: "Positioning angle: underwriting depth at Brightline reframed as the direct analogue to Plaid Consumer Credit's thin-file decisioning work" and "Strongest proof point headlined: the 12% decline-rate cut on thin-file applicants Q2-Q3 2025".
- **`/apply` closing offered a clear next-step nudge: PASS.** turn 6: "Next: want me to draft a short cover note, or move on to interview-prep?"
- **`/interview-prep` adapted 3-5 stories: PASS.** turn 8: "Pulled 4 stories adapted for Plaid hiring-manager round:" followed by four adapted story bullets.
- **`/interview-prep` closing nudge context-aware: PASS.** turn 8: "Practise with `pm-job-search:interviewer-simulator` (mock round) ... Debrief after with `/pm-job-search:interview-analysis`." — both named, and in the right order for a doc just saved ahead of a hiring-manager round.

### Verdict

**PASS** — every in-scope `[required]` criterion passed on quoted evidence, and the two NOT EXERCISED criteria (2 and 4) had preconditions the transcript never shows being met.

## Tone

### Findings

- **turn 4:** "Looking at your CV, your strongest underwriting/credit signals are split across two threads: the SMB lending feature at your current fintech (clear B2B2C credit decisioning angle) and the consumer onboarding work that touched KYC/risk earlier in your career — for a Senior PM Consumer Credit role at Plaid, which sits closer to the consumer side of the credit stack, do you want the CV to lead with the SMB lending work (deeper credit-model proof, but B2B-flavoured) or reframe the consumer onboarding/risk work as the headline (better audience fit, but thinner on actual underwriting depth)?" — Violates "Direct asks. Single question, no preamble": the actual ask arrives ~60 words in, chained into one unbroken em-dash sentence with parenthetical asides, so the user has to parse the analysis before finding what they are being asked.

### Verdict

**PASS** — One over-built question in turn 4 is the only place the voice slips; everywhere else the copy is short, direct and plainly worded (turn 5's single outcome ask, turn 7's four-option round question, turn 6's "edit anything that doesn't sound like you"), with no hedging, superlatives, clichés or motivational register a real user would notice as off.

## Verdict

    Lint:          FAIL (1)
    Groundedness:  FAIL (3)
    Coherence:     PASS
    Conformance:   PASS
    Tone:          PASS

    Gate: Lint AND Groundedness AND Conformance

**Overall: FAIL**
