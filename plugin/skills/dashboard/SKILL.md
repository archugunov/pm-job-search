---
name: dashboard
description: This skill should be used when the user asks to "/dashboard", "open the dashboard", "show me my pipeline visually", "launch the dashboard", or wants a browser-based view of their job-search pipeline. Launches a local Python server that serves a React + Mantine SPA reading from `userdata/companies/*/meta.md`, `userdata/strategy.md`, and the latest `userdata/outputs/daily-brief-*.md`. Supports inline status changes and timestamped notes per company. New positions are created via `/pm-job-search:evaluate-position <link>`, not from the dashboard itself. The dashboard reads and writes the same md files all other skills use — markdown remains the source of truth.
---

# /dashboard

Launches the pm-job-search visual dashboard.

## What it does

1. Starts a local Python server (`plugin/dashboard/serve.py`) on port 7890 (or the next free port up to 7900).
2. Opens the user's default browser to `http://localhost:<port>`.
3. Prints the URL to chat so the user can copy it if auto-open fails.
4. Waits in the foreground until the user hits ctrl-C.

The dashboard provides:
- A top status bar showing pipeline counts, weekly progress vs `strategy.md` targets, and days-to-target-offer countdown.
- A grouped applications table (toggle Status / Tier) with inline status dropdowns; click any row to open the notes drawer.
- A bottom panel rendering the latest `daily-brief-*.md` (with a stale-brief banner when older than today).
- To add a new position: run `/pm-job-search:evaluate-position <link>` in Claude Code. The dashboard does not write new positions itself.

## When to invoke

- User types `/dashboard`.
- User asks to "open the dashboard", "show me my pipeline", "launch the visual view".
- User wants to do bulk pipeline maintenance (status sweeps, quick notes against several companies).

## How to invoke

The skill runs one shell command:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/dashboard/serve.py" --userdata "$(pwd)/userdata"
```

`${CLAUDE_PLUGIN_ROOT}` resolves to the plugin install directory. `$(pwd)` resolves to the user's workspace root (the dir containing `userdata/`).

If the user is running this from somewhere other than their workspace root, ask for the workspace path and pass it explicitly: `--userdata <path>/userdata`.

## Failure modes and what to do

- **Bundle missing** (`error: dashboard bundle not found`). The plugin's `dist/` is not committed or got deleted. Tell the user to reinstall the plugin; this should not happen in a clean install.
- **Port range exhausted** (`error: no free port in 7890-7899`). Something else is using all ten ports. Suggest `--port 7900` (or higher) explicitly.
- **userdata not found**. The user is in the wrong directory. Ask for the workspace path.

## What this skill does NOT do

- Does not modify md files itself — all writes go through the dashboard's REST API, which uses atomic file writes.
- Does not run `/today`, `/evaluate-position`, or any other skill. The dashboard renders the latest brief; it doesn't recompute it.
- Does not handle authentication, multi-user, or remote access. Local-only.
- Does not add Python dependencies. Server uses stdlib only.

## Tone

Match plugin/TONE.md: low-effort, terse, no marketing voice. When announcing the URL, say it once and stop talking.
