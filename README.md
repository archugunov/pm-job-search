# pm-job-search

A Claude Code plugin for senior PM and Head of Product job searches. Finds open roles, scores fit, tracks your pipeline, runs live interview practice, and gives you an honest career coach. Markdown by default — expandable with integrations.

## How it works

1. **Set up once.** `/pm-job-search:setup` — 11 questions, ~10-15 min.
2. **Daily loop.** `/pm-job-search:today` for the morning brief. `/pm-job-search:evaluate-position <url>` to score new roles. Before interviews: `/pm-job-search:interview-prep <Company>` to prep, `pm-job-search:interviewer-simulator` to rehearse, `/pm-job-search:interview-analysis` after.
3. **Coach on call.** `pm-job-search:career-coach` for anything strategic — offer to weigh, feeling stuck, positioning not landing. Diagnoses before it suggests.

## What makes it different

Built for senior PMs. Tracks your pipeline like other tools — and pushes back when it's not working.

- **The simulator interviews you, for real.** Hard questions, pushback when you're hand-waving, debrief after. Four reviewer agents (CPO, eng manager, design manager, interview coach) critique your drafts in parallel.
- **The coach tells you what's actually wrong.** Three same-stage rejections? Eight weeks of thin pipeline? `/today` hands you to `career-coach`, which surfaces things like wrong level, hollow-HoP risk, or "this search needs restarting" — not "send more applications". `/evaluate-offer` runs the same check on offers when they land.

MCP integrations (Granola / Calendar / Gmail) plug in via `/pm-job-search:integrations`.

## Why pure markdown

Your repo of `.md` files IS the system of record. Skills read markdown, write markdown — that's it. The `userdata/` directory is gitignored by default; nothing leaves your machine unless you choose to share it.

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

## The workflow — 9 skills

**One-time setup (~10-15 min):**

| Skill | What it does |
|---|---|
| `/pm-job-search:setup` | 11 questions including target offer date. Writes profile + strategy + workspace `CLAUDE.md`. Re-runnable. Pre-fills positioning from a CV if you drop one into `userdata/cv.md`. |

**Daily / weekly:**

| Skill | What it does |
|---|---|
| `/pm-job-search:today` | Daily brief: where you are, weekly progress vs targets, top 3 actions, pipeline state, heads-up. Routes you to `pm-job-search:career-coach` when multi-week patterns suggest the strategy itself needs rework. First run offers to set up 9am daily auto-runs. |
| `/pm-job-search:evaluate-position <url-or-paste>` | Score a posting against your tier rubric with company-shape adjustment. Hard-filter + anti-goal gates, posting-liveness check, user-override. Writes the company folder (meta + ~200-word research brief). |
| `/pm-job-search:job-search` | Weekly sweep. Parallel subagents recheck your P0/P1 companies via public ATS APIs (Ashby / Greenhouse / Lever) and discover new roles via `site:`-scoped search. Scores and files results via `/evaluate-position`. Optional `--with-playwright` for link verification. |

**Interview cluster:**

| Skill | What it does |
|---|---|
| `/pm-job-search:story-builder` | Maintain your universal STAR-story bank. Each story carries 3-5 pre-loaded angles for different question types. |
| `/pm-job-search:interview-prep <Company>` | Adapt 3-5 stories from the bank for a specific upcoming round. `--stage` shapes the prep (recruiter / hiring-manager / panel / cpo-round / final-loop / take-home). Late-stage rounds include three founder-vetting questions. Take-home variant produces a working-doc skeleton. |
| `/pm-job-search:interview-analysis` | Post-interview debrief from a pasted transcript or `--from-file`. Anchors findings to transcript quotes: what landed, what didn't, interviewer signals, deltas vs the prep, recommended updates. Auto-pulls from Granola when wired. |
| `/pm-job-search:evaluate-offer` | Sense-check an offer (or compare two) against your profile + anti-goals + the senior-PM archetype/anti-pattern references. Verdict, comp shape, role-shape re-check, archetype fit, named-anti-pattern scan, weighted decision factors, downside scenario, 3-5 specific negotiation moves to ask for. Always pairs with a "what would I regret in 2 years?" handoff to the coach. |

**Optional — wire in external tools:**

| Skill | What it does |
|---|---|
| `/pm-job-search:integrations` | Probes for Granola / Calendar / Gmail MCPs and wires the ones you have. Granola feeds `/interview-analysis`, Calendar feeds `/today` heads-up, Gmail feeds journal updates. Saves invocation patterns to `userdata/integrations.md`. Optional — the plugin works fine without any of them. See [INTEGRATIONS.md](plugin/INTEGRATIONS.md) for Notion, Playwright, Slack as manual-setup. |

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

The plugin is markdown-only by default, but power users can wire in existing MCP servers to make specific skills more capable. See [INTEGRATIONS.md](plugin/INTEGRATIONS.md) for documented prompt patterns covering:

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

## Audience

Designed for senior PM / Head of Product roles. The tier rubric, status pipeline, story shape, and reviewer agents are tuned for that target. Different role family (engineer, designer, marketer)? Fork it — the architecture is reusable, the defaults aren't.

## Privacy + contributing

Your `userdata/` directory is gitignored except `userdata/examples/`. Personal data you put there (profile, journal, company notes) never leaves your machine unless you choose to share it.

A privacy-check CI workflow scans every push and PR for the plugin author's personal-data blocklist via ripgrep. If you fork, either replace the blocklist with your own terms or remove the workflow entirely — your fork, your privacy posture.

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for scope, install-for-development, the privacy hard rule, testing conventions, and what to file issues for vs not.

## Licence

MIT. See [LICENSE](LICENSE).
