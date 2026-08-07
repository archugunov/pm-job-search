# Transcript — maya-active-loop

**Date:** 2026-06-07
**Snapshot:** maya-active
**Max turns:** 30
**Note:** Phase 2 schema check caught one drift on first attempt — `## Companies of interest` was missing from the snapshot's profile.md. Snapshot patched (commit 55a785e) and journey restarted with valid state.

---

## Turn 1 — USER

/pm-job-search:job-search

## Turn 1 — ASSISTANT

Filed 2 new roles: 2 tier-1.

- Plaid — Lead PM, Risk — to triage — https://example.com/plaid-lead-pm-risk
- Atom Bank — Senior PM, Mortgages — to triage — https://example.com/atom-senior-pm-mortgages

Open the dashboard to triage — or say `mark <Company> to apply` and I'll update it.

## Turn 2 — USER

mark Plaid to apply

## Turn 2 — ASSISTANT

Which Plaid role do you want to mark as to-apply?

1. Lead PM, Risk
2. Senior PM, Consumer Credit
3. Senior PM, Growth Loops

## Turn 3 — USER

Consumer Credit. That's my lane.

## Turn 3 — ASSISTANT

> Updated Plaid → Senior PM, Consumer Credit → to_apply.
>
> Tip: you can also click the company row in the dashboard and add this note directly — same `meta.md` underneath.

## Turn 4 — USER

/pm-job-search:apply Plaid

## Turn 4 — ASSISTANT

Looking at your CV, your strongest underwriting/credit signals are split across two threads: the SMB lending feature at your current fintech (clear B2B2C credit decisioning angle) and the consumer onboarding work that touched KYC/risk earlier in your career — for a Senior PM Consumer Credit role at Plaid, which sits closer to the consumer side of the credit stack, do you want the CV to lead with the SMB lending work (deeper credit-model proof, but B2B-flavoured) or reframe the consumer onboarding/risk work as the headline (better audience fit, but thinner on actual underwriting depth)?

## Turn 5 — USER

Lead with the SMB lending underwriting story — it's the stronger proof. Frame the positioning so the underwriting muscle reads as transferable to consumer credit risk.

## Turn 5 — ASSISTANT

What's the single most defensible quantitative outcome from the SMB underwriting work you'd want headlined at the top of the CV — e.g., approval-rate lift, default-rate reduction, NIM impact, or portfolio size unlocked — and over what time window?

## Turn 6 — USER

Cut decline rate by 12% on thin-file applicants across Q2-Q3 2025 without any uptick in defaults, by replacing the hard cutoff with a cashflow-based secondary check.

## Turn 6 — ASSISTANT

Drafted your tailored CV for Plaid — Senior PM, Consumer Credit and saved it to `userdata/companies/Plaid/senior-pm-consumer-credit/cv-2026-06-07.md`.

What I leaned on:
- Positioning angle: underwriting depth at Brightline reframed as the direct analogue to Plaid Consumer Credit's thin-file decisioning work, with the "Not a process PM — a PM who writes specs, runs the SQL, and sits close to risk" reframe
- Strongest proof point headlined: the 12% decline-rate cut on thin-file applicants Q2-Q3 2025 via cashflow-based secondary check, called out as the closest analogue to the JD
- Pricing experiment programme from NorthLoop pulled in as a current-seat proof point for risk-pricing trade-offs
- Activation experimentation programme from Lumio pulled in as relevant to the onboarding work Plaid will need
- Dropped: the APM mentorship line and the CEO-cited shipping-cadence framing — this is a senior IC seat on an 18-person bet, so coaching breadth and process-leadership signal aren't what they're hiring for

Open the file and edit anything that doesn't sound like you before you send it. Next: want me to draft a short cover note, or move on to interview-prep?

## Turn 7 — USER

/pm-job-search:interview-prep Plaid

## Turn 7 — ASSISTANT

Which round is this — recruiter screen, hiring manager, panel, or final/founder-vetting?

## Turn 8 — USER

hiring manager

## Turn 8 — ASSISTANT

Saved as `userdata/companies/Plaid/senior-pm-consumer-credit/interview-prep-2026-06-07.md`.

Pulled 4 stories adapted for Plaid hiring-manager round:
- Underwriting zero-to-one — leads on risk-appetite negotiation while shipping fast, anchors to thin-file segment + bureau-integration reuse
- Consumer credit onboarding pivot — first-loan UX angle, the moment Maya killed a track and re-scoped
- Payments pricing experiment — closest analogue to Plaid's risk-pricing trade-offs, opens the Capital Markets question naturally
- Risk team dissent — disagree-and-commit signal for a founder-close pod

Practise with `pm-job-search:interviewer-simulator` (mock round) — or open the doc and rehearse out loud first. Debrief after with `/pm-job-search:interview-analysis`.

## Turn 9 — USER

thanks

## Termination

Met: transcript contains "Saved as `userdata/companies/Plaid/senior-pm-consumer-credit/interview-prep-2026-06-07.md`" AND simulator acknowledged with brief ack ("thanks"). Loop terminated cleanly at turn 8 (plugin) + turn 9 (simulator), well within max_turns=30.
