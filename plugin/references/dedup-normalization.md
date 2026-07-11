# Dedup normalization — role identity keys

The single authority for how `/job-search` and `/evaluate-position` decide
whether two postings are the same role. Both skills derive the same keys from a
`(company, position, link)` triple so their dedup decisions never disagree.

Schema field names come from `plugin/schemas/meta.md.schema.md`. Use `position:`
never `role:`.

## The four keys

Derive these from each role (an existing meta.md entry, a seen-ledger line, or a
fresh candidate):

- **`company_key`** — `company`, lowercased, punctuation stripped, whitespace
  collapsed. Example: `Plaid, Inc.` → `plaid inc`.
- **`strict_key`** — `company_key` + ` ` + the full `position`, lowercased and
  flattened, with these substitutions applied in order:
  - `pms` → `product managers`, `pm` → `product manager`
  - seniority synonyms: `snr`/`sr`/`sen` → `senior`; `gpm` → `group product
    manager`; `lead pm`/`lead product manager` → `lead product manager`;
    `principal pm` → `principal product manager`; `dir`/`director of product` →
    `director product`; `head of product`/`hop` → `head of product`
  - strip punctuation, collapse whitespace
  Example: `Snr PM, Payments` at Plaid → `plaid senior product manager payments`.
- **`base_key`** — `strict_key` with any trailing qualifier removed: cut
  everything from the first comma, en-dash `–`, em-dash `—`, hyphen `-`, colon,
  or opening parenthesis onward, then re-collapse whitespace.
  Example: `plaid senior product manager payments` → `plaid senior product
  manager`; `… — growth` and `… (remote)` reduce the same way.
- **`url_key`** — `link`, lowercased, `?…` query and `#…` fragment stripped,
  trailing `/` removed, leading `www.` removed. Empty links produce no `url_key`.

## Match rules

Compare a fresh candidate against the union of (existing meta.md entries + the
seen-ledger):

1. **Hard duplicate** — `url_key` matches OR `strict_key` matches. This is the
   same posting (or the same role re-parsed / re-posted). Drop it silently; if it
   matches an existing meta.md entry, touch that entry's `last_seen:`.
2. **Soft duplicate** — `base_key` matches at the same `company_key`, but neither
   `url_key` nor `strict_key` matches. Same base title, different qualifier — it
   *might* be the same role reworded, or a genuinely distinct second team's role.
   Do NOT silently drop: skip filing by default but surface it in the run summary
   under "Skipped as likely repeats" with its title + link, so the user can say
   "no, file that one" (which routes through `/evaluate-position`'s 1→2 migration).
3. **New** — no key matches. File it.

Guarantee preserved: same company + a genuinely different position is never a
hard duplicate. Only exact/URL identity drops silently; anything fuzzier is shown.
