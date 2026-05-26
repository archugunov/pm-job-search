---
title: Underwriting zero-to-one
story_type: ambiguity-0-to-1
themes: [zero-to-one, underwriting, risk, ambiguity]
role_lens: [strategy, analytics, design-partnership]
companies_used_in: [Cleo, Plaid]
last_practised: 2026-05-15
---

# Underwriting zero-to-one

## Situation

UK consumer lender, credit-builder product targeting thin-file applicants with
no prior credit history. The business wanted to launch a credit-builder loan
(£250 cap) as a new product line. The challenge: no historical default data
existed for this segment within our portfolio. The data science team's existing
underwriting model was calibrated on our prime borrower book — applying it
directly to thin-file applicants would produce systematic mispricing. There was
no comparable product in-house to bootstrap from and no clean external dataset
that mapped to our specific applicant channel.

## Task

I was Senior PM owning the credit-builder product end to end. My job was to
get from zero (no model, no product, no segment data) to a calibrated
underwriting model and a live product, within a fiscal year. The constraint was
that we couldn't launch commercially until the model had enough real-world
default signal to be defensible to the credit committee.

## Action

- Partnered with the data science lead to design a three-phase data strategy:
  phase 1 (weeks 1–6) used synthetic data to scaffold model structure —
  generating plausible applicant profiles from known thin-file population
  statistics to set prior distributions and test model architecture; phase 2
  (weeks 7–14) ran real applicants through a manual-review-plus-low-cap track
  (£250 loans, decisions reviewed by a credit analyst) to gather real default
  signal without model risk; phase 3 (week 15+) used the phase 2 default
  signal to calibrate and retrain, then launched with the full automated model.
- Defined the instrumentation schema before phase 2 started: every application
  decision, repayment event, and default trigger was tagged to a feature bucket
  to enable clean model attribution at phase 3. This prevented the common
  failure mode of arriving at retraining with an uninstrumented dataset.
- Ran weekly model-calibration reviews with data science and the credit
  committee observer throughout phase 2 — not to change decisions in-flight,
  but to build the committee's trust in the signal quality before the full
  launch ask.
- Wrote the credit committee submission at phase 3, framing the model
  performance against the pricing target rather than against holdout accuracy
  alone — because the committee's decision variable was net margin, not AUC.

## Result

- Model performance was within 2% of the pricing target by month 4 — ahead of
  the internal estimate of month 6.
- £40M of credit originated in year 1 on the credit-builder product.
- Default rate at 2.8% vs. 3.2% target — better than pricing assumption,
  attributed partly to the manual-review phase surfacing behavioural signals
  that improved the phase 3 feature set.
- The three-phase data strategy became the internal playbook for any new
  segment launch — data science adopted it formally after the credit-builder
  postmortem.

## Angles for different prompts

**"Tell me about a 0-to-1."** Lead with the data problem, not the product. The 0-to-1 was the model, not the loan. The question was how you build a defensible underwriting model when you have no ground truth data — and the answer was a structured data-collection strategy before the product was commercially live. Don't lead with the £40M; lead with the phase design.

**"Tell me about leading through ambiguity."** Lead with the credit committee dynamic. There was genuine ambiguity about whether the credit committee would accept a synthetic-data-seeded model as a legitimate basis for a commercial launch. The way through wasn't to argue the methodology — it was to get them into the weekly reviews during phase 2, so that by the time the submission arrived they were participants, not evaluators.

**"Tell me about analytics depth."** Lead with the instrumentation schema design. The failure mode for this kind of project is arriving at phase 3 with uninstrumented phase 2 data — you have defaults but you can't attribute them to features. Defining the schema before the first real applicant was processed is the analytical decision that made everything else possible. Walk through the feature bucket structure and why each bucket was defined the way it was.

**"Tell me about working with a technical or data science team."** Lead with the model-calibration reviews and the credit committee framing. The partnership with data science wasn't "PM gives requirements, DS builds model" — it was joint design of the data strategy, shared ownership of the phase 2 instrumentation schema, and co-authoring the committee submission in a language that the committee could evaluate. The framing of model performance against pricing target rather than holdout accuracy was a joint call — data science trusted the business case framing, not just the technical one.
