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
| Set or refresh your strategy (goals, weekly targets, anti-goals) | `/strategy` |
| Daily brief (pipeline state + progress vs targets) | `/today` |
| Score a job posting against the tier model | `/evaluate-position <url-or-paste>` |
| Weekly job discovery sweep | `/job-search` |
| Maintain your universal story bank | `/story-builder` |
| Prep stories for a specific upcoming interview | `/interview-prep <Company>` |
| Post-interview debrief from a transcript | `/interview-analysis` |

For reviewing any draft — story, research brief, outreach message, take-home assignment — invoke one or more reviewer agents:

| Agent | Lens |
|---|---|
| `cpo-reviewer` | Strategy, scale, business model |
| `eng-manager-reviewer` | Feasibility, engineering trade-offs |
| `design-manager-reviewer` | UX, craft, discovery rigour |
| `interview-coach` | How the candidate comes across — narrative, clarity |
| `career-coach` | Career strategy, offers, positioning (broader than draft review) |

## Data layout

- `userdata/profile.md` — your profile (identity, positioning, tier rubric). Single source of truth for who you are.
- `userdata/strategy.md` — your plan (target offer date, weekly targets, checkpoints). Drives `/today`'s progress tracking. Revisit every 2-3 weeks.
- `userdata/cv.md` — optional. Drop your CV here as md or txt and `/setup` will use it to seed positioning and proof points.
- `userdata/journal.md` — free-form daily notes you append to.
- `userdata/companies/<Company>/` — one folder per company. If you're pursuing a single role, `meta.md` and supporting docs (research, prep, debriefs) live directly inside. If two or more roles at the same company are tracked, each role gets its own slug subfolder: `userdata/companies/<Company>/<role-slug>/meta.md`. Skills handle the 1→2 migration automatically.
- `meta.md` frontmatter per role: `company`, `position`, `status`, `tier`, `link`, dates, optional `monitoring: true|false`.
- `userdata/stories/<filename>.md` — universal STAR-story bank. Filenames are auto-derived from each story's title.
- `userdata/outputs/` — daily briefs and the `applications.md` index. Both `/today` and you can edit `applications.md` freely.

## Status pipeline (used in `meta.md` frontmatter)

**Typical forward path:** `new` → `to_apply` → `applied` → `interviewing` → `offer`

**Exit states reachable from any active stage:**
- `rejected` — they rejected you (or went silent on an application). Reachable from `applied` or `interviewing`.
- `closed` — you closed it (changed mind, listing expired, withdrew at any stage, no longer relevant). Reachable from any active stage including `new`.

**State definitions:**
- `new` — fresh role at top of inbox, decision pending.
- `to_apply` — decided to pursue.
- `applied` — submitted.
- `interviewing` — any active conversation (intro calls, panels, test assignments).
- `offer` — offer in hand.
- `rejected` — they rejected you.
- `closed` — you closed it (withdrew, not interested, no qualifying role, listing expired).

**Monitoring** is a boolean `monitoring: true|false` field on `meta.md` frontmatter, orthogonal to `status`. It means "watch this company for new qualifying roles" — a flag, not a state. A company in any status (including `rejected` or `closed`) can also be `monitoring: true`. `/job-search`'s weekly recheck pass scans `monitoring: true` companies for new roles and adds them; new roles found at monitoring companies don't change the monitoring flag.

**Dedup:** the `(company, position)` exact pair is never duplicated, regardless of status. A new `to_apply` entry never overwrites an old `rejected` entry for the same role — both are real history. A second role at the same company is added as a new role-slug subfolder (see Data layout above).
