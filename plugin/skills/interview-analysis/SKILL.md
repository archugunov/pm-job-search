---
name: interview-analysis
description: This skill should be used when the user asks to "/interview-analysis", "analyze my interview", "debrief my interview", "what did I miss in the interview", "review my interview transcript", or pastes a transcript / notes from a just-finished interview. Reads the transcript (pasted or from --from-file), pulls context from userdata/companies/<Co>/{meta,research-brief,interview-prep-*}.md and userdata/profile.md, and writes userdata/companies/<Co>/interview-debrief-<YYYY-MM-DD>-<stage>.md with: what landed, what didn't, interviewer signals, deltas vs the prep doc, and recommended updates (story angles, profile.md What-NOT items, monitoring flag).

---

# /interview-analysis — post-interview debrief from a transcript

Single-pass analysis. Take a transcript (or notes), produce a debrief that's useful for: (a) the next round at the same company, (b) updates to the user's universal artefacts (stories, anti-patterns), (c) status decisions on `meta.md`.

## Inputs

- Transcript source — one of:
  - Pasted into chat after invocation.
  - `--from-file <path>` — read from the given path (can be inside or outside the workspace).
  - If neither: prompt `Paste the transcript, or give me a file path.`
  - If the user has only notes (not a verbatim transcript), accept them — flag in the debrief that analysis is from notes, not transcript.
- `<Company>` — required. Take as positional arg (`/interview-analysis Plaid`), infer from `--from-file` parent folder if path is inside `userdata/companies/<Co>/`, or ask if neither.
- `<stage>` — required for the filename and for shaping. Pass via `--stage` or ask: `Which round was this — recruiter / hiring-manager / panel / cpo-round / final-loop / take-home / other?` Free-text accepted; will be slugged.
- `userdata/companies/<Co>/meta.md` and `research-brief.md` — for company context.
- The most recent `userdata/companies/<Co>/interview-prep-*.md` if it exists — for the "vs the prep" delta analysis. Match on `--stage` if multiple; otherwise pick the most recent same-stage prep, or the most recent prep regardless.
- `userdata/profile.md` — `## Positioning`, `## Tone of Voice`, `## What NOT to Frame As`.
- All `userdata/stories/*.md` — to spot which stories were used (match by title hints in the transcript) and judge whether the angles landed.

## Parse the transcript

Extract these structured pieces. If something can't be identified, mark `unknown` rather than guessing.

1. **Interviewer(s)** — names and roles if stated; otherwise generic ("CPO", "hiring manager").
2. **Questions asked** — list, with the user's answer-summary alongside.
3. **Stories the user told** — match each user-told story against the universal bank's titles + themes. Surface mismatches: "user told a story not in the bank — candidate for new entry."
4. **Direct signals from the interviewer** — verbatim quotes that indicate enthusiasm, hesitation, scope-concerns, or culture cues.
5. **Topics the interviewer kept returning to** — these are the real evaluation axes for this round.
6. **Items the interviewer mentioned about next steps** — process, timeline, who's next, when to expect a decision.
7. **Compensation signals** — if comp was discussed, capture the band as stated.

## Debrief structure

Write `userdata/companies/<Co>/interview-debrief-<YYYY-MM-DD>-<stage-slug>.md`:

```markdown
# Interview debrief — <Company> / <Position>
**Date:** <date>  **Stage:** <stage>  **Source:** transcript | notes  **Tier (pre):** <P0|P1|P2>

## What landed
- <Specific bullets, each anchored to a quote or moment from the transcript.>
- (e.g. "The pricing-experiment story drew an explicit 'this is exactly the
  shape we need' from the CPO at 24:15 — clear signal it lands here.")

## What didn't land
- <Bullets, also anchored. Be specific — vague self-criticism isn't useful.>
- (e.g. "When asked about activation, the answer drifted into pricing again
  rather than the activation funnel story — visible interviewer cool-off.")

## Interviewer signals
- **Enthusiasm:** <list quoted signals.>
- **Concerns / hesitations:** <list, with interpretation in parentheses.>
- **Scope cues:** <what the interviewer kept asking about — that's their
  actual decision criterion.>
- **Culture cues:** <e.g. how they described the team, what they praised
  in past hires.>

## Vs the prep doc
<If a same-day or recent prep doc exists, compare:>
- **Stories planned vs told:** which prep-doc stories made it in, which
  didn't, and any stories told that weren't in the prep.
- **Questions asked vs prepped:** how many of the planned "Questions to
  ask THEM" were actually used.
- **Anchors deployed:** which prep-doc anchors (why-us, salary, etc.)
  came through and which got buried.
<If no prep doc: omit this section entirely.>

## Process / next steps
- <Bullets capturing what the interviewer said about timeline, next
  rounds, decision process, who's involved.>

## Recommended updates
- **Stories to add or sharpen** — list. If a told story isn't in the bank,
  recommend `/story-builder --new "<title>"`. If a told story landed weakly,
  recommend a new angle.
- **Profile updates** — if the interview surfaced a misfit (e.g.
  "interviewer pushed on people-management depth and you don't have it"),
  recommend a `## What NOT to Frame As` addition.
- **Meta updates** — recommend status / monitoring changes. E.g. "Move
  status to interviewing-paused if they signalled a 2-week pause," or
  "Flip monitoring: true if you exit at any reason short of mutual no."
- **Next-round prep** — if this isn't the final round, list 3-5 prep items
  the user should focus on for the next round (lifted from interviewer
  signals + concerns).
```

If a section's evidence list is empty, render the section with `<None — see notes.>` rather than omitting (the structure helps with cross-debrief comparison).

## Tone of voice for the debrief

Use the user's `## Tone of Voice` from profile.md. Default if unset: direct, short sentences, no euphemism. The debrief is for the user's own use — softening hurts more than helps.

## Status hints (do NOT mutate meta.md)

The debrief surfaces recommendations under "Meta updates" but never edits `meta.md` itself. The user runs the change (`/today` will surface the suggestion or the user edits directly). Reasoning: status transitions are decisions, not derivations — the user's call.

If the interview signal is unambiguous (e.g. "we don't think this is a fit, thank you for your time"), make the recommendation explicit:
> **Strongly recommend** updating `meta.md`: status: rejected, date_rejected: <date>, rejection_stage: <stage>, rejection_note: "<verbatim or summary from interviewer>".

For ambiguous signals, recommend a wait period: `Hold for 5 business days before flipping to closed; recruiter may circle back.`

## Output to chat

After writing the debrief file, print to chat (compact):

```
Debrief filed: userdata/companies/<Co>/interview-debrief-<date>-<stage>.md
  - <N> stories landed, <M> didn't
  - <K> recommended updates (see "Recommended updates" section)
  - Next step (from interviewer): <one-line summary, or "unclear">
```

If the debrief recommends a meta.md status change, repeat it in the chat output (don't bury it in the file):

```
> Recommended next: update meta.md status to <X>. /today will surface this
  but you make the call.
```

## What /interview-analysis never does

- Never edits `meta.md` directly. Recommendations only.
- Never edits the universal story bank (no story body changes, no angle additions). It recommends; `/story-builder` executes.
- Never edits the prep doc the interview used. The prep was a forecast; the debrief is what happened.
- Never invents transcript content. If a section can't be evidenced from the input, the bullet is `<None evidenced — needs user fill-in.>`.
- Never deletes prior debriefs at the same company / stage. If the same stage gets a re-interview (rare), the new debrief has the suffix `-v2` (or `-v3`, etc.).

## Smoke test against the Maya example

There's no transcript in Maya's example install — this skill is exercised by the user pasting real content. A synthetic test would mock a transcript for Plaid's CPO round and verify the output structure. Defer until a real interview happens.
