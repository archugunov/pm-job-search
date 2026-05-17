# pm-job-search

A Claude Code plugin for senior PM and Head of Product job searches. Tracks your pipeline, runs live interview practice, and has an honest career coach you can call on. Markdown by default — expandable with integrations.

## How it works

1. **Set up once.** `/pm-job-search:setup` walks you through 11 questions (~10-15 min). It writes your profile, a strategy file with auto-derived weekly targets, and a workspace `CLAUDE.md` so every Claude Code session in this folder knows your context.
2. **Daily loop.** Every morning: `/pm-job-search:today` for the 5-section brief. As roles surface: `/pm-job-search:evaluate-position <url>` to score and file them. Before interviews: `/pm-job-search:interview-prep <Company>` for prep, `pm-job-search:interviewer-simulator` to rehearse. After: `/pm-job-search:interview-analysis` with the transcript.
3. **Coach on call.** `pm-job-search:career-coach` is there for anything strategic — got an offer, feeling stuck, positioning not landing, "should I widen the search?". It reads your install state first, then diagnoses before it suggests.

Everything lives as markdown in `userdata/` (gitignored by default). You can edit any file manually anytime; the plugin is opinionated structure on top of files you own.

## What makes it different

Three things most job-search tools don't do:

- **Honest coaching.** A career-coach agent that diagnoses what's actually wrong — and will tell you the search itself needs restarting when the data says so, not just suggest more applications. Five trigger patterns (level miscalibration, comp underselling, sunk-cost reset, pattern-of-rejection, hard-stop check) surface uncomfortable truths with specific data, not generic motivation.
- **Live interview practice.** A simulator agent that PLAYS the interviewer — asks real hard questions, pushes back on hand-wavy answers, debriefs at the end. Three modes: full mock-round simulation, single-question deep-dive, or pressure-test on one story's weak angle. Not draft review — real-pressure rehearsal.
- **A daily brief that escalates.** When patterns suggest structural problems (5 rejections at the same stage, 8 weeks of thin pipeline, cadence drift for 4 weeks running), `/today` doesn't say "keep going". It points at the right help with the specific data.

The cost: no Notion sync, no calendar integration, no email parsing by default. You bring the search; the plugin gives you structure, scoring, reflection, practice, and honest coaching. If you already run MCPs and want to wire them in, [INTEGRATIONS.md](INTEGRATIONS.md) documents the prompt patterns.

## Why pure markdown

Every other job-search tool starts with "first sign up to <SaaS>, get an API token, duplicate this template…". By the time you're tracking roles, you've spent more time on tooling than searching. `pm-job-search` is the opposite — the user's repo of `.md` files IS the system of record. Skills read markdown, write markdown, full stop. Your `userdata/` directory is gitignored by default; nothing leaves your machine unless you choose to share it.

## Install

```sh
# inside Claude Code, in any workspace:
/plugin marketplace add https://github.com/archugunov/pm-job-search.git
/plugin install pm-job-search@pm-job-search

cd <your-workspace>
# inside Claude Code:
/pm-job-search:setup           # 10-15 min — identity, target role, salary, hard filters, target date
# you're done. run /pm-job-search:today every morning to see your daily brief.
# ask pm-job-search:career-coach anytime — stuck, got an offer, or want to sharpen your positioning / outreach.
```

> Use the full `https://` URL above (not the `archugunov/pm-job-search` shorthand) — the shorthand defaults to SSH and fails for anyone without SSH keys configured for GitHub. HTTPS reads public repos anonymously.

> The `pm-job-search:` prefix on every command is the deterministic namespaced form — it works regardless of what other plugins you have installed. The unprefixed forms (`/setup`, `/today`, etc.) also work as long as no other installed plugin has a colliding name; the prefix removes the ambiguity.

## The workflow — 8 skills

**One-time setup (~10-15 min):**

| Skill | What it does |
|---|---|
| `/pm-job-search:setup` | Onboarding. 11 questions including target offer date. Writes `userdata/profile.md`, a populated `userdata/strategy.md` (auto-derived weekly cadences based on your timeline + an auto-composed headline goal), an empty `userdata/journal.md`, and a workspace-root `CLAUDE.md`. Idempotent — re-run anytime. CV-import mode (Mode B) reads `userdata/cv.md` to draft positioning + proof points. Closes by optionally invoking `pm-job-search:career-coach` to sharpen positioning. |

