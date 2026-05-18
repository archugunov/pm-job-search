# Interview debrief — Linear / Group PM, Workflow Automation
**Date:** 2026-05-04  **Stage:** hm  **Source:** notes  **Tier (pre):** P1

## What landed
- The PLG pricing restructure story landed cleanly. When I walked through the cohort comparison methodology — new-customer cohorts on old vs new pricing, isolating the attribution from organic growth — Karri asked a follow-up about how I'd apply the same methodology to a rules-engine surface without an existing conversion baseline. That follow-up was the signal: he understood the story was directly relevant to workflow automation and wanted to extend it.
- The question about whether Linear measures workflow-automation adoption as a primary retention signal or a secondary engagement metric got a genuine answer and a 4-minute side-thread on how Linear thinks about power-user surfaces. Showed I'd done the research and was already thinking in their vocabulary.

## What didn't land
- Karri disengaged when I shifted to the apps-vs-platform framing. I used the phrase "platform surface" to describe the workflow-automation layer's relationship to the core product — as in, "automation as a platform play on top of issue tracking." His tone shortened and he redirected to a specific rules-engine feature instead. He's not thinking about this surface as a platform — he's thinking about it as a product feature that power users adopt. The framing was accurate but it was the wrong abstraction level for where they are.
- The api-deprecation story felt thin in the room. I told it to illustrate cross-functional dissent, but workflow automation at 80 people doesn't have the stakeholder surface area of a public DevTools company with enterprise customers. The story's context didn't transfer cleanly.

## Interviewer signals
- **Enthusiasm:** Follow-up questions on PLG metrics and cohort methodology — Karri took notes during the pricing-restructure walk-through. Side-thread on power-user adoption philosophy ran 4 minutes unprompted.
- **Concerns / hesitations:** Visible disengagement when apps-vs-platform abstraction surfaced — shorter responses, topic redirected to a specific feature. Not hostile; he just wasn't interested in that level of framing. Signal: he wants someone who thinks in feature-level specifics, not architecture abstractions.
- **Scope cues:** Questions clustered around PLG metrics, rules-engine adoption, and how to get power users to discover automation features without a sales assist. That's the real evaluation axis — bottom-up adoption without a sales layer.
- **Culture cues:** Karri is direct and speed-runs filler. When the framing was right (PLG metrics, cohort methodology) the conversation was energised. When it wasn't (platform abstraction, enterprise-scale dissent) he redirected quickly with no softening. The culture values precision over range.

## Vs the prep doc
- **Stories planned vs told:** PLG-pricing-restructure told — cohort-methodology angle used and landed well. api-deprecation-stakeholder-dissent told — landed weakly (context mismatch; too enterprise-scale for Linear at 80 ppl). devtools-onboarding-zero-to-one never raised — correct call given how the conversation went after the platform-framing misfire.
- **Questions asked vs prepped:** Primary retention signal question asked — got a genuine answer and a thread. Conversion path from free to paid on automation features asked — got a partial answer ("rule count is the current gate, team count is the future direction"). First-90-days question dropped due to time.
- **Anchors deployed:** PLG motion and founder-led culture anchors used in the opening — landed well. Salary anchor not raised (HM stage, too early). Apps-vs-platform framing attempted mid-conversation — misfired.

## Role shape verdict
**🟡 mixed**

The round was substantively good on PLG mechanics but had a visible warning sign that explains the post-HM silence. Signals:
- Positive build signal: Karri's follow-up on cohort methodology extended into a 4-minute side-thread on adoption measurement for power-user surfaces — that's active intellectual engagement, not a box-check interview.
- Mixed signal: disengagement on platform-framing suggests the role's evaluation axis is narrower than the JD implied. This is a product-feature GPM role, not a platform-architecture role. That's a smaller scope than my prior work.
- Mixed signal: the api-deprecation story's weak landing (enterprise-context mismatch) suggests Karri is pattern-matching against small-team, bottom-up product work — and stories from 200+ person companies don't transfer cleanly.
- No next-step commitment from Karri despite a follow-up note from Anna on 2026-05-04 — "coming soon" is recruiter-speak for a decision that isn't moving quickly. The post-HM silence is consistent with a 🟡 round.

## Process / next steps
- Anna (recruiter) sent a follow-up note on 2026-05-04 — "next round coming soon." No specific timeline.
- No direct next-steps signal from Karri at close.
- As of 2026-05-04, no further inbound. Interview trajectory is stale.

## Recommended updates
- **Stories to add or sharpen:** Add a new angle to `plg-pricing-restructure` scoped explicitly to "PLG surface instrumentation at small-team scale" — removing enterprise-scale context (CFO alignment, NDA pricing tests) and keeping the cohort-methodology core. That version will land at companies like Linear where the referent is 2-engineer surfaces, not $40M ARR processes. Separately, `api-deprecation-stakeholder-dissent` needs a small-team variant or should be retired from Linear-type companies entirely.
- **Profile updates:** Consider adding to `## What NOT to Frame As` — "don't use apps-vs-platform framing at sub-100 person companies — it reads as an abstraction layer the company hasn't reached yet."
- **Meta updates:** Mark `monitoring: true` if 10 business days pass with no round-2 invite. The post-HM silence plus 🟡 round verdict suggests a genuine decision point for Linear, not a process delay. If no inbound by 2026-05-20, consider status: `closed`.
- **Next-round prep:** If a panel invite arrives — (1) drop api-deprecation entirely from Linear prep; (2) rewrite devtools-onboarding-zero-to-one with small-team instrumentation framing (sub-50-engineer company, no existing baseline); (3) prepare a specific view on how to grow bottom-up adoption of automation features without a sales-assist layer — that is the real evaluation axis.
