---
name: saas-grader
description: >
  This skill should be used when the user asks to audit, score, grade, or
  analyze a SaaS website, homepage, or pricing page. Triggers include
  "grade my SaaS site", "audit this homepage", "score my pricing page",
  "what's wrong with my landing page", "review my SaaS website against
  best practices", "run the 47-rule checklist", "export a SaaS optimization
  report", "how do I improve my SaaS homepage", "conversion optimization audit",
  "pricing page review", or "SaaS website teardown".
---

# SaaS Grader

A research-backed analysis tool that scores SaaS websites against 47 optimization rules drawn from peer-reviewed marketing science and UX research. Every rule includes the full research citation — no opinions, no fluff.

## Purpose

Analyze a SaaS homepage and pricing page against every rule in the playbook. For each rule, the output includes what it is, why it matters (the science), the source citation, a compliance verdict (PASS/FAIL/N/A), the specific observation, and a concrete fix recommendation if failing. The full analysis is exported as a standalone `.md` file.

## How It Works

One command does everything — `/saas-grader:saas <url>`:

1. **Classify the site** first (B2B/B2C, utilitarian/hedonic, new/established,
   monetization, pricing model) — conditional rules score against this declared
   classification instead of re-deciding it per rule
2. **Extract measured evidence** — rendered-DOM dump via local headless Chromium,
   distilled to a signals JSON by `scripts/extract-signals.mjs` (headline, CTAs,
   prices, social-proof numbers, ratings, trial mentions, fonts, text stats)
3. **Screenshot** the homepage AND the pricing page (visual-position rules are never
   scored from text)
4. **Score every rule** — PASS, FAIL, N/A, or UNVERIFIED, each with cited evidence,
   the criterion that fired, and a confidence level
5. **Print** a scorecard with computed priorities to the terminal
6. **Write** a comprehensive `.md` report (with a machine-readable JSON block for
   run-over-run deltas) to `~/Documents/Inbox/`

## The 47-Rule Checklist

### 1. Brand & Messaging (8 rules: BM-1 to BM-8)
Productized headline, top 3 benefits, present tense, newness signal, simple language, social proof numbers, 4-4.5 star rating, curated first testimonial.
> See [reference/brand-messaging.md](reference/brand-messaging.md)

### 2. Page Design & Visuals (14 rules: PD-1 to PD-14)
Design structure matches product type, brand-appropriate colors, layout adapted to SaaS type, moderate complexity, rounded CTAs, machine font, CTA upper-right, before/after left-to-right, video for exciting software, video speed, above-the-fold prioritization, content succinctness, scannable structure, signal-to-noise ratio.
> See [reference/page-design.md](reference/page-design.md)

### 3. Pricing Plans (9 rules: PR-1 to PR-9)
3-5 plans, decoy plan, left-to-right ordering, price below features, price-difference framing, simple pricing, easy math, flat+usage hybrid, flat-rate option.
> See [reference/pricing-plans.md](reference/pricing-plans.md)

### 4. Free Trials (4 rules: FT-1 to FT-4)
Full-feature trial, 7-day length, high trial usage, extensions over discounts.
> See [reference/free-trials.md](reference/free-trials.md)

### 5. Freemium (2 rules: FM-1 to FM-2)
Usage-limited freemium, freemium decoy plan.
> See [reference/freemium.md](reference/freemium.md)

### 6. Churn Prevention (3 rules: CP-1 to CP-3)
Customer gifts, auto-enrolling loyalty program, generous downgrades.
> See [reference/churn-prevention.md](reference/churn-prevention.md)

### 7. Affiliates (2 rules: AF-1 to AF-2)
Optimize affiliate payment model, protect from deceptive affiliates.
> See [reference/affiliates.md](reference/affiliates.md)

### 8. Referrals (5 rules: RF-1 to RF-5)
Altruistic framing, pre-filled messages, avoid money rewards, keep rewards small, targeted referrals.
> See [reference/referrals.md](reference/referrals.md)

## Scoring

Every rule carries a static tier (`mech` = measured, `judg` = anchored judgment,
`prac` = operational practice), an evidence grade for its underlying research, an
impact grade from its cited effect size, and a weight. Letter grades (A+ through F)
come from the weighted pass rate over applicable rules; N/A and UNVERIFIED are
excluded from denominators, and practice-tier rules (churn, affiliates, trial ops)
live in an ungraded Practices Review appendix. Fix priority is computed per FAIL:
rule weight + effort bonus (copy > design > product). See
`reference/shared-procedures.md` for the classification step, evidence pipeline,
verdict semantics, scoring table, and delta procedure.

## Output Format

For each of the 47 rules, the `.md` report includes:
- **What it is** — description of the rule (from the reference)
- **Why it matters** — the science behind it (from the reference)
- **Source** — full research citation with authors, journal, date, and universities
- **Recommendation** — actionable guidance from the research (from the reference)
- **Observation** — the concrete evidence (quotes, measured counts, screenshot
  descriptions), stated before the verdict
- **Compliance** — PASS, FAIL, N/A, or UNVERIFIED, naming the criterion that fired,
  with a confidence level
- **How to fix** — concrete, actionable recommendation with effort class (only if FAIL)

The report also opens with the site classification and evidence-source table, notes
verdict changes since the previous audit of the same company, and ends with a
machine-readable JSON block used for those run-over-run comparisons.

