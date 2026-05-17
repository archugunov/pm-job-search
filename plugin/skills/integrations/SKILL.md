---
name: integrations
description: This skill should be used when the user asks for "/integrations", "/pm-job-search:integrations", "wire up integrations", "set up Granola", "connect my calendar", "connect Gmail", "what integrations can I use", or asks how to make the plugin pull from external tools. Probes which of the three MCP-based integrations (Granola, Calendar, Gmail) are installed, walks through wiring each available one in with at most 1-2 config questions per integration, and writes the customized invocation patterns to userdata/integrations.md so the user can paste them into /today, /interview-analysis, and journal updates anytime.
---

# /integrations — wire MCP-based integrations into the daily loop

Probes the user's installed MCPs for the three high-value integrations documented in `${CLAUDE_PLUGIN_ROOT}/INTEGRATIONS.md` (Granola → `/interview-analysis`, Calendar → `/today`, Gmail → `journal`), reports what's available, walks the user through wiring each one in with minimal config, and saves the customized invocation patterns to `userdata/integrations.md`.

**Voice:** every prompt, status line, and saved invocation pattern follows `${CLAUDE_PLUGIN_ROOT}/TONE.md`. Apply the low-effort-first principle — probe before asking, offer defaults, accept skip on every question, stop the moment value is delivered.

The other three integrations in INTEGRATIONS.md (Notion, Playwright, Slack) stay manual-setup — the user reads INTEGRATIONS.md and applies them directly. This skill covers the three that plug into the daily/weekly loop.

## Inputs

No required arguments. Optional flag:

- `--refresh` — re-probe and rewrite `userdata/integrations.md` even if it already exists. Default behaviour: if `userdata/integrations.md` exists, show what's wired and ask whether to refresh, add new integrations only, or exit.

## Flow

1. **Probe** each of the three MCPs.
2. **Report** detection results in a compact table.
3. **Wire** each available integration via a per-integration sub-flow (1-2 questions max).
4. **Write** `userdata/integrations.md` with the customized invocation patterns.
5. **Close** with 2-4 example invocations the user can copy-paste.

## Probe step

Probe order: Granola → Calendar → Gmail. Each probe attempts a safe, read-only call. The skill must NOT ask the user "do you have <MCP>?" before probing — detect first.

### Granola

Attempt: any `mcp__granola__*` tool that returns metadata cheaply (e.g. `mcp__granola__get_account_info` or `mcp__granola__list_meeting_folders`). If the call succeeds, mark `wired`. If the tool isn't available (no `mcp__granola__*` tools surface in the deferred-tool list), mark `not_installed`.

### Calendar

Calendar MCPs vary by vendor — there's no canonical name. Probe order:

1. Search the deferred-tool list for any tool matching `mcp__*gcal*__*`, `mcp__*calendar*__*`, `mcp__*google_calendar*__*`. If exactly one match: use it. Mark `wired` and store the detected tool prefix.
2. If multiple matches: list them in chat, ask the user which one they want to wire (max one question).
3. If zero matches: mark `not_installed`.

If a matching tool exists but returns an auth error on the probe call, mark `installed_but_unauthed` and tell the user: `Calendar MCP detected (<name>) but not authenticated. Run its auth flow first, then re-run /pm-job-search:integrations.`

### Gmail

Same approach as Calendar. Probe order:

1. Search for `mcp__*gmail*__*`, `mcp__*inbox*__*`, `mcp__*email*__*`.
2. If exactly one match: use it. Multiple: ask. Zero: mark `not_installed`.
3. Auth errors → `installed_but_unauthed`.

## Report step

After probing, print a compact table:

```
Integration detection — <YYYY-MM-DD>

| MCP       | Status                 | What it adds                                |
|---        |---                     |---                                          |
| Granola   | ✅ wired               | Interview transcripts → /interview-analysis |
| Calendar  | ✅ wired (mcp__gcal_x) | Upcoming interviews → /today heads-up       |
| Gmail     | ❌ not detected         | Recruiter convos → journal (manual fallback works) |
```

For any `not_installed` row, append a one-line pointer: `See INTEGRATIONS.md §<N> for install link.`

If zero MCPs detected, close gracefully: `None of the three integrations are wired. INTEGRATIONS.md has install links for each. Re-run /pm-job-search:integrations once any of them are installed.` Don't write integrations.md.

## Wiring step

For each `wired` (or `installed_but_unauthed` after auth-fix) integration, run the matching sub-flow. Maximum 1-2 questions per integration. Always offer defaults the user can accept with a single keystroke.

### Granola wiring

No config questions needed. The invocation pattern is generic: it takes `<Company>` and `<stage>` at invocation time.

Saved pattern:

```
"Find the most recent Granola meeting where the title or attendees mention <Company>.
Use it as the transcript for /pm-job-search:interview-analysis <Company> --stage <stage>."
```

### Calendar wiring

One question. Default offered:

> `Calendar heads-up scan for /today — include events whose title contains: interview, recruiter, screen, round, intro call, plus any company name from userdata/companies/*/meta.md. Accept default, add keywords, or skip?`

