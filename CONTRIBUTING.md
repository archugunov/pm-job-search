# Contributing to pm-job-search

Thanks for taking a look. This plugin is small enough that contribution is mostly: file an issue, propose a fix, send a PR.

## What this plugin is for

Senior PM / Head of Product job searches. The tier rubric, status pipeline, story shape, and reviewer agents are tuned for that target. Different role family (engineer, designer, marketer)? Fork it — the architecture is reusable, the defaults aren't.

## Install for development

Clone, install as a Claude Code plugin pointing at your local checkout:

```bash
git clone https://github.com/archugunov/pm-job-search.git
cd pm-job-search
```

Then in any Claude Code workspace, install from your local path:

```
/plugin install <path-to-clone>/plugin
```

Or install from the published GitHub:

```
/plugin marketplace add https://github.com/archugunov/pm-job-search.git
/plugin install pm-job-search@pm-job-search
```

When developing, you'll want to test changes against the example installs in `userdata/examples/maya/` (full) and `userdata/examples/diego/` (skeletal). Maya stress-tests the rich-pipeline case; Diego stress-tests the missing-files case.

## Plugin shape

```
plugin/
├── .claude-plugin/
│   ├── plugin.json         # plugin manifest
│   └── marketplace.json    # marketplace manifest (lives at repo root, points at ./plugin)
├── skills/<name>/SKILL.md  # 7 skills
├── agents/<name>.md         # 5 agents
├── templates/               # profile / strategy / CLAUDE templates
├── TONE.md                  # voice + UX guidelines — read this before editing user-facing copy
└── README.md
```

The TONE.md file is the most important thing to read before submitting any change that touches user-facing text. It locks in voice (casual yet professional, simple language, direct asks) and the low-effort-first UX principle (auto-detect before asking, skip-and-fill-later always, defaults > prompts).

## Privacy hard rule

This repo must contain **zero personal data**. Before any PR, run:

```bash
rg -i 'arkadii|arcady|samokat|manychat|impress|delivery club|bookmate|skyeng|yandex|barcelona|reforge|MSU|kolmogorov|/Users/arkadii|673625|9452fc52|€80|€100|€110|€140' \
   --glob='!.github/' \
   --glob='!CONTRIBUTING.md' \
   .
```

Must return zero matches (exit code 1). The `.github/` and `CONTRIBUTING.md` exclusions are because both legitimately contain the blocklist as documentation (the CI workflow's rule + this file).

**CI enforces this** — every push to `main` and every PR runs the scan via `.github/workflows/privacy-check.yml`. PRs with privacy violations will not merge.

If you're forking for your own use, you'll inevitably add your own personal data to `userdata/` while you're using the plugin. That's fine — `userdata/` is gitignored except `userdata/examples/`. Don't open a PR with personal data in `userdata/` (or anywhere else); the CI will catch it. If you fork as a standalone for your own search, you can either replace the blocklist in the CI workflow with your own terms or delete that workflow.

## Testing changes

Two example installs exist for testing: `userdata/examples/maya/` (full — profile + strategy + journal + 2 companies + 2 stories + applications.md) and `userdata/examples/diego/` (skeletal — profile + strategy + 1 company + 1 story, no journal). When changing a skill, mentally trace its behaviour against both:

- Maya covers: rich pipeline, multiple companies in different statuses, two stories with frontmatter, fully populated install
- Diego covers: missing journal, missing applications.md, only 1 story (tests the "<3 stories in bank" branch), no `monitoring: true` companies

For larger spec changes, consider running through one of the multi-step skills (`/pm-job-search:setup` end-to-end, or `/pm-job-search:interview-prep <Company>` end-to-end) mentally and writing out what each step would produce.

## Commit messages

Lower-case, verb-first, scope-prefixed where it helps. Examples from the repo:

- `add /interview-prep skill`
- `/today: collapse tier-rubric YAML wall into 3 clean options`
- `career-coach: refactor strategy-reflection around user complaints`
- `tone: drop superlatives from career-coach proposed reframes`

Co-authored-by lines are welcome but not required.

## Issues

File issues for:
- Bugs in skill behaviour (output diverges from the SKILL.md spec)
- Spec gaps surfaced during real use (the behaviour is undefined for case X)
- TONE.md violations in user-facing copy
- Privacy gaps (a blocklist term needs to be added)

Please don't file issues for:
- Feature requests outside the senior-PM scope (fork it instead)
- Requests for the plugin to support other tools (Notion / Gmail / Calendar integrations are deliberately out of scope for v1 — see "Why pure markdown" in the README)

## License

MIT. Contributing code means you license your contribution under MIT. Author block stays generic ("pm-job-search contributors") rather than tracking individual contributors — fork attribution lives in git history.
