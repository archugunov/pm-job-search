# Diego — example install

Synthetic reference install for pm-job-search. Demonstrates a lived-in state at 2026-05-18: Mexico City-based, fully-remote, B2B SaaS / dev tools / PLG HoP / Group PM candidate (US-overlap timezone). Currently 1 active interview (Retool — panel Tue 2026-05-19), 1 stale interview (Linear — silent for 14d), 1 stale applied (Supabase — 28d), 2 in-progress applications (Vercel DX + Edge), 4 decided (3 same-stage take-home rejections + 1 closed pre-app). No offer yet — longer arc than Maya's install.

## What's reachable when you emulate `/today` against this install

- Late-stage interview prompts — fires for Retool (`interviewing`, `last_inbound` 3d ago, within 7d).
- Stale applied bullet — fires for Supabase (`applied`, 28d, >14d threshold).
- Closed-summary line — counts 4 decided this search; 3 rejected (Fly.io, Render, Railway), 1 withdrew (Replit). Fly.io is outside the 30-day Decided-table window but counts in the summary.
- Pipeline table dual-glob — both flat and role-slug-subfolder companies appear. Vercel (multi-role: Senior PM Edge + Group PM DX) tests the dual-glob discovery.
- Calendar-event reference — Retool's `next_event: "Panel round Tue 2026-05-19 16:00"` is 1 day out from today; would surface in Heads-up if calendar were wired (it isn't in this install).
- Weekly reflection trigger — fires (marker `outputs/.last-weekly-reflection` is ISO week 20; today is ISO week 21).
- First-run automation nudge — suppressed (marker `outputs/.automation-nudge-shown` exists; delete to see the nudge).
- Monitoring recheck — Fly.io carries `monitoring: true`. /job-search recheck would scan Fly.io for new postings.

## Coach triggers this install is designed to reach

- Trigger C condition 2 (pattern-of-rejection same stage) — reachable. Three rejections at the take-home stage: Fly.io 2026-04-08, Render 2026-04-18, Railway 2026-04-29. Surface to coach with "I keep getting rejected at the same stage" or via diagnose-first triage.
- Trigger C condition 1 (long search, thin pipeline) — partially reachable by emulating /today 4+ weeks forward. Diego has only 1 active fresh interview thread (Retool) and 0 offers; 9+ weeks since /setup, condition fires.
- Trigger A (cadence-drift 3 weeks) — reachable if journal applications counts under 50% targets for 3 weeks running; check by emulating /today against the journal's middle weeks.

Trigger B (closed-without-applying + empty anti-goals) is NOT reachable as shipped — Diego has 4 populated anti-goals in `strategy.md`. To exercise Trigger B locally, comment out the anti-goal bullets and re-run /today.

## What's NOT wired

This install has no `userdata/integrations.md`. Calendar / Gmail / Granola code paths in /today are skipped silently. Journal entries demonstrate the post-integration bullet format anyway (`(source: granola, confirmed)`, etc.) for fixture completeness.

## Files

Standard install layout:
- `profile.md` — persona definition. Fully remote, Mexico City + US-overlap, B2B SaaS / dev tools, PLG focus, $190-230K USD band.
- `strategy.md` — target_offer_date, weekly_targets, 4 populated anti-goals.
- `journal.md` — 4 weeks of dated entries (2026-03-18 → 2026-05-16) + 2 weekly reflection blocks.
- `companies/` — 7 company folders, 8 status slots (Vercel is multi-role).
- `stories/` — 5 STAR stories spanning pricing/growth, 0-to-1, stakeholder-dissent, failed-launch, bet-that-paid-off.
- `outputs/applications.md` — GENERATED block + free-text Notes area.
- `outputs/.last-weekly-reflection` + `.automation-nudge-shown` — marker files (see above).