**Daily / weekly:**

| Skill | What it does |
|---|---|
| `/pm-job-search:today` | Daily brief. Five sections: where you are, this week's progress vs targets, top 3 actions today, pipeline state table, heads-up. Surfaces late-stage interview prompts, shape-mismatch warnings, Monday weekly retrospective, and three coach-nudge triggers (cadence drift / closing roles without applying / sunk-cost structural rethink) that route you to `pm-job-search:career-coach` when patterns warrant it. Saves to `userdata/outputs/daily-brief-<date>.md` and regenerates `userdata/outputs/applications.md`. |
| `/pm-job-search:evaluate-position <url-or-paste>` | Score a posting against your tier rubric (5 dimensions × 1-3) with company-shape adjustment. Hard-filter gate before scoring, anti-goal soft warning, quick posting check (🟢 looks live / 🟡 looks stale / 🔴 looks dead), user-override on the score. Writes `userdata/companies/<Co>/meta.md` + `~200-word research-brief.md`. Handles 1→2 role folder migration when a second role is added at the same company. |
| `/pm-job-search:job-search` | Three-phase weekly sweep. Pre-flight builds dedup data; Phase 1 runs Recheck-A / Recheck-B / Discovery in parallel subagents (recheck uses public no-auth ATS APIs — Ashby / Greenhouse / Lever; discovery uses `site:`-scoped WebSearch against ATS domains to skip aggregators); Phase 2 merges, scores, and delegates filing to `/pm-job-search:evaluate-position`. Optional `--with-playwright` for link-liveness verification. |

**Interview cluster:**

| Skill | What it does |
|---|---|
| `/pm-job-search:story-builder` | Maintain your universal STAR-story bank. Picker shows existing stories by title (sorted by `last_practised`), user edits or describes new. Filenames are auto-derived kebab-slugs. STAR + "Angles for different prompts" structure — each story carries 3-5 angles pre-loaded for different question types. |
| `/pm-job-search:interview-prep <Company>` | Adapt 3-5 stories from the bank for a specific upcoming round. `--stage` shapes the prep (recruiter / hiring-manager / panel / cpo-round / final-loop / take-home). Late-stage rounds auto-include the three founder-vetting questions. Take-home variant produces a working-doc skeleton. Updates each used story's `companies_used_in` + `last_practised`. |
| `/pm-job-search:interview-analysis` | Post-interview debrief from a pasted transcript or `--from-file`. Sections: what landed (anchored to transcript quotes) / what didn't / interviewer signals / vs the prep doc / role shape verdict (🟢 building / 🟡 mixed / 🔴 defending) / process / recommended updates. |

**Optional — wire in external tools:**

| Skill | What it does |
|---|---|
| `/pm-job-search:integrations` | Probes which MCP integrations are installed (Granola, Calendar, Gmail), walks through wiring each available one with at most 1-2 questions per integration, saves customized invocation patterns to `userdata/integrations.md`. Granola feeds `/interview-analysis`, Calendar feeds `/today` heads-up, Gmail feeds journal updates. Skip-friendly — none required. The other three integrations in [INTEGRATIONS.md](INTEGRATIONS.md) (Notion, Playwright, Slack) stay manual-setup. |

## Agents — 6 personas

Four reviewers + one strategic coach + one interview-practice simulator.

