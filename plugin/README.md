# pm-job-search

A Claude Code plugin for senior PM and Head of Product job searches. Finds open roles, scores fit, tracks your pipeline, runs live interview practice, and gives you an honest career coach. Markdown by default — expandable with integrations.

## How it works

1. **Set up once.** `/pm-job-search:setup` — 11 questions, ~10-15 min.
2. **Daily loop.** `/pm-job-search:today` for the morning brief. `/pm-job-search:evaluate-position <url>` to score new roles. Before interviews: `/pm-job-search:interview-prep <Company>` to prep, `pm-job-search:interviewer-simulator` to rehearse, `/pm-job-search:interview-analysis` after.
3. **Coach on call.** `pm-job-search:career-coach` for anything strategic — offer to weigh, feeling stuck, positioning not landing. Figures out what's actually wrong before proposing a fix.

### Visual dashboard

Run `/pm-job-search:dashboard` to open a browser view of your pipeline. The dashboard reads the same md files all other skills use (`userdata/companies/*/meta.md`, `userdata/strategy.md`, latest `userdata/outputs/daily-brief-*.md`) and can write two things back: status changes and timestamped notes (`notes.md` per company). New positions are created via `/pm-job-search:evaluate-position <link>` — the dashboard doesn't try to scaffold positions itself because evaluation can't be triggered from a separate process. Built with React + Mantine; the bundle is pre-built and committed, so installation costs zero. Stops on ctrl-C.

## What makes it different

Built for senior PMs. Tracks your pipeline like other tools — and pushes back when it's not working.

- **Says what's actually wrong, with the data to back it.** Three take-home rejections in a row? `/today` tells you it's a written-communication gap, not bad luck. Eight weeks in and one thread? `career-coach` tells you the search itself isn't working — adjusting the cadence won't fix it. A Head-of-Product offer at a 200-person company? `/evaluate-offer` flags hollow-HoP risk before you sign.
- **Built around how senior-PM searches actually work.** Reviewer agents that play the four people who'll interview you (CPO, eng manager, design manager, interview coach). The three founder-vetting questions show up in every late-stage prep. When you're weighing an offer, it checks the role's stage against how you actually operate (builder, scaler, or operator). And there's a simulator for practising the hardest questions when you want it.

MCP integrations (Granola / Calendar / Gmail) plug in via `/pm-job-search:integrations`.

## Why pure markdown

Your repo of `.md` files is the system of record. Skills read markdown, write markdown — that's the whole contract. The `userdata/` directory is gitignored by default, so nothing leaves your machine unless you share it on purpose.

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

## The workflow — 10 skills

**One-time setup (~10-15 min):**

| Skill | What it does |
|---|---|
| `/pm-job-search:setup` | 11 questions including target offer date. Writes profile + strategy + workspace `CLAUDE.md`. Re-runnable. Pre-fills positioning from a CV if you drop one into `userdata/cv.md`. |

**Daily / weekly:**

| Skill | What it does |
|---|---|
| `/pm-job-search:today` | Daily brief: where you are, weekly progress vs targets, top 3 actions, pipeline state, heads-up. Routes you to `pm-job-search:career-coach` when multi-week patterns suggest the strategy itself needs rework. First run offers to set up 9am daily auto-runs. |
| `/pm-job-search:dashboard` | Visual dashboard — pipeline view, inline status changes, quick notes per company. Reads the same md files all other skills use; writes status changes + notes back. React + Mantine, pre-built bundle, zero install. |
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
| `/pm-job-search:integrations` | Probes for Granola / Calendar / Gmail MCPs and wires the ones you have. Granola feeds `/interview-analysis`, Calendar feeds `/today` heads-up, Gmail feeds journal updates. Saves invocation patterns to `userdata/integrations.md`. Optional — the plugin works fine without any of them. See [INTEGRATIONS.md](INTEGRATIONS.md) for Notion, Playwright, Slack as manual-setup. |

## Agents — 6 personas

Four reviewers, one strategic coach, one interview-practice simulator.

The four reviewers (cpo / eng-manager / design-manager / interview-coach) share the same four-section output — what works, what doesn't, where it sounds weak from that persona's lens, one rewrite suggestion. Run 2-4 of them in parallel and read them as a panel.

