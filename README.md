# pm-job-search

An opinionated daily-driver for senior PM / Head of Product job searches. Pure markdown — no Notion, no API tokens, no external services. Clone, install the plugin, run `/pm-job-search:setup`, then `/pm-job-search:today` every morning.

## Why pure markdown

Every other job-search tool starts with "first sign up to <SaaS>, get an API token, duplicate this template…". By the time you're tracking roles, you've spent more time on tooling than searching. `pm-job-search` is the opposite — the user's repo of `.md` files IS the system of record. Skills read markdown, write markdown, full stop.

Trade-off: no calendar integration, no email parsing, no Slack notifications. You bring the search; the plugin gives you structure, scoring, reflection, and per-interview prep.

If you already run MCPs (Granola, Gmail, Calendar, Notion, Playwright) and want to wire them in, see [plugin/INTEGRATIONS.md](plugin/INTEGRATIONS.md) for the prompt patterns that bridge them into specific skills. The plugin doesn't auto-detect or require any of them; the integrations are user-driven and entirely optional.

## Install

```sh
# inside Claude Code, in any workspace:
/plugin marketplace add https://github.com/archugunov/pm-job-search.git
/plugin install pm-job-search@pm-job-search

cd <your-workspace>
# inside Claude Code:
/pm-job-search:setup           # 10 min — identity, target role, salary, hard filters, target date
# you're done. run /pm-job-search:today every morning to see your daily brief.
# ask pm-job-search:career-coach anytime — stuck, got an offer, or want to sharpen your positioning / outreach.
```

> Use the full `https://` URL above (not the `archugunov/pm-job-search` shorthand) — the shorthand defaults to SSH and fails for anyone without SSH keys configured for GitHub. HTTPS reads public repos anonymously.

> The `pm-job-search:` prefix on every command is the deterministic namespaced form — it works regardless of what other plugins you have installed. The unprefixed forms (`/setup`, `/today`, etc.) also work as long as no other installed plugin has a colliding name; the prefix removes the ambiguity.

## The workflow

**One-time setup (~25 min total):**

| Skill | What it does |
|---|---|
| `/pm-job-search:setup` | Onboarding. 11 questions including target offer date. Writes `userdata/profile.md`, a populated `userdata/strategy.md` (with auto-derived weekly cadences based on your timeline + an auto-composed headline goal), an empty `userdata/journal.md`, and a workspace-root `CLAUDE.md`. Idempotent — re-run anytime. CV-import mode (Mode B) reads `userdata/cv.md` to draft positioning + proof points. Closes by optionally invoking `pm-job-search:career-coach` to sharpen positioning. |
| `pm-job-search:career-coach` (agent) | The home for deeper strategy work — anti-goals, pre-committed checkpoints, weekly-cadence rebalancing, positioning refinement, offer evaluation, search-strategy resets. Invoked on-demand by natural language ("help me think through my anti-goals", "should I take this offer?"). |

**Daily / weekly:**

