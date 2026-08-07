# Manual release checks — no journey covers these

Run all four before tagging a release, after the 3 release-gate journeys
and the golden-set grade pass. Back up `userdata/` first (it is
gitignored): `cp -R userdata ~/pm-job-search-userdata-backup-$(date +%F)`.

## 1. /setup re-run mode (~2 min)

With an existing `userdata/profile.md`, run `/pm-job-search:setup`. It
must enter re-run mode, not fresh-install: current value shown one at a
time, keep / update / skip, Steps 1–8 in order. Confirm:

- it does NOT re-read the CV (Step 0 does not apply on re-run)
- it does NOT ask about companies of interest (that question lives in
  /job-search Phase 0 now)
- `keep` on everything changes no file except the workspace CLAUDE.md
- freeform `## Tone of Voice` and `## What NOT to Frame As` sections
  survive untouched

Found a real self-contradiction on 2026-08-04 — this check earns its keep.

## 2. job-sweep → /setup handoff (~5 min)

Hand-build `job-sweep/profile.md` and `job-sweep/seen-roles.jsonl`
(two-three rows), run `/pm-job-search:setup`. Confirm both carry over
and the ledger append de-duplicates on `strict_key`.

## 3. CV dropped into job-sweep/ (~2 min)

Place a CV at `job-sweep/cv.md`, run `/job-sweep:sweep`. Confirm
extraction lands under `job-sweep/` and nothing is written to
`userdata/`. (The `cv-extraction.md` call site with zero journey
coverage — sweep-smoke deliberately takes the no-CV path.)

## 4. /setup CV-first path (~5 min)

The `cold-start-cv` journey that used to cover this was retired; the
`profile.md` schema check replaces only one of its twelve criteria, and
only partly. Cheap to run by hand — the `empty-with-cv` snapshot still
exists for it: copy its `cv.md` into a scratch `userdata/`, run
`/pm-job-search:setup` against it. Confirm:

- the CV is auto-detected without asking the user to drop one
- name, city, email and LinkedIn are confirmed in a SINGLE message, not
  four separate questions
- target titles and industries are each offered as a multi-select with
  an evidence line naming source material from the CV
- nothing in the written `profile.md` is absent from the CV and
  unconfirmed by the user — nothing was invented to fill a field
