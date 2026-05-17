# Senior PM story taxonomy

Reference doc for `/story-builder` (gap analysis) and `/interview-prep` (story-selection tiebreaker). Defines 12 story types senior PMs need in their bank, the round-types each type tends to be probed in, and the level-differentiation (which types HoP rounds probe more heavily than Senior PM rounds).

User overrides: drop `userdata/references/story-taxonomy.md` to add or rename story types.

## The 12 story types

Every senior PM's universal story bank should cover most of these. A complete bank doesn't mean one story per type — it means each type has at least one strong story that can be adapted to multiple prompts via the "Angles for different prompts" structure.

### 1. Ambiguity / 0-to-1

**What it shows:** Comfort starting from a vague problem, framing it, defining success, picking the first bet.

**Common probe phrasings:** "Tell me about a time you started something from scratch." / "How did you decide what to build first?" / "Walk me through a 0-to-1 launch you led."

**Strongest signals to weave in:** how you framed the problem, what hypothesis you tested first, what you ruled out, how you knew when to stop iterating.

### 2. Strategic pivot

**What it shows:** Ability to recognise the original plan isn't working and reframe the bet without burning credibility.

**Common probe phrasings:** "Tell me about a time you changed direction mid-stream." / "When did you realise the plan was wrong?" / "How do you decide when to kill a project?"

**Strongest signals to weave in:** the specific signal that triggered the pivot, how you brought the team along, what you preserved vs scrapped, what the outcome was.

### 3. Scope contraction

**What it shows:** Discipline to cut scope under constraint; saying no to good ideas to ship a great one.

**Common probe phrasings:** "Tell me about a time you cut scope." / "What did you NOT ship and why?" / "How do you prioritise when everything seems important?"

**Strongest signals to weave in:** what specifically got cut, the criteria you used, the trade-off you accepted, the conversation with stakeholders who wanted the cut features.

### 4. Stakeholder dissent

**What it shows:** Navigating disagreement without flattening into either dictatorship or consensus paralysis.

**Common probe phrasings:** "Tell me about a time you disagreed with your manager / a peer / engineering." / "How do you handle stakeholder pushback?" / "Walk me through a tough conversation."

**Strongest signals to weave in:** what you understood about their position, where you held the line, where you moved, how you preserved the relationship.

### 5. Failed launch / postmortem

**What it shows:** Ownership of failure; learning instead of blame; honest reflection.

**Common probe phrasings:** "Tell me about a project that failed." / "What's something that didn't work?" / "Walk me through your worst launch."

**Strongest signals to weave in:** what specifically failed (be concrete), what your role was in it, what you learned, what you'd do differently. **Never the answer "we shipped on time but adoption was lower than expected" without owning the part you missed.**

### 6. Hiring decision (or wished-had-fired)

**What it shows:** Senior judgment on people; willingness to make hard calls; comfort with hiring rubrics.

**Common probe phrasings:** "Tell me about a hire you're proud of." / "Have you ever fired someone? Or wished you had?" / "How do you evaluate PM candidates?"

**Strongest signals to weave in:** the specific bet you made, what signals you weighted, the outcome, what you'd do differently. For "wished had fired": the cost of NOT firing, the relationships affected, what you learned about your own threshold.

### 7. Build vs buy vs partner judgment

**What it shows:** Strategic judgment under constraint; thinking beyond "we should build this".

**Common probe phrasings:** "Tell me about a time you decided not to build something." / "How do you evaluate build vs buy?" / "When did you partner instead of going alone?"

**Strongest signals to weave in:** the trade-off you considered, the constraints you weighed (time, cost, capability), the second-order effects you anticipated.

### 8. Pricing / monetization

**What it shows:** Comfort with the business model; willingness to engage with revenue not just product.

**Common probe phrasings:** "Tell me about a pricing decision." / "How did you approach monetization for X?" / "Walk me through a pricing experiment."

**Strongest signals to weave in:** the model you tested, the elasticity signal, what you learned about willingness-to-pay, how the change affected acquisition / retention / LTV.

### 9. Activation / retention experiment

