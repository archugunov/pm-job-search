# pm-job-search

An opinionated daily-driver for senior PM / Head of Product job searches. Pure markdown — no Notion, no API tokens, no external services. Clone, install the plugin, run `/setup` then `/strategy`, then `/today` every morning.

## Why pure markdown

Every other job-search tool starts with "first sign up to <SaaS>, get an API token, duplicate this template…". By the time you're tracking roles, you've spent more time on tooling than searching. `pm-job-search` is the opposite — the user's repo of `.md` files IS the system of record. Skills read markdown, write markdown, full stop.

Trade-off: no calendar integration, no email parsing, no Slack notifications. You bring the search; the plugin gives you structure, scoring, reflection, and per-interview prep.

## Install

```sh
# add the plugin to a Claude Code workspace (publish path TBD)
# claude plugin install pm-job-search

cd <your-workspace>
# inside Claude Code:
/setup           # 10 min — identity, target role, salary, hard filters
/strategy        # 15-20 min — goals, weekly targets, anti-goals, checkpoints
# you're done. run /today every morning to see your daily brief.
```

## The workflow

**One-time setup (~25 min total):**

| Skill | What it does |
|---|---|
| `/setup` | Onboarding. 10 questions. Writes `userdata/profile.md`, a placeholder `userdata/strategy.md`, an empty `userdata/journal.md`, and a workspace-root `CLAUDE.md`. Idempotent — re-run anytime. CV-import mode (Mode B) reads `userdata/cv.md` to draft positioning + proof points. Closes by offering `/strategy`. |
| `/strategy` | 15-20 minute conversational reflection across 5 themes (destination / weekly cadence / pipeline floor / pre-committed checkpoints / anti-goals). Writes `userdata/strategy.md`. Re-run every 2-3 weeks as the search evolves. `--theme <name>` jumps to one theme. |

**Daily / weekly:**

| Skill | What it does |
|---|---|
| `/today` | Daily brief. Five sections (where you are, this week's progress vs targets, top 3 actions today, pipeline state table, heads-up). Surfaces late-stage interview prompts, shape-mismatch warnings, Monday weekly retrospective. Saves to `userdata/outputs/daily-brief-<date>.md` and regenerates `userdata/outputs/applications.md`. |
| `/evaluate-position <url-or-paste>` | Score a posting against your tier rubric (5 dimensions × 1-3) with company-shape adjustment. Hard-filter gate before scoring, posting-legitimacy verdict (🟢/🟡/🔴), user-override on the score. Writes `userdata/companies/<Co>/meta.md` + `~200-word research-brief.md`. Handles 1→2 role folder migration. |
| `/job-search` | Three-phase weekly sweep. Pre-flight builds dedup data; Phase 1 runs Recheck-A / Recheck-B / Discovery in parallel subagents (recheck uses public no-auth ATS APIs — Ashby / Greenhouse / Lever; discovery uses `site:`-scoped WebSearch against ATS domains to skip aggregators); Phase 2 merges, scores, and delegates filing to `/evaluate-position`. Optional `--with-playwright` for link-liveness verification. |

**Interview cluster:**

| Skill | What it does |
|---|---|
| `/story-builder` | Maintain your universal STAR-story bank. Picker shows existing stories by title (sorted by `last_practised`), user edits or describes new. Filenames are auto-derived kebab-slugs. STAR + "Angles for different prompts" structure. |
| `/interview-prep <Company>` | Adapt 3-5 stories from the bank for a specific upcoming round. `--stage` shapes the prep (recruiter / hiring-manager / panel / cpo-round / take-home). Late-stage rounds auto-include the three founder-vetting questions. Take-home variant produces a working-doc skeleton. Updates each used story's `companies_used_in` + `last_practised`. |
| `/interview-analysis` | Post-interview debrief from a pasted transcript or `--from-file`. Sections: what landed (anchored to transcript quotes) / what didn't / interviewer signals / vs the prep doc / role shape verdict (🟢 building / 🟡 mixed / 🔴 defending) / process / recommended updates. |

## Reviewer agents

Five personas for reviewing any draft — case study, story, prep doc, take-home, outreach, research brief. All share a fixed four-section output contract (What works / What doesn't work / Where it sounds weak from a <persona> lens / One rewrite suggestion) so you can invoke 2-4 in parallel and read them as a panel.

| Agent | Lens |
|---|---|
| `cpo-reviewer` | Strategy, scale, business model, judgement under uncertainty |
| `eng-manager-reviewer` | Technical feasibility, engineering trade-offs, collaboration with engineers |
| `design-manager-reviewer` | UX judgement, craft, discovery rigour, how designers are treated |
| `interview-coach` | Narrative, clarity, voice authenticity, how the candidate comes across |
| `career-coach` | Positioning, market readability, offer leverage, whether the artefact serves the bigger plan |

Each agent has its own project-scoped memory at `.claude/agent-memory/<agent>/`. Pass `--save <Company>` and a company arg to also write the review to `userdata/companies/<Co>/review-<persona>-<date>.md`.

`career-coach` is also invoked by `/setup`'s closing positioning-helper offer — a ~5-minute interview that proposes a sharpened `## Positioning` paragraph for you to paste into `profile.md`.

## What's in `userdata/examples/`

Two fictional personas pre-populated so you can see what a working install looks like before running `/setup`:

- **`userdata/examples/maya/`** — Maya Patel, senior PM in London consumer credit / fintech. Full install: profile, strategy, journal, two companies (one interviewing, one rejected), one story with adaptation angles, generated applications.md index.
- **`userdata/examples/diego/`** — Diego Alvares, VP Product in Mexico City applying for fully-remote US roles. Skeletal install (profile, strategy, one company, one story) — there to stress-test the schema against USD compensation, no anchor city, US English, B2B SaaS vertical.

Both personas are entirely fictional.

## Audience + caveats

Designed for **senior PM / Head of Product** roles. The tier rubric, status pipeline, story shape, and reviewer agents are tuned for that target. Different role family (engineer, designer, marketer)? Fork it — the architecture is reusable, the defaults aren't.

This is opinionated. The skills surface stop-and-switch nudges, stale-application warnings, shape-mismatch flags on active interviews, and 14-day-out checkpoint reminders. If you want a neutral tracker that doesn't push back, this is the wrong tool.

## Licence

MIT. See [LICENSE](../LICENSE).
