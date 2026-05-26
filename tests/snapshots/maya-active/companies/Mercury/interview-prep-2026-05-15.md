# Interview prep — Mercury / Sr PM, Banking
**Date:** 2026-05-15  **Stage:** case-study  **Format:** 30-min present + 30-min discussion, on Saturday 2026-05-16  **Tier:** P1

## The prompt

> Mercury Banking is launching a sub-product for bookkeeping firms with multi-entity client accounts. Frame the opportunity, name the top three risks, and recommend a sequence.

## Frame I'll present

**Segment:** bookkeeping firms managing 10-200 client entities. The user we're serving is the bookkeeper, but the buyer is the firm. The end client (small business) is a downstream effect, not a target.

**Opportunity:** these firms currently stitch Mercury (or equivalent) across separate logins per client. The pain is consolidation — single sign-on across entities, parent-level visibility, batch operations. Revenue mechanic: per-entity SaaS fee + interchange on the new accounts opened through the firm's referral path.

**Why this expansion makes sense for Mercury specifically:** the bookkeeping-firm segment is the natural adjacency to startup-founder banking, because bookkeepers already advise the same startup founders Mercury serves on the personal-business side. The customer-acquisition path is half-built.

## Top three risks I'll name

1. **Multi-entity access controls are a regulatory landmine.** BSA/KYC isn't designed for the "agent acting on behalf of multiple beneficial owners" pattern. Will need explicit treatment in the sub-product spec, not bolted on after.

2. **The firm-buyer / bookkeeper-user split kills standard B2B PLG motion.** PLG works when the user can self-serve to value. Here the user (bookkeeper) wants the product, but the firm partner has to approve the procurement. Different motion — closer to vertical SaaS than to startup-banking.

3. **Cannibalisation of existing Mercury customers.** Many startup founders already use Mercury direct; if their bookkeeper now manages the account, the firm becomes the relationship owner, not Mercury. Need explicit policy on relationship ownership before launch, not after the first churn dispute.

## Recommended sequence

- **Weeks 1-4:** discovery — 25 bookkeeping-firm interviews, segmented by firm size (≤10 clients, 11-50, 51+). Goal: validate which workflows actually cost the firm meaningful time vs. which are tolerable friction.
- **Weeks 5-12:** build single-sign-on + parent-level visibility for one beachhead segment (probably 11-50, where pain is highest and decision-making is single-person).
- **Weeks 13-20:** beta with 8-12 firms, measure activation-to-monthly-active by firm, not by end-client account.
- **Weeks 21+:** decide on tiered pricing (per-entity SaaS) vs. flat-firm pricing based on cohort retention data, not pre-launch instinct.

## Questions I'll have ready for the discussion

- What's the internal narrative on cannibalisation? Is there an explicit policy I haven't surfaced from the public material?
- Has the team already done discovery here, or is the prompt genuinely open?
- What does the regulatory team's first reaction to multi-entity access controls look like?
- Who would the buyer-side relationship sit with — Mercury sales, or a partner-channel team?

## Anti-patterns to avoid

- Don't present this as a "product-led" expansion when the buyer-user split makes it a sales-led motion. The framing has to match the reality.
- Don't recommend a build before discovery. The case study is testing judgement, not speed.
- Don't skip the cannibalisation risk — it's the awkward one and they'll respect me naming it.

## Notes from the panel round

- Jamie said the Banking team's strategy work is "more narrative than data" at the moment — meaning the case study probably weighs framing as much as numbers. Lean into that.
- The team that would own this sub-product hasn't been named yet in interviews. If it's the team I'd join, the case study doubles as "would you actually want this scope?"
