# Senior PM job-search anti-patterns

Reference doc for `career-coach`, `today`, and `evaluate-offer`. Each pattern has a **trigger signal** (what to detect), **what's actually happening** (the underlying problem), and **what to do instead** (the corrective). Agents cite the pattern BY NAME when surfacing it — vague brutality ("you're stuck") is worse than gentle suggestion; SPECIFIC brutality ("you're in spray-and-pray mode — 47 applications, 4% response rate, no warm channel") is what works.

User overrides: drop `userdata/references/career-anti-patterns.md` to add your own patterns.

---

## 1. Spray-and-pray

**Trigger signal:** Application count over the last 30 days exceeds 30 AND response rate is under 15% AND warm-outreach count is under 5.

**What's actually happening:** The candidate has switched from targeted search to volume search. Usually a stress response to a thin pipeline. The math doesn't work — cold senior-PM apps convert at 2-5%; you can't compensate with volume because every dud application is also 60 minutes of customisation you can't recover.

**What to do instead:** Recalibrate target list to 20-30 P0/P1 companies. Build a warm channel for each (ex-colleague, recruiter, founder touchpoint). Stop new cold apps for 2 weeks while the warm channel matures.

---

## 2. Title chasing

**Trigger signal:** Candidate is targeting "Head of Product" titles at companies under 30 ppl, OR is interviewing for HoP-titled roles where the scope-on-paper is Senior PM work.

**What's actually happening:** The title is being optimised for narrative ("I'm a HoP now") rather than work. At seed/early-A companies, "Head of Product" often means "first PM hire managing 0 people" — fine work, wrong title for the next move.

**What to do instead:** 5-year-clock test — "where will this title get me in 5 years if the company doesn't IPO?". If the scope is actually Senior PM, take a Senior PM role at a stronger brand instead. If the scope IS HoP-level (rare at seed), check that the equity makes the trade worthwhile.

---

## 3. Stage mismatch

**Trigger signal:** Candidate is interviewing at Series-A or earlier AND their last role was at a 500+ ppl company. OR vice versa: interviewing at a public company AND last role was 20 ppl.

**What's actually happening:** Founders at seed/A expect builder-archetype hands-on energy and tolerate (require) chaos. People from mature orgs expect process and reports. Mismatch usually surfaces in the HM round and kills the loop, but sometimes the offer comes through and the candidate signs into 18 months of pain.

**What to do instead:** In the HM round, ask: "what does a typical week look like — how much time hands-on with product vs in meetings?" Listen for builder vs operator signals. Run [[senior-pm-archetypes]] against your own pattern; if your archetype doesn't fit the stage, withdraw or de-prioritise.

---

## 4. Vertical drift

**Trigger signal:** Candidate is applying to companies in 3+ unrelated verticals (e.g., fintech + healthcare + dev tools + B2C marketplaces).

**What's actually happening:** Either positioning is muddy or the candidate is in opportunistic mode (taking what comes). Hiring managers smell this — broad vertical exposure reads as no depth in any.

**What to do instead:** Pick 1-2 anchor verticals you can credibly speak to. Make the third only if it shares a structural pattern (e.g., "B2C subscription apps" works across fitness / education / media). Update anti-goals in strategy.md to filter the others.

---

## 5. Resume bloat

**Trigger signal:** CV is 3+ pages OR lists 10+ shipped features OR has more than 4 roles in 8 years.

**What's actually happening:** Either trying to mask gaps with detail, or hasn't decided what their best work was. Senior-PM resumes that work are curated — 3-5 high-signal wins with quantified outcomes, not exhaustive log of features.

**What to do instead:** For each role, pick the 1-3 outcomes that prove the level you want next. Cut everything else. If you can't get to 1 outcome per role that proves the next level, that's the actual problem — your story bank, not the resume.

---

## 6. Interview cramming

**Trigger signal:** Candidate is going into a panel or CPO round without having run a mock round in the previous 7 days.

**What's actually happening:** Either confidence overrides preparation (often a sign the candidate underestimates the round), or they didn't know mock practice was an option. Real-pressure rehearsal is the single highest-leverage prep move for senior PM rounds.

**What to do instead:** Run `pm-job-search:interviewer-simulator` in mock-round mode 48-72 hours before the live round. Use the debrief to identify hand-wave moments. Re-run pressure-test mode on the weakest story.

---

## 7. Withdrawing too early

**Trigger signal:** Candidate has marked status: rejected or status: closed within 24 hours of a single bad signal in an active loop.

**What's actually happening:** A single hesitant interviewer or a delayed response is being read as a final no. Sometimes correctly, but often the loop is still alive and the candidate just lost their bet on themselves.

**What to do instead:** Wait 48 hours before flipping status. If the bad signal was clear (interviewer said "we're not moving forward"), that's a real no — flip immediately. If it was ambiguous (slow follow-up, mixed feedback), assume the loop is alive until a process step confirms otherwise.

---

## 8. Stuck-IC syndrome

**Trigger signal:** Candidate has been Senior PM for 4+ years AND is being passed over for HoP roles AND has never explicitly tested whether they want management.

**What's actually happening:** They're stuck between two stories — IC career growth (plateaued) and management (untried). The plateau is unhappy but management is unknown.

