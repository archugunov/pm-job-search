# Integrations — wiring external tools into pm-job-search

The plugin works as-is — markdown only, zero external dependencies. This guide is for users who already run other MCP servers (Granola, Gmail, Calendar, Notion, Playwright) and want to wire them into specific skills to make them more capable. **None of these are required.** The plugin does not auto-detect or auto-install any of them.

## Quickstart — `/pm-job-search:integrations`

For the three integrations that plug into the daily/weekly loop (Granola, Calendar, Gmail), the easiest path is `/pm-job-search:integrations`. It probes which MCPs are installed, walks through wiring each available one with at most 1-2 questions, and saves customized invocation patterns to `userdata/integrations.md` for copy-paste later. Re-run anytime to refresh detection or add newly-installed MCPs.

The remaining three integrations below (Notion, Playwright, Slack) stay manual-setup — read the section, apply the pattern. They sit outside the daily loop so a guided skill would be more ceremony than value.

Why even document this? Two reasons:
1. The "zero deps" pitch sometimes meets the "but I have my interview transcripts in Granola already" objection. This guide shows the upgrade path without forcing it on default users.
2. MCPs already running on the user's machine ARE effectively zero-setup from the plugin's perspective — they're just tools the agents can use. The original "zero deps" rule was about installation friction, not about refusing to USE servers the user already trusts.

## How to think about integrations

Each integration is a **prompt pattern** more than a code change. You don't edit the plugin. You invoke a skill with a specific prompt that tells Claude to pull from the MCP. Example:

> "Find the most recent Granola meeting for Plaid and use it as the transcript for `/pm-job-search:interview-analysis`."

Claude reads that, calls the Granola MCP to fetch the meeting, then runs `/pm-job-search:interview-analysis` with the result. No plugin code touches Granola directly; the user-level intent does.

The format below documents 6 useful integrations. Each section follows the same shape:

1. **Use case** — what it adds, in plain English
2. **MCP** — install reference (or "doesn't exist yet — closest equivalent")
3. **Example invocation** — verbatim what the user types
4. **Where it plugs in** — which skill, which step
5. **Privacy / ToS** — what to be aware of
6. **Fallback if MCP unavailable** — what the plugin still does

---

## 1. Granola — meeting transcripts straight into `/interview-analysis`

**Use case.** Instead of pasting an interview transcript (or pointing `--from-file` at a download), let `/pm-job-search:interview-analysis` pull it directly from Granola. Saves the copy-paste step + keeps the transcript source-of-truth in Granola while the structured debrief lands in `userdata/companies/<Co>/`.

**MCP.** Granola's official MCP (see Granola docs for current install link). Typical tools exposed: `query_granola_meetings`, `get_meeting_transcript`, `list_meetings`.

**Example invocation:**

> "Find my most recent Granola meeting that mentions Plaid in the title or attendees. Use it as the transcript for `/pm-job-search:interview-analysis Plaid --stage cpo-round`."

Claude calls the Granola MCP to fetch the matching meeting, extracts the transcript, then invokes `interview-analysis` with the transcript as inline content.

**Where it plugs in.** `/pm-job-search:interview-analysis` step 1 (transcript source). The skill's existing flow handles everything from there.

