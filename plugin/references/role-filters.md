# Role filters — which titles count as a match

Shared by `/job-search` (Discovery + recheck) and `job-sweep`. One definition, so
a title that qualifies in one place qualifies in the other.

## Title-match set

Case-insensitive substring — at least ONE must match:

- `head of product`
- `lead product manager`, `lead pm`
- `group product manager`, `group pm`
- `senior product manager`, `senior pm`
- `principal product manager`, `principal pm`
- `director of product`
- `staff product manager`

## Negative filter

Drop the title if it contains ANY of these:

- `junior`, `intern`, `associate`
- `.net`, `java`, `blockchain`, `data engineer`, `software engineer`, `qa`, `sales`

## Adapting to the user

The defaults above suit a senior-PM / Head-of-Product hunt. Widen or narrow them
from the user's own `target_titles` — those are the canonical levels they are
hunting. A user targeting `Director of Product` and `VP Product` should not have
`senior product manager` results dropped, and vice versa: never filter out a title
the user explicitly listed as a target.