**What to do instead:** Either run [[senior-pm-archetypes]] honestly and commit to IC excellence (Staff / Principal PM is a real career — own it), OR take an interim step (coach a peer, lead a project with 1-2 reports, run a hiring loop) to test the management instinct before betting a job on it.

---

## 9. Hollow-HoP risk

**Trigger signal:** Candidate is about to accept a HoP title at a company where: headcount > 150 AND vertical isn't PLG/B2C/mobile/creator/marketplace AND there's no explicit equity/brand signal in the offer.

**What's actually happening:** The role will be primarily stakeholder management, not product work. The shape-mismatch warning in /today fires for this reason. Senior PMs who are wired as builders get hollowed out in these roles within 18 months even when comp + brand are right.

**What to do instead:** Re-run the build-vs-defend verdict from the last interview-analysis. If the role is defending-shape, decline OR pursue only if compensated for the 18-month hollowing risk (sign-on, equity floor, explicit scope agreement). Don't optimise for title alone.

---

## 10. Comp tunnel vision

**Trigger signal:** Candidate's primary frame in offer evaluation is total comp 1-year. They mention base + equity numbers before mentioning manager, ICP, or stage fit.

**What's actually happening:** Comp is the most legible single dimension, so it dominates when other dimensions feel fuzzy. But comp 1-year correlates poorly with 5-year career trajectory; manager quality, ICP fit, and stage are the load-bearing variables.

**What to do instead:** Run /evaluate-offer with all factors explicit. Force-rank: would you take this role at 10% less comp if the manager were great? If yes, the comp framing is misleading. If no, dig into why comp matters so much right now (mortgage, child-care, runway) — those are real constraints, but they should be named explicitly.

---

## 11. Recruiter-first dependency

**Trigger signal:** 80%+ of pipeline came through recruiter inbound. Warm-outreach count < 1 per week. No specialist-recruiter relationships named.

**What's actually happening:** The candidate has handed the search to recruiters. Works in hot markets; collapses in cold ones. Also caps you at whatever roles recruiters are commissioned to fill — usually generic Senior PM, rarely the differentiated HoP role you actually want.

**What to do instead:** Build the warm channel in parallel — 2-3 specialist-recruiter relationships (people who specifically place HoPs), 3-5 ex-colleague touchpoints per month, 1-2 founder earned-touchpoints per month. Inbound recruiters become one channel of three, not the whole funnel.

---

## 12. Pattern-of-rejection (same-stage)

**Trigger signal:** 3+ rejections at the same round type (e.g., 3 take-home reviews, 3 panel rounds).

**What's actually happening:** Something specific to that round is the gap. Same stage across companies = systematic skill or signal issue, not random.

**What to do instead:** Mine the recruiter feedback (yes, ask — many will tell you). Run interviewer-simulator's pressure-test mode on the questions that came up in those rounds. If take-home is the gap, study 1-2 strong examples publicly available and structure your next take-home against them. If panel is the gap, the cross-functional collaboration signal is probably weak — practice with a friendly cross-functional partner before the next loop.

---

## 13. Burnout signal

**Trigger signal:** Candidate has been searching 12+ weeks AND weekly cadence has dropped to under 50% of target for 4+ weeks AND no offers in pipeline.

**What's actually happening:** Either the search shape is wrong (covered by [[reference-anti-patterns]] 14 — sunk-cost), or burnout is degrading execution. Often both — burnout makes you reach for "more apps" (anti-pattern 1) instead of restructuring.

**What to do instead:** Honest read with the coach. If the search shape is wrong, fix that first (anti-pattern 14). If you're genuinely burnt out, a 1-2 week strategic pause beats grinding at 30% effectiveness.

---

## 14. Sunk-cost continuation

**Trigger signal:** Candidate has been searching 12+ weeks AND has < 2 active interview threads AND has not changed target list / positioning / geography in that period.

**What's actually happening:** The strategy isn't working. More effort against the same plan won't fix it. Trigger C in /today fires for this reason.

**What to do instead:** Stop. Restart the strategy conversation with career-coach. Specific questions worth asking: Is the target level right? Is the geography right (remote / city / relocation)? Is the vertical right? Is the positioning landing? At least one of these is wrong; identify which and restructure around it.

---

## 15. Premature "I'll just freelance"

**Trigger signal:** Candidate proposes contracting / fractional / freelance as a search exit BEFORE running an honest stop-and-switch diagnostic.

**What's actually happening:** Usually a face-saving move at the 12-week mark when the search isn't working. Sometimes a real strategic call (contracting can be the right move for a builder during a between-fund-raises lull). The diagnosis matters.

**What to do instead:** Run the full sunk-cost diagnostic first (anti-pattern 14). If the search itself is broken and contracting buys runway while you fix it, it's a legitimate move. If contracting is a way to avoid the diagnostic, you'll be in the same situation in 6 months with less leverage.

---

## How agents use this reference

- `career-coach`: when diagnosing a user complaint, scan triggers above against pipeline data; cite matched patterns BY NAME with specific data. Never invoke a pattern without evidence.
- `today`: existing Trigger A/B/C continue to fire on the same conditions; anti-pattern names give them sharper language ("Spray-and-pray pattern — 47 apps, 4% response, 0 warm").
- `evaluate-offer`: scan for relevant patterns at offer-stage (especially #2 title-chasing, #3 stage-mismatch, #9 hollow-HoP, #10 comp-tunnel-vision); surface in the verdict.