**What it shows:** Comfort with growth-loop thinking; data-driven iteration; understanding of leading-vs-lagging metrics.

**Common probe phrasings:** "Tell me about an activation experiment." / "How did you improve retention?" / "Walk me through a metric you moved."

**Strongest signals to weave in:** the metric you chose and why, the hypothesis, the intervention, the result, what you learned about user behaviour vs your model of it.

### 10. Ethical edge / values trade-off

**What it shows:** Willingness to engage with hard trade-offs; not optimising for ship-it metrics alone.

**Common probe phrasings:** "Tell me about a time your team made a tough ethical call." / "How do you balance user value with business value?" / "When did you push back on something that would have shipped a metric?"

**Strongest signals to weave in:** the specific tension you saw, how you surfaced it, the call you made, what you traded off, what you'd do again vs differently.

### 11. Crisis management

**What it shows:** Composure under fire; ability to act under uncertainty; ownership of impact.

**Common probe phrasings:** "Tell me about a time something broke." / "Walk me through your worst day at work." / "How did you handle a customer-facing incident?"

**Strongest signals to weave in:** the specific situation, what you did in the first hour, who you involved, what you learned about your team and the system.

### 12. Bet that paid off — and one that didn't

**What it shows:** Honesty about your own track record; pattern recognition across wins and losses.

**Common probe phrasings:** "Tell me about a bet you're most proud of." / "What's a decision you got right? One you got wrong?" / "What's your hit rate on big calls?"

**Strongest signals to weave in:** for the win, what made it a non-obvious call vs obvious. For the loss, what made you confident at the time + what specifically broke the thesis.

## Coverage matrix — which round probes which type

Heavy probing = X. Likely probing = ·. Empty = unlikely to come up at this round.

| Story type | Recruiter | HM | Panel | CPO/Final | Take-home |
|---|---|---|---|---|---|
| 1. Ambiguity / 0-to-1 | · | X | · | X | X |
| 2. Strategic pivot | | X | · | X | · |
| 3. Scope contraction | | X | X | X | X |
| 4. Stakeholder dissent | | X | X | X | |
| 5. Failed launch | | X | · | X | |
| 6. Hiring decision | | · | X | X | |
| 7. Build vs buy | | X | · | X | · |
| 8. Pricing / monetization | | · | · | X | X |
| 9. Activation / retention | | · | X | · | X |
| 10. Ethical edge | | | · | X | |
| 11. Crisis management | | · | · | X | |
| 12. Bet paid off / didn't | | X | · | X | |

## Level differentiation — HoP vs Senior PM probing patterns

These are the story types that **disproportionately** come up when the role is Head of Product (vs Senior PM):

- **6. Hiring decision** — at Senior PM rounds, this is occasional. At HoP rounds, it's near-universal. Hiring is a HoP's primary lever.
- **2. Strategic pivot** — Senior PM probes ask about feature pivots; HoP probes ask about whole-product or whole-team pivots.
- **10. Ethical edge** — Senior PM rounds rarely probe this. HoP rounds want to see judgment on the harder calls.
- **11. Crisis management** — Senior PM rounds occasionally; HoP rounds heavily, especially anything where you carried the team through.
- **12. Bet that paid off / didn't** — for Senior PM, often about feature bets. For HoP, often about strategic bets affecting the whole org.

Story types that come up roughly equally at both levels:
- 1 (ambiguity), 3 (scope contraction), 4 (stakeholder dissent), 5 (failed launch), 7 (build-vs-buy), 8 (pricing), 9 (activation/retention)

## How agents use this reference

- `story-builder --gap-check`: scan userdata/stories/*.md for story_type frontmatter; compare against the 12 types; surface missing types ranked by relevance to profile.md target_titles (HoP-targets weight the level-differentiation list above more heavily)
- `interview-prep`: when selecting 3-5 stories for a round, use the coverage matrix as a tiebreaker — prefer stories whose story_type maps to the round's "heavily probed" column
- Future: career-coach could surface "your bank has 4 ambiguity stories and 0 hiring stories — that's a HoP-readiness gap" as part of self-audit conversations
