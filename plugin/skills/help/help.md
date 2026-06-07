# pm-job-search

A Claude Code plugin for senior product leaders running a job search. Finds open roles, scores fit, tracks your pipeline, runs live interview practice, and gives you an honest career coach.

Pure markdown by default — optional browser dashboard and MCP integrations (Granola / Calendar / Gmail) on top.

## Who it's for

Senior PM, lead PM, or head of product running an active search. A different role? You can fork the architecture, but the defaults will need rework.

## The 5 phases

| # | Phase | Skill(s) |
|---|---|---|
| 1 | Setup | `/pm-job-search:setup` |
| 2 | Discover & score | `/pm-job-search:job-search` · `/pm-job-search:evaluate-position <url>` |
| 3 | Apply | `/pm-job-search:apply <Company>` |
| 4 | Interview | `/pm-job-search:story-builder` · `/pm-job-search:interview-prep <Company>` · `/pm-job-search:case-practice` · `pm-job-search:interviewer-simulator` · `/pm-job-search:interview-analysis` |
| 5 | Decide | `/pm-job-search:evaluate-offer` |

## Running alongside

| Skill | When |
|---|---|
| `/pm-job-search:today` | Every morning. |
| `pm-job-search:career-coach` | Anytime you're stuck or weighing something strategic. |
| `/pm-job-search:dashboard` | When you want a visual scan of the pipeline. |
| `/pm-job-search:integrations` | At setup, or after installing a new MCP server. |

## Skills (11)

One-time setup

| Skill | What it does | Use when |
|---|---|---|
| `/setup` | 11 questions, writes profile + strategy + workspace CLAUDE.md. | First install, or you want to update positioning / salary band / target date. |

Daily and weekly

| Skill | What it does | Use when |
|---|---|---|
| `/today` | Two-phase daily brief: catches fresh facts from Calendar/Gmail/Granola, then prints top 3 actions + pipeline + heads-up. | Starting your day. |
| `/job-search` | Weekly sweep. Rechecks P0/P1 companies via ATS APIs, discovers new roles via scoped search. | Once a week, or any time you want fresh roles. |
| `/evaluate-position <url-or-paste>` | Scores one posting, writes the company folder + 200-word research brief. | A single role landed in your inbox. |
| `/apply <Company>` | Tailors your master CV for one role. Up to 5 clarifying questions, then a single-pass draft. | You've decided to apply. |
| `/dashboard` | Browser view of your pipeline; inline status changes + notes. | You want a visual scan instead of reading meta.md files. |
| `/integrations` | Wires in Granola / Calendar / Gmail MCPs if installed. | Setting up, or after installing a new MCP server. |

Interview cluster

| Skill | What it does | Use when |
|---|---|---|
| `/story-builder` | Maintains the universal STAR-story bank. | You remember a story worth capturing, or you want a `--gap-check` of missing senior-PM story types. |
| `/interview-prep <Company>` | Adapts 3–5 stories for a specific round. `--stage` shapes the prep. | You have an interview coming up. |
| `/case-practice [Company]` | MC rapid-recognition drill for product cases. Scores each pick by the failure mode it shows, tracks an 80% readiness gate, writes a session log. | You have a case / product-sense round coming up and want to drill recognition. |
| `/interview-analysis` | Debriefs a transcript (pasted, file, or auto-Granola). Quotes the transcript, flags what landed, names deltas vs prep. | A round just finished. |

Offer decision

| Skill | What it does | Use when |
|---|---|---|
| `/evaluate-offer` | Sense-check verdict, comp shape, archetype fit, anti-pattern scan, 3–5 negotiation moves. | You have an offer (or two) to weigh. |

## Agents (6)

Reviewer panel — invoke 1–4 in parallel on the same draft (case study, prep doc, outreach, take-home). Each returns the same four-section output: what works · what doesn't · weak spots · one rewrite suggestion.

| Agent | Lens | Use when |
|---|---|---|
| `pm-job-search:cpo-reviewer` | CPO: strategy clarity, scale-readiness, business-model fit, judgement under uncertainty. | You want the strategic read. |
| `pm-job-search:eng-manager-reviewer` | EM: technical feasibility, honest trade-offs, collaboration shape. | The draft makes technical claims. |
| `pm-job-search:design-manager-reviewer` | DM: UX judgement, discovery depth, craft, designer treatment. | The draft touches product craft. |
| `pm-job-search:interview-coach` | Narrative: clarity, pacing, voice authenticity, how you come across. | You want a "does this land?" read. |

Strategy and practice

| Agent | What it does | Use when |
|---|---|---|
| `pm-job-search:career-coach` | The honest coach. Offer evaluation, positioning sharpening, anti-goals, search-strategy resets, "something feels off" diagnostics. | You're stuck, weighing something strategic, or your search itself isn't working. |
| `pm-job-search:interviewer-simulator` | Live interview practice. Three modes: full mock round (6–10 questions + pushback), single-question deep-dive, pressure-test on one story's weak angle. | You want to rehearse, not review. |

## Recommended first week

| When | Do this |
|---|---|
| Day 1 | Drop a CV at `userdata/cv.md` if you have one, then `/setup`. Optionally `/integrations`. |
| Day 1–2 | `/job-search` to seed the pipeline, or `/evaluate-position <url>` for one-off roles. |
| Daily | `/today` every morning. |
| Anytime | `pm-job-search:career-coach` when you're stuck or weighing something. |
