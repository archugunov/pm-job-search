# Maya — example install

Synthetic reference install for pm-job-search. Demonstrates a lived-in state at 2026-05-18: London-based Senior PM / HoP candidate in UK fintech with 1 offer in hand (Lendable), 4 active interviews (Plaid CC, Brex, Mercury, Cleo), 4 applied (Marshmallow, Ramp, Anthropic Lead PM Claude Code, iwoca), 2 to-apply (Plaid Growth Loops, Zopa), and 5 decided (2 rejected, 3 not-interested). Weekly reflection happened last week (2026-05-11).

## What's reachable when you emulate `/today` against this install

- Late-stage interview prompts — fires for Plaid Consumer Credit (`last_inbound` 5d ago) and Brex (`last_inbound` 2d ago); both within the 7d window.
- Stale applied bullet — fires for iwoca (`applied`, `date_applied` 2026-04-22 = 26d ago, >14d threshold).
- Shape-mismatch warning — fires for Cleo (`interviewing` at ~180 ppl, over Maya's preferred 150-ppl ceiling, no equity signal in research-brief).
- Closed-summary line — counts 5 decided this search; 2 rejected (Stripe at take-home, Anthropic Applied PM), 3 not-interested (Atom Bank, Pleo, GoCardless).
- Pipeline table dual-glob — both flat and role-slug-subfolder companies appear. Plaid (Senior PM, Consumer Credit + Senior PM, Growth Loops) and Anthropic (Applied PM, Claude API + Lead PM, Claude Code) exercise the multi-role subfolder layout; the rest are flat.
- Calendar-event reference — Lendable's `next_event: "Reference call Wed 2026-05-20 11:00"` is 2 days out from today; would surface in Heads-up if calendar were wired (it isn't in this install — see "What's NOT wired" below).
- Weekly reflection trigger — fires (marker `outputs/.last-weekly-reflection` is in ISO week 20; today is ISO week 21).
- First-run automation nudge — suppressed (marker `outputs/.automation-nudge-shown` exists; delete it to see the nudge).

## Coach triggers — none fire cleanly as shipped

None of Trigger A, B, or C fires from this install at 2026-05-18 as shipped. Each is reachable with a small fixture tweak — useful when manually testing the coach-handoff code path.

- **Trigger A** (cadence drift, >50% application miss for 3 weeks running). Actual windows ending 2026-05-18: 2/3 (not a miss), 1/3 (miss), 1/3 (miss) — two consecutive misses, not three, so does NOT fire. To exercise: delete or shift the `date_applied` of either Marshmallow (2026-05-13) or Ramp (2026-05-12) so the most-recent window also misses.
- **Trigger B** (3+ `not_interested` AND empty anti-goals). Maya has 3 not_interested (Atom Bank, Pleo, GoCardless) ✓ but 5 populated anti-goals in `strategy.md` — does NOT fire. To exercise: comment out the anti-goal bullets in `strategy.md`.
- **Trigger C condition 1** (long search + thin pipeline). 9 weeks since /setup ✓, but Maya has 4 active interviews + 1 offer; condition requires <2 interviews AND 0 offers — does NOT fire. Diego's install demonstrates this naturally.
- **Trigger C condition 2** (3+ rejections at the same stage). Maya has 2 rejections but only 1 has a `rejection_stage` (Stripe at take-home) — does NOT fire. Diego's install demonstrates this.
- **Trigger C condition 3** (cadence-drift escalation: 4 consecutive weekly misses). Same blocker as Trigger A — does NOT fire. Reachable by shifting more dates AND moving "today" forward; not practical to demo statically.

## What's NOT wired

This install has no `userdata/integrations.md`. Calendar / Gmail / Granola code paths in /today are skipped silently. Journal entries demonstrate the post-integration bullet format anyway (`(source: calendar, confirmed)`, etc.) for fixture completeness — but those entries were authored as if from an integration, not actually written by a wired integration in this install.

## Files

Standard install layout:
- `profile.md` — persona definition. London hybrid, UK fintech, messy-middle consumer credit positioning.
- `strategy.md` — target_offer_date 2026-08-01, weekly_targets (5 outreach, 3 applications), 5 populated anti-goals.
- `journal.md` — 4 weeks of dated entries + 2 weekly reflection blocks.
- `companies/` — 14 company folders, 16 status slots (Plaid and Anthropic are multi-role; the other 12 are flat).
- `stories/` — 6 STAR stories spanning growth/pricing, strategy-pivot, 0-to-1, cross-functional-dissent, failed-launch, activation-funnel.
- `outputs/applications.md` — GENERATED block + free-text Notes area.
- `outputs/.last-weekly-reflection` + `.automation-nudge-shown` — marker files (see above).