**Privacy / ToS.** Granola transcripts contain the full meeting audio's text. They live in Granola already; pulling into the plugin moves a copy through Claude's context window during the run. The structured debrief (what landed / what didn't / signals / recommendations) ends up in `userdata/companies/<Co>/interview-debrief-<date>-<stage>.md` — verbatim quotes from the transcript will be in there. If you sync `userdata/` to git or anywhere shared, those quotes go with it.

**Fallback if MCP unavailable.** `/pm-job-search:interview-analysis` accepts a pasted transcript or `--from-file <path>` to a local file. No degradation in skill quality; you just paste manually.

---

## 2. Gmail (or any inbox MCP) — extract recruiter conversations into `journal.md`

**Use case.** Recruiters mostly talk over email. Manually copying that context into `journal.md` is friction the plugin doesn't catch. With a Gmail (or generic inbox) MCP, the user can periodically pull recent recruiter touch-points into journal entries — which then feed into `/today`'s `last_inbound` updates + outreach-count tracking + stale-applied warnings.

**MCP.** Look for a Gmail MCP supporting read + search. Tools typically named like `search_emails`, `get_email`. Most general inbox MCPs work — Outlook, Fastmail, etc. — as long as they expose read+search.

**Example invocation:**

> "Search my Gmail for the last 7 days of emails from any address containing 'recruiter', 'talent', or '@<company-domain>'. Summarise each in one line and append a new dated entry to `userdata/journal.md`."

Claude calls the inbox MCP, summarises, writes to journal. The journal entries then power `/today`'s warm-outreach count + the `last_inbound` updates the user does manually on company meta.md files (or asks Claude to do).

**Where it plugs in.** Upstream of `/today` (journal feeds the warm-outreach count) and `/evaluate-position` (recruiter context informs the score). Not a direct skill modification — the user runs it as a pre-flight before `/today`.

**Privacy / ToS.** Reading personal email through any MCP means email contents pass through Claude's context. Be deliberate about which queries you run; the search filters above scope it to recruiter conversations, but a too-broad query reads more than you'd want. Gmail's ToS allows authenticated API access; check your MCP's auth model.

**Fallback if MCP unavailable.** Maintain `journal.md` by hand — append a `## YYYY-MM-DD` heading every day or two and jot what happened. `/today` already keyword-scans last 7 days for outreach signals; the manual journal works fine.

---

## 3. Calendar (gcal MCP / ical) — upcoming interviews surfaced in `/today`

**Use case.** `/today`'s heads-up section already shows late-stage interview prompts for any company with `status: interviewing` AND `last_inbound` within 7 days. With a calendar MCP, you can additionally surface SPECIFIC scheduled interviews for the next 14 days — "you have Plaid CPO round Wed 14:00, Bark intro Thu 11:00" — without the user maintaining a separate file.

**MCP.** A Google Calendar MCP (search "gcal MCP" for current options) or any iCal-format reader.

**Example invocation:**

> "Before running `/pm-job-search:today`, check my calendar for the next 14 days. List any event whose title contains a company name from `userdata/companies/*/meta.md` or the words 'interview', 'recruiter', 'screen', 'round'. Pass that list into the today brief as additional heads-up context."

`/today` doesn't natively know about your calendar. With this pattern, the user injects the calendar list as preamble — Claude folds it into the heads-up section organically.

**Where it plugs in.** Pre-flight to `/pm-job-search:today`. Doesn't change the skill spec; the user just provides extra context via natural language.

**Privacy / ToS.** Calendar access reads all events in the queried range. Be specific about the date window. The plugin doesn't persist calendar data anywhere; it's used in-conversation only.

**Fallback if MCP unavailable.** Maintain a `next_event` (or similar) field on company meta.md manually — `next_event_date: 2026-06-15`, `next_event: cpo-round`. `/today` doesn't currently parse this but a future spec extension easily could. Or just rely on the existing late-stage-interview-prompts logic.

---

## 4. Notion — sync companies as Notion DB rows

**Use case.** Some users want their pipeline visible as a Notion board (kanban view, calendar view, etc.) ALONGSIDE the markdown files. The plugin's source-of-truth stays as `userdata/companies/*/meta.md`; Notion becomes a derived view for visual scanning.

**MCP.** Notion's official MCP. Tools typically: `notion-create-pages`, `notion-update-data-source`, `notion-search`.

**Example invocation:**

> "Read every `userdata/companies/*/meta.md` and `userdata/companies/*/*/meta.md` file. For each, upsert a row in my Notion database `<DB-ID>` with columns matching the meta.md frontmatter (company, position, status, tier, link, dates). Use the company+position pair as the unique key."

The user runs this on demand — daily, weekly, whenever they want the Notion view refreshed. The plugin doesn't auto-sync; the markdown source stays canonical.

**Where it plugs in.** Read-only derivative of `userdata/companies/`. Doesn't change any skill behaviour. If the user edits in Notion, those edits don't propagate back unless they explicitly tell Claude to sync the other direction (which is fragile — recommend treating Notion as read-only).

**Privacy / ToS.** Notion DB lives in the user's workspace. Personal info in meta.md (company names, salary discussions in fit_note) ends up there. Notion's own ToS applies.

**Fallback if MCP unavailable.** The plugin's `userdata/outputs/applications.md` already provides a markdown-rendered pipeline table view. Less interactive than Notion but no setup required.

---

## 5. Playwright (browser MCP) — link liveness check + interviewer research

**Use case (already supported by `/job-search`):** verify JD URLs are still live during the discovery sweep. Already documented via the `--with-playwright` flag in `/pm-job-search:job-search`. The skill detects whether the MCP is installed and uses it; otherwise tags candidates `link_verified: false` and the user verifies manually.

**Use case (new):** interviewer research. Given a LinkedIn URL (the user pastes — Playwright can navigate but the user has to provide the URL), summarise the interviewer's background, prior hires, recent posts. Surfaces what kind of questions they tend to ask + which proof points to lead with.

**MCP.** Playwright MCP — see plugin marketplaces for current install.

**Example invocation (interviewer research):**

> "Use Playwright to navigate to <linkedin-URL>. Summarise their background, current role, prior roles, recent posts (if visible). What kind of PM hire would this person make? Save the summary to `userdata/companies/<Company>/interviewer-<name>-<date>.md`."

**Where it plugs in.** New workflow — sits alongside `/pm-job-search:interview-prep`. The user runs it before a round when they've been told who'll be interviewing them. The output file lives in the company folder + can be referenced in subsequent prep doc generation.

**Privacy / ToS.** LinkedIn's ToS prohibits automated scraping. Playwright navigation as a logged-in user reading individual profiles is in a gray area — different lawyers will say different things. Personally use at your own risk; never automate broad scrapes. The plugin's spec doesn't condone or require this; this guide just documents the pattern for users who already use Playwright for personal research.

**Fallback if MCP unavailable.** Read the LinkedIn profile manually, paste the relevant facts (background, prior roles, what they post about) into chat, ask Claude to summarise + suggest prep adjustments. Same outcome, more typing.

---

## 6. Slack (or Telegram, Discord, etc.) — pipe `/today` digest to a channel

**Use case.** Self-accountability via public visibility. The user pipes their daily `/today` brief into a private Slack channel that an accountability partner can see. Catches the weeks where the user stops running `/today` at all.

**MCP.** Any Slack MCP exposing message-send. Telegram and Discord MCPs work the same way; this section uses Slack as the example.

**Example invocation:**

> "Run `/pm-job-search:today`. Take the resulting brief and post it to my Slack channel `#job-search-accountability` as a single message. Strip the `# /today —` heading; lead with the date as plain text."

The user could chain this — set up a daily reminder in their calendar that triggers `Run today + post to Slack` — but that's a self-discipline pattern, not a plugin feature.

**Where it plugs in.** Downstream of `/pm-job-search:today`. The brief is generated normally; this just routes a copy somewhere visible.

**Privacy / ToS.** The brief contains pipeline state — company names, statuses, salary aspirations, anti-goals. Don't pipe it to any channel you don't control. A 1-1 DM with your accountability partner is the typical pattern.

**Fallback if MCP unavailable.** Manually copy the brief into wherever you want it. Or just commit to running `/today` every morning without external accountability.

---

## Writing your own integration

If you want to wire in a tool not listed above, the pattern is:

1. **Identify the skill the integration enhances.** Read its SKILL.md and find the step where external data would help (e.g. `/interview-analysis` step 1 = transcript source).
2. **Pick an MCP that exposes the data.** Search the Claude Code MCP marketplaces for what's available. If nothing exists, you can write your own MCP server — see [Claude Code MCP docs](https://docs.claude.com/claude-code) for the protocol.
3. **Document the invocation pattern.** It's almost always "Before running /skill, fetch X from MCP and pass it in as Y context." The plugin doesn't need code changes for this — the user's prompt threads the integration through.
4. **Add a privacy / ToS note** for yourself + anyone you share the pattern with.

If you build an integration pattern that works well, consider PR-ing this file to add a section for it. See [CONTRIBUTING.md](../CONTRIBUTING.md) for the contribution shape.

## What the plugin will NEVER do

To stay sharp, here's what's out of scope even with MCPs available:

- **Auto-poll / background sync.** Plugins don't have a persistent process. If you want the calendar checked every morning, you set up a cron / reminder yourself; the plugin doesn't run unattended.
- **Direct ATS integration as a default.** `/job-search` already uses Ashby/Greenhouse/Lever public APIs for monitoring recheck (no auth needed). Beyond those, ATS-specific integrations stay user-driven.
- **Email sending.** Read-only is the line. If you want outreach automation, that's a different tool.
- **CRM-style contact management.** People mentioned in journal.md or company meta.md are notes for you; the plugin won't build a contact graph.
