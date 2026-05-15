# pm-job-search

> **WIP** — scaffolding is in place; skills and agents land in upcoming
> commits. This README will be expanded once the skills can actually run.

An opinionated daily-driver for senior PM / Head of Product job searches.
Pure markdown — no Notion, no API tokens, no external services. Clone, install
the plugin, run `/setup`, run `/today` every morning.

## Install

```sh
# add this plugin to a workspace (path TBD once published)
# claude plugin install pm-job-search

cd <your-workspace>
# run the onboarding flow inside Claude Code
/setup
# you're done. run /today to see your daily brief.
```

## The daily loop

| Skill | What it does |
|---|---|
| `/setup` | First-run onboarding. Writes `userdata/profile.md` + `CLAUDE.md`. |
| `/today` | Daily brief from your pipeline state. Saves to `userdata/outputs/`. |
| `/evaluate-position <url-or-paste>` | Score a job posting against your tier model. |
| `/job-search` | Weekly discovery sweep against your target titles + industries. |
| `/story-builder` | Maintain your universal STAR-story bank. |
| `/interview-prep <Company>` | Adapt stories for a specific upcoming interview. |
| `/interview-analysis` | Debrief from a pasted transcript. |
| `/pm-case-study` | Work on a PM take-home strategy memo. |

Reviewer agents (`cpo-reviewer`, `eng-manager-reviewer`, `design-manager-reviewer`, `interview-coach`, `tech-career-coach`) review case-study drafts on demand.

## What's in `userdata/example/`

A working install populated with a fictional persona — Maya Patel, a senior PM
in fintech. Browse `userdata/example/` to see what every file looks like
before running `/setup`.

## Audience + caveats

Designed for **senior PM / Head of Product** roles. The tier rubric, status
pipeline, and skills are tuned for that target. Different role family
(engineer, designer, marketer)? Fork it — the architecture is reusable, the
defaults aren't.

## Licence

MIT. See [LICENSE](../LICENSE).
