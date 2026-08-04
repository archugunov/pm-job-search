# CV extraction

Shared by `/setup` and `job-sweep`. Covers finding a CV, reading it, and what may
be taken from it. Drafting rules — tone, banned phrases, proof-point format —
are NOT here; they belong to the skill that drafts.

## Finding the CV

Check, in order: `userdata/cv.md`, `userdata/cv.txt`, `userdata/cv.pdf`. First hit wins.

If a `cv.*` file exists in an unreadable format (`.docx`, `.pages`, `.rtf`, or
anything else), print exactly one line and continue without it:

> `Found userdata/cv.<ext>. Readable formats are .md, .txt, or .pdf — convert your CV first if you want me to draft from it.`

If no `cv.*` file exists, offer the drop. Create `userdata/` and the three
`.gitkeep` files (`userdata/companies/.gitkeep`, `userdata/stories/.gitkeep`,
`userdata/outputs/.gitkeep`) FIRST, so the user has somewhere to put it, then say:

> `I've created userdata/ for you — drop your CV there as cv.md, cv.txt, or cv.pdf. Say 'ready' when it's in.`

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

## What is NOT extractable

Nothing in a CV states any of these. Never infer them:

- salary expectations
- where the user is willing to work (a CV says where they have lived, not where
  they want to be)
- hard filters / red flags
- companies they are interested in
- when they want an offer
