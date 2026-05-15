<!--
  pm-job-search — profile template.
  /setup fills in the {{PLACEHOLDERS}} from your answers, then leaves this
  file in userdata/profile.md as the single source of truth for all skills.
  You can edit it directly anytime.
-->
---
name: {{NAME}}                            # your full name
city: {{CITY}}                            # e.g. "London, UK"
timezone: {{TIMEZONE}}                    # IANA, auto-detected (e.g. "Europe/London")
email: {{EMAIL}}
linkedin_url: {{LINKEDIN_URL}}

target_titles:                            # roles you're aiming for
  - Head of Product
  - Lead PM
  - Senior PM

target_industries:                        # verticals where your experience lands
  - B2C SaaS
  - PLG SaaS
  - mobile
  - e-commerce

geography:
  mode: {{GEOGRAPHY_MODE}}                # onsite | remote | both | other
  mode_detail: {{GEOGRAPHY_DETAIL}}       # optional free text (e.g. "open to EMEA relocation")

salary_band: "{{SALARY_BAND}}"            # single open string; any currency
                                          # examples: "£90-110K" or "£85-105K IC / £115-140K leadership"

# Tier scoring rubric. Score each dimension 1-3, sum across all five, then
# apply tier_thresholds. Senior-PM-tuned defaults — edit values inline if your
# preferences differ.
tier_weights:
  role_fit:
    1: "IC-only or >8 direct reports (GM scope)"
    2: "Senior PM (few or no reports)"
    3: "Head of Product / Lead PM / Group PM / Principal PM"
  domain_fit:
    1: "Outside target verticals (e.g. enterprise infra if you target B2C)"
    2: "Adjacent vertical"
    3: "Direct match to a target_industries entry"
  business_health:
    1: "No funding or red flags"
    2: "Funded or profitable, unclear trajectory"
    3: "Strong growth, recent funding, or profitable & scaling"
  location_fit:
    1: "Requires relocation outside acceptable region"
    2: "Remote within acceptable region"
    3: "On-site or hybrid in your city"
  competitive_edge:
    1: "No clear overlap with your background"
    2: "Partial match"
    3: "Strong direct domain/skills match"

tier_thresholds:                          # score (sum of five dimensions, max 15)
  p0: 13                                  # 13-15 → P0 — pursue now
  p1: 11                                  # 11-12 → P1 — apply when bandwidth allows
                                          # ≤10  → P2 — monitor

hard_filters:                             # exclude outright; plain-language strings
  - "More than 500 employees AND enterprise/sales-led AND no PLG signal"
  - "More than 8 direct reports (GM scope)"
  - "Requires relocation outside your acceptable region"

company_shape_adjustment:                 # role_fit ± 1, capped at 1-3
  bonus: "+1 to role_fit if 20-80 ppl, Series A-B, founder-led, with craft or PLG signal"
  penalty: "-1 to role_fit if >150 ppl AND outside target_industries AND no equity or brand signal"
---

## Positioning

{{POSITIONING}}

<!--
  2-3 paragraphs. Who you are professionally, what you solve, what kind of
  role you're aiming for. Honest form, not LinkedIn-puffed. Skills inject
  this as voice/context when drafting outreach, prep notes, case studies.
-->

## Proof Points

{{PROOF_POINTS}}

<!--
  Bullet list. Numbers required where possible. Each line is a specific
  outcome you owned with a measurable result. Skills cite these in
  evaluations and interview prep.
-->

## Moat

{{MOAT}}

<!--
  One sentence. What's the rare thing you bring that's hard to replicate?
-->

## Tone of Voice

Direct, short sentences. One idea per sentence. No filler phrases.
Honest about gaps, then reframe — never oversell. UK English. Low-pressure CTAs.
Sign off with first name only.

<!--
  These are sensible defaults. Edit to match how you actually write.
  Skills use this for any outreach/comm draft they produce.
-->

## What NOT to Frame As

- Don't position me as a process PM or stakeholder-manager.
- Don't claim AI ownership I don't have — describe collaboration with AI teams honestly.
- Don't use superlatives or vague seniority language ("truly passionate", "highly strategic").

<!--
  Anti-patterns. Skills check drafts against this list before showing them
  to you. Add your own as you notice yourself rejecting drafts for the
  same reason twice.
-->
