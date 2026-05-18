# pm-job-search dashboard

Status: design (approved by user 2026-05-18)
Implementation plan: docs/superpowers/plans/2026-05-18-dashboard.md

## Problem

Day-to-day pipeline operation in pm-job-search lives in two places: skills write canonical state to `userdata/companies/*/meta.md`, but the user keeps a separate Notion DB to actually *look at* the pipeline — drag cards between status columns, scan tier and last-activity at a glance, capture quick notes against a company. Two surfaces drift. Either Notion goes stale and stops being useful, or the user spends time mirroring state from md back into Notion by hand.

The user wants one surface. Markdown remains the source of truth, but a browser-based dashboard replaces Notion for daily operation. Pipeline view, quick notes, status changes, and new-company capture all happen there. Skills (`/today`, `/evaluate-position`, `/interview-prep`, etc.) keep running as before — they read and write the same md files.

## Scope

In scope:
- A new `/dashboard` skill that launches a local server and opens the browser.
- A React + Mantine single-page app that reads pipeline state, strategy targets, and the latest daily brief.
- Three writes from the dashboard: status change, timestamped note, new-company scaffold.
- A pre-built Vite bundle committed to the repo so plugin users install zero additional dependencies.
- A reference rebuild section in CONTRIBUTING.md for contributors who need to modify the dashboard.