**Reviewer panel** (cpo / eng-manager / design-manager / interview-coach) — all share a fixed four-section output contract (What works / What doesn't work / Where it sounds weak from a <persona> lens / One rewrite suggestion) so you can invoke 2-4 in parallel and read them as a panel.

| Agent | Lens |
|---|---|
| `pm-job-search:cpo-reviewer` | Strategy, scale, business model, judgement under uncertainty |
| `pm-job-search:eng-manager-reviewer` | Technical feasibility, engineering trade-offs, collaboration with engineers |
| `pm-job-search:design-manager-reviewer` | UX judgement, craft, discovery rigour, how designers are treated |
| `pm-job-search:interview-coach` | Narrative, clarity, voice authenticity, how the candidate comes across |
| `pm-job-search:career-coach` | The strategic coach. Handles positioning, outreach, anti-goals, cadence rebalancing, offer evaluation, search-strategy resets, and "something feels off and I can't name it" diagnostics. **Honest-calibration mode** surfaces the brave assessments most tools dodge — with specific data, not generic motivation. Broader than the four reviewers; covers the whole career arc. |
| `pm-job-search:interviewer-simulator` | The practice agent. Plays the interviewer in three modes: full mock-round (6-10 questions, push back on each), single-question deep-dive (one question + three escalating follow-ups), or pressure-test (the most uncharitable version of a question targeting one story's weak angle). End-of-round debrief surfaces what landed, what didn't, and hand-wave moments. Optional `--save <Company>` writes the transcript + debrief. |

Each agent has its own project-scoped memory at `.claude/agent-memory/<agent>/`. Reviewer agents take `--save <Company>` to write the review to `userdata/companies/<Co>/[<role-slug>/]review-<persona>-<date>.md`.

`pm-job-search:career-coach` is the home for any deeper strategy work. `/pm-job-search:setup` writes a minimal `strategy.md` (target date + auto-derived weekly cadences + auto-composed headline goal) and defers everything else — anti-goals, checkpoints, target tuning, rubric calibration — to a conversation with career-coach. Invoke by natural language ("got an offer to weigh", "I'm stuck and don't know why", "help me think through what I won't do this search"). The agent diagnoses what's actually wrong before proposing a fix, and routes to the right mechanic (rubric tuning vs anti-goal vs cadence change vs positioning rework).

## Extending the plugin

The plugin is markdown-only by default, but power users can wire in existing MCP servers to make specific skills more capable. See [INTEGRATIONS.md](INTEGRATIONS.md) for documented prompt patterns covering:

- **Granola** — pull meeting transcripts directly into `/interview-analysis`
- **Gmail (or any inbox MCP)** — extract recruiter conversations into `journal.md`
- **Calendar (gcal / iCal)** — surface upcoming interviews in `/today`
- **Notion** — sync companies as Notion DB rows alongside the markdown source
- **Playwright** — JD link-liveness verification + interviewer research
- **Slack / Telegram / Discord** — pipe `/today` digests to an accountability channel

Each integration is a prompt pattern, not a plugin code change. The plugin doesn't auto-detect or require any of them.

## What's in `userdata/examples/`

Two fictional personas pre-populated so you can see what a working install looks like before running `/pm-job-search:setup`:

- **`userdata/examples/maya/`** — Maya Patel, senior PM in London consumer credit / fintech. Full install: profile, strategy, journal, two companies (one interviewing, one rejected), two stories with adaptation angles, generated applications.md index.
- **`userdata/examples/diego/`** — Diego Alvares, VP Product in Mexico City applying for fully-remote US roles. Skeletal install (profile, strategy, one company, one story) — stress-tests the schema against USD compensation, no anchor city, US English, B2B SaaS vertical.

Both personas are entirely fictional.

## Audience + caveats

Designed for **senior PM / Head of Product** roles. The tier rubric, status pipeline, story shape, and reviewer agents are tuned for that target. Different role family (engineer, designer, marketer)? Fork it — the architecture is reusable, the defaults aren't.

This is opinionated. The skills surface stop-and-switch nudges, stale-application warnings, shape-mismatch flags on active interviews, sunk-cost triggers, and 14-day-out checkpoint reminders. The career-coach will tell you uncomfortable things when the data warrants. If you want a neutral tracker that doesn't push back, this is the wrong tool.

## Privacy + contributing

Your `userdata/` directory is gitignored except `userdata/examples/`. Personal data you put there (profile, journal, company notes) never leaves your machine unless you choose to share it.

A privacy-check CI workflow scans every push and PR for the plugin author's personal-data blocklist via ripgrep. If you fork, either replace the blocklist with your own terms or remove the workflow entirely — your fork, your privacy posture.

Contributions welcome. See [CONTRIBUTING.md](../CONTRIBUTING.md) for scope, install-for-development, the privacy hard rule, testing conventions, and what to file issues for vs not.

## Licence

MIT. See [LICENSE](../LICENSE).
