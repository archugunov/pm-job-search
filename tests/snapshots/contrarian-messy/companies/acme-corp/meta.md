---
company: AcmeCorp
position: Senior Product Manager
status: new
tier: unscored
link: https://example.com/acmecorp-senior-product-manager
first_seen: 2026-05-22
last_seen: 2026-05-22
---

# AcmeCorp — Senior Product Manager

Duplicate of `acmecorp/` (different folder slug, same company name, slightly different position string). Intentional — tests whether the plugin's dedup logic catches near-duplicate entries on the `company:` frontmatter field even when folder names differ.

Note: this was originally specced as a case-collision (`AcmeCorp/` vs `acmecorp/`) but macOS APFS is case-insensitive by default. Folder slug changed to `acme-corp/` to keep two real directories on disk; the test still exercises dedup on the company name.
