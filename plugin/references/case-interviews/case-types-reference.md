# PM Case Interview Types — Comprehensive Reference

A reference for Senior PM / Head of Product / CPO interviews. Covers all eight case
types you will meet across FAANG, infra/payments, Amazon-style LP loops, and Series A-B
founder-led pipelines. Each type gives: when it shows up, the framework, a worked
example, the senior-vs-junior moves, common traps, and a tactical sentence library.

> The three most-common types (1-3) include a full worked example; types 4-8 are summary-format (frameworks, senior moves, traps, tactical sentences) — consult them when prepping for a loop likely to test those types.

> Spaced-practice / 4-day drill plans live in `practice-methodology.md`, not here.

## When each case type shows up

| Case type | FAANG (Meta/Google) | Stripe / Infra | Amazon | Series A-B founder-led |
|---|---|---|---|---|
| Product Sense (FPSSL) | Core round | Yes, "product judgement" | Yes | Yes, often unstructured |
| Metric Movement (Diagnose-Validate-Fix-Land) | Meta "Execution"; Google "Analytical" | Yes | Light | Sometimes informal |
| Metric Tree (Clarify → NSM → Decompose → Validate) | Meta Execution sub-step; Google standalone | Sometimes inside product sense | Inside LP rounds | Often standalone for HoP |
| Prioritisation / Trade-off | Inside product sense | Yes, explicit | OLP "Bias for Action" | Very common for HoP |
| Strategy | Senior loop only (E6+ at Meta) | Yes, "strategy" round | "Think Big" round | **Core round** at HoP level |
| Estimation / Market Sizing | Rare for PM (more BD/BizOps) | Rare | Rare | Almost never |
| Technical / System Design PM | Google TPM, Meta infra PMs | **Core round** | APM/Sr PMT | Rare unless infra |
| Behavioural (Sr / HoP / CPO) | "Leadership & Drive" round | "Leadership" round | 5 LP rounds | Always — usually final |

---

## 1. Product Sense (FPSSL)

> **Use when** the prompt is open-ended: "you're a PM at [product], how would you improve it?" or "design a feature for [user] of [product]." No metric given, no specific direction.
>
> **Time budget:** ~22-25 min spoken.
>
> **Graded on:** structured judgement, segment + need + solution coherence, and the *cut* — what you're explicitly not doing and why. The interviewer is looking for someone who *commits*, not someone who lists.

### Trigger prompts

- "You're a PM at [Spotify / Notion / Airbnb / Duolingo]. How would you improve the product?"
- "Design a feature for [user type] of [product]."
- "What would you build next for [product]?"
- "If you joined [product] tomorrow, what would your first 90 days look like?"
- "[Product] has a hard problem with [X]. How would you approach it?"

### Framework: FPSSL — Frame → Pick → Probe → Solve → Land

| # | Stage | Time | What you ship |
|---|---|---|---|
| **1** | **Frame** | 3-4m | Clarify (4 questions) + state goal in one sentence |
| **2** | **Pick** | 2-3m | 3-4 segments, pick 1 with 3-clause reasoning + name what you're cutting |
| **3** | **Probe** | 4-5m | 4-5 needs tagged PAIN/OPP, pick 2-3 with 3-clause reasoning, **coherence check** (does the need live in the segment?) |
| **4** | **Solve** | 6-8m | 4-5 ideas (≥1 inventive), prioritise, name 1 cut + why |
| **5** | **Land** | 3-4m | NSM + 2 leading + 1 guardrail + 1 risk + **trade-off at recommendation level**. Optional senior overlay: 1-line positioning close if you can fill it authentically. |

**The senior move:** the *cut* is the work. Junior PMs list. Senior PMs commit + name what they're rejecting and why.

### Worked example — "Improve Spotify on TV"

> *Prompt: "You're a PM at Spotify. How would you improve Spotify on TV?"*

#### Frame (~3 min)

**Clarification (one breath, ~30 sec):**

> "Four scoping questions:
> 1. Specific geo or market?
> 2. Platform constraint — Apple TV, Roku, Smart TV, all?
> 3. Specific user segment, or open?
> 4. Business goal driving this — engagement, monetisation, defending against something?"

*Assumed answers: open geo, all TV platforms, open segment, goal = close the engagement gap with the mobile app.*

**Goal statement (one sentence):**

> "We're improving Spotify on TV to close the engagement gap with mobile. The metric I'll hold us to is **weekly active TV listeners with at least one session ≥15 min**."

No competitor map. No strategy preamble. Move on.

#### Pick (~2 min)

> "Four segments worth considering for Spotify TV:
> 1. **Co-listening at home** — friends/family on the sofa, dinner, parties. Social, episodic.
> 2. **Background-while-doing-something** — WFH, cleaning, cooking. Solo, frequent, low-attention.
> 3. **Lean-back discovery** — evening, alone, exploring new music.
> 4. **Music-video / visual content** — Spotify's pushing video; TV is the natural surface.
>
> I'm picking segment 2 — **background-while-doing-something** — because (1) highest frequency (potentially daily), (2) maps to TV's native strength as an always-on speaker, and (3) least served by current Spotify TV UX, which is built for browsing not 'set and forget.' The trade-off I'm accepting: I'm leaving music-video off the table — that's a separate strategic play with a different team, not the right fight inside this case."

One pick. Three reasons. Named trade-off.

#### Probe (~5 min)

> "For a user hiring Spotify TV as background while they do something else, five needs:
>
> 1. **'Start something good in under 5 seconds without thinking.'** **[PAIN]** Past 5 seconds, attention shifts and they switch to YouTube.
> 2. **'Don't make me get up to change it.'** **[PAIN]** Volume, skip, switch require the remote.
> 3. **'Last me for the duration of what I'm doing without going off-mood.'** **[PAIN]** Algorithmic radio drifts after 30-40 min; users notice and disengage.
> 4. **'Match the room, not just my taste.'** **[OPPORTUNITY]** Time of day, who's in the room, what activity — none are inputs today.
> 5. **'Make me look good when guests are over.'** **[OPPORTUNITY]** The music at a dinner is social signalling. Curation-as-identity is under-used on TV.
>
> Three pains, two opportunities. I'm solving primarily for **#1 and #3 — the 'start fast, last long' axis** — because they hit the highest-frequency moment and solving them turns this segment into a daily habit."

**Coherence check (5 seconds, out loud):** "Does start-fast / last-long actually live in the segment I picked? Yes — WFH background listening is exactly when start-fast and last-long bite hardest. Proceed."

#### Solve (~7 min)

> "Five ideas, then I'll prioritise:
>
> **a. 'Resume the room.'** Open Spotify TV → instantly resumes a multi-hour ambient mix tuned to time-of-day and listening history, zero clicks.
>
> **b. 'Workday mode.'** A one-tap '8-hour focused background session' on the TV home. One mood band, no algorithmic drift.
>
> **c. 'Phone as second screen.'** When TV is playing, phone gets persistent rich notification — skip, vol, switch — without unlocking.
>
> **d. Ambient visuals layer.** TV shows tasteful generative visuals tied to the track. Spotify becomes the background vibe of the room.
>
> **e. Improve TV recommendations.** Generic 'tune the algorithm' play.
>
> Prioritising on impact × confidence × effort:
> - **(a) Resume the room** — highest impact on need #1, medium effort, high confidence → **build first**
> - **(b) Workday mode** — high impact on need #3, low effort (curation + button) → **ship parallel**
> - **(c) Phone as second screen** — medium impact on need #2, medium effort → **sequence second**
> - **(d) Ambient visuals** — high differentiation upside, lower confidence on user demand → **park as v2; test cheaply with one visual style first**
> - **(e) Better recs** — diffuse impact, hard to move the needle → **not doing**
>
> **The cut I'm making explicitly:** rejecting the obvious 'tune the recommendation engine' play even though it sounds safe. It doesn't change behaviour at the moment that matters — the first 5 seconds after the user picks up the remote. The job isn't 'better next track'; it's 'don't make me pick.'"

