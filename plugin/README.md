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

Reviewer agents (`cpo-reviewer`, `eng-manager-reviewer`, `design-manager-reviewer`, `interview-coach`, `tech-career-coach`) review any draft on demand — stories, research briefs, outreach messages, take-home assignments.

## What's in `userdata/examples/`

Two fictional personas pre-populated so you can see what a working install
looks like before running `/setup`:

- **`userdata/examples/maya/`** — Maya Patel, senior PM in London consumer
  credit / fintech. Full install: profile, strategy, journal, two companies
  (one interviewing, one rejected), one story with adaptation angles,
  generated index.
- **`userdata/examples/diego/`** — Diego Alvares, VP Product in Mexico City
  applying for fully-remote US roles. Skeletal install (profile, strategy,
  one company, one story) — there to stress-test the schema against USD
  compensation, no anchor city, US English, B2B SaaS vertical.

Both personas are entirely fictional.

## Audience + caveats

Designed for **senior PM / Head of Product** roles. The tier rubric, status
pipeline, and skills are tuned for that target. Different role family
(engineer, designer, marketer)? Fork it — the architecture is reusable, the
defaults aren't.

## Licence

MIT. See [LICENSE](../LICENSE).
