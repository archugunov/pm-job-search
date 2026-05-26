---
name: test-personas
description: Internal test harness for plugin maintainers. End users should not invoke this. Runs synthetic personas through critical journeys against the plugin and produces LLM-judge findings reports. Trigger words "/test-personas", "run the test harness", "test the plugin end-to-end", "run the test personas".
---

# /test-personas — maintainer-only end-to-end test orchestrator

**Audience:** plugin maintainers only. Do NOT invoke if you are an end user running a real job search — this clobbers `userdata/` from a test snapshot.

## What this skill does

For each `(persona × journey)` pairing requested, runs five phases:

1. **Snapshot reset** — `rsync` a clean snapshot into `userdata/`.
2. **Schema validation** — verify the snapshot matches current plugin expectations.
3. **Conversation loop** — orchestrate two sub-agents (plugin-under-test + user-simulator) until termination.
4. **Judge** — one sub-agent reads the transcript + four rubrics, produces structured findings.
5. **Aggregate** — write a `SUMMARY.md` across all journeys in this run.

## Argument parsing

Parse the user's invocation message for these forms (no native flag support in skills — match free-text):

- `/test-personas` (no args) → full sweep, all 4 journeys, all 3 personas as configured.
- `--journey <name>` or `journey: <name>` → run only the named journey. Valid names: `cold-start`, `active-loop`, `reflection`, `edge-recovery`.
- `--persona <name>` or `persona: <name>` → run only journeys whose `journey_fit` includes that persona. Valid names: `maya`, `diego`, `contrarian`.
- `--skip-judge` or `skip judge` → run conversation loops but skip Phase 4 (transcripts only).

If both `--journey` and `--persona` are specified, intersect them — only the named journey AND only if the named persona is its assigned persona. If they don't match, error with a clear message.

If the user's message is ambiguous, ask one clarifying question (Rule A) and stop.

## Phase 0: Setup before any journey runs

1. Resolve the run date: `RUN_DATE=$(date +%Y-%m-%d)` via Bash.
2. Create the run output directory:
   ```bash
   mkdir -p userdata/test-runs/$RUN_DATE
   ```
3. Read all four rubric files into memory (Read tool):
   - `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/rubrics/lint-checklist.md`
   - `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/rubrics/tone.md`
   - `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/rubrics/spec-criteria.md`
   - `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/rubrics/open-critique.md`
4. Read the simulator prompt: `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/simulator-prompt.md`.
5. Read the judge prompt: `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/judge-prompt.md`.

## Phase 1: Snapshot reset (per journey)

Before each journey, reset `userdata/` to the journey's declared snapshot.

1. Read the journey file `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/journeys/<journey>.md`. Extract `snapshot:` from frontmatter.
2. **Confirmation prompt before clobbering:** show the user what will happen and ask permission once per run (not per journey within a run):

   > "Each journey will reset `userdata/` from its declared snapshot under `tests/snapshots/`. Existing userdata content will be lost (test-run outputs are preserved between journeys). Continue?"

   If user declines, abort the entire run cleanly (do not partially execute).

3. Run rsync via Bash, excluding the test-runs directory so prior journeys' outputs survive:
   ```bash
   rsync -a --delete --exclude=test-runs/ tests/snapshots/<snapshot>/ userdata/
   ```
   (Note the trailing slash on the source — copies the contents, not the directory itself. The `--exclude=test-runs/` flag protects `userdata/test-runs/` from being removed between journeys in the same run.)

   Special case for the `empty` snapshot: the `--delete` flag plus a near-empty source effectively empties `userdata/`. The `.gitkeep` in `userdata/` should remain. Verify after rsync.

## Phase 2: Schema validation (per journey)

Before invoking sub-agents, check the snapshot's contents match what the journey's first skill expects to read. This catches drift between plugin schema updates and snapshot staleness.

For each journey, the validation checks vary. Use this rule of thumb:

