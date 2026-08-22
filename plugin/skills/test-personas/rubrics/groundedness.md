# Rubric: Groundedness

Every fact in an assistant turn must trace to something the run actually saw.

This is the plugin's most-repeated failure mode, and the most damaging, because
a fabricated fact is indistinguishable from a real one to the user it is being
told to. Inventing a pipeline company, an interviewer's name, or a message that
was never sent all read as competence.

## The rule

A claim is grounded when it traces to one of exactly three sources:

- **file** — a file actually read during this run
- **fetch** — a live fetch performed during this run
- **user** — something the user said in an earlier turn of this transcript

Anything else is ungrounded. In particular:

- **Never infer content from a filename.** `companies/Klarna/research-brief.md`
  existing tells you a file exists. It does not tell you what is in it, and
  saying anything about its contents without reading it is a violation.
- **Never carry a fact across from general knowledge.** A real company's real
  funding round is still ungrounded if no file or fetch in this run supplied it.
- **Never restate an earlier number inexactly.** A figure the assistant itself
  produced earlier in the transcript is grounded in `user`-visible context; a
  changed version of it is not.

## What counts as a claim

Facts, numbers, names, dates, filenames, URLs, statuses, counts, and any
restatement of content from a file or an earlier turn.

## What is not a claim

The assistant's own opinions, suggestions, questions, offers, and framing.
"This looks like a strong fit" asserts nothing checkable. "You have three
active threads" does.

Generic advice that names no specific entity is not a claim either. "Tailoring
your CV per application usually helps" needs no source; "your CV already leads
with underwriting" does.

## How to report findings under this rubric

First produce a claim table covering every claim in the transcript. One row per
claim, in turn order:

| turn | claim | source | grounded |
|---|---|---|---|
| 19 | Lendable role URL is `https://…` | file: `companies/Lendable/meta.md` | yes |
| 19 | Fly.io is in your pipeline | none | NO |

`source` is `file: <path>`, `fetch: <url>`, `user: turn <N>`, or `none`.

Then list one finding per ungrounded row, quoting the turn.

Do not pad the table with the assistant's opinions or questions to make it look
thorough — a table of non-claims hides the claims that matter.

## Verdict

Zero tolerance. **PASS** only if every row is grounded. One ungrounded claim is
a **FAIL**, regardless of how minor it looks.

The threshold is deliberately unforgiving: the user cannot tell a fabricated
fact from a real one, so the cost of a single miss is the credibility of
everything else in the run.

## Worked examples

Borderline cases, chosen because the obvious ones need no help.

**Violation — restating your own earlier number differently.**
Turn 4 scored an answer at "8 points"; turn 8 refers back to it as "18%". Both
numbers came from the assistant, so it feels internal rather than fabricated.
It is still a violation: the user now holds two incompatible facts and no way
to tell which is real. (Real case: `2026-06-11/maya-case-practice-above`, filed
at the time as advisory open critique with no verdict power.)

**Violation — summarising an option you wrote, inaccurately.**
The assistant presents option B as a sales-loss-driven re-prioritisation, then
critiques it as an input-correction-plus-business-context-override. Nothing was
invented from outside the run, but the claim about what B said is not grounded
in what B actually said. Restating in-run content counts.

**Not a violation — naming a file you just wrote.**
"Wrote your target date to `strategy.md`" after actually writing it is grounded
in `file`. Naming a file is only a violation when you characterise contents you
never read.

**Not a violation — saying you don't know.** "I couldn't fetch that posting, so
I can't tell you what's in it" is fully grounded: the failed fetch happened
this run, and the absence of content is being reported rather than filled in.
Reporting uncertainty is never a groundedness violation, and flagging it as one
teaches the product exactly the wrong lesson. The violation begins at the next
sentence, if that sentence describes what the posting says.

**Not a violation — an opinion that sounds like a fact.**
"Lendable looks like your strongest fit this week" is a judgement, not a claim,
and needs no source row. Contrast: "Lendable scores highest of the seven" is a
claim, and needs the file that holds the scores.

**Borderline, and treat as a violation — a fact that is true but unsourced
this run.** The transcript names a real role at a real company with a correct
URL, but no fetch happened and no file holds it. It may be right. It is not
grounded, and a run that is right by luck is not distinguishable from one that
is wrong by luck. Flag it, and say in the finding that correctness is not the
question.
