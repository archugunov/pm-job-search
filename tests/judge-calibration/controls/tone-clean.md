# Transcript — maya-cold-start (NEGATIVE CONTROL, hand-repaired)

**Date:** 2026-08-22
**Snapshot:** empty
**Max turns:** 30

> **SYNTHETIC — not a real harness run.** Hand-edited from
> `runs/2026-08-07/maya-cold-start.md` with every known tone problem removed:
> the missing skip affordance at turn 1, the redundant "Ready?" gate, the
> grudging "you just type more", "best email", the unexplained LinkedIn ask,
> the `--refresh` command surfaced to the user, and the ladder of role titles
> that didn't match the candidate. Everything else is unchanged.
>
> Purpose: a negative control. Every transcript in `runs/` is a run with real
> defects, so a judge that failed everything would score perfectly. This one is
> supposed to PASS on tone. If a tone judge fails it, the rubric is too strict —
> that is the whole point of keeping it.
>
> Conformance and groundedness are NOT controlled for here; only tone.

---

## Turn 1 — USER

/pm-job-search:setup

## Turn 1 — ASSISTANT

I've created `userdata/` for you. If you have a CV, drop it in there as cv.md, cv.txt or cv.pdf and say "ready" — it saves you most of the typing. Or say "skip" and we'll go through it together.

## Turn 2 — USER

I don't have a CV handy — go ahead without it.

## Turn 2 — ASSISTANT

What's your name?

## Turn 3 — USER

Maya Patel.

## Turn 3 — ASSISTANT

Where are you based? City + country works (e.g. London, UK).

## Turn 4 — USER

London, UK.

## Turn 4 — ASSISTANT

What's your email?

## Turn 5 — USER

maya.patel@example.com

## Turn 5 — ASSISTANT

I've set your timezone to Europe/London from that. Say the word if it's wrong.

What roles are you targeting? List as many as you'd take, comma-separated.

## Turn 6 — USER

Head of Product, Lead PM, Senior PM.

## Turn 6 — ASSISTANT

What industries are you looking at? E.g. fintech, healthcare, climate tech, enterprise SaaS. Comma-separated.

## Turn 7 — USER

Fintech, consumer credit. Maybe adjacent B2C fintech generally.

## Turn 7 — ASSISTANT

Where are you looking?

- On-site in London
- Remote
- Both
- Other (free text)

## Turn 8 — USER

Both.

## Turn 8 — ASSISTANT

What salary band are you aiming for? Whatever shape works — "£90-110K", or "$190-230K base + equity". Skip if you'd rather not anchor a number yet.

## Turn 9 — USER

£90-110K for an IC role, £115-140K if it's proper leadership scope.

## Turn 9 — ASSISTANT

Last one, and it's the one that pays off most later: positioning — who you are and what you're best at.

- A. Write it now — paste 1-3 sentences about yourself and I'll draft it with you
- B. Skip — I'll ask again once you've seen a few roles

## Turn 10 — USER

B — skip for now.

## Turn 10 — ASSISTANT

Skipped. You're set up.

Wrote your profile and your target date to `userdata/`. Next: run `/pm-job-search:job-search` and I'll find roles that match what you just told me.

## Turn 11 — USER

Great, thanks.
