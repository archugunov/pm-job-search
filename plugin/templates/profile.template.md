<!--
  pm-job-search — profile template.

  /setup fills in {{PLACEHOLDERS}} from your answers and leaves this file in
  userdata/profile.md as the single source of truth for all skills.

  - Placeholders ({{X}}) → answered during /setup.
  - Hardcoded values (tier_weights, tier_thresholds, company_shape_adjustment)
    → opinionated senior-PM-tuned defaults; edit values inline if your
    preferences differ.
  - Empty prose sections → you fill in your own. Skills use what you write
    here as voice/context when drafting outreach, prep notes, case studies.
-->
---
name: {{NAME}}                            # your full name
city: {{CITY}}                            # e.g. "London, UK"
timezone: {{TIMEZONE}}                    # IANA, auto-detected (e.g. "Europe/London")
email: {{EMAIL}}
linkedin_url: {{LINKEDIN_URL}}

target_titles: {{TARGET_TITLES}}          # YAML list. /setup writes from your answers.
                                          # Examples: Head of Product, Lead PM, Senior PM, VP Product.

target_industries: {{TARGET_INDUSTRIES}}  # YAML list. /setup writes from your answers.
                                          # Examples: fintech, B2C SaaS, PLG SaaS, DevTools, creator tools.

geography:
  mode: {{GEOGRAPHY_MODE}}                # onsite | remote | both | other
  mode_detail: {{GEOGRAPHY_DETAIL}}       # optional free text (e.g. "open to EMEA relocation")

salary_band: "{{SALARY_BAND}}"            # single open string; any currency
                                          # examples: "£90-110K" or "$190-230K base + equity"

# Tier scoring rubric. Score each dimension 1-3, sum across all five, then
# apply tier_thresholds. Senior-PM-tuned defaults — edit values inline if your
# preferences differ.
tier_weights:
  role_fit:
    1: "IC-only or >8 direct reports (GM scope)"
    2: "Senior PM (few or no reports)"
    3: "Head of Product / Lead PM / Group PM / Principal PM"
  domain_fit:
    1: "Outside target verticals"
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

hard_filters: {{HARD_FILTERS}}            # YAML list. /setup writes from your answers.
                                          # Plain-language strings. Companies matching any of these
                                          # are excluded outright. Examples:
                                          #   - "More than 500 employees AND no PLG signal"
                                          #   - "More than 8 direct reports (GM scope)"
                                          #   - "Requires relocation outside Europe"

company_shape_adjustment:                 # role_fit ± 1, capped at 1-3
  bonus: "+1 to role_fit if 20-80 ppl, Series A-B, founder-led, with craft or PLG signal"
  penalty: "-1 to role_fit if >150 ppl AND outside target_industries AND no equity or brand signal"
---

## Positioning

{{POSITIONING}}

<!--
  2-3 paragraphs. Who you are professionally, what you solve, what kind of
  role you're aiming for. Honest form, not LinkedIn-puffed.
-->

## Proof Points

{{PROOF_POINTS}}

<!--
  Bullet list. Numbers required where possible. Each line is a specific
  outcome you owned with a measurable result.
-->

## Moat

{{MOAT}}

<!--
  One sentence. The rare thing you bring that's hard to replicate.
-->

## Tone of Voice

<!--
  Write 3-6 lines describing how skills should sound when they draft
  outreach, debriefs, or case studies on your behalf. Cover:
  - Sentence length and rhythm (short vs flowing)
  - Vocabulary register (casual vs formal)
  - English variant (UK / US / EU-international)
  - Sign-off convention
  - CTA style (direct vs low-pressure)

  Skills use this verbatim. The more honest, the more your drafts sound
  like you.
-->

## What NOT to Frame As

<!--
  Bullet list of anti-patterns. Skills check drafts against this list before
  showing them to you. Add your own as you notice yourself rejecting drafts
  for the same reason twice.

  Useful prompts to seed this section:
  - What kind of PM are you NOT? (e.g. "not a process PM", "not a marketer")
  - What claims would feel like overreach for your actual experience?
  - What language patterns make you cringe in others' profiles?
-->