| Agent | Lens |
|---|---|
| `pm-job-search:cpo-reviewer` | Strategy, scale, business model, judgement under uncertainty |
| `pm-job-search:eng-manager-reviewer` | Technical feasibility, engineering trade-offs, collaboration with engineers |
| `pm-job-search:design-manager-reviewer` | UX judgement, craft, discovery rigour, how designers are treated |
| `pm-job-search:interview-coach` | Narrative, clarity, voice authenticity, how the candidate comes across |
| `pm-job-search:career-coach` | The strategic coach. Handles positioning, outreach, anti-goals, cadence rebalancing, offer evaluation, search-strategy resets, and "something feels off and I can't name it" diagnostics. **Honest-calibration mode** surfaces the brave assessments most tools dodge — with specific data, not generic motivation. Broader than the four reviewers; covers the whole career arc. |
| `pm-job-search:interviewer-simulator` | The practice agent. Plays the interviewer in three modes: full mock-round (6-10 questions, push back on each), single-question deep-dive (one question + three escalating follow-ups), or pressure-test (the most uncharitable version of a question targeting one story's weak angle). End-of-round debrief surfaces what landed, what didn't, and hand-wave moments. Optional `--save <Company>` writes the transcript + debrief. |

Each agent has its own project-scoped memory at `.claude/agent-memory/<agent>/`. Reviewer agents take `--save <Company>` to write the review to `userdata/companies/<Co>/[<role-slug>/]review-<persona>-<date>.md`.

`pm-job-search:career-coach` is the home for any deeper strategy work. `/setup` writes a basic `strategy.md` — target date, weekly cadences derived from your timeline, headline goal — and leaves everything else (anti-goals, checkpoints, target tuning, rubric calibration) for a conversation with career-coach when you want it. Invoke by natural language — "got an offer to weigh", "I'm stuck and don't know why", "help me think through what I won't do this search". The agent figures out what's actually wrong before proposing a fix, and routes to the right mechanic (rubric tuning, anti-goal, cadence change, positioning rework — whichever it is).

## Extending the plugin

Markdown-only is the default, but you can wire in MCP servers you're already running to make specific skills more capable. See [INTEGRATIONS.md](INTEGRATIONS.md) for the prompt patterns, covering:

- **Granola** — pull meeting transcripts straight into `/interview-analysis`
- **Gmail (or any inbox MCP)** — extract recruiter conversations into `journal.md`
- **Calendar (gcal / iCal)** — surface upcoming interviews in `/today`
- **Notion** — sync companies as Notion DB rows alongside the markdown source
- **Playwright** — link-liveness verification + interviewer research
- **Slack / Telegram / Discord** — pipe `/today` digests to an accountability channel

Each one is a prompt pattern, not a plugin code change — nothing to install on the plugin side, nothing it auto-detects.

## What's in `userdata/examples/`

Two fictional personas so you can see what a working install looks like before running `/setup`:

- **`userdata/examples/maya/`** — Maya Patel, senior PM in London doing consumer credit / fintech. Full install: profile, strategy, journal, two companies (one interviewing, one rejected), two stories with adaptation angles, a generated applications.md index.
- **`userdata/examples/diego/`** — Diego Alvares, VP Product in Mexico City going after fully-remote US roles. Skeletal install (profile, strategy, one company, one story) — stress-tests the schema against USD compensation, no anchor city, US English, B2B SaaS.

Both personas are entirely fictional.

## Audience

Designed for senior PM / Head of Product roles. The tier rubric, status pipeline, story shape, and reviewer agents are tuned for that target. Different role family (engineer, designer, marketer)? Fork it — the architecture is reusable, the defaults aren't.

## Privacy + contributing

Your `userdata/` directory is gitignored except for the example installs. Anything you put there — profile, journal, company notes — stays on your machine unless you share it on purpose.

A CI workflow scans every push and PR for the plugin author's personal-data blocklist (via ripgrep). If you fork, swap the blocklist for your own terms or remove the workflow entirely — your fork, your call.

Contributions welcome. [CONTRIBUTING.md](../CONTRIBUTING.md) covers scope, dev install, the privacy hard rule, testing conventions, and what's in scope for issues vs not.

## Licence

MIT. See [LICENSE](../LICENSE).