#### Land (~3 min)

> **NSM:** weekly active TV listeners with ≥1 session ≥15 min.
>
> **Leading indicators:** time-to-first-play after app open (target median <5s); share of TV sessions ≥60 min; adoption of the one-tap entry.
>
> **Guardrail:** mobile-app engagement — grow the TV habit, don't cannibalise mobile, which has higher monetisation density today.
>
> **Risk — load-bearing assumption:** auto-play on open is welcome, not intrusive. If 'Resume the room' wakes households at 7am or plays the wrong thing when guests are over, we kill trust. I'd ship with a learned quiet-hours model and obvious mute-on-open default, and A/B-test the default state before going wide.
>
> **Trade-off accepted at recommendation level:** my recommendation accepts that we're not serving the lean-back discovery segment or the music-video opportunity this quarter. The alternative I considered was leading with music-video as Spotify's TV differentiator — I'm passing because that's a different team's bet with unclear demand evidence, whereas 'set and forget' has a clean leading indicator we can measure in 4 weeks. If 'set and forget' doesn't move the NSM by end of Q2, lean-back discovery is the natural next test.

*(Optional senior overlay — include only if you can fill the template authentically; otherwise stop at the trade-off):*

> **Positioning close:** Spotify's defensible edge on TV isn't catalogue — YouTube has that. It's **knowing what this household sounds like.** Building 'set and forget' on top of that data turns Spotify TV from a browse-the-app product into the always-on background layer of the home. That's the version of this product where Spotify wins.

*[Stop. Don't apologise for time. Don't fill silence. Look up.]*

### Tactical sentence library (the senior-discrimination moves)

**Canonical — use in every case:**

1. *"I'm picking [segment] because (1) [highest volume/severity], (2) [directly drives the goal metric], and (3) [I have a believable hypothesis to act on it]. Leaving [other] off the table because [reason]; would come back to it if [trigger]."*
2. *"Does the need I picked actually live in the segment I picked?"* — say this out loud after Probe pick, 5-second coherence check.
3. *"I'm solving for [need] because (1) [hits the segment hard/frequently], (2) [drives the NSM], and (3) [we have an unfair advantage to solve it via [data/position/insight]]."*
4. *"The cut I'm making explicitly is [obvious safe option]. Reason: [it doesn't change behaviour at the moment that matters]."*
5. **(The canonical Land closer — Meta grades this explicitly):** *"The trade-off my recommendation accepts is [specific cost]; the alternative I considered was [Y], which I'd revisit if [trigger]."*
6. *"Past [threshold], the user [bails to X]"* — quantified pain in the so-clause of a JTBD need.
7. *"The inventive play here is [X] — it [inverts an assumption / uses a uniquely available signal / removes a step]. Most competitors won't have thought of it."*

**Optional senior overlay — only if you can fill it authentically:**