| Skill | What it does |
|---|---|
| `/pm-job-search:today` | Daily brief. Five sections (where you are, this week's progress vs targets, top 3 actions today, pipeline state table, heads-up). Surfaces late-stage interview prompts, shape-mismatch warnings, Monday weekly retrospective. Saves to `userdata/outputs/daily-brief-<date>.md` and regenerates `userdata/outputs/applications.md`. |
| `/pm-job-search:evaluate-position <url-or-paste>` | Score a posting against your tier rubric (5 dimensions × 1-3) with company-shape adjustment. Hard-filter gate before scoring, quick posting check (🟢 looks live / 🟡 looks stale / 🔴 looks dead), user-override on the score. Writes `userdata/companies/<Co>/meta.md` + `~200-word research-brief.md`. Handles 1→2 role folder migration. |
| `/pm-job-search:job-search` | Three-phase weekly sweep. Pre-flight builds dedup data; Phase 1 runs Recheck-A / Recheck-B / Discovery in parallel subagents (recheck uses public no-auth ATS APIs — Ashby / Greenhouse / Lever; discovery uses `site:`-scoped WebSearch against ATS domains to skip aggregators); Phase 2 merges, scores, and delegates filing to `/pm-job-search:evaluate-position`. Optional `--with-playwright` for link-liveness verification. |

**Interview cluster:**

| Skill | What it does |
|---|---|
| `/pm-job-search:story-builder` | Maintain your universal STAR-story bank. Picker shows existing stories by title (sorted by `last_practised`), user edits or describes new. Filenames are auto-derived kebab-slugs. STAR + "Angles for different prompts" structure. |
| `/pm-job-search:interview-prep <Company>` | Adapt 3-5 stories from the bank for a specific upcoming round. `--stage` shapes the prep (recruiter / hiring-manager / panel / cpo-round / take-home). Late-stage rounds auto-include the three founder-vetting questions. Take-home variant produces a working-doc skeleton. Updates each used story's `companies_used_in` + `last_practised`. |
| `/pm-job-search:interview-analysis` | Post-interview debrief from a pasted transcript or `--from-file`. Sections: what landed (anchored to transcript quotes) / what didn't / interviewer signals / vs the prep doc / role shape verdict (🟢 building / 🟡 mixed / 🔴 defending) / process / recommended updates. |

## Agents

Six personas. Four reviewers + one strategic coach + one interview-practice simulator.

**Reviewer panel** (cpo / eng-manager / design-manager / interview-coach) — all share a fixed four-section output contract (What works / What doesn't work / Where it sounds weak from a <persona> lens / One rewrite suggestion) so you can invoke 2-4 in parallel and read them as a panel.

| Agent | Lens |
|---|---|
| `pm-job-search:cpo-reviewer` | Strategy, scale, business model, judgement under uncertainty |
| `pm-job-search:eng-manager-reviewer` | Technical feasibility, engineering trade-offs, collaboration with engineers |
| `pm-job-search:design-manager-reviewer` | UX judgement, craft, discovery rigour, how designers are treated |
| `pm-job-search:interview-coach` | Narrative, clarity, voice authenticity, how the candidate comes across |
| `pm-job-search:career-coach` | Search-strategy work — positioning, outreach, anti-goals, cadence rebalancing, offer evaluation, "something feels off and I can't name it" diagnostics. Honest-calibration mode for the brave assessments. Broader than the four reviewers; covers the whole career arc. |
| `pm-job-search:interviewer-simulator` | PLAYS the interviewer — not draft review, live practice. Three modes: full mock-round simulation, single-question deep-dive, or pressure-test on a story's weak angle. Pushes back on every answer with one calibrated follow-up. End-of-round debrief surfaces what landed vs hand-waves. |

Each agent has its own project-scoped memory at `.claude/agent-memory/<agent>/`. Pass `--save <Company>` and a company arg to also write the review to `userdata/companies/<Co>/review-<persona>-<date>.md`.

`pm-job-search:career-coach` is the home for any deeper strategy work. `/pm-job-search:setup` writes a minimal `strategy.md` (target date + auto-derived weekly cadences + auto-composed headline goal) and defers everything else — anti-goals, checkpoints, target tuning, rubric calibration — to a conversation with career-coach. Invoke by natural language ("got an offer to weigh", "I'm stuck and don't know why", "help me think through what I won't do this search"). The agent diagnoses what's actually wrong before proposing a fix, and routes to the right mechanic (rubric tuning vs anti-goal vs cadence change vs positioning rework). Also invoked by `/setup`'s closing positioning-helper offer — a ~5-minute interview that proposes a sharpened `## Positioning` paragraph for you to paste into `profile.md`.

## What's in `userdata/examples/`

Two fictional personas pre-populated so you can see what a working install looks like before running `/pm-job-search:setup`:

- **`userdata/examples/maya/`** — Maya Patel, senior PM in London consumer credit / fintech. Full install: profile, strategy, journal, two companies (one interviewing, one rejected), one story with adaptation angles, generated applications.md index.
- **`userdata/examples/diego/`** — Diego Alvares, VP Product in Mexico City applying for fully-remote US roles. Skeletal install (profile, strategy, one company, one story) — there to stress-test the schema against USD compensation, no anchor city, US English, B2B SaaS vertical.

Both personas are entirely fictional.

## Audience + caveats

Designed for **senior PM / Head of Product** roles. The tier rubric, status pipeline, story shape, and reviewer agents are tuned for that target. Different role family (engineer, designer, marketer)? Fork it — the architecture is reusable, the defaults aren't.

This is opinionated. The skills surface stop-and-switch nudges, stale-application warnings, shape-mismatch flags on active interviews, and 14-day-out checkpoint reminders. If you want a neutral tracker that doesn't push back, this is the wrong tool.

## Licence

MIT. See [LICENSE](../LICENSE).
