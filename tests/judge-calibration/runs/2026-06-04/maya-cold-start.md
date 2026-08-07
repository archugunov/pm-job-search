# Transcript — maya-cold-start (verification run, reusing 2026-05-27 turns)

**Date:** 2026-06-04
**Snapshot:** empty
**Max turns:** 30 (transcript truncated at turn 10 — sufficient for verifying judge mechanism)
**Note:** Same 10-turn body as the 2026-05-27 smoke test, used here to verify the new verdict + memory.md inclusion + confirmation re-run behavior.

---

## Turn 1 — USER

/pm-job-search:setup

## Turn 1 — ASSISTANT

OK, let's get you set up. Twelve quick questions — none of it locked in, you can rerun anytime. Ready?

## Turn 2 — USER

Yep, go.

## Turn 2 — ASSISTANT

What's your name?

## Turn 3 — USER

Maya Patel.

## Turn 3 — ASSISTANT

Where are you based? City + country works (e.g. London, UK).

## Turn 4 — USER

London, UK.

## Turn 4 — ASSISTANT

I'm seeing your timezone as `Europe/London` — that right? Override if not.

## Turn 5 — USER

Yep, London's right.

## Turn 5 — ASSISTANT

What's the best email for you?

## Turn 6 — USER

maya@example.com

## Turn 6 — ASSISTANT

LinkedIn URL? Or skip.

## Turn 7 — USER

skip

## Turn 7 — ASSISTANT

Where are you looking?

1. On-site in London
2. Remote
3. Both
4. Other (free text)

## Turn 8 — USER

3

## Turn 8 — ASSISTANT

Positioning next — who you are and what you're best at. Three ways to handle this:

- A. Drop your CV (recommended)
- B. Write it now
- C. Skip for now

## Turn 9 — USER

C

## Turn 9 — ASSISTANT

Fill in later — `/pm-job-search:setup --refresh` picks up where you leave it.

Q7: What roles are you targeting? Typical senior-PM examples: Director of Product, Principal PM, Group PM, Staff PM. List as many as you'd take, comma-separated.

## Turn 10 — USER

Head of Product, Lead PM, Senior PM

## Loop terminated

Transcript stopped at turn 10 to verify the judge mechanism; full /setup wrap, /job-search, /dashboard, /today were NOT exercised.
