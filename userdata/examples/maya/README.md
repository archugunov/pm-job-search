# Maya — example install

Synthetic reference install for pm-job-search. Demonstrates a lived-in state at 2026-05-18: London-based Senior PM / HoP candidate in UK fintech with 1 offer in hand (Lendable), 2 active interviews (Plaid CC, Cleo), 1 stale applied (iwoca), 1 closed pre-app (Atom Bank). Weekly reflection happened last week (2026-05-11).

## What's reachable when you emulate `/today` against this install

- Late-stage interview prompts — fires for Plaid (Consumer Credit role; `interviewing`, `last_inbound` 5d ago — within 7d window).
- Stale applied bullet — fires for iwoca (`applied`, `date_applied` 2026-04-22 = 26d ago, >14d threshold).
- Shape-mismatch warning — fires for Cleo (`interviewing` at 180 ppl, over Maya's preferred 150-ppl ceiling, no equity signal).
- Closed-summary line — counts 2 decided this search; 1 rejected (Stripe), 1 withdrew (Atom Bank).
- Pipeline table dual-glob — both flat and role-slug-subfolder companies appear. Plaid (multi-role: Consumer Credit + Growth Loops) tests the dual-glob discovery.
- Calendar-event reference — Lendable's `next_event: "Reference call Wed 2026-05-20 11:00"` is 2 days out from today; would surface in Heads-up if calendar were wired (it isn't in this install — see "What's NOT wired" below).
- Weekly reflection trigger — fires (marker `outputs/.last-weekly-reflection` is in ISO week 20; today is ISO week 21).
- First-run automation nudge — suppressed (marker `outputs/.automation-nudge-shown` exists; delete it to see the nudge).

## Coach triggers this install is designed to reach

- Trigger C condition 3 (cadence-drift escalation) — reachable by emulating /today 4 weeks forward from 2026-05-18 (weekly target gaps would compound).

Trigger A (cadence drift 3 weeks), Trigger B (closed-without-applying + empty anti-goals), and Trigger C conditions 1 and 2 are NOT cleanly reachable from this install as shipped:
- Trigger A — fires from this install as shipped: three consecutive application weeks under 50% target (0/3, 0/3, 1/3 for the windows ending 2026-05-18). No forward emulation needed.
- Trigger C condition 3 — would require simulated longer time history (Trigger A firing in 4+ consecutive /today runs, which would require persistent state or 4 weeks of continued cadence drift).
- Trigger B — Maya has 5 populated anti-goals in `strategy.md` (the populated state is part of her persona). To exercise Trigger B locally, comment out the anti-goal bullets in `strategy.md` and re-run /today.
- Trigger C condition 1 (long search, thin pipeline) — Maya has 2 active interviews and 1 offer; condition requires <2 interviews + 0 offers. Diego's install demonstrates this.
- Trigger C condition 2 (pattern-of-rejection same stage) — Maya has only 1 rejection (Stripe at take-home); condition requires 3. Diego's install demonstrates this.

## What's NOT wired

This install has no `userdata/integrations.md`. Calendar / Gmail / Granola code paths in /today are skipped silently. Journal entries demonstrate the post-integration bullet format anyway (`(source: calendar, confirmed)`, etc.) for fixture completeness — but those entries were authored as if from an integration, not actually written by a wired integration in this install.

## Files

Standard install layout:
- `profile.md` — persona definition. London hybrid, UK fintech, messy-middle consumer credit positioning.
- `strategy.md` — target_offer_date 2026-08-01, weekly_targets (5 outreach, 3 applications), 5 populated anti-goals.
- `journal.md` — 4 weeks of dated entries + 2 weekly reflection blocks.
- `companies/` — 7 company folders, 8 status slots (Plaid is multi-role).
- `stories/` — 5 STAR stories spanning growth/pricing, strategy-pivot, 0-to-1, cross-functional-dissent, failed-launch.
- `outputs/applications.md` — GENERATED block + free-text Notes area.
- `outputs/.last-weekly-reflection` + `.automation-nudge-shown` — marker files (see above).
