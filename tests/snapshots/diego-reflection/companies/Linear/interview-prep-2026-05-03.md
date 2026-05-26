# Interview prep — Linear / Group PM, Workflow Automation
**Date:** 2026-05-03  **Stage:** hm  **Tier:** P1

## Anchors
- **Why this company:** Real PLG motion at exactly the right stage — free-to-paid through product gates, founder still in product decisions, small enough that GPM scope means actual IC-leadership not GM overhead.
- **Why this role:** Workflow Automation is a rules-engine surface layered on top of a product Diego knows well; the challenge is adoption and instrumentation without an existing baseline — a familiar problem shape from platform API work.
- **Salary anchor:** $190-230K base + equity; floor is $190K. Linear is Series C-equivalent; ask for percentage, not cash value on equity. Don't anchor down.
- **Open questions from research:** How does Linear measure adoption on the Workflow Automation surface — primary retention signal or secondary engagement metric? What does the conversion path look like from free workspace to paid specifically on the automation surface?

## Stories to land

### 1. PLG pricing restructure
**Angle:** "Tell me about analytics depth." Lead with the cohort comparison methodology — comparing new-customer cohorts under old vs new pricing, isolating the attribution.

At my Series C SaaS role, paid-conversion had stalled at 4.8% of weekly-active free workspaces and SMB net revenue retention had dipped below 100%. The CEO wanted a funnel fix; I came back with a diagnosis that the pricing surface itself was the problem — tiers didn't map to how teams actually used the product. I co-designed three architecture options with the CFO and analyst, ran NDA pricing tests with ten existing customers before picking the winner, and shipped in three phased waves to isolate conversion lift from other growth signals. The cohort comparison was the critical analytical move: comparing new-customer cohorts on old vs new pricing gave us a clean attribution that ruled out seasonality. Paid-conversion went from 4.8% to 7.2% within four months; ARR from $26M to $40M over 14 months with roughly $5-6M attributed to the pricing change. For Linear: Karri will probe on whether I understand PLG metrics at the pricing layer, not just top-of-funnel signups — this story demonstrates the analytical depth on freemium-to-paid conversion that the workflow-automation surface will need as it builds its own conversion path.

### 2. devtools-onboarding-zero-to-one
**Angle:** "Building a new user journey where no baseline exists — how do you instrument and iterate when there is no prior conversion benchmark."

At my public DevTools company, I owned the onboarding journey for the integrations surface, which had no historical baseline — no prior completion rate, no instrumented funnel. I built the measurement framework first: defined the funnel stages, instrumented each one, set provisional targets from adjacent products in the same ecosystem. Got to a meaningful baseline within six weeks of launch, iterated over three quarters. For Linear: the Workflow Automation surface is in a similar position — power-user adoption without a clear prior baseline. Showing I've launched features without an existing conversion target and instrumented from scratch is more directly useful than showing I've optimised against an existing one.

### 3. api-deprecation-stakeholder-dissent
**Angle:** "Tell me about a time you had to push a decision through cross-functional resistance."

At the DevTools company, deprecating a legacy API version required getting engineering, GTM, and three enterprise customers aligned on a timeline all of them initially pushed back on. Engineering wanted six more months; GTM wanted twelve; the customers wanted indefinite support. I built the case around migration-cost data (what continued maintenance actually cost per quarter), ran bilateral sessions with each stakeholder before the all-hands, and proposed a phased sunset with a clear customer migration path. The deprecation shipped on the original timeline with zero customer defections. For Linear: the workflow-automation surface will require cross-functional alignment on which automations get built natively vs remain API-only — the dissent pattern will be familiar.

## Questions to ask THEM
- How does Linear currently measure success on the Workflow Automation surface — is there a primary retention metric or is it still being defined?
- What does the conversion path from free to paid look like specifically for automation features — is it gated on rule count, team size, or trigger complexity?
- Where does the Group PM for Workflow Automation sit in the product org day-to-day — is Karri the direct counterpart, or is there a VP layer?
- What does the first 90 days look like for whoever takes this role — onboarding to existing roadmap, or blank-slate prioritisation?
- How does the engineering team working on Workflow Automation interface with product right now — spec-driven, or embedded pairing?

## Anti-patterns to avoid this round
- Don't position as a generic SaaS PM — the work is specifically PLG B2B with a usage-pricing model. Karri will know the difference.
- Don't anchor on team size or budget managed — anchor on revenue motion and retention outcomes.
- Don't claim deep ML / LLM ownership — the workflow-automation surface will have trigger logic, not model work; stay in the lane.
- Don't use superlatives ("truly passionate", "deeply strategic") — they read as filler and the Linear culture skews direct.
