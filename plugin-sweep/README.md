# job-sweep

A weekly sweep for open product roles that match you — and it remembers what it
already showed you, so week two isn't week one again.

That's the whole tool. No pipeline to maintain, no company folders, no scoring
rubric to tune.

## Install

```sh
/plugin marketplace add https://github.com/archugunov/pm-job-search.git
/plugin install job-sweep@pm-job-search
```

## Use

```
/job-sweep:sweep
```

First run asks for a CV or three questions — target titles, industries, where
you'll work. Every run after that just sweeps, and writes
`job-sweep/roles-<date>.md` next to a running ledger of what you've already seen.

## When you want more

`job-sweep` finds roles. If you get to the point of tracking applications,
scoring fit, prepping interviews and running a whole search, the full
[pm-job-search](https://github.com/archugunov/pm-job-search) plugin does that —
and its `/setup` reads your `job-sweep/profile.md`, so nothing you answer here is
wasted.

MIT licensed.
