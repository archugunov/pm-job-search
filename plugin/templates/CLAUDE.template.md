<!--
  pm-job-search — CLAUDE.md template.
  /setup writes a copy of this file to your workspace root after filling in
  the {{INCLUDE}} markers with content from userdata/profile.md.
  Re-run /setup --refresh to update it after editing profile.md.
-->

# Job Search — Claude Context

> All career-related skills in this workspace read `userdata/profile.md` as
> their source of truth. Edit that file (or re-run `/setup`) to change your
> positioning, target role, salary band, or tier rubric.

## About me

{{INCLUDE: userdata/profile.md sections=positioning,proof_points,moat}}

## Workflow

Use the skills shipped by the pm-job-search plugin.

| Task | Skill |
|---|---|
| First-run install / re-configure | `/setup` |
| Daily brief (pipeline state + priorities) | `/today` |
| Score a job posting against the tier model | `/evaluate-position <url-or-paste>` |
| Weekly job discovery sweep | `/job-search` |
| Maintain your universal story bank | `/story-builder` |
| Prep stories for a specific upcoming interview | `/interview-prep <Company>` |
| Post-interview debrief from a transcript | `/interview-analysis` |
| Work on a PM take-home case study | `/pm-case-study` |

For reviewing a case study draft, invoke one or more reviewer agents:

| Agent | Lens |
|---|---|
| `cpo-reviewer` | Strategy, scale, business model |
| `eng-manager-reviewer` | Feasibility, engineering trade-offs |
| `design-manager-reviewer` | UX, craft, discovery rigour |
| `interview-coach` | How the candidate comes across — narrative, clarity |
| `tech-career-coach` | Career strategy, offers, positioning (broader than case-study review) |

## Data layout

- `userdata/profile.md` — your profile (frontmatter + prose). Single source of truth.
- `userdata/journal.md` — free-form daily notes you append to.
- `userdata/companies/<Company>/meta.md` — YAML frontmatter per company: status, tier, position, link, dates.
- `userdata/companies/<Company>/*.md` — research briefs, interview prep, debriefs, case studies — written by skills, edited by you.
- `userdata/stories/<filename>.md` — universal STAR-story bank. Filenames are auto-derived from each story's title.
- `userdata/outputs/` — generated artefacts (daily briefs, applications.md index).

## Status pipeline (used in `meta.md` frontmatter)

`new` → `to_apply` → `applied` → `interviewing` → (`offer` | `rejected` | `closed`)

- `new` — fresh role at top of inbox, decision pending.
- `to_apply` — decided to pursue.
- `applied` — submitted.
- `interviewing` — any active conversation (intro calls, panels, test assignments).
- `offer` — offer in hand.
- `rejected` — they rejected you.
- `closed` — you closed it (withdrew, not interested, no qualifying role).

Monitoring is a tier (P2) plus `to_apply` status, not a separate state.
