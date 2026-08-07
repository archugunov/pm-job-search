# Transcript — maya-cold-start

**Date:** 2026-07-11
**Snapshot:** empty
**Max turns:** 30

---

## Turn 1 — USER

/pm-job-search:setup

## Turn 1 — ASSISTANT

OK, let's get you set up. Twelve quick questions — none of it locked in, you can rerun anytime. Ready?

## Turn 2 — USER

Yes, ready. Go.

## Turn 2 — ASSISTANT

What's your name?

## Turn 3 — USER

Maya Patel

## Turn 3 — ASSISTANT

Where are you based? City + country works (e.g. London, UK).

## Turn 4 — USER

London, UK

## Turn 4 — ASSISTANT

I'm seeing your timezone as `<host-timezone>` — that right? Override if not.

## Turn 5 — USER

Europe/London.

## Turn 5 — ASSISTANT

What's the best email for you?

## Turn 6 — USER

maya.patel@example.com

## Turn 6 — ASSISTANT

LinkedIn URL? Or skip.

## Turn 7 — USER

No LinkedIn, skip it.

## Turn 7 — ASSISTANT

Where are you looking? Pick one:

- On-site in London
- Remote
- Both
- Other (tell me where)

## Turn 8 — USER

Both.

## Turn 8 — ASSISTANT

Positioning next — who you are and what you're best at. Three ways to handle this:

- A. Drop your CV (recommended)
- B. Write it now
- C. Skip for now

Which works for you?

## Turn 9 — USER

A

## Turn 9 — ASSISTANT

I've created `userdata/` for you — drop your CV there as `cv.md`, `cv.txt`, or `cv.pdf`. Say 'ready' when it's in.

## Turn 10 — USER

ready — CV's in userdata/ as cv.pdf

## Turn 10 — ASSISTANT

Quick note: your CV came through as cv.md, not cv.pdf, but it's here and I read it. Here's a first draft of your positioning based only on what's in it.

Positioning

Senior PM with nine years in consumer credit and growth-stage B2C SaaS. I own growth-pricing surfaces end-to-end — experimentation roadmap, guardrail metrics, and delivery across eng and risk. Most of my work sits where pricing meets credit risk: moving revenue without breaking the guardrails that keep a lending book healthy. Not a generalist growth PM — a pricing-and-credit PM who can carry the risk conversation.

Proof points

**Pricing experiments:** Led a pricing-experiment programme at a Series B BNPL fintech (~£60M ARR) that lifted MRR +18% over Q3 with no measurable churn impact. (Senior PM, Growth Pricing.)

**Underwriting 0→1:** Ran a 0→1 underwriting integration with a new credit bureau, cutting decline rate 12% on thin-file applicants without raising defaults. (Senior PM.)

**Guardrail ownership:** Own the growth pricing surface end-to-end — experimentation roadmap and guardrail metrics — not just shipping tests but holding the risk line while doing it. (Senior PM.)

**Cross-functional delivery:** Drove pricing work across engineering and risk functions, keeping revenue and credit-risk stakeholders aligned on the same roadmap. (Senior PM.)

**Depth of range:** Nine years across consumer lending and subscription-growth products, spanning both regulated credit and B2C SaaS. (2015–present.)

Moat candidate

I move revenue on a lending product without breaking the credit guardrails — the pricing-and-risk overlap most growth PMs hand off.

Want to accept this as-is, edit any part, or discard and start over? Edit anything that doesn't sound like you — drafts are starting points, not finished copy.

## Turn 11 — USER

Yeah, that's right. Approve it.

## Turn 11 — ASSISTANT

Got it, positioning approved.

What roles are you targeting? Typical senior-PM examples: Director of Product, Principal PM, Group PM, Staff PM. List as many as you'd take, comma-separated.

## Turn 12 — USER

Head of Product, Lead PM, Senior PM — and I'd also look at Group PM or Principal PM if the scope and comp are right.

## Turn 12 — ASSISTANT