- **cold-start** (snapshot: `empty`) — no validation needed; the journey starts by writing files, not reading them.
- **active-loop** (snapshot: `maya-active`) — check `userdata/profile.md` exists and contains sections `## Companies of interest` and `## Proof Points` (note the capitalization — match what's actually in the snapshot). Check `userdata/strategy.md` has frontmatter keys `target_offer_date` and `weekly_targets`. Check `userdata/companies/` has at least one subdirectory.
- **reflection** (snapshot: `diego-reflection`) — check `userdata/journal.md` has at least 3 dated `## YYYY-MM-DD` entries.
- **edge-recovery** (snapshot: `contrarian-messy`) — check that at least 2 directories exist in `userdata/companies/` (proves the dedup test setup landed correctly).

If any check fails, write a clear error and stop the journey:

> "Snapshot `<name>` failed schema validation: <which check failed>. Update the snapshot manually before re-running."

Do not silently proceed; do not modify the snapshot from this skill.

## Phase 3: Conversation loop (per journey)

This is the heart of the harness.

### Setup for the loop

1. Read the journey file. Extract `persona`, `snapshot`, `max_turns`, the `Opening message`, the `Mid-journey instructions`, the `Termination` conditions, and the `Spec criteria`.
2. Read the persona file `${CLAUDE_PLUGIN_ROOT}/skills/test-personas/personas/<persona>.md`.
3. Create the transcript file path: `TRANSCRIPT=userdata/test-runs/$RUN_DATE/$persona-$journey.md`.
4. Initialize the transcript with a header:

   ```bash
   cat > "$TRANSCRIPT" <<'EOF'
   # Transcript — <persona>-<journey>

   **Date:** <RUN_DATE>
   **Snapshot:** <snapshot>
   **Max turns:** <max_turns>

   ---
   EOF
   ```

### The loop itself

Initialize: `LATEST_USER_MESSAGE` is the journey's `Opening message` (e.g. `/pm-job-search:setup`).

Loop until termination:

1. **Append the user turn to the transcript.** Write `## Turn N — USER\n\n<LATEST_USER_MESSAGE>\n\n` to the transcript file using the Read+Edit pattern or by re-reading and Writing.
2. **Dispatch the plugin-under-test agent** via the Agent tool:
   - `subagent_type: general-purpose`
   - `description: "Plugin turn N for <persona>-<journey>"`
   - `prompt:` constructed as follows (see template below)
   - Wait for the agent's reply. Capture its assistant message as `LATEST_PLUGIN_OUTPUT`.
3. **Append the assistant turn to the transcript.** Write `## Turn N — ASSISTANT\n\n<LATEST_PLUGIN_OUTPUT>\n\n`.
4. **Check termination conditions** from the journey file's `Termination` section. If satisfied, exit the loop.
5. **Check max_turns.** If reached, exit with a note in the transcript: `## Loop ended: max_turns reached`.
6. **Dispatch the user-simulator agent** via the Agent tool:
   - `subagent_type: general-purpose`
   - `description: "Simulator turn N for <persona>-<journey>"`
   - `prompt:` constructed as follows (see template below)
   - Capture its reply as the next `LATEST_USER_MESSAGE`.
7. Continue.

### Plugin-under-test prompt template

The plugin agent is a fresh sub-agent each turn. It needs the full transcript-so-far + the latest user message to behave coherently. Send:

```
You are running the pm-job-search Claude Code plugin as a fresh Claude Code session. The plugin is loaded in your environment. The user is sending you messages in a real conversation.

This is turn N of a multi-turn conversation. The transcript so far is below. Read it to understand context. Then respond to the LATEST USER MESSAGE as you would in a real session — invoke skills if asked, follow plugin instructions, use the plugin's tools.

Do not break character as a Claude Code instance. Do not say "I am a sub-agent" or "this is a test". Just respond as the plugin would.

--- TRANSCRIPT SO FAR ---

<paste full transcript file contents here>

--- LATEST USER MESSAGE ---

<paste LATEST_USER_MESSAGE here>
```

### User-simulator prompt template

Send the simulator agent:

```
<paste full contents of simulator-prompt.md here>

--- PERSONA ---

<paste full contents of personas/<persona>.md here>

--- JOURNEY ---

<paste full contents of journeys/<journey>.md here>

--- TRANSCRIPT SO FAR ---

<paste full transcript file contents here>

--- LATEST FROM PLUGIN ---

<paste LATEST_PLUGIN_OUTPUT here>
```

The simulator replies with exactly the next user message — nothing else.

### Termination detection

After each plugin turn, check the journey's `Termination` section for satisfied conditions. Common patterns:

- Sentinel phrase match: search `LATEST_PLUGIN_OUTPUT` for the journey's named sentinels (e.g. `## Heads-up`, `Saved as`, `Let's wrap`).
- File presence: e.g. `interview-prep-*.md` exists in the relevant company directory after `/interview-prep`.
- Acknowledgement: the simulator's next reply matches a brief acknowledgement pattern (e.g. `^(ok|thanks|got it|sounds good)`).

Each journey defines its own termination — use the journey file as truth.

### Loop safety

- Hard cap on turns: respect `max_turns` from journey frontmatter.
- Empty plugin reply: if `LATEST_PLUGIN_OUTPUT` is empty or whitespace-only, exit with a note.
- Empty simulator reply: if the simulator returns empty, exit with a note (simulator hit its termination cue).

## Phase 4: Judge (per journey, unless --skip-judge)

After the conversation loop terminates, run the judge.

1. Build the judge input by concatenating:
   - The four rubric files (read once in Phase 0, available in memory).
   - The journey file's own `Spec criteria` section, appended to Rubric 3 (spec-criteria).
   - The full transcript file contents.
   - Metadata: `journey`, `persona`, `snapshot`, `date`.
2. Dispatch a third sub-agent via the Agent tool:
   - `subagent_type: general-purpose`
   - `description: "Judge for <persona>-<journey>"`
   - `prompt:` is the `judge-prompt.md` contents + the input blocks (transcript, rubrics, metadata) in the labelled format the prompt specifies.
3. The judge returns markdown findings. Write the result to `userdata/test-runs/$RUN_DATE/$persona-$journey.judge.md`.

## Phase 5: Aggregate (once per run)

After all journeys in the requested run have finished:

1. Read each `.judge.md` file in `userdata/test-runs/$RUN_DATE/`.
2. Extract the severity counts from each (parse the markdown table in the `## Summary` section).
3. Write `userdata/test-runs/$RUN_DATE/SUMMARY.md`:

```markdown
# Test run — <RUN_DATE>

| Journey | Hard | Soft | Spec gaps | Critiques |
|---|---|---|---|---|
| <journey1> | <h1> | <s1> | <sg1> | <c1> |
| <journey2> | <h2> | <s2> | <sg2> | <c2> |
| ...

See per-journey `.judge.md` files for details.

## Files in this run

- <persona1>-<journey1>.md (transcript)
- <persona1>-<journey1>.judge.md (findings)
- ...
```

4. Print a brief plain-prose summary to chat (Rule B — no fenced summary):

> Test run complete — <N> journeys, results in `userdata/test-runs/<RUN_DATE>/`.
>
> Severity totals: H hard, S soft, G spec gaps, C critiques.
>
> Open `SUMMARY.md` for the per-journey table, or read individual `.judge.md` files for findings.

## End-of-run nudge

After the run summary, suggest the natural next action based on the findings:

- If any hard violations: "Open `SUMMARY.md` and the per-journey `.judge.md` files. Fix hard violations before tagging the next release."
- If only soft issues + critiques: "Open `SUMMARY.md`. Soft issues are advisory; review and decide what to fix."
- If everything clean: "Clean run — no findings. Safe to tag the next release."

(This nudge follows the recommended-flow convention but is harness-specific since `/test-personas` is maintainer-only and not in the main user flow.)

## Cost note for maintainer

A full run (4 journeys × ~15-25 turns × 2 sub-agent calls per turn + 4 judge calls) is roughly 130-200 sub-agent invocations. On Claude Max this counts against weekly quota — expect a full run to consume a notable chunk of weekly limits. Use `--journey <name>` for single-journey runs when iterating on a specific skill.

## Voice for this skill's own output

This skill's own chat messages follow `${CLAUDE_PLUGIN_ROOT}/TONE.md` (plain prose, no fenced summaries, one ask per message, no preambles). The sub-agents' outputs are captured in transcripts and judged — they follow their own prompts.
