# Interview prep — Mercury / Sr PM, Banking
**Date:** 2026-05-13  **Stage:** panel  **Panelists:** Jamie (PM peer), Raj (EM), Priya (Sr Designer)  **Tier:** P1

## Anchors

- **Read forward from HM:** Sarah named "activation-to-retention for sub-£50K monthly inflow accounts" as the unsolved problem. The panel will probe how I'd approach that surface — be ready to walk through a discovery → spec → ship sequence in concrete terms.
- **Gap I named:** deposit-product mechanics. Panel may push harder on this than Sarah did. Same answer: "3-month onboarding curve, here's my plan." Have the plan ready in concrete weeks-to-milestones form, not generic.
- **Risk story recast:** new framing is BSA/KYC, not credit risk. Story shape unchanged — Compliance flagged a re-onboarding flow post-launch, I built a shared-assumptions doc + joint sensitivity analysis, we landed on a tripwire monitor instead of pulling the feature. Carry forward "Compliance is a design input, not a sign-off gate."

## Stories to land

### 1. Pricing-experiment (for Jamie — PM peer)
**Angle:** "Pricing decisions read as a system: fee structure, retention, and unit economics as one model."

Jamie has been on the Banking team 18 months per LinkedIn. He'll listen for whether I think about pricing the way Mercury's product org does (not as a marketing lever). Reframe the lending pricing-experiment as: changing one variable (rate) only moves the system if I model the second-order effects (retention, default exposure, capital cost). For Mercury: same shape applies to fee changes — change the wire-transfer fee, model the cohort-level retention impact, not just the per-transaction revenue.

### 2. Risk-dissent recast (for Raj — EM)
**Angle:** "Compliance as design input — banking-native framing."

Use the BSA/KYC recast (see Anchors above). Raj will probe for whether I escalate or absorb friction. Land on: "I'd rather rebuild the spec than escalate the disagreement." Concrete proof point: the shared-assumptions doc.

### 3. Onboarding pivot (for Priya — Sr Designer)
**Angle:** "Mid-flight pivot driven by unit-economics — and how I co-authored the new direction with Design, not handed it down."

Priya will be listening for whether I treat designers as a finishing layer or a thinking partner. Lead with: "we ran the redesign open with Design from week one — I wasn't bringing a finished strategy and asking for the UI." Concrete: the original brief assumed retention was the problem; Design's input from user interviews reshaped it to intent-at-entry. The pivot was theirs as much as mine.

## Questions to ask the panel

- **For Jamie:** what's the weirdest second-order effect you've seen from a Banking pricing change? (Reveals whether his pricing instincts run as deep as Mercury's strategy implies.)
- **For Raj:** how does the Banking team handle a feature where Eng has a strong "we'd build it differently" opinion that the PM hasn't surfaced? (Reveals trust patterns + escalation defaults.)
- **For Priya:** what's the part of the Banking surface where Design feels under-represented in the decision-making? (Reveals whether the team treats Design as co-author or finishing layer — Priya's answer will tell me what she wants to hear me say.)

## Anti-patterns to avoid

- Don't repeat the lending-credit framing of the risk story. It landed flat with Sarah; Raj will be even less forgiving.
- Don't pitch one story per panelist explicitly — let the conversation flow, but know which story has the best angle for each.
- Don't overpromise on the "3-month onboarding curve" if Raj probes feasibility. Give a real week-by-week breakdown, not a generic answer.

## Notes from HM round

- Sarah said the legacy-core migration is "half-rebuilt by autumn" — that's a real, dated commitment. Reference if the panel asks about timelines.
- "Name the gap, don't fudge it" landed at HM. Repeat the framing if the panel pushes on deposit-mechanics depth.