If the user accepts the default or adds keywords, save the customized pattern. If they skip, mark Calendar as `detected_but_not_wired` and move on.

Saved pattern (with placeholders for keywords and the detected tool prefix):

```
"Before running /pm-job-search:today, use <detected-mcp-tool> to list events in
the next 14 days whose title matches any of: <keyword-list>, OR contains a
company name from userdata/companies/*/meta.md. Pass that list into /today as
additional heads-up context."
```

### Gmail wiring

One question. Default offered:

> `Recruiter-scan filter for journal updates — match emails from addresses containing 'recruiter' or 'talent', plus any subject containing 'opportunity', 'role at', or a company name from userdata/companies/*/meta.md. Accept default, refine, or skip?`

If accepted/refined, save. If skipped, mark `detected_but_not_wired`.

Saved pattern:

```
"Search my Gmail for the last 7 days using filter: <filter-string>. Summarise
each match in one line and append a new dated entry to userdata/journal.md."
```

## Write step

Write `userdata/integrations.md` with this structure. If the file exists and the user chose to refresh, overwrite. If they chose "add new only", merge by integration name (keep existing user-customized invocation patterns; add new integration sections that weren't there before).

```markdown
# integrations

Last detected: <YYYY-MM-DD>. Re-run `/pm-job-search:integrations` to refresh.

## granola — <status>
**Used by:** /interview-analysis
**Tool prefix:** mcp__granola__
**Invocation pattern (copy + fill in placeholders when invoking):**
> "Find the most recent Granola meeting where the title or attendees mention <Company>. Use it as the transcript for /pm-job-search:interview-analysis <Company> --stage <stage>."

## calendar — <status>
**Used by:** /today (heads-up — upcoming interviews)
**Tool prefix:** <detected-prefix>
**Keywords:** <keyword-list>
**Invocation pattern:**
> "Before running /pm-job-search:today, use <tool-prefix> to list events in the next 14 days whose title matches any of: <keywords>, OR contains a company name from userdata/companies/*/meta.md. Pass that list into /today as additional heads-up context."

## gmail — <status>
**Used by:** journal updates (warm-outreach signal for /today)
**Tool prefix:** <detected-prefix>
**Filter:** <filter-string>
**Invocation pattern:**
> "Search my Gmail for the last 7 days using filter: <filter-string>. Summarise each match in one line and append a new dated entry to userdata/journal.md."
```

For each integration that's `not_installed` or `detected_but_not_wired`, render a short stub section instead of the full pattern:

```markdown
## <name> — not_installed
See `${CLAUDE_PLUGIN_ROOT}/INTEGRATIONS.md` §<N> for install link.
```

## Closing summary

Show 2-4 example invocations the user can paste, drawn from the integrations that were wired. Per TONE.md: stop after value is delivered, no upsells.

Example output when Granola + Calendar wired, Gmail not:

```
Wired up. Saved to userdata/integrations.md.

You can now say:
- "pull today's Granola meeting for Plaid into /pm-job-search:interview-analysis --stage cpo-round"
- "before running /pm-job-search:today, check my calendar for the next 14 days"

Gmail wasn't detected — INTEGRATIONS.md §2 has install pointers for when you want it.
```

## Hard rules

- Detect before asking. Never ask "do you have <MCP>?" — probe first, ask only if probing is genuinely ambiguous (multiple matching MCPs for the same slot).
- One question per integration maximum (except disambiguation). Offer a default that accepts in one keystroke.
- Save the user's invocation customizations verbatim — don't paraphrase what they specified.
- Idempotent. Re-running the skill must not destroy user-customized invocation patterns unless they explicitly choose `--refresh`.
- If `userdata/integrations.md` already exists, present three options and act on the chosen one: refresh (overwrite) / add-new-only (merge) / exit (no changes).

## Anti-patterns

- Do NOT modify `/today`, `/interview-analysis`, or `/journal` flows to auto-inject integration data. The user pastes the invocation patterns into chat when they want them; auto-injection is out of scope for this skill (v2 candidate).
- Do NOT cover Notion, Playwright, or Slack. Those stay in `INTEGRATIONS.md` as manual-setup. Scope creep across all 6 MCPs would make the skill heavier than the manual approach.
- Do NOT auto-install any MCP. Skills cannot install MCPs; that's a user action via `/plugin` or their config. Always point at INTEGRATIONS.md for install steps.
- Do NOT save MCP credentials, OAuth tokens, or auth state anywhere in `userdata/`. The MCP itself handles auth; this skill is invocation-pattern bookkeeping only.

## File outputs

- `userdata/integrations.md` — the customized invocation patterns + detection status. Single file, overwritten on refresh.

## See also

- `${CLAUDE_PLUGIN_ROOT}/INTEGRATIONS.md` — full prompt-pattern reference covering all 6 integrations (the three this skill wires + Notion, Playwright, Slack as manual-setup).
- `${CLAUDE_PLUGIN_ROOT}/TONE.md` — voice + low-effort-first rule.
