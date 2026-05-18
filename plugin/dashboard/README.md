# pm-job-search dashboard

React + Mantine SPA served by a Python stdlib HTTP server. Launched via the
`/dashboard` skill in the parent plugin.

- **Spec:** [docs/superpowers/specs/2026-05-18-dashboard-design.md](../../docs/superpowers/specs/2026-05-18-dashboard-design.md)
- **Rebuild:** `cd plugin/dashboard && npm install && npm run build` (then commit `dist/`)
- **Test (Python):** `python3 -m pytest -v`
- **Run locally:** `python3 serve.py --userdata <path-to-userdata>`

Users do not need to run any of the above. The committed `dist/` bundle and
the stdlib-only Python server are everything required at install time.
