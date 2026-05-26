# Diego — example install

Synthetic reference install for pm-job-search. Demonstrates a lived-in state at 2026-05-18: Mexico City-based, fully-remote, B2B SaaS / dev tools / PLG HoP / Group PM candidate (US-overlap timezone). Currently 2 interviewing (Retool fresh, Linear stale 14d), 2 applied (Supabase stale 28d, Vercel Group PM DX), 1 to-apply (Vercel Senior PM Edge), and 4 decided (3 same-stage take-home rejections + 1 closed pre-app). No offer yet — longer arc than Maya's install.

## What's reachable when you emulate `/today` against this install

- Late-stage interview prompts — fires for Retool (`interviewing`, `last_inbound` 3d ago, within 7d).
- Stale applied bullet — fires for Supabase (`applied`, 28d, >14d threshold).
- Closed-summary line — counts 4 decided this search; 3 rejected (Fly.io, Render, Railway), 1 not-interested (Replit). Fly.io is outside the 30-day Decided-table window but counts in the summary.
- Pipeline table dual-glob — both flat and role-slug-subfolder companies appear. Vercel (multi-role: Senior PM Edge Platform + Group PM Developer Experience) tests the dual-glob discovery; the other 7 are flat.
- Calendar-event reference — Retool's `next_event: "Panel round Tue 2026-05-19 16:00"` is 1 day out from today; would surface in Heads-up if calendar were wired (it isn't in this install).
- Weekly reflection trigger — fires (marker `outputs/.last-weekly-reflection` is ISO week 20; today is ISO week 21).
- First-run automation nudge — suppressed (marker `outputs/.automation-nudge-shown` exists; delete to see the nudge).
- Monitoring recheck — Fly.io carries `monitoring: true`. /job-search recheck would scan Fly.io for new postings.

## Coach triggers this install reaches

- **Trigger A** (cadence drift, >50% application miss for 3 weeks running) — **fires as shipped.** Application windows ending 2026-05-18: 1/3 (miss), 0/3 (miss), 0/3 (miss). All three under 50% of target.
- **Trigger C condition 2** (3+ rejections at the same stage) — **fires as shipped.** Three rejections all at `take-home`: Fly.io 2026-04-08, Render 2026-04-18, Railway 2026-04-29. Highest-severity (C suppresses A's bullet when both fire).
- **Trigger C condition 1** (long search + thin pipeline) — does NOT fire as shipped. Spec counts all `status: interviewing` regardless of freshness; Diego has 2 (Retool fresh, Linear stale). Condition needs `<2`. To exercise: flip Linear to `applied` or `not_interested` and re-run.
- **Trigger C condition 3** (cadence-drift escalation: 4 consecutive weekly misses) — reachable by shifting Diego's `date_applied` set so all 4 of the most-recent weeks miss, or by emulating "today" further into the future.
- **Trigger B** (3+ `not_interested` AND empty anti-goals) — does NOT fire as shipped. Diego has only 1 not_interested (Replit) and 4 populated anti-goals. To exercise: add 2+ more not_interested rows AND comment out anti-goals.

## What's NOT wired

This install has no `userdata/integrations.md`. Calendar / Gmail / Granola code paths in /today are skipped silently. Journal entries demonstrate the post-integration bullet format anyway (`(source: granola, confirmed)`, etc.) for fixture completeness.

## Files

Standard install layout:
- `profile.md` — persona definition. Fully remote, Mexico City + US-overlap, B2B SaaS / dev tools, PLG focus, $190-230K USD band.
- `strategy.md` — target_offer_date, weekly_targets, 4 populated anti-goals.
- `journal.md` — 4 weeks of dated entries (2026-03-18 → 2026-05-16) + 2 weekly reflection blocks.
- `companies/` — 8 company folders, 9 status slots (Vercel is multi-role; the other 7 are flat).
- `stories/` — 5 STAR stories spanning pricing/growth, 0-to-1, stakeholder-dissent, failed-launch, bet-that-paid-off.
- `outputs/applications.md` — GENERATED block + free-text Notes area.
- `outputs/.last-weekly-reflection` + `.automation-nudge-shown` — marker files (see above).
