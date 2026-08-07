# Contrarian — messy example install

Synthetic reference install for pm-job-search, used by the `edge-recovery` journey.
Demonstrates a lived-in state at 2026-08-05, deliberately messy: a duplicated
company folder (`acmecorp` and `acme-corp` for the same employer), a long-stale
application (`stalecorp`), an empty `## Companies of interest` carrying the italic
`_None yet — fill in as you discover them._` placeholder, and a `target_date:` key
in `strategy.md` where the schema calls for `target_offer_date:`.

None of that is accidental. The journey exists to check the plugin degrades
gracefully on state a real user actually produces — deduplicating without silently
dropping a genuine second role, and not re-asking the companies question every week
once it has been answered with "none".

Dates here are rebased by `make rebase-fixtures`; the anchor is the newest journal
entry. Do not hand-edit them.
