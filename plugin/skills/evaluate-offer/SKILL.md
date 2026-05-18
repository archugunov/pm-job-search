---
name: evaluate-offer
description: This skill should be used when the user asks to "/evaluate-offer", "evaluate this offer", "compare offers", "I got an offer", "I have two offers", "should I take this offer", "should I push back on this offer", or pastes offer details for sense-checking. Reads userdata/profile.md (target_titles, salary_band, anti-goals), userdata/strategy.md (target_offer_date, walk-away threshold), userdata/companies/<Co>/* if it exists, plus the senior-pm-archetypes + career-anti-patterns references. Conversationally collects offer details (one to two questions), then writes userdata/companies/<Co>/offer-evaluation-<YYYY-MM-DD>.md with: verdict (take / negotiate / push back / decline), comp shape analysis, role-shape re-check, archetype fit, decision factors weighted, downside scenario, and 3-5 specific negotiation moves to ask for.

---

# /evaluate-offer — sense-check an offer against your bigger plan

A senior-PM-tuned offer evaluation. Reads the user's profile + strategy + company history, applies the senior-PM-archetype + anti-pattern references, and produces a verdict with specific negotiation moves. Different from `/evaluate-position` — that scores **opportunities** (postings) against your tier rubric; this scores **offers in hand** against your career arc.

**Voice:** every prompt and the written evaluation follows `${CLAUDE_PLUGIN_ROOT}/TONE.md`. Apply the low-effort-first principle — ask for the smallest set of offer details that unlocks a useful verdict; only drill if a load-bearing detail is missing.

## Inputs

- **Offer details** — collected conversationally. Required minimum:
  - Company name
  - Title
  - Base salary + currency
  - Equity (% or $ value, vesting + cliff if known)
  - Sign-on (if any)
  - Stage (seed / Series A / B / C / D+ / late-stage / public)
  - Location / remote arrangement
  - Manager (name + brief)
  - Start date (if discussed)
  - User-provided fit notes (e.g. "their CPO is on parental leave for the first 4 months")
- **Second offer** (optional) — if the user mentions a second offer or `--compare-with <Company>`, collect the same minimum set for the second offer and produce a side-by-side comparison instead of a single-offer verdict.
- `userdata/profile.md` — frontmatter (`target_titles`, `salary_band`, `geography`, `hard_filters`, `target_industries`), `## Positioning`, `## Moat`, `## What NOT to Frame As`.
- `userdata/strategy.md` — frontmatter (`target_offer_date`, `weekly_targets`), `## Headline goal`, `## Anti-goals`, `## Checkpoints`.
- `userdata/companies/<Company>/[<role-slug>/]meta.md` + `research-brief.md` + any prior `interview-debrief-*.md` if the company is in the pipeline. Especially: the most recent debrief's "role shape verdict" (🟢 / 🟡 / 🔴) is load-bearing for this evaluation.
- Reference docs (per TONE.md userdata-override convention):
  - `userdata/references/senior-pm-archetypes.md` || `${CLAUDE_PLUGIN_ROOT}/references/senior-pm-archetypes.md` — used for archetype-fit diagnosis (does the role need a builder / scaler / operator? does your positioning match?).
  - `userdata/references/career-anti-patterns.md` || `${CLAUDE_PLUGIN_ROOT}/references/career-anti-patterns.md` — used to scan for #2 title-chasing, #3 stage-mismatch, #9 hollow-HoP, #10 comp-tunnel-vision. Surface BY NAME when detected.

If `userdata/profile.md` or `userdata/strategy.md` are missing, tell the user to run `/setup` first — offer evaluation depends on stated targets + decision constraints.

## Conversational flow

Per TONE.md low-effort-first: the user pastes whatever they have; you fill the gaps with one targeted question at a time. Don't run a multi-part questionnaire.

1. **Open:** if the user pasted offer text, parse what you can; ask for ONE most-load-bearing missing detail (usually equity %/$ or manager name).
2. **Stage check:** if stage isn't stated, ask. ("Seed, A, B, later? Affects everything about how to read the equity.")
3. **Fit notes prompt (optional):** *"Anything from the rounds I should weigh — anyone you'd be working closely with, anything from the founder you can't unhear?"* Skip if user has nothing to add.
4. **Second offer trigger:** if user mentions comparing, switch to compare mode and collect the same minimum set for the second offer. Otherwise proceed to single-offer verdict.

When you have enough to render: write the evaluation file (see structure below) and print a 4-5 line summary to chat.

## Evaluation structure

Write `userdata/companies/<Company>/[<role-slug>/]offer-evaluation-<YYYY-MM-DD>.md`:

```markdown
# Offer evaluation — <Company> / <Title>
**Date:** <YYYY-MM-DD>  **Stage:** <seed / A / B / ...>  **Tier (from meta.md if exists):** <P0|P1|P2|new>

## Verdict
**<TAKE / NEGOTIATE / PUSH BACK / DECLINE>** — <one-line rationale anchored in the load-bearing factor>

## Comp shape
- **Base:** <base + currency>. <One-line comparison vs profile.md salary_band — at, above, below.>
- **Equity:** <% or $>. <One-line read on whether the equity sizing fits the stage — e.g. "0.4% at Series A is below typical HoP range of 0.5-1.5%".>
- **Total 1-year:** <number>. **Total 4-year (with equity at current valuation):** <number>.
- **Stage-vs-equity read:** <Is base-vs-equity tilt right for this stage? Late-stage with equity-heavy = high risk; seed with cash-heavy = founder doesn't believe in their own equity.>

## Role-shape re-check (build-vs-defend)
<If prior interview-debrief exists for this company, lift its role-shape verdict (🟢 / 🟡 / 🔴) and quote the signals. If 🔴 defending, this becomes the load-bearing factor in the verdict.>
<If no prior debrief: prompt the user — "We don't have a debrief on file. Quick gut check: were the rounds mostly about how you'd ship, or how you'd manage stakeholders? That changes the verdict.">

## Archetype fit
- **Role's archetype need (based on stage + scope):** <builder / scaler / operator — drawn from senior-pm-archetypes.md stage-fit map.>
- **Your archetype (based on profile.md positioning + proof points):** <builder / scaler / operator — your read of how the user describes their work.>
- **Match:** <strong / partial / mismatch>. <If mismatch: cite which trap from senior-pm-archetypes.md ("hollow HoP at scaled co", "operator at seed", etc.) and the 18-month hollowing risk.>

## Anti-pattern scan
<Scan career-anti-patterns.md for matches against this offer. Common at offer-stage:>
- **#2 title-chasing**: <fires if this is a HoP title at <30 ppl co OR scope-on-paper reads Senior PM>
- **#3 stage-mismatch**: <fires if user's last role was much-larger or much-smaller co>
- **#9 hollow-HoP risk**: <fires if headcount >150 + non-PLG/B2C vertical + no equity signal>
- **#10 comp-tunnel-vision**: <fires if user has framed the offer primarily through comp numbers in this conversation>
<Surface each matching pattern BY NAME with the corrective from the reference. Skip the section entirely if no patterns match.>

## Decision factors (weighted)
Rank the 5-7 load-bearing factors. Each gets one line; the most decisive ones come first.

1. **<Factor name>** — <how it cuts. e.g. "Manager fit: strong — the CPO described prioritisation debates as collaborative; matches what you said you need.">
2. ...

Common factors to consider (pick the 5-7 that actually move the verdict for THIS offer):
- Manager quality
- ICP / vertical fit
- Stage fit (vs archetype)
- Comp vs profile.md salary_band
- Equity reasonable for stage
- Growth / learning surface
- Downside / reversibility (if this fails in 18 months, what's the story?)
- Geography / commute / remote arrangement
- Cultural signals from rounds (build-vs-defend, founder visibility, etc.)
- Anti-goals from strategy.md (any conflicts — flag explicitly)

## Anti-goals check
<Lift the anti-goals from strategy.md ## Anti-goals. For each, mark CLEAR or CONFLICTING (with quote evidence from the offer). Hard rule: never propose TAKE without explicitly running this check.>
<If conflicting: surface the conflict at the TOP of the verdict, not buried here.>

## Downside scenario
If this offer fails in 18 months, what's your story?
- **For the next-role recruiter:** <one paragraph the user could tell — based on the role's actual scope, not the offered title>
- **For your network:** <one paragraph — what was the learning?>
- **What this rules out for the next move:** <e.g. "if you take this hollow-HoP role and leave at 14 months, your next HoP search will be harder — recruiters read short HoP tenures as 'didn't work out'">

## Negotiation moves (3-5 specific asks)
Specific, anchored, ordered by leverage. Each ask has: WHAT to ask, RATIONALE the company can hear, FALLBACK if they decline.

1. **<Specific ask>** — <Rationale framed in the company's terms.> <Fallback: e.g. "if they can't move base, ask for a sign-on of X to bridge."> 
2. ...

Typical leverage points worth considering (pick what fits THIS offer):
- Base salary (anchor to profile.md salary_band)
- Sign-on (bridges base gaps; one-time, easier yes for the company)
- Equity floor / refresh-grant commitment
- Start date (often free to ask, signals seriousness)
- Title clarification (especially HoP at seed: get the scope agreement in writing)
- Scope agreement (1-3 explicit deliverables for the first 90 days, agreed in writing)
- Manager / reporting line clarification (especially if the role spans an org change)
- Vacation / remote-day count

## Reversibility check
- **Easy to reverse:** <bullets — what you'd recover if this doesn't work>
- **Hard to reverse:** <bullets — what's locked in. e.g. "if you decline your other offer in hand to take this, you can't reopen.">
- **Window to decide:** <when does this offer expire? if not stated, ask.>

## What to do next (concrete)
<2-3 bullets. Examples:>
- Sleep on this 24h before responding.
- Run `pm-job-search:career-coach` with: "I'm about to <accept / decline / push back>. What would I regret in 2 years?"
- If pushing back: send the ask in writing today; verbal asks get re-negotiated mid-stream.
- If declining: keep the relationship — recruiters and founders move companies, decline notes get read.
```

## Compare-mode structure

When two offers are in play, replace single-offer sections with side-by-side. Same sections, two columns. Add a final section:

```markdown
## Compare verdict

| Factor | <Offer A> | <Offer B> | Winner |
|---|---|---|---|
| Manager | ... | ... | A / B / tie |
| Stage fit | ... | ... | A / B / tie |
| Comp 4-year | ... | ... | A / B / tie |
| Archetype match | ... | ... | A / B / tie |
| Anti-goals clear | ... | ... | A / B / tie |
| Reversibility | ... | ... | A / B / tie |

**Tilt:** <which offer the data points to, in one sentence. NEVER hide a real tilt — if A clearly wins on 5/6 factors, say so. If they're genuinely close, say that too.>

**5-year clock test:** which offer gets you further toward the headline goal in strategy.md? <One sentence.>
```

## Chat output

After writing the evaluation file, print to chat (compact):

```
Filed: userdata/companies/<Co>/[<role-slug>/]offer-evaluation-<date>.md

Verdict: <TAKE / NEGOTIATE / PUSH BACK / DECLINE>
Headline reason: <one line>
Top negotiation ask: <verbatim from the negotiation moves section>

Before responding: sleep 24h, then run pm-job-search:career-coach with "I'm about to <verb> — what would I regret in 2 years?"
```

## Hard rules

- **Never recommend TAKE without running the anti-goals check explicitly.** Anti-goals from strategy.md are user-stated decision constraints, not rubric inputs. A TAKE recommendation that ignores an explicit anti-goal conflict is malpractice.
- **Never invent comp numbers, equity benchmarks, or market data.** If you need a comparator and the user hasn't provided one, ask — don't fabricate.
- **Never override the user's stated `salary_band` from profile.md.** Your role is to validate the comp fit against THEIR stated band, not to substitute your own.
- **Always cite anti-patterns by name** when scanning detects a match. The user benefits from having a handle for the pattern across conversations.
- **Always include the closing nudge** to run career-coach with the "what would I regret in 2 years?" question. Offer evaluation is decision support; the regret check is the human moment that decision-support tools should ALWAYS hand off.

## What /evaluate-offer never does

- Never edits `meta.md`. Recommendations only — the user updates status (`offer`, `not_interested`, etc.) themselves.
- Never edits `profile.md` or `strategy.md`. If the evaluation surfaces that the salary band is wrong, recommend the user run `pm-job-search:career-coach` to revisit.
- Never auto-sends acceptance / decline / pushback emails. The output file is for the user; communication with the company is the user's move.
- Never recommends signing without a 24-hour delay if the user shows signs of urgency. Acceptance under pressure is anti-pattern territory.

## Smoke test against the Maya example

Run `/evaluate-offer` with a synthetic Plaid offer against `userdata/examples/maya/`:

- User pastes: "Plaid offered me Senior PM Consumer Credit, £125K base, 0.05% equity (Series E), £15K sign-on, remote-friendly with quarterly NYC visits, start 2026-07-01. Manager would be the CPO (Lina Vasquez)."
- Skill reads Maya's profile.md (target_titles include Head of Product; salary_band £110-140K), strategy.md (target_offer_date 2026-08-01; anti-goals include "no full-time relocation outside London"), companies/Plaid/meta.md + research-brief + the prior CPO-round debrief.
- Comp shape: base mid-band ✓, equity 0.05% at Series E is normal-low for Senior PM at this stage, sign-on modest.
- Role-shape re-check: lift the debrief's verdict (assume 🟢 building based on memory).
- Archetype fit: Maya describes herself as a builder; Plaid Series E is operator-shape territory; FLAG mismatch with the 18-month hollowing note from senior-pm-archetypes.md.
- Anti-pattern scan: #3 stage-mismatch fires (Maya's last role was Series A scale). #9 hollow-HoP doesn't fire (this is Senior PM not HoP title) but the underlying mismatch insight transfers.
- Anti-goals check: "no full-time relocation outside London" → CLEAR (offer is remote with visits, not relocation).
- Decision factors: manager fit (data thin — no specific signal in research-brief), stage mismatch (concerning), comp at mid-band (not a tilt either way), no growth surface specifics in user's notes.
- Verdict: NEGOTIATE — comp is fine but the archetype-vs-stage mismatch is the load-bearing factor; the negotiation should buy scope agreement in writing (1-3 explicit first-90-days deliverables) so Maya can verify the role is closer to builder-shape than the org chart suggests.
- Negotiation moves: scope agreement in writing (top of list, per the diagnosis); base nudge to £130K (mid-band+); sign-on bump to £20K (bridges to senior-PM market median); start date confirmed.
- File: `userdata/examples/maya/companies/Plaid/offer-evaluation-2026-05-17.md`.
- Chat summary: 4 lines per the contract.

If the smoke test diverges materially, the skill is mis-reading either the profile or the references — fix before promoting.
