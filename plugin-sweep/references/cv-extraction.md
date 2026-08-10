# CV extraction

Shared by `/setup` and `job-sweep`. Covers finding a CV, reading it, and what may
be taken from it. Drafting rules — tone, banned phrases, proof-point format —
are NOT here; they belong to the skill that drafts.

## Finding the CV

The calling skill states its state directory — `/setup` states `userdata/`,
`job-sweep` states `job-sweep/`. Everything below is relative to it, written here
as `<state directory>`.

Check, in order: `<state directory>cv.md`, `<state directory>cv.txt`,
`<state directory>cv.pdf`. First hit wins.

The check itself is silent. Never narrate it — no "Found X? No", no "checking
for a CV", no restating the branch you took. The user sees only the one line the
branch below prints, and nothing before it.

**Branch A — a `cv.*` file exists but in an unreadable format** (`.docx`,
`.pages`, `.rtf`, or anything else). Before printing, substitute BOTH
placeholders: `<state directory>` becomes the path the calling skill states
below, and `<ext>` becomes the actual extension you found. A line printed with
either placeholder still in it is a bug — it sends the user to convert a file
that isn't there. Then print exactly this one line and continue without the CV:

> `Found <state directory>cv.<ext>. Readable formats are .md, .txt, or .pdf — convert your CV first if you want me to draft from it.`

**Branch B — no `cv.*` file exists at all.** Branch A's line does NOT apply here;
printing it, or any narrated variant of it, when there is no CV file is the most
common failure of this reference. Offer the drop instead. The calling skill states its own state
directory and any scaffold files that go with it (`/setup` states `userdata/`
plus the three `.gitkeep` files; `job-sweep` states `job-sweep/` with no scaffold
files). Create that directory and those scaffold files, if any, FIRST, so the
user has somewhere to put it. Then substitute `<state directory>` with the path
the calling skill stated — again, a printed placeholder is a bug — and say
exactly this, with nothing before it:

> `I've created <state directory> for you — drop your CV there as cv.md, cv.txt, or cv.pdf. Say 'ready' when it's in.`

When the user says ready, re-detect. Still absent → continue without a CV; every
step below simply has no pre-filled value.

## The governing rule

**Never fill a field the CV does not contain.** A CV with no email means the
email question gets asked. It does not mean guessing an address from the name, a
company domain, or anything else. The same holds for city, LinkedIn, titles and
industries.

Inventing a plausible value is worse than asking, because the user confirms
without reading and the wrong value silently propagates into every later skill.

## Tier 1 — facts

Read directly off the page. High confidence, safe to present as a single batch
for one confirmation.

| Field | Where it usually is | If absent |
|---|---|---|
| `name` | header, largest text | ask |
| `city` | header contact block, or most recent role's location | ask |
| `email` | header contact block | ask |
| `linkedin_url` | header contact block | ask (skippable) |

`timezone` is not a CV field. Detect it from the system:
`realpath /etc/localtime | sed 's|.*/zoneinfo/||'` → e.g. `Europe/London`. Never
use `date +%Z`, which returns abbreviations like `BST`, not IANA strings.

## Tier 2 — inferences

Derived from the CV's shape, not copied off it. Lower confidence. Always shown
with the evidence they rest on, and never auto-accepted.

**Target titles.** Read the last two or three roles and the trajectory between
them. Propose the current level plus the natural next one — a Senior PM whose
last move was from PM proposes Senior PM and Lead/Group PM, not VP Product.
Propose 3-5, never more.

**Target industries.** Read the employer list and what each company does. Propose
the industries with two or more roles behind them, plus any single role that was
the most recent. Propose 3-5, never more.

**Evidence line.** Every Tier 2 proposal is presented with the roles it came
from, e.g. `from Lead PM at Monzo, Senior PM at Wise`. The user needs to see what
the inference rests on to judge whether it is wrong.

List the roles most recent first, and use the same order every time. Two evidence
lines in the same run that disagree on ordering — titles oldest-first, industries
newest-first — read as carelessness to a user skimming them back-to-back.

## What is NOT extractable

Nothing in a CV states any of these. Never infer them:

- salary expectations
- where the user is willing to work (a CV says where they have lived, not where
  they want to be)
- hard filters / red flags
- companies they are interested in
- when they want an offer