What industries are you looking at? E.g. healthcare, climate tech, education, enterprise SaaS. Comma-separated.

## Turn 13 — USER

Fintech and consumer credit.

## Turn 13 — ASSISTANT

What salary band are you aiming for? Whatever shape works — '£90-110K' or '$190-230K base + equity', or skip if you'd rather not anchor a number yet.

## Turn 14 — USER

£90-110K for an individual contributor role, or £115-140K if it's got leadership scope.

## Turn 14 — ASSISTANT

Any red flags? Roles you'd skip immediately regardless of other fit. E.g. "no companies under 50 people", "no GM or business-owner roles", "no five-day in-office", "no relocation". List a few, or skip.

## Turn 15 — USER

I skip anything that needs relocation outside EMEA, sales-led enterprise B2B with no self-serve or PLG signal, and roles with more than ~8 direct reports where it's really a GM or business-owner seat rather than product leadership.

## Turn 15 — ASSISTANT

Any companies you have in mind already? List a few, or skip.

## Turn 16 — USER

Plaid, Klarna, Lendable, and Mercury are the main ones on my radar right now.

## Turn 16 — ASSISTANT

Got it — Plaid, Klarna, Lendable, and Mercury on the radar.

When do you want the offer signed by? Concrete date — even a best guess. Vague dates make `/today`'s countdown noisy.

## Turn 17 — USER

Let's say end of September — 30 September 2026.

## Turn 17 — ASSISTANT

The existing CLAUDE.md already begins with the real header (not the template comment), so I left it untouched per the guardrail.

Setup complete. Here's what I wrote:

- `userdata/profile.md` — identity, target titles, industries, £90-110K IC / £115-140K leadership band, hard filters, and your approved Positioning / Proof Points / Moat.
- `userdata/strategy.md` — target offer date 2026-09-30 plus your derived cadence.
- `userdata/journal.md` — empty log, ready for daily notes.
- `userdata/companies/`, `stories/`, `outputs/` — `.gitkeep` placeholders in place.
- `CLAUDE.md` — left as-is (already populated from a prior run).

Your cadence, based on the ~11-week timeline to 30 Sep: 8 applications/week, 8 warm outreaches/week, with a floor of 4 active interview threads and 6 P0 roles in the pipeline.

Want to sharpen your positioning before we wrap? I can pull in the `pm-job-search:career-coach` agent — quick 5-min back-and-forth, it'll suggest a tighter version. Or skip and edit `profile.md` whenever.

## Turn 18 — USER

Skip it, thanks.

## Turn 18 — ASSISTANT

Want `/pm-job-search:today` to run automatically every day? (y / n)

- Yes
- No, I'll run it manually

## Turn 19 — USER

No, I'll run it manually.

## Turn 19 — ASSISTANT

Setup done. Run `/pm-job-search:job-search` to seed your applications list — or `/pm-job-search:today` right now if you'd rather see a daily brief first.

## Turn 20 — USER

/pm-job-search:job-search

## Turn 20 — ASSISTANT

Filed 8 new roles this week, all set to status new. 3 tier-1 (Finom Lead PM, SME Lending; Finom Head of Product, Cards; Lendable Senior PM, UK Cards), 4 tier-2 (Lendable Senior PM; Klarna Senior PM, Consumer Products; YouLend Senior PM; Creditstar Senior PM), plus 1 tier-3 watch role at Plaid. Everything came from live listings on public job boards, seeded by your companies of interest plus your target titles and the fintech/consumer-credit focus. Nothing was skipped as a repeat — this is your first sweep, so the pipeline started empty.

The strongest fits cluster around the pricing-meets-credit-risk surface you position around: Finom's two leadership-band credit roles and Lendable's UK Cards role all put you directly on a consumer-lending P&L in London or EMEA-remote. A few carry an open question worth checking before you invest in a tailored application:

- Lendable — Senior Product Manager - UK Cards — new — https://jobs.ashbyhq.com/lendable/636b90ec-028d-461a-b358-c7b871918dd8
- Finom — Lead Product Manager - SME Lending — new — https://jobs.eu.lever.co/pnlfin/2e8625e8-cccd-4dac-8816-0cdb6fbfab69
- Finom — Head of Product (Cards) — new — https://jobs.eu.lever.co/pnlfin/c90ab505-2c97-4a81-9405-4cd43a574ffd
- Lendable — Senior Product Manager — new — https://jobs.ashbyhq.com/lendable/ae6109be-8b05-411f-8649-fa7e4dc0c933
- Klarna — Senior Product Manager - Consumer Products — new — https://jobs.lever.co/klarna/83937bc7-8042-4177-bd4c-61d756224f65
- YouLend — Senior Product Manager — new — https://apply.workable.com/youlend-1/j/B025072D98
- Creditstar — Senior Product Manager — new — https://apply.workable.com/creditstar/j/DB9B914F61
- Plaid — Senior Product Manager — new — https://jobs.lever.co/plaid/6ce66588-0d49-42be-bcdd-724425d02b8b

A couple of watch-outs I noted in the research briefs: the Finom Head of Product role could brush your GM-scope filter if it carries a large team, so confirm reporting lines first; Klarna, Creditstar and the Plaid role all hinge on whether they support a London or EMEA-remote base; and YouLend is embedded B2B finance, so check there's a real product surface rather than a bespoke-integrations role. Plaid reads US-based, hence the lower tier — worth flagging for monitoring so an EMEA-based req surfaces automatically next time.

Open the dashboard to triage these into to-apply or not-interested, or just tell me here which ones to move.

## Turn 21 — USER

mark Lendable to apply — the UK Cards Senior PM

## Turn 21 — ASSISTANT

Done. Lendable's Senior Product Manager - UK Cards role is now marked to apply.

Tip: you can also click the company row in the dashboard and add this note directly — same data underneath.

## Turn 22 — USER

/pm-job-search:dashboard

## Turn 22 — ASSISTANT

Opening your job-search dashboard at http://localhost:7890 — you'll see every role you're tracking in one view. Change a status, add a note, or archive a role inline. To add a new role, drop the link to me here and I'll score and file it.

Heads up: I can't hold the server open from here, so run `python3 ${CLAUDE_PLUGIN_ROOT}/dashboard/serve.py --userdata "$(pwd)/userdata"` in your own terminal to keep it running.

## Turn 23 — USER

/pm-job-search:today

## Turn 23 — ASSISTANT

# Daily brief — 2026-07-11

## Top 3 actions today
- Lendable (UK Cards) — your one decided-to-pursue role. Tailor your CV with `/apply Lendable` and get it out.
- Applications this week: 0 of 8. Nothing has gone out yet — the Lendable submission is the first one to bank.
- Triage the 7 fresh roles below. Finom is showing two P0 openings (Head of Product, Cards and Lead PM, SME Lending) — worth an early look.

## Heads-up
Nothing flagged today.

## Pipeline state

| Status | Company | Tier | Position | Last activity |
|---|---|---|---|---|
| to apply | Lendable | P0 | Senior Product Manager - UK Cards | today |
| new | Finom | P0 | Head of Product (Cards) | today |
| new | Finom | P0 | Lead Product Manager - SME Lending | today |
| new | Lendable | P1 | Senior Product Manager | today |
| new | Klarna | P1 | Senior Product Manager - Consumer Products | today |
| new | YouLend | P1 | Senior Product Manager | today |
| new | Creditstar | P1 | Senior Product Manager | today |
| new | Plaid | P2 | Senior Product Manager | today |

---

Your whole pipeline landed today from one discovery sweep, so the next move is a decision, not a wait: start with `/apply Lendable` for the UK Cards role you've already committed to, then run through the two Finom P0s to decide if they're worth pursuing.

## Turn 24 — USER

thanks

## Loop ended: termination reached (brief printed with `## Heads-up` / `Nothing flagged today.`; simulator acknowledged)