8. *"This works because [unique-to-this-company advantage] + [trend/context] = [strategic outcome the CEO cares about]."* — Positioning close. NOT in any standard framework (CIRCLES/Aakash/StellarPeers don't have it). It's a senior-overlay move that lands at CPO and founder rounds when the strategic claim is real. If you can't fill the template with specifics, **drop it** — ending at the trade-off (#5) is canonically complete. A forced positioning sentence is worse than no positioning sentence.

### Solutions distribution (force this shape across your 4-5 ideas)

| Shape | Source |
|---|---|
| **Safe play** | Improve existing flow |
| **Leverage play** | Use a unique-to-this-company asset |
| **Inventive play** | Invert assumption / borrow from adjacent / remove a step |
| **Wild play** | Way-out, often the one you cut — naming it shows range |

The inventive play is the senior-vs-competent line. Where it comes from:
- **Invert the assumption:** "everyone thinks Spotify TV is for browsing. What if you never browsed?" → 'Resume the room.'
- **Borrow from adjacent:** "Netflix has Continue Watching. What's the music version?"
- **Use a uniquely available signal:** "TV knows it's 3pm Tuesday. What changes if you use that?"
- **Remove a step:** "what if the user never picked a track?"

### Common traps

| Trap | Why it kills you |
|---|---|
| Listing ideas joined by "or" | Pick ONE. "Or" = haven't decided. |
| Re-architecting segments mid-flow | Commit once. Push through even if the pick feels wrong later. |
| Probe = 2 needs collapsed into one | Forces 4-5 needs minimum, tagged PAIN or OPPORTUNITY |
| Need doesn't live in segment | Always coherence-check before solving |
| Full JTBD template in delivery ("when I…, I want to…, so I can…") | Sounds rehearsed. Use lean format: user-voice headline + tag + 1-line consequence |
| No inventive play | All ideas are algorithm tweaks = competent, not senior |
| No explicit cut | Reads as "I'll build everything" — false |
| "Improve recommendations" as a solution | Almost always the wrong answer; recs are the safe play, never the leverage play |
| Skipping the trade-off at recommendation level | This is the canonical Land closer Meta grades on. Skipping it = junior. |
| Forced positioning close | A weak business case ("this works because Spotify is a leader") is worse than no business case. Drop if you can't fill the template authentically. |

---

## 2. Metric Movement (Diagnose-Validate-Fix-Land)

> **Use when** the prompt names a specific metric and asks you to either (a) diagnose why it moved, or (b) improve it by some target.
>
> **Time budget:** ~22-25 min spoken.
>
> **Graded on:** root-cause analysis (for drops) or lever-identification (for improvement goals) + product judgement. Less about creative ideation, more about structured thinking.

### Trigger prompts

- "Our WAU dropped 15% last month. What happened?"
- "We need to improve activation from 30% to 45% in two quarters. How?"
- "Feature X has 40% week-1 adoption and 8% week-4 adoption. What would you do?"
- "Our top-decile NRR fell from 130% to 110% — diagnose it."
- "Free-to-paid conversion has plateaued. Walk me through how you'd grow it."

### Framework: Diagnose-Validate-Fix-Land

**Step 1 — Fork at the top:** *Is this a drop to diagnose, or a goal to hit?*

Both branches share Validate + Fix + Land. The fork only changes how you open.

| Stage | Time | Drop branch | Improvement branch |
|---|---|---|---|
| **1. Clarify** | 2-3m | Metric definition + shape of curve + segment breakdown + significance check | Metric definition + current baseline + segment breakdown + what's been tried |
| **2. Diagnose / Find levers** | 6-8m | Trial vs retention reframe → MECE internal vs external → hypotheses → pick lead with reasoning from data shape | Decompose metric into components → identify levers per sub-component → pick highest-leverage with reasoning |
| **3. Validate** | 2-3m | Multi-modal: quant + qual + observational. Score by frequency × severity × leverage | Same — what data confirms the lever actually moves the metric |
| **4. Fix / Plan** | 5-7m | Solutions tied to root cause; prioritise; **name explicit cut** | Interventions tied to highest-leverage levers; prioritise; name explicit cut |
| **5. Land** | 2-3m | NSM-tied success metric + 1 risk + 1-line business case | Same + holdout/ramp plan |

**Senior move:** don't jump to ideas in either branch. First 8 min are about correctly identifying *what's broken* or *where leverage is*. Junior PMs list 10 improvements; senior PMs decompose, then target.

### Worked example — Jira AI Assistant adoption drop

> *Prompt: "Jira launched an AI assistant that summarises tasks. Week 1 adoption: 40%. Week 4: 8%. What would you do?"*

#### Clarify (~2 min)

> "Five quick scoping questions:
> 1. Adoption metric — % WAU who used ≥1x, or repeated use?
> 2. Is week 4's 8% the same week-1 cohort, or current weekly rate?
> 3. Surfacing — pushed or pulled?
> 4. User base — all Jira users, or measured within a role?
> 5. Is there a role breakdown of retention?"

*Interviewer reveals: all Jira users, pulled surface, PMs drop fastest.*

That role data is gold — anchor the diagnosis on it.

#### Diagnose (~7 min)

**Reframe trial vs retention.**

> "40% week 1 means discovery worked. 8% week 4 means retention failed. 80% drop — classic high-trial, low-value-on-second-use shape. The case isn't 'improve adoption,' it's 'why didn't the 60% of triers come back?'"

**Pick the segment with 3-clause logic.**

> "I'm picking PMs because (1) they're the steepest drop, (2) they're org-level Jira decision-makers — losing them risks strategic position, not just engagement, and (3) I have a believable theory: PMs being the *fastest* churners tells me something specific about value-fit."

**Name the deeper insight.**

> "The assistant was designed for the user who lacks context — but adopted by the user who has the most context. PMs are sophisticated tool-tryers, so week-1 40% was inflated by their curiosity. Week-4 8% reveals reality."

**Hypotheses (6 across 4 categories):**

| Category | Hypothesis |
|---|---|
| Context fit | **H1:** PMs hold the strategic narrative; AI summary is below their mental model — they stop opening it |
| Unit of analysis | **H2:** PMs work across 30+ tasks surveying, not deep-diving — per-task summary is wrong unit |
| Job competition | **H3:** Summarising is the PM's paid job; AI competes with their synthesis at lower quality |
| Wrong moment | **H4:** Shown on task-open; real need is task return-after-absence or stand-up prep |
| Output quality | **H5:** Summaries generic / paraphrasing visible content |
| Trust | **H6:** Inaccurate early summaries killed trust |

**Lead pick + shape-of-decay reasoning.**

> "H1 + H2. The smooth 4-week decay rules out trust collapse (H6) and acute quality (H5) — those produce a cliff not a slide. PMs specifically dropping fastest rules out generic quality and wrong-moment — those would hit ICs and EMs similarly. PMs being the canary points specifically to context-fidelity and unit-of-analysis."

#### Validate (~3 min)

> "Most important ≠ most loudly complained. I'd triangulate three ways:
> - **Quant** for what's happening: cross-task vs per-task usage, session length, time-of-day clustering
> - **Qual** for why: 6-8 PM interviews — 'walk me through your last week,' not 'how do you feel about the assistant'
> - **Observational** for what they do vs say: 1-week diary study
>
> Score problems by frequency × severity × leverage. Build for what appears in all three methods; noise is what only appears in one."

#### Fix (~6 min)

- **Fix 1 (highest leverage) — Cross-task PM view.** "What needs my decision this week? Which dependencies shifted? Where is the team waiting on me?" A job no PM can do efficiently themselves; AI genuinely better than human scanning.
- **Fix 2 — De-target PMs from per-task surface.** Keep per-task summary for ICs returning to tasks they don't own; hide it for PMs on tasks they actively manage.
- **Fix 3 (inventive) — 1:1 brief.** AI prepares a brief before each scheduled 1:1: what changed in reports' tasks, what they might raise, what to ask. Uses calendar + Jira together.
- **Explicit cut: "Improve AI quality" alone.** Tuning a feature serving the wrong job makes it less useless, not useful. We need a different unit of analysis, not a better model.

#### Land (~3 min)

- **NSM:** WAU PMs with ≥2 cross-task brief sessions per week.
- **Leading:** 4-week cohort retention for PMs (target ≥25% from 8%); action-taken-after-view rate.
- **Guardrail:** task-completion time across all users; overall Jira engagement.
- **Risk — load-bearing assumption:** non-PM retention is healthy. If IC retention is also <10%, whole product is misconceived. Validate before scaling Fix 2.
- **Business case:** "The assistant's value isn't summarising — it's eliminating context-rebuild time. The strategic position is to make Jira the 'remembers everything for you' layer on top of work-tracking. That's a moat Linear and Asana can't easily copy because Jira has 20+ years of work-tracking context to draw from."

### How the framework adapts if the prompt is "improve adoption to 30%"

Same framework, different opener:

- **Clarify:** ask current baseline + segment + what's been tried. Skip "shape of curve."
- **Diagnose → "Find levers":** decompose adoption = awareness × trial × habit-formation; identify which sub-component is the binding constraint.
- **Validate / Fix / Land:** identical.

**Reframe for improvement:**

> "To grow adoption to 30%, I need to identify which sub-component is the binding constraint. Awareness can't take us above the visibility ceiling; trial can't exceed the activated base; habit-formation can't exceed the value-fit ceiling. I'd find which one we're closest to maxing out and unlock that lever first."

The Jira example would run: trial is already 40% (not the binding constraint) — the binding constraint is habit-formation. So the same Fix 1 (cross-task PM view) is the right intervention either way.

### Tactical sentence library (the "they write this down" lines)

1. *"Before I list hypotheses, let me check the shape of the curve — sudden cliff or gradual decay tells us which family of causes to prioritise."*
2. *"Let me separate trial from retention first — a drop in 'adoption' is two completely different problems depending on which one moved."*
3. *"I want to split MECE between internal and external — internal because we shipped or broke something, external because the world changed around us."*
4. *"Is this concentrated in a segment or universal? Concentration usually means targeting or platform; universal usually means tracking, pricing, or external."*
5. *"This feels less like a model problem and more like a job-to-be-done problem — let me check whether the users who adopted have the job we designed for."*
6. *"I'd put roughly 60% weight on hypothesis A, 25% on B, 15% on C — here's the one data cut that would shift those weights."*
7. *"Before I recommend a fix, the trade-off I'm accepting is X — here are the two alternatives I considered and why I'm not picking them."*
8. *"I'd validate with a holdout — leading indicator at week 1, durable signal at week 4, guardrail on [adjacent metric]."*

### Common traps

| Trap | Why it kills you |
|---|---|
| Jumping to ideas before diagnosing | "Maybe better onboarding" in minute 3 = junior tell |
| Listing 10 generic improvements | Range without depth = haven't decided |
| Treating one metric drop as one population | Misses segment concentration |
| Skipping trial-vs-retention split | "Adoption down" is two different problems |
| Not asking for segment breakdown | Misses the highest-information cut |
| "Improve quality" as the fix | Tuning a wrong-job feature doesn't fix the job |
| No explicit trade-off named | Reads as "all upside, no cost" — false |
| Skipping holdout/ramp in Land | No FAANG-shipping signal |

---

## 3. Metric Tree (Clarify → NSM → Decompose → Validate)

> **Use when** the prompt asks you to design how a product's success would be measured top-to-bottom — not just one NSM, but the full causal chain of inputs the team can act on.
>
> **Time budget:** ~22-25 min spoken.
>
> **Graded on:** business-model fluency, causal decomposition, and whether each leaf is actually a lever the team can move. Not creative ideation.

### Trigger prompts

- "Build a metric tree for [Spotify / Notion / Stripe]."
- "If you were the PM for X, what would you measure and how would the metrics connect?"
- "Walk me through the success metrics for [product]. Show me how the team would use them weekly."
- "What's your North Star for X, and what drives it?"
- "Design a measurement framework for [new feature] across launch, ramp, and steady-state."

### Framework: Clarify → NSM → Decompose → Validate (4 stages)

| Stage | Time | What you ship |
|---|---|---|
| **1. Clarify** | 2-3m | Product + business model + strategic goal + who'll use this tree (CEO / team / both) |
| **2. Define NSM** | 3-4m | One top-level metric. Unit + behaviour + threshold + cadence. Defended against alternatives. |
| **3. Decompose** | 8-10m | Break NSM into causal inputs — equation form OR ratio form. Two levels deep. Each leaf = a lever the team can move. |
| **4. Validate the tree** | 5-7m | Completeness check; controllability check; measurability check; Goodhart's-law pressure test; add counter-metrics + guardrails. |

**Senior move:** the tree is only useful if the leaves are *operable*. A tree that bottoms out at "engagement" is decoration. A tree that bottoms out at "% of new users who add ≥1 song to a playlist in week 1" is a roadmap.

### Equation form vs ratio form (decomposition styles)

You'll use both. Pick the right one for each layer.

| Style | Shape | Use when |
|---|---|---|
| **Equation form** | NSM = A + B + C | Components are additive sub-populations (e.g., total listening hours = new + returning + resurrected user hours) |
| **Equation form (multiplicative)** | NSM = A × B × C | Components compound (e.g., revenue = users × paying% × ARPU) |
| **Ratio form** | NSM = numerator / denominator | The metric is a rate or quality measure (e.g., activation rate = activated users / new sign-ups) |

**Senior tell:** name which form you're using and why before decomposing. Junior PMs mix them silently and end up with double-counted leaves.

### Worked example — Spotify metric tree

> *Prompt: "Build a metric tree for Spotify."*

#### Clarify (~2 min)

> "Three quick questions:
> 1. Which side of Spotify — listener side, creator side, or advertiser side? I'll assume listener.
> 2. Business model focus — engagement (ad-supported) or subscription retention (Premium)? I'll assume both since they share the upstream lever (engaged listening), and split where they diverge.
> 3. Who'll use this tree — exec board or team weekly review? I'll design for team weekly review with a CEO-facing roll-up at the top."

#### Define NSM (~3 min)

> "Spotify is a pay-to-amplify freemium product — free users get the core experience (real listening), Premium amplifies (no ads, offline, higher quality). So the leading indicator of revenue isn't 'paying users' — it's *engaged listening at the value-moment*, regardless of paid status. Because:
>
> - A non-listening user won't upgrade (Premium doesn't fix 'I never use this')
> - A heavily-engaged free user is the leading indicator of conversion to Premium AND of high ad inventory yield
>
> **NSM: Weekly Active Listeners with ≥3 hours listened.**
>
> - Unit: listener (covers free + paid)
> - Behaviour: hours listened (the actual value delivered)
> - Threshold: ≥3 hours (filters drive-bys, captures meaningful habit)
> - Cadence: weekly (matches Spotify's actual usage rhythm)
>
> I'm picking this over alternatives: 'DAU' is too coarse, 'Premium subscribers' is the lagging outcome, 'hours per user' averages over a base diluted by curiosity sign-ups. WAU-with-threshold combines reach with depth."

#### Decompose (~10 min) — two levels deep

**Level 1 — Equation form (multiplicative):**

```
WAU≥3h = Total active base × % hitting 3h threshold
       = (New active + Returning active + Resurrected active) × Engagement-depth rate
```

**Level 2a — Decompose "New active":**

Ratio form:
```
New active week N = Sign-ups week N × Activation rate
```
Where **Activation rate** = % of new sign-ups who hit ≥1 song-add or ≥1 playlist follow in their first 7 days. (Spotify's actual activation milestone, per public growth-team talks.)

Leaves under Activation rate:
- % completing onboarding (taste-onboarding → first-play)
- % adding ≥1 song to library in week 1
- % following ≥1 playlist in week 1
- Time-to-first-meaningful-play

**Level 2b — Decompose "Returning active":**

```
Returning active = Last week active × W1-retention rate
```
Where **W1-retention rate** decomposes into:
- % returning via notification
- % returning organically (open app on their own)
- % returning via cross-device handoff (laptop → phone, phone → car)

The senior insight here: the *highest-leverage* leaf is organic return rate, because it's the only one that doesn't decay over time (notification fatigue, cross-device requires both devices).

**Level 2c — Decompose "Engagement-depth rate" (% hitting 3h):**

```
Engagement-depth rate = f(sessions per week × hours per session)
```
Sub-leaves:
- Sessions/week: notifications opened, organic returns, cross-device pickups
- Hours/session: track length × tracks listened × (1 - skip rate)

Skip rate is the secret leverage point — high skip rate signals bad personalisation; low skip rate compounds session length and return likelihood.

**Counter-metrics** (per branch):
- New active: "fake sign-ups" — sign-ups with zero week-1 activity (would inflate the top but lower activation)
- Engagement: track-finish rate (don't optimise hours by playing background unattended)

**Guardrails** (cross-branch):
- Premium-to-free downgrade rate (don't grow engagement by cannibalising Premium)
- Creator royalty pool sustainability (over-listening on free tier could damage label relationships)

#### Validate the tree (~5 min)

> "Three tests before I commit:
>
> **1. Completeness.** Does every parent fully decompose? Yes — total listening = (new + returning + resurrected) × depth-rate covers the full population.
>
> **2. Controllability.** Is every leaf a lever the team can move? Let me audit:
> - Activation rate ✓ (onboarding team)
> - Organic return rate ✓ (personalisation team)
> - Skip rate ✓ (ranking/discovery team)
> - Time-to-first-play ✓ (mobile app team)
>
> No 'engagement' or 'satisfaction' as leaves — those are summaries, not levers.
>
> **3. Measurability.** Every leaf instrumented in product analytics? Yes — Spotify already tracks these.
>
> **4. Goodhart's-law pressure test.** Could a hostile PM game any leaf and look good? Skip rate could be gamed by autoplaying long ambient tracks; counter-metric (track-finish + active-engagement signal) closes that loophole.
>
> **5. Leading vs lagging.** NSM is leading (predicts revenue 4-12 weeks ahead). Leaves are leading (predict NSM 1-4 weeks ahead). No lagging metrics in the tree — those (MRR, churn) belong in the CEO dashboard, not the team weekly review."

### Tactical sentence library

1. *"I'm picking [NSM] because it's the earliest signal that the user got the value the business is paid for — not the lagging outcome."*
2. *"I want one counter-metric and one guardrail per branch: counter catches us breaking our own product, guardrail catches us damaging the ecosystem."*
3. *"Every leaf in this tree has to be a lever the team can move. 'Engagement' isn't a leaf — it's a summary. Let me decompose until I hit something we can sprint on."*
4. *"I'm using equation form here because the components are additive sub-populations; I'll switch to ratio form when I decompose into rates."*
5. *"If a hostile PM wanted to game this metric, they could do [X] — so I'd pair it with [Y] to close that loophole."*
6. *"The tree has two layers in the room because that's the depth a team can act on weekly. The exec roll-up sits on top; the third layer is for quarterly reviews, not weekly."*
7. *"The highest-leverage leaf here is [organic return rate / activation milestone] — it's the only one that compounds without decaying over time."*
8. *"This NSM is leading. I'm explicitly not putting MRR or churn in the tree — those lag by 6+ weeks and belong in the CEO dashboard, not the team's weekly review."*

### Common traps

| Trap | Why it kills you |
|---|---|
| NSM = revenue | Revenue is lagging; PM has no direct levers. Pick the leading proxy. |
| Leaves that aren't levers ("engagement," "satisfaction") | Decoration, not roadmap |
| Mixing equation and ratio form silently | Double-counted leaves; tree doesn't add up |
| No counter or guardrail | Reads as junior; ignores risk dimension |
| Three+ layers deep in a 25-min round | Lost in tactics; lose the exec audience |
| Same metric in two branches | Tree isn't MECE; one move shifts both branches |
| Forgetting Goodhart's-law check | "Could this be gamed?" is the senior pressure test |
| No business-model anchor | NSM has to trace back to *how the company makes money* — otherwise it's an engagement vanity tree |

---

## 4. Prioritisation / Trade-off

"You have 3 features, prioritise them." / "100 engineers, allocate them." / "User wants A, business wants B — which?"

### Naming conventions

- **Coaches:** IGotAnOffer "Prioritisation & Trade-off"; Lewis Lin teaches a prioritisation chapter in Decode; Aakash Gupta — "Estimation/Prioritisation"; Hustle Badger — "Resource Allocation."
- **Meta:** sub-step inside Execution ("you have a roadmap, what ships in H2").
- **Stripe:** standalone "Prioritisation" can appear in Sr/Staff loops.
- **Amazon:** wrapped into "Bias for Action" and "Have Backbone; Disagree and Commit."

### Prompt patterns

1. "You have engineering capacity for 1 of these 3 features next quarter. Pick one."
2. "Sales wants enterprise SSO, growth wants self-serve onboarding, the CEO wants AI — what do you tell the team Monday?"
3. "A top customer threatens to churn unless you build X. Do you?"
4. "How do you decide what *not* to build?"
5. "You inherit a roadmap with 12 items and 4 engineers. Walk me through your first week."

### Top frameworks

**1. RICE (Intercom, Sean McBride 2017)**

Reach × Impact × Confidence ÷ Effort. Score is a single number per item; rank descending.
- Reach: users/quarter affected.
- Impact: 0.25 (minimal) / 0.5 / 1 / 2 / 3 (massive) per user.
- Confidence: % (data-backed = 100, gut = 50, moonshot = 20).
- Effort: person-months.
- **Strong for:** comparable items in the same surface; defending a roadmap with stakeholders.
- **Weak for:** strategic bets where Impact is wildly uncertain (Confidence collapses the score); items that are not substitutes; cross-team allocation.

**2. ICE (Sean Ellis, GrowthHackers)**

Impact × Confidence × Ease. Lightweight RICE. Used for growth experiments.
- **Strong for:** weekly experiment sizing; situations where Reach is constant.
- **Weak for:** roadmap-level decisions; senior rounds (reads as junior unless paired with another lens).

**3. Kano Model (Noriaki Kano, 1984)**

Classifies features by user emotional response:
- **Must-haves** — absence kills satisfaction, presence doesn't lift it (login works).
- **Performance** — linear: more is better (search latency).
- **Delighters** — absence is fine, presence creates surprise (auto-generated suggestions for a brand-new user).
- **Indifferent** — users don't care.
- **Reverse** — presence *hurts* (over-personalisation creeping users out).
- **Strong for:** B2C, UX-driven, justifying delighters that don't score on RICE.
- **Weak for:** pure-B2B contracts where buyers ≠ users; engineering trade-offs.

**4. MoSCoW (Dai Clegg, DSDM 1994)**

Must / Should / Could / Won't. Allocation, not scoring.
- **Strong for:** scoping a single release, contract delivery.
- **Weak for:** continuous discovery, senior strategic prioritisation (too coarse).

**5. Value vs Effort 2x2 (classic)**

- **Strong for:** quick visual; good for stakeholder workshops.
- **Weak for:** the answer that lands in a Sr PM interview — too simple unless paired with explicit value definition.

### Senior PM moves

- **Define "value" before you score.** Value to whom: end user, paying customer (often different in B2B), business, or platform health? Sr PMs name this; juniors apply RICE to "users."
- **Name what you're NOT doing and why.** The rejected options carry the seniority signal. *"I'd ship A and explicitly defer B for two quarters because [reason]; here's how I'd communicate that to the customer asking for B."*
- **Articulate the *one* trade-off accepted.** "Shipping A means we take on technical debt in C; we'll budget Q3 capacity to address it."
- **Bring in time horizons.** Quarter vs year vs three-year. Many roadmap conflicts dissolve once you separate "what do we ship in Q2" from "what's the bet for the year."
- **Reframe the prompt.** Senior candidates often *don't* pick from the three options — they say "you're framing this as a feature choice; it's actually a positioning choice, and once we settle that, the prioritisation falls out." Use sparingly and only when justified.
- **Acknowledge stakeholder power dynamics.** "Sales asking for X is a signal — what's the underlying customer problem? If I just shipped X I'd be doing custom dev; if I solve the *category* I get reusable revenue."

### Common traps

- Scoring with RICE then accepting the rank order with no judgement layer ("the score says ship X" — but you're the PM, not a spreadsheet).
- Picking the option the interviewer's company seems to favour (sycophancy detector).
- Saying "it depends" without naming the conditions under which each option wins.
- Treating "user wants A, business wants B" as a real conflict — usually it's a framing failure; sr PMs find the third option.
- Ignoring opportunity cost of the team's attention.
- Not naming the decision owner. "I'd recommend X to the CEO" is different from "I'd ship X."

### Tactical sentences

- *"Before I score anything, I want to be explicit about what 'value' means here — for this product, value is [X]. Otherwise we're optimising for the wrong axis."*
- *"My recommendation is A. The reason it's not B is [specific], and the reason it's not C is [specific] — those aren't bad ideas, they're just lower-leverage given [constraint]."*
- *"The trade-off I'm accepting by picking A is [specific cost]; here's how I'd mitigate it within 90 days."*
- *"This looks like a feature prioritisation but it's actually a [positioning / sequencing / pricing] decision — once we resolve that, the order falls out."*
- *"I'd defer this customer's ask, and here's the message I'd send them — I'd rather lose this one deal cleanly than pollute the roadmap with custom dev."*

### How interviewers grade

- **IGotAnOffer rubric:** "method for making choices and trade-offs; considering the most relevant factors." Score lifts when candidate explicitly names criteria, applies them, and articulates the accepted cost.
- **Stripe:** systems thinking; whether the candidate maps incentives across stakeholders before picking.
- **Meta Execution:** "strong prioritisation and understanding of tradeoffs."

---

## 5. Strategy

"Should we enter market X?" / "3-year strategy for product Y?" / "Competitor shipped Z, respond." / "CPO for a day at company X."

The most senior-coded case. Mostly absent for IC PM, near-certain for HoP/CPO loops.

### Naming conventions

- **Coaches:** Hustle Badger — "Product Strategy"; Lenny Rachitsky — "Situation, Complication, Resolution" (borrowed from McKinsey's MECE-style problem framing); IGotAnOffer — "Strategy Questions"; Aakash Gupta — "Strategy Interview."
- **Meta:** appears only at E6+ in Product Sense framed as "vision for [product] in 3 years."
- **Stripe:** explicit "Strategy" round; very common at Sr/Staff+.
- **Amazon:** "Think Big" LP-anchored strategy questions; Bar Raiser often probes vision.

### Prompt patterns

1. "You're CPO of [adjacent company]. What's your 3-year strategy?"
2. "[Competitor] just launched [feature]. How do you respond?"
3. "Should [your company] enter [adjacent market]?"
4. "What's the biggest threat to [product] over the next 5 years?"
5. "We're 18 months post-Series B. Where do we focus to get to Series C?"

### Top frameworks

**1. Situation → Complication → Resolution (McKinsey via Lenny Rachitsky)**

- **Situation:** where we are — market, product, traction, capabilities. Numbers required.
- **Complication:** what's changing or unresolved that forces a decision — competitive move, market shift, capability gap.
- **Resolution:** the bet, with sequencing.
- **Strong for:** open-ended strategy prompts ("what's your vision"). Forces the candidate to earn the recommendation.
- **Weak for:** time-boxed "should we enter X yes/no" — overkill.

**2. Porter's Five Forces (Michael Porter, 1979)**

Buyer power, supplier power, threat of new entrants, threat of substitutes, rivalry.
- **Strong for:** market entry; competitive positioning; defensibility questions.
- **Weak for:** intra-product strategy; tactical 12-month roadmap. Reads as MBA-coded if used badly; pair with concrete examples to ground it.

**3. Where to play / How to win (Roger Martin, "Playing to Win")**

Five linked choices: winning aspiration → where to play → how to win → capabilities required → management systems.
- **Strong for:** HoP/CPO-level strategy answers; sequencing capability builds.
- **Weak for:** if you can't fill all five honestly, don't invoke it; partial Martin reads worse than no framework.

**4. JTBD at strategic level (Christensen)**

Identify the "job" customer hires the product for, then map alternatives competing for the same job (often outside the obvious category).
- **Strong for:** "should we build X" questions where the right framing is "what job are we trying to own."
- **Weak for:** competitive response in commodity markets.

**5. Hustle Badger's product strategy template**

Mission → Insights (what's true about market/customers that competitors miss) → Bets → Sequencing → Anti-goals. The "insights" step is the load-bearing one; without a non-obvious insight, there's no real strategy.
- **Strong for:** in-role product strategy and interview answers where you have time.
- **Weak for:** 25-min strategy rounds — compress to insight + bets + sequencing.

### Senior PM / HoP moves

- **Lead with a *thesis*, not a framework.** "Here's what I think is true that the market hasn't priced yet" — then justify. Frameworks are for showing your work, not for replacing the bet.
- **Name the non-obvious insight.** Most candidates list facts; HoP candidates name an insight ("the market thinks X is about Y; we think it's about Z, and that re-orders the priorities").
- **Sequence the bets.** Year 1 / 2 / 3. What unlocks what. "We can't do C until we've earned the right via A; here's why."
- **Name anti-goals.** What we explicitly *won't* do. This is the clearest seniority signal in strategy answers.
- **Acknowledge the alternative strategy that loses by a hair.** "The strongest counter-argument is [X]; I'd reject it because [Y], but I'd revisit if [trigger]." Decision-artifact thinking applied at strategy level.
- **Tie to capability and team.** Strategy without "and here's the org I'd need to execute it" is a deck, not a plan.
- **Build in a kill criterion.** "If [leading indicator] hasn't moved by Q2, I'd pivot to [Plan B]."

### Common traps

- Listing frameworks instead of taking a position. Porter ≠ answer.
- Three-year vision with no Q1 action — reads as fantasy.
- Ignoring the existing team and capability constraints — strategy = bet + path, not just bet.
- "We should be the [unique-thing] for [user]" with no insight into *why* this hasn't been done.
- Assuming the company has unlimited cash and zero competitor reaction.
- Skipping the "what's the moat in 18 months" question.
- Strategy answers that are actually tactical (feature lists in disguise).

### Tactical sentences

- *"Before I commit to a recommendation, I want to state what I'm assuming — if any of these are wrong, the strategy changes."*
- *"My core thesis is [X]. The two facts that make me believe it are [Y, Z]. Here's what I'd do about it."*
- *"The bet I'm making is that [insight]. If that's wrong, we've still built [capability], which is recoverable."*
- *"Year 1 is buying us the right to do Year 2. Year 1 is [specific]; Year 2 unlocks because we now have [capability]."*
- *"The kill criterion is — if [leading indicator] hasn't moved by [date], we re-plan, because that signal means [the thesis was wrong]."*
- *"What I'm explicitly not doing is [X]. Here's the steel-man for X, and here's why I'm still passing."*

### How interviewers grade

- **Meta (Product Sense, E6+):** vision clarity, sequencing, willingness to take a non-consensus position with justification.
- **Stripe:** systems thinking ("map the ecosystem first"); whether the strategy survives a 5-min adversarial push.
- **Series A-B founder-led:** founder is testing — *would I trust this person to run a third of my roadmap autonomously?* The signal is conviction + judgement + ability to be wrong cleanly, not framework recall.
- **Hustle Badger:** quality of insight; sharpness of anti-goals.

---

## 6. Estimation / Market Sizing

"How many X are there in country Y?" / "Estimate the market for Z." / "How much storage does [product] need?"

### Naming conventions

- **Coaches:** Lewis Lin "Estimation & Market Sizing" (Decode); Aakash Gupta "Estimation"; Exponent "Market Sizing"; consulting world calls them "Guesstimates."
- **Google:** historically asked these; mostly dropped from PM loops post-2018 (still in BizOps/Strategy & Operations).
- **Meta:** rare for PM; appears as sub-step inside Execution ("how big is this opportunity").
- **Stripe / Amazon / most series A-B HoP loops:** rare standalone; common as sub-step in strategy/pricing.

### Prompt patterns

1. "How many [product type] are sold in [region] per year?"
2. "Estimate the addressable market for [feature] at [company]."
3. "How much storage does [Spotify / Gmail / YouTube] need?"
4. "How many search queries per second does [product] handle?"
5. "What's the revenue upside of [feature]?" (estimation hiding inside strategy)

### Top frameworks

**1. Top-down (TAM → SAM → SOM)**

Start from a known macro number (population, GDP, total market), narrow with successive % filters.
- **Strong for:** rough order-of-magnitude; when public data exists at the top.
- **Weak for:** estimating a new category (top doesn't exist); estimating a feature inside a product.

**2. Bottom-up (unit economics build)**

Start from a single user/transaction, multiply by volume.
- E.g. "average shopper does N searches/session, M sessions/month, K shoppers per retailer, R retailers."
- **Strong for:** feature-level estimates, anything where you can ground the per-unit number in observed behaviour. Generally preferred for senior answers.
- **Weak for:** when per-unit data is unknowable; risk of compounding small errors.

**3. Triangulation (Lewis Lin)**

Do both top-down and bottom-up, compare, explain the gap. Best practice for senior answers.

### Senior PM moves

- **Choose bottom-up unless top data is genuinely known.** Bottom-up shows product instinct; top-down shows arithmetic.
- **State assumptions explicitly and label confidence.** "I'm assuming 30% smartphone penetration — I'd confirm before committing to the number."
- **Sanity-check at the end.** "This gives £4B/year — that's roughly 10% of e-commerce search spend in EMEA, which feels in-range." A sanity check vs a known benchmark is the senior move.
- **Round aggressively.** £1.2B not £1,247,392,000. The fake precision is the junior tell.
- **Use the estimate to make a decision.** The number alone scores low; "and that's why I'd / wouldn't pursue this" scores high.
- **Acknowledge the question behind the question.** If a strategy round asks for a market size, the *real* question is "is this worth pursuing" — answer both.

### Common traps

- Spending 3 minutes on world population maths when the bottleneck is per-unit revenue.
- Not stating assumptions out loud — interviewer can't follow your reasoning.
- Confusing TAM (total) with SAM (serviceable) with SOM (capturable).
- Multiplying without sanity-checking.
- Treating the number as the answer rather than the input to a decision.

### Tactical sentences

- *"I'll go bottom-up because the unit economics are more knowable than the macro number here. Let me state my assumptions first."*
- *"I'm going to round to the nearest order of magnitude — the precision lives in the assumptions, not the multiplication."*
- *"That gives roughly £X. Sanity check: this is about [known benchmark]. That feels [right / off by 2x because…]."*
- *"The number matters because it tells us [decision]; if it's £100M we ship, if it's £10M we don't."*

### How interviewers grade

- Structure of decomposition > arithmetic accuracy.
- Quality of assumptions and willingness to revise them out loud.
- Sanity-check at the end (signals senior).
- Whether the candidate connected the number to a decision.

---

## 7. Technical / System Design PM

"Design an API for X." / "Walk me through how Y works." / "Design notifications for Z." / "How does ranking work and what would you change?"

Core for infra PM, technical PM, and most search/ranking roles.

### Naming conventions

- **Google:** "Technical PM" round for TPM track; "Product Architecture" for senior infra PM.
- **Meta:** "Technical depth" sub-step in some infra PM loops.
- **Stripe:** "Technical Depth" — explicit round, expected at every level.
- **Amazon:** "Technical PM" loop has system-design lite; senior PMTs get full system design.
- **Coaches:** Exponent "System Design for PMs"; Hello Interview "PM Technical Round"; Lewis Lin covers it in Decode chapter on technical questions.

### Prompt patterns

1. "Design the API for [feature]." (e.g. an autocomplete endpoint)
2. "Walk me through how [ranking / search / payments] works under the hood."
3. "Design a notifications system for [product]."
4. "How would you scale [feature] to 10x traffic?"
5. "We're seeing 200ms p95 on search — walk through where the time is going and what you'd improve."

### Top frameworks

**1. Functional → Non-functional → Components → Trade-offs (Exponent / Hello Interview)**

- **Functional requirements:** what the system does (API contracts, user flows).
- **Non-functional:** latency, throughput, availability, consistency, cost.
- **High-level components:** clients, load balancer, app servers, cache, DB, queues, workers.
- **Trade-offs:** CAP-position, SQL vs NoSQL, sync vs async, push vs pull.
- **Strong for:** PM technical rounds; pairs well with most prompts.
- **Weak for:** very deep IC engineering rounds (those want algorithm-level reasoning).

**2. CAP theorem framing (Brewer 2000)**

Consistency, Availability, Partition tolerance — pick 2 (in practice, partition is forced, so it's C vs A under partition).
- **Strong for:** trade-off articulation in distributed systems; payments (Stripe loves this) and search infra both relevant.
- **Weak for:** simple stateless services where CAP doesn't bite; using it as a buzzword without applying it to the actual choice.

**3. PACELC (Daniel Abadi extension)**

If Partition → A or C. Else (normal ops) → Latency or Consistency.
- **Strong for:** senior infra PM answers; shows you know CAP is incomplete.
- **Weak for:** non-distributed-systems prompts.

### Senior PM moves

- **Start with functional requirements out loud.** Most candidates jump to components. "First — let me state what this system needs to do, then what 'good' looks like (latency, throughput, availability), then we'll size it."
- **State an order-of-magnitude estimate up front.** "10M users, 100 reqs/user/day = 1B reqs/day = ~12K rps avg, p99 burst ~100K rps" — this anchors every component choice.
- **Trade-offs over correctness.** A PM answer is not "the architecture" — it's the *choice* between options with named trade-offs. "We could push or pull notifications. Push wins on freshness, loses on scale to inactive users. For our case I'd pick pull-with-server-hint because [X]."
- **Mention cost and ops, not just perf.** Sr PMs ask "what does this cost to run?" and "who pages at 3am?" — IC engineers often skip both.
- **Name what's out of scope.** "I'm not going to design auth or billing in this round; assume those exist." Saves time and signals seniority.
- **Connect to product impact.** "Lowering p95 from 200ms to 80ms is worth N basis points of conversion based on [benchmark]." Pure systems answers without product framing are also weak for PM rounds.

### Common traps

- Drawing boxes without naming traffic patterns first.
- "We'd use Kafka" — *why* Kafka over SQS/Redis Streams/Kinesis? The buzzword without the trade-off is a junior tell.
- Ignoring failure modes. "What happens when the cache goes down?" should be answered before the interviewer asks.
- Over-engineering. A v1 doesn't need a multi-region active-active deployment.
- Pretending depth you don't have. If you don't know what a consistent hash is, say so — Stripe explicitly rewards humility over bluffing.
- Forgetting that this is a PM round, not an engineer round — the *product* trade-off must surface.

### Tactical sentences

- *"Before I draw any boxes, let me get explicit about the workload — reads vs writes, latency target, consistency requirement."*
- *"Order of magnitude: [N] users, [M] req/sec average, peak ~[K] — that decides whether we're in single-region territory or not."*
- *"For this system the dominant trade-off is [latency vs consistency / push vs pull / sync vs async]. I'd lean [X] because [product reason]."*
- *"Here's the failure I'd plan for first: [specific]. The blast radius is [N] users for [M] minutes, and the recovery story is [path]."*
- *"I want to flag what I'm not designing today: [auth, billing, analytics]. Happy to come back if useful."*

### How interviewers grade

- **Stripe:** trade-off articulation under technical pressure; written-first clarity; willingness to say "I don't know" rather than bluff.
- **Google TPM:** systems mental model; ability to estimate; clean component decomposition.
- **Amazon Sr PMT:** ownership signals (who pages, what's the SLO, how do we measure).

---

## 8. Behavioural (Senior / HoP / CPO)

Senior loops test what is *specific* to senior leadership rounds vs IC PM behavioural rounds. Use `story-builder` to maintain your universal STAR-story bank, and `story-taxonomy.md` to check which senior-PM story types you're missing.

### Naming conventions

- **Meta:** "Leadership & Drive."
- **Amazon:** "Leadership Principles" — 5 rounds, 2-3 LPs each, Bar Raiser overlay.
- **Stripe:** "Leadership."
- **Google:** "Googleyness & Leadership."
- **Series A-B founder-led:** usually a founder round + 1-2 ops/Eng peer rounds — less structured, more lethal.

### Prompt patterns (Sr / HoP / CPO specific)

1. "Tell me about a time you had to fire a senior person."
2. "Describe a strategy you championed that turned out to be wrong."
3. "Walk me through how you'd assess the product org in your first 30 days."
4. "Tell me about a time you disagreed with the CEO."
5. "When did you have to descope or kill a product after significant investment?"
6. "Tell me about a hire that didn't work out — what did you miss?"
7. "How do you decide whether to manage or be a senior IC?"

### Top frameworks

**1. STAR (classic) + senior overlay**

Situation → Task → Action → Result.
- **Senior overlay:** what *trade-off* did you accept; what would you do differently; what was the second-order effect.

**2. DIGS (Lewis Lin, Decode and Conquer)**

Dramatise (set the stakes) → Indicate (your role and what was at risk) → Go Through actions (specific, sequenced) → Summarise impact + learning.
- **Strong for:** generative thinking under high-bar follow-ups; transforms memorised stories into adaptable answers.
- **Weak for:** Amazon LP rounds where STAR is the expected structure — DIGS can read as evasive there.

**3. Decision-Artifact format**

Setup → Options (including ones ruled out) → The Call (+ trade-off accepted) → Reasoning (evidence used, instincts overridden, pushback received) → Retrospective (what worked, what partly failed, what you'd change).
- **Strong for:** Senior loops, particularly founder rounds and Bar Raiser. Reads as Director-level judgement.
- **Weak for:** if compressed into <90s, loses force; deploy when interviewer probes.

### Senior PM / HoP / CPO-specific moves

- **Stories must scale.** A Sr PM story shows IC craft + small-team leverage. A HoP story shows org design, hire/fire, capital allocation across a portfolio. Use the right altitude for the role — a HoP candidate telling a "I shipped this feature" story sounds like a Sr PM.
- **Name what you got wrong.** Senior loops weight self-awareness 2x. "What I learned" beats "what I achieved."
- **Rejected paths > final outcome.** Two real alternatives + trade-off accepted + retrospective. Surface this when probed; the upfront opener stays 60s.
- **Team outcomes, not personal heroics.** "I" for the decisions, "we" for the execution.
- **Honest about hiring misses.** A HoP/CPO who's never had a bad hire either hasn't hired enough or isn't honest.
- **Founder rounds at Series A-B:** the founder is asking "will I trust you on Monday." Answer the question behind the question. "Tell me about a strategy you championed that was wrong" = "are you safe to delegate to."
- **Founder-vetting questions back (late-stage / final):** ask the questions that separate building from politics — how decisions actually get made, where the last roadmap fight landed, what the founder would never delegate.

### Common traps

- The 4-minute opener. Long answers kill senior rounds — 60s, then breathe, then deepen on probe.
- "We" everywhere — interviewer can't isolate the candidate's contribution.
- The "perfect" story with no failure mode named.
- IC-altitude stories for HoP roles (or vice-versa).
- Telling instead of showing — "I'm a strong leader" with no specific decision.
- Generic STAR with no specific company nouns ("the company," "the team" instead of names, products, metrics).
- Practising stories word-for-word — anchor-based delivery beats memorisation under stress.

### Tactical sentences

- *"The decision was mine. The execution was the team's. Here's the call I made, the two options I rejected, and the one trade-off I accepted."*
- *"In retrospect, the part I'd change is [X]. What I'd repeat is [Y]. Here's what I now look for that I didn't before."*
- *"The hardest part wasn't shipping it — it was deciding what we'd stop doing to make room for it."*
- *"I was wrong about [X]. I caught it because [signal]. Cost us [N] weeks; the recovery was [path]."*
- *"That hire didn't work. The reason wasn't [obvious thing] — it was [specific]. I now interview for [X] differently."*

### How interviewers grade

- **Amazon:** explicit LP-mapping; STAR completeness; depth of follow-up survival (the Bar Raiser probe is 2-3 layers deep).
- **Meta Leadership & Drive:** ability to lead, deal with conflict, facilitate communication.
- **Stripe:** humility paired with conviction; whether the candidate's stories scale with the level applied for.
- **Series A-B founder:** unstructured, but the founder is testing — judgement under uncertainty, will they own the outcome, will they push back when needed.

### Picking the right altitude

Sr PM stories show IC craft + small-team leverage — you in the weeds, shipping, moving a metric with a handful of people. HoP / CPO stories show org design, hire/fire decisions, and portfolio-level capital allocation across multiple teams. Pick the altitude that matches the role: a HoP loop wants org-and-portfolio stories and will read a "I shipped this feature" answer as under-levelled; a Sr PM loop wants craft-and-execution stories and will read a "I restructured the org" answer as over-reaching for the scope on offer. Use `story-builder` to capture stories at both altitudes and tag their `role_lens`, and `story-taxonomy.md` to spot which altitude you're thin on before the loop.

---

## Sources

- [The Ultimate PM Interview Bible — Aakash Gupta](https://www.news.aakashg.com/p/complete-pm-interview-guide)
- [PMs Keep Failing This Interview: Success Metrics — Aakash Gupta](https://www.news.aakashg.com/p/success-metrics-interview)
- [Cracking PM Interviews: Estimation — Aakash Gupta](https://aakashgupta.medium.com/cracking-product-management-interviews-a-strategic-guide-to-estimation-questions-used-at-google-c0a10b23e4de)
- [How to Use Google's HEART Framework — ProductPlan](https://www.productplan.com/learn/heart-framework-product-decisions)
- [Goals-Signals-Metrics — The Fountain Institute](https://www.thefountaininstitute.com/blog/goals-signals-metrics)
- [Product Metric Interviews — IGotAnOffer](https://igotanoffer.com/blogs/product-manager/product-metric-interview-questions)
- [Prioritization & Trade-Off Questions — IGotAnOffer](https://igotanoffer.com/blogs/product-manager/prioritization-and-trade-off-interview-questions)
- [RICE Prioritization Framework — Intercom](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/)
- [Prioritization Techniques — Get Product People](https://www.getproductpeople.com/blog/prioritization-techniques-rice-moscow-ice-kano)
- [How to Write a Great Product Strategy — Hustle Badger](https://www.hustlebadger.com/product-management/product-strategy/)
- [Lenny's Product Strategy Essentials — Product Folks](https://www.theproductfolks.com/product-management-blog/lenny-rachitskys-product-strategy-essentials)
- [Preparing for a PM Interview — Lenny Rachitsky](https://www.lennysnewsletter.com/p/preparing-for-a-pm-interview)
- [Decode and Conquer — Lewis Lin](https://lewis-lin.com/decode-and-conquer/)
- [System Design Interview Prep — Exponent](https://www.tryexponent.com/blog/system-design-interview-guide)
- [CAP Theorem for System Design — Hello Interview](https://www.hellointerview.com/learn/system-design/core-concepts/cap-theorem)
- [Stripe PM Interview — IGotAnOffer](https://igotanoffer.com/blogs/product-manager/stripe-product-manager-interview)
- [Meta Analytical Thinking Interview — IGotAnOffer](https://igotanoffer.com/blogs/product-manager/facebook-execution-interview)
- [Meta Leadership & Drive Interview — IGotAnOffer](https://igotanoffer.com/en/advice/meta-leadership-and-drive-interview)
- [Amazon Behavioral Interview Questions — Exponent](https://www.tryexponent.com/blog/how-to-nail-amazons-behavioral-interview-questions)
- [Amazon Leadership Principles — IGotAnOffer](https://igotanoffer.com/en/advice/amazon-leadership-principles)
- [Counter Metric vs Guardrail — Product Simply](https://medium.com/product-simply/whats-the-difference-between-a-guardrail-and-a-countermetric-product-management-interview-tips-0e2de9ce78ae)
- [Chief Product Officer Interview Questions — Yardstick](https://www.yardstick.team/interview-questions/chief-product-officer)