Out of scope:
- Editing tier, score, or scoring rationale (those are `/evaluate-position`'s job).
- Editing date fields like `last_inbound` or `date_applied`.
- Editing `research-brief.md`, `interview-prep-*.md`, or `interview-debrief-*.md`.
- Re-implementing `/today`'s trigger logic in JavaScript. The dashboard renders the latest brief; it doesn't recompute it.
- Cross-platform desktop packaging (no Electron, no Tauri).
- Authentication, multi-user, or remote hosting.
- A query language à la Obsidian Dataview. The dashboard is opinionated about what it shows; users don't write queries.

## Design

### Three-zone layout

The browser shows a single page with three vertically-stacked zones, built entirely from default Mantine components. No hand-rolled CSS, no custom design tokens, no wrapper components introducing new spacing rules.

**Top zone — pipeline status.** A `<Group>` of `<Stack>` blocks. Left cluster: one `<Stack>` per active status (`Interviewing`, `Applied`, `Discovered`) showing count + label. Right cluster: weekly progress (`<Progress>` bar from Mantine) and days-to-target-offer countdown (computed against `strategy.md`'s `target_offer_date`).

The weekly progress bar shows count-vs-target for the largest single key in `strategy.md`'s `weekly_targets` map (typically `outreach` or `applications`, but the spec is target-agnostic — whichever field is largest wins the bar slot). Count is derived by globbing `userdata/companies/*/meta.md` + `userdata/companies/*/*/meta.md` and counting entries whose `date_added` (for outreach) or `date_applied` (for applications) falls within the current ISO week. Field-name matching is hard-coded: the bar's label matches the strategy.md key it's tracking.

**Middle zone — grouped applications table.** A `<SegmentedControl data={['Status', 'Tier']}>` toggle defaults to `Status`. Below it, a Mantine `<Accordion multiple>` where each `<Accordion.Item>` is a group. Each group's panel is a `<Table striped highlightOnHover>` with columns:

1. Tier — `<Badge color={tierColor}>P0</Badge>`
2. Company — bold text + secondary line for short status note (e.g. "recruiter 2d ago")
3. Position — plain text
4. Status — inline `<Select>` (`StatusSelect.tsx`) wired to the status-change endpoint
5. Last activity — relative date `<Text size="xs" c="dimmed">`
6. Actions — `<ActionIcon>` cluster: add-note (opens `<Drawer>`), open-in-editor (`vscode://` URL targeting the company's `meta.md`)

A `<Button leftSection={<IconPlus/>}>New company</Button>` sits to the right of the segmented control. Click opens `<NewCompanyModal>` (`TextInput` for company + position, `Select` for tier, `TextInput` for link, `Select` for status with `discovered` as default).

Multi-role companies surface as one row per discovered `meta.md`. A company with two positions appears as two rows. This matches the project's `(company, position)` dedup rule.

**Bottom zone — today's actions / heads-up.** A `<Paper p="md" withBorder>` containing the latest `userdata/outputs/daily-brief-*.md` rendered via `react-markdown` inside a `<TypographyStylesProvider>`. If no brief exists, an empty-state line: "No daily brief yet — run `/today`". If the latest brief is older than today, a `<Alert color="yellow">` line: "Last brief from {date} — run `/today` to refresh".

### Backend — Python stdlib HTTP server

`plugin/dashboard/serve.py` (~150-200 LOC) implements a minimal HTTP server using `http.server`, `json`, `os`, `pathlib`, `re`, `webbrowser` — all standard library. No `pip install` ever.

Server responsibilities:
- Pick a free port (start at 7890, increment until bind succeeds).
- Serve `plugin/dashboard/dist/` static assets (index.html + Vite-built JS/CSS bundles).
- Expose the REST API below.
- Open the user's default browser to `http://localhost:<port>`.
- Print the URL to stdout for the user to copy if the auto-open fails.
- Clean up cleanly on ctrl-C (SIGINT handler closes the socket).

CORS is not needed — same-origin (browser and API on the same `localhost:<port>`).

### REST API

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/state` | One fat read: all companies + strategy + latest brief. |
| `PATCH` | `/api/positions/<folder_path>/status` | Body: `{status}`. Rewrites `status:` in frontmatter. |
| `POST` | `/api/positions/<folder_path>/notes` | Body: `{note}`. Appends dated bullet to that position's `notes.md`. |
| `POST` | `/api/companies` | Body: `{company, position, tier, link, status}`. Creates folder + scaffolded `meta.md`. |

`<folder_path>` in the URL is the exact `folder_path` value returned by `/api/state` for that position (URL-encoded). For single-role companies it's `Plaid`; for multi-role it's `Stripe/lead-pm-growth`. One path shape for both layouts — no special-casing on the frontend.

**`position_slug` derivation rule.** Lowercase the position string, replace any run of non-alphanumeric characters with a single hyphen, trim leading/trailing hyphens. `"Senior PM, Consumer Credit"` → `"senior-pm-consumer-credit"`. `"Lead PM / Growth"` → `"lead-pm-growth"`. This is the rule the existing skills already use (per `/evaluate-position`'s migration logic) — the dashboard must match.

The `/api/state` response shape:

```json
{
  "companies": [
    {
      "company": "Plaid",
      "position": "Senior PM, Consumer Credit",
      "position_slug": "senior-pm-consumer-credit",
      "tier": "P0",
      "status": "interviewing",
      "score": 14,
      "link": "https://...",
      "date_added": "2026-04-22",
      "date_applied": "2026-04-25",
      "last_inbound": "2026-05-15",
      "monitoring": false,
      "folder_path": "Plaid",
      "is_multi_role": false
    }
  ],
  "strategy": {
    "target_offer_date": "2026-06-28",
    "weekly_targets": {"outreach": 7, "applications": 3}
  },
  "latest_brief": {
    "date": "2026-05-18",
    "markdown": "..."
  }
}
```

`folder_path` is the path relative to `userdata/companies/`. For single-role companies it's `<Company>`; for multi-role it's `<Company>/<position-slug>`. The frontend uses this to construct write URLs and `vscode://` open-in-editor links.

`is_multi_role` is true if the company has 2+ positions. Used for routing notes writes correctly (notes.md sits at the same depth as meta.md).

### Frontend stack and build

- **Framework:** React 18 + TypeScript.
- **Components:** Mantine v7. Use defaults. No custom theming beyond `defaultColorScheme="dark"`. No new tokens, spacing rules, or wrapper components.
- **Markdown rendering:** `react-markdown` + `remark-gfm`.
- **Icons:** `@tabler/icons-react` (Mantine's recommended pairing).
- **Bundler:** Vite.
- **Build artefact:** `plugin/dashboard/dist/` is committed to git. Users get static files; they never install Node or run a build.

Contributors who modify dashboard source run `cd plugin/dashboard && npm install && npm run build` and commit both source and `dist/` changes. CONTRIBUTING.md documents this.

### Write contracts

**Status change.** Read the file, locate the `status:` line inside the frontmatter (between the opening `---` and the next `---`), substitute the new value while preserving the original quoting style (`status: interviewing` stays bare; `status: "interviewing"` keeps double quotes; `status: 'interviewing'` keeps single quotes). Write to a tempfile in the same directory, `os.rename` to the target path. Atomic on POSIX (Mac, Linux). Other frontmatter fields untouched: key order preserved, comments preserved, blank lines preserved.

**Note append.** Notes for a position land in a `notes.md` file living alongside that position's `meta.md`. For a single-role company at `userdata/companies/Plaid/meta.md`, notes go to `userdata/companies/Plaid/notes.md`. For a multi-role company at `userdata/companies/Stripe/lead-pm-growth/meta.md`, notes go to `userdata/companies/Stripe/lead-pm-growth/notes.md`. Format appended:

```
## 2026-05-18 14:32

User's note text here.
```

Creates the file with a heading-style title (`# Notes — <Company> <Position>`) on first write.

**New company.** Validates that `(company, position)` is unique among all existing meta.md files. If unique, creates the folder (and parent if needed for multi-role layout) and writes a scaffolded `meta.md`:

```markdown
---
company: <Company>
status: <status>
tier: <Tier>
score: 0
position: <Position>
link: <URL>
date_added: <today>
---

# <Company>

(Scaffolded from dashboard on <today>. Run /evaluate-position for full scoring + research brief.)
```

If `(company, position)` already exists, returns 409 Conflict with a message the frontend surfaces in the modal.

### Multi-role folder layout

The project already supports two layouts for `companies/<Co>/`:
- **Flat:** single-role companies have `meta.md` directly inside the company folder.
- **Subfolder:** multi-role companies have `<position-slug>/meta.md` for each role.

Skills handle the flat→subfolder migration automatically (per the existing convention). The dashboard does NOT trigger this migration. If the user adds a second role to a flat-layout company via the dashboard:
- Server detects the existing flat-layout meta.md.
- Returns 409 Conflict with message: "Multi-role companies need the subfolder layout. Run `/evaluate-position` for this new role — it handles the migration."

The dashboard surfaces this clearly in the modal so the user knows where to go next.

### Data flow

On mount: `GET /api/state`. After every successful write: `GET /api/state` again. No partial updates, no optimistic merge logic beyond a brief "saving…" spinner on the affected row.

Total payload for a senior-PM-scale search (~30 active + closed companies) is small (~10-30KB). Per-resource endpoints add complexity for no UX win.

## Architectural fork (decided)

The dashboard is **a React + Mantine app built with Vite, served by a Python stdlib HTTP server**. The bundle (`dist/`) is committed to the repo so installation costs zero.

Rejected alternatives:
- **Vanilla JS + hand-rolled CSS.** Initial proposal. Rejected by user — UI feels off when you compose your own spacing/components rather than using a library's defaults.
- **shadcn/ui.** Rejected — shadcn's whole point is you own and customize components, which violates the "no new components, tokens, spacing rules" constraint.
- **CDN UMD Mantine + `htm`.** Considered for "no build" purity. Rejected — DX is awkward, no tree-shaking, will regret in 6 months as the dashboard grows.
- **File System Access API.** Considered to skip the server entirely. Rejected — Chromium-only and asks for folder permission every session.
- **Read-only HTML + writes via Claude Code commands.** Rejected — worst day-to-day UX; doesn't feel like a working tool.

Locked in: React + Mantine v7 + Vite + committed `dist/` + Python stdlib server.

## Risks / unknowns

- **Frontmatter rewrite preserving formatting.** Risk: a regex-based status rewrite could damage adjacent frontmatter (comments, multi-line values, unusual whitespace). Mitigation: the rewrite targets only the literal `status:` line via a line-anchored regex inside the frontmatter block; all other lines pass through unchanged. Covered by TDD.

- **Port conflicts.** Risk: 7890 is sometimes used. Mitigation: server tries ports 7890–7900 in order; fails with a clear message if all are taken.

- **`dist/` drift from `src/`.** Risk: a contributor edits source but forgets to rebuild and commit `dist/`. Mitigation: a CI check that runs `npm run build` and diffs against the committed `dist/`; PRs fail if they disagree. (Same pattern as the privacy-check workflow.)

- **Bundle size with Mantine.** Mantine is feature-heavy. Mitigation: import from `@mantine/core` selectively, rely on Vite tree-shaking. Target: `dist/` under 500KB gzipped. If we miss it materially, revisit.

- **`vscode://` URL on non-VS-Code editors.** Risk: users on JetBrains, Cursor, Zed don't get the open-in-editor jump. Mitigation: fall back to a "copy path" action if `vscode://` doesn't resolve. Out of scope to detect editor; we provide both.

- **Server doesn't terminate on browser tab close.** Expected: user keeps the tab open while working, then ctrl-C the terminal when done. Document this in the skill.

- **First-run install size.** Committing `dist/` adds ~100-300KB to the repo. Acceptable for the install-time DX win. Smaller than most node_modules artefacts users have grown to tolerate.

## Verification

1. **Privacy scan clean.** The repo's `rg` blocklist scan (the one enforced by `.github/workflows/privacy-check.yml`) runs against all new files (serve.py, src/, dist/) and returns zero hits. CI privacy-check workflow passes.

2. **Cold-start launch.** Fresh `/dashboard` invocation on Maya's example install: server starts, browser opens to `localhost:<port>`, three zones render, table groups by Status by default, status counts match what's in Maya's `meta.md` files.

3. **Read parity.** Compare /api/state's `companies` array against a `grep -l meta.md userdata/companies/` count — every meta.md is represented exactly once. Multi-role companies in Maya's install (if any) surface as multiple rows.

4. **Status change round-trip.** Change Plaid's status from `interviewing` to `rejected` via the dropdown. Refresh the page. Status persists. `cat userdata/companies/Plaid/meta.md` shows `status: rejected` with all other frontmatter unchanged (key order, comments, blank lines preserved).

5. **Note append round-trip.** Add a note to Plaid via the drawer. `cat userdata/companies/Plaid/notes.md` shows the note under a `## YYYY-MM-DD HH:MM` heading. Add a second note; both present, ordered.

6. **New company creation.** Add "Lendable / Senior PM Underwriting / P1" via the modal. New folder + meta.md scaffolded with correct frontmatter. Reload: row appears in `Discovered` group.

7. **New company conflict.** Try to add a duplicate `(company, position)`. Modal surfaces 409 message clearly. No file written.

8. **Multi-role conflict surfacing.** On a flat-layout company, attempt to add a second position. Modal shows the migration message pointing at `/evaluate-position`. No file written.

9. **Bottom-zone states.** With today's brief present → renders. With no brief → empty-state message. With a brief from 2 days ago → yellow alert + render the stale brief.

10. **Port conflict handling.** Manually bind port 7890 first, then run `/dashboard`. Server picks 7891 (or next free), prints the URL.

11. **Atomic write under interrupt.** Mid-write, simulate process kill (`kill -9` during write). Target meta.md is either old-state or new-state, never partial. Tempfile cleaned up on next run.

12. **Build determinism.** `cd plugin/dashboard && npm install && npm run build` produces a `dist/` that matches the committed one (or differs only in expected build-id strings). CI check enforces this.

## Files to be created or modified

NEW:
- `plugin/skills/dashboard/SKILL.md` — `/dashboard` skill spec.
- `plugin/dashboard/serve.py` — Python stdlib HTTP server.
- `plugin/dashboard/tests/test_serve.py` — pytest tests for serve.py's pure functions (frontmatter parse, status rewrite, slug derivation, glob, atomic write). Pytest is dev-only (CI), not an install-time dep.
- `plugin/dashboard/package.json` — React + Mantine + Vite + react-markdown + tabler-icons.
- `plugin/dashboard/vite.config.ts`
- `plugin/dashboard/tsconfig.json`
- `plugin/dashboard/index.html` — Vite entry.
- `plugin/dashboard/src/main.tsx` — Mantine provider, dark scheme default.
- `plugin/dashboard/src/App.tsx` — three-zone shell.
- `plugin/dashboard/src/api.ts` — typed fetch wrappers.
- `plugin/dashboard/src/types.ts` — TypeScript types matching the API contract.
- `plugin/dashboard/src/components/PipelineStats.tsx`
- `plugin/dashboard/src/components/ApplicationsTable.tsx`
- `plugin/dashboard/src/components/StatusSelect.tsx`
- `plugin/dashboard/src/components/NewCompanyModal.tsx`
- `plugin/dashboard/src/components/NoteDrawer.tsx`
- `plugin/dashboard/src/components/TodaySection.tsx`
- `plugin/dashboard/dist/` — committed Vite build output (index.html + assets/).
- `plugin/dashboard/README.md` — short note pointing at this spec + the rebuild command.
- `.github/workflows/dashboard-build-check.yml` — CI workflow that runs `npm run build` and diffs against committed `dist/`.

MODIFY:
- `README.md` + `plugin/README.md` — add `/dashboard` to the skills table; add a "Visual dashboard" section under "How it works".
- `CONTRIBUTING.md` — add a "Modifying the dashboard" section with the `npm install && npm run build` flow and the "always commit `dist/`" rule.
- `.gitignore` — add `plugin/dashboard/node_modules/` (and confirm `plugin/dashboard/dist/` is NOT ignored).
- `plugin/TONE.md` — one-line note that the dashboard uses Mantine defaults without custom theming, mirroring the markdown-first low-friction principle in visual form.

## Implementation pipeline (superpowers patterns)

The spec is sized to be executed via `superpowers` patterns, not as a one-shot session. Pipeline:

1. **This spec → user-approved.**
2. **`superpowers:using-git-worktrees`** — create `feat/dashboard` branch in a worktree off main, so node_modules + dist build artefacts don't contaminate the main checkout.
3. **`superpowers:writing-plans`** — produces a plan at `docs/superpowers/plans/2026-05-18-dashboard.md` structured around the slices below.
4. **`superpowers:subagent-driven-development` + `superpowers:dispatching-parallel-agents`** — execute slices in waves.
5. **`superpowers:test-driven-development`** — for the Python server's pure functions (frontmatter parse, status rewrite, slug derivation, atomic write, glob across flat + subfolder layouts).
6. **`superpowers:verification-before-completion`** — actually launch `/dashboard` against Maya's install, exercise every verification step above, run privacy-check + dashboard-build-check CI workflows locally before claiming done.

### Independent slices for parallel dispatch

| Slice | Files | Depends on | Can start when |
|---|---|---|---|
| A — Python API server | `serve.py`, `tests/test_serve.py` | This spec (API contract) | Wave 1 |
| B — Vite + Mantine app shell | `package.json`, `vite.config.ts`, `tsconfig.json`, `index.html`, `src/main.tsx`, `src/App.tsx`, `src/api.ts`, `src/types.ts` | This spec | Wave 1 |
| C — Table + writes UI | `ApplicationsTable`, `StatusSelect`, `NewCompanyModal`, `NoteDrawer` | Slice B's shell + types | Wave 2 |
| D — Top + bottom zones | `PipelineStats`, `TodaySection` | Slice B's shell + types | Wave 2 |
| E — `/dashboard` SKILL.md | `plugin/skills/dashboard/SKILL.md` | Slice A runnable | Wave 2 |
| F — Docs, privacy, CI, build-check | `README.md`, `CONTRIBUTING.md`, `.gitignore`, `TONE.md`, `dashboard-build-check.yml`, commit `dist/` | All other slices | Wave 3 |

Wave 1 (parallel): A, B.
Wave 2 (parallel): C, D, E.
Wave 3: F (also runs the build that produces the committed `dist/`).

## Ship cadence

Single PR. The slices are coupled by the API contract and the committed `dist/` is meaningful only when all source slices are in place. Splitting into per-slice PRs would mean intermediate states where the API exists but no UI consumes it, or the UI exists but `/dashboard` can't launch it. One reviewable PR off the `feat/dashboard` branch.
