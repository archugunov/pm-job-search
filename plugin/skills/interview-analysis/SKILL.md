---
name: interview-analysis
description: This skill should be used when the user asks to "/interview-analysis", "analyze my interview", "debrief my interview", "what did I miss in the interview", "review my interview transcript", or pastes a transcript / notes from a just-finished interview. Reads the transcript (pasted, from --from-file, or auto-pulled from Granola when userdata/integrations.md shows granola wired), pulls context from userdata/companies/<Co>/{meta,research-brief,interview-prep-*}.md and userdata/profile.md, and writes userdata/companies/<Co>/interview-debrief-<YYYY-MM-DD>-<stage>.md with: what landed, what didn't, interviewer signals, deltas vs the prep doc, and recommended updates (story angles, profile.md What-NOT items, monitoring flag).

---

# /interview-analysis — post-interview debrief from a transcript

Single-pass analysis. Take a transcript (or notes), produce a debrief that's useful for: (a) the next round at the same company, (b) updates to the user's universal artefacts (stories, anti-patterns), (c) status decisions on `meta.md`.

**Voice:** the transcript-source prompt, stage prompt, and the written debrief itself follow `${CLAUDE_PLUGIN_ROOT}/TONE.md`. Apply the low-effort-first principle — accept notes if no transcript is available, infer Company / stage from filename if possible, only ask when the answer can't be derived.

## Inputs

- Transcript source — resolve in this priority order. The FIRST source that produces content wins:
  1. **Pasted content** in the same message as the invocation.
  2. **`--from-file <path>`** — read from the given path (can be inside or outside the workspace).
  3. **Auto-Granola fetch** — if `userdata/integrations.md` shows `granola` status `wired` AND neither of the above produced content, automatically attempt the Granola fetch (see "Granola fetch" below). No flag needed.
  4. **Prompt the user** — `Paste the transcript, or give me a file path.` Only fires when 1-3 all came up empty.
  - If the user has only notes (not a verbatim transcript), accept them — flag in the debrief that analysis is from notes, not transcript.
- `<Company>` — required. Take as positional arg (`/interview-analysis Plaid`), infer from `--from-file` parent folder if path is inside `userdata/companies/<Co>/`, or ask if neither.
- `<stage>` — required for the filename and for shaping. Pass via `--stage` or ask: `Which round was this — recruiter / hiring-manager / panel / cpo-round / final-loop / take-home / other?` Free-text accepted; will be slugged.
- `userdata/integrations.md` if it exists — parse the `## granola` section for wired-status. Skip silently if absent.
- `userdata/companies/<Co>/meta.md` and `research-brief.md` — for company context.
- The most recent `userdata/companies/<Co>/interview-prep-*.md` if it exists — for the "vs the prep" delta analysis. Match on `--stage` if multiple; otherwise pick the most recent same-stage prep, or the most recent prep regardless.
- `userdata/profile.md` — `## Positioning`, `## Tone of Voice`, `## What NOT to Frame As`.
- All `userdata/stories/*.md` — to spot which stories were used (match by title hints in the transcript) and judge whether the angles landed.

## Granola fetch (when granola wired)

When auto-Granola fires (or when the user explicitly says "pull from Granola"):

1. Query Granola for meetings matching `<Company>`. Primary path: call `mcp__granola__list_meetings` (or equivalent under the saved tool prefix) and title-scan the response for case-insensitive substring matches against `<Company>` (plus any common aliases from `userdata/companies/<Co>/meta.md`). If the list returns >10 meetings AND >3 candidate matches survive the title scan, refine via `mcp__granola__query_granola_meetings` to narrow. Reason for list-first: the query tool has been observed returning false negatives even when matching meetings exist; the list endpoint is more reliable as the source of truth.
2. Handle the result count:
   - **One match:** print `Found: <Meeting title> on <Date> — use this transcript?` Wait for y/n. If wrong, ask the user to describe the meeting and re-query.
   - **Multiple matches:** present a numbered list `1. <Title> — <Date> — <Duration>` and ask `Which interview — pick a number, or comma-separate to bundle rounds.` Bundling multiple selections concatenates them in chronological order with `--- next meeting ---` separators between transcripts.
   - **No matches:** print `Couldn't find any Granola meeting matching '<Company>'. Paste the transcript or give me a file path instead.` Fall through to source #4.
3. For the selected meeting(s), call `get_meeting_transcript` with the meeting ID. Extract the transcript text. Pass that downstream as if it had been pasted.
4. If the Granola call returns an auth or quota error: print one line `Granola fetch failed (<error type>). Paste the transcript or give me a file path instead.` and fall through to source #4. Do not retry silently.

Auto-Granola is opportunistic. If the user has explicitly pasted a transcript or passed `--from-file`, that wins — Granola is never queried in those runs.

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

## Role shape verdict
**🟢 building-with-team / 🟡 mixed / 🔴 defending-positions**

<One-line verdict, then 2-4 bullets quoting the transcript signals that
drove it. Read the round for what kind of work the role actually is — the
JD often says "build the product strategy" but the interviewer's stories
reveal whether the last person spent their time shipping or putting out
political fires.>

Signal categories to scan for:
- **🟢 Building** — interviewer describes recent shipping cadence, names
  the engineering / design leads they collaborate with, talks about
  what's NEXT for the surface, asks about your favourite product debates.
- **🟡 Mixed** — interviewer describes the role as "stabilising" or
  "getting the team to a steady state", references at least one named
  internal conflict, asks about cross-functional alignment.
- **🔴 Defending** — interviewer talks about "rebuilding trust", names
  specific stakeholders who "need to be brought along", describes the
  role as primarily senior-stakeholder management, the role exists
  because the last person left under tension.

If signals are insufficient to call (e.g. recruiter screen, < 20 minutes
of substantive content), render: `Insufficient signal — defer verdict to
next round.` Do NOT guess.

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
- Never writes to `userdata/integrations.md`. Granola is read-only from this skill's perspective.
- Never persists the raw Granola response anywhere. The transcript text gets used to produce the debrief; the saved file is the debrief, not the API response. (The transcript stays in Granola — that's its source of truth.)
- Never retries failed Granola calls silently. One attempt, fall through to manual paste on failure.

## Smoke test against the Maya example

There's no transcript and no `integrations.md` in Maya's example install — this skill is exercised by the user pasting real content. A synthetic test would mock a transcript for Plaid's CPO round and verify the output structure. Defer until a real interview happens.

To exercise the auto-Granola code path, run the skill in a workspace where `userdata/integrations.md` has granola wired (run `/pm-job-search:integrations` first), invoke `/interview-analysis <Company>` with NO pasted transcript and no `--from-file`, and verify the Granola query / disambiguation / fetch flow runs before any "paste the transcript" prompt would appear.
