---
description: Run 47 SaaS optimization rules against a website — prints scorecard to terminal and writes full report to file
argument-hint: <website-url>
allowed-tools: Read, Write, Bash, WebFetch
---

# Command: saas

Analyze a SaaS website against 47 research-backed optimization rules. Prints a
high-level scorecard with prioritized fixes to the terminal, then writes a
comprehensive `.md` report to disk.

## Usage
```
/saas-grader:saas <url>
```

## What It Does

All shared procedures live in `skills/saas-grader/reference/shared-procedures.md`.
Follow them in this order:

1. **Classify the site** (Step 0) — record the classification with evidence
2. **Collect evidence** — DOM extraction via `extract-signals.mjs`, screenshots of
   homepage AND pricing page, WebFetch only as fallback
3. **Score every rule** using the four-verdict system (PASS / FAIL / N/A / UNVERIFIED),
   the per-rule decision procedures, and the symmetric rigor protocol. Observation
   before verdict; every verdict cites its criterion and carries a confidence level
4. **Compute grades** — raw and weighted, per the scoring table. Practice-tier rules
   go to the Practices Review appendix, ungraded
5. **Compute priorities** per FAIL: weight + effort bonus (copy +3, design +2,
   product +0) → Critical ≥8, Medium 5–7, Low ≤4
6. **Check for a previous report** for the same company in the output directory and
   build the Changes Since Last Audit section from its JSON block
7. **Print the terminal summary** (below), then **write the full report** to
   `~/Documents/Inbox/[company]-saas-report-[YYYY-MM-DD].md` (create the directory if
   needed; never write to Desktop)

---

## Terminal Output

Print this to the terminal first:

```
SAAS AUDIT: [Company Name] — [raw pass]/[applicable] passing · weighted [W%] ([overall grade])
Classified: [B2B/B2C] · [utilitarian/hedonic] · [new/established] · [monetization]
Evidence: [DOM ✓/✗] [homepage screenshot ✓/✗] [pricing screenshot ✓/✗] · [n] UNVERIFIED

  Brand & Messaging     [grade]  (X/Y · weighted W%)
  Page Design           [grade]  (X/Y · weighted W%)
  Pricing Plans         [grade]  (X/Y · weighted W%)
  Free Trials           [grade]  (X/Y · weighted W%)   ← FT-1, FT-2 only
  Freemium              [grade]  (X/Y · weighted W%)
  Referrals             [grade]  (X/Y · weighted W%)
  Practices Review      [n verified / n unverified]    ← ungraded: CP, AF, FT-3/4

━━━ CRITICAL — Fix This Week (priority ≥ 8) ━━━

1. [Rule ID] ([weight]+[effort bonus]=[priority]): [Rule Name]
   Problem: [One-sentence observation — quote the actual headline, CTA, etc.]
   Fix: [Specific, actionable recommendation with a concrete example]
   Impact: [Cited research effect size]

━━━ MEDIUM — Fix This Month (5–7) ━━━

2. [Rule ID] ([priority]): [Rule Name]
   Problem: [observation]
   Fix: [recommendation]

━━━ LOW — Backlog (≤ 4) ━━━

3. [Rule ID] ([priority]): [Rule Name]
   Problem: [observation]
   Fix: [recommendation]

━━━ TOP WINS (What's Working) ━━━

- [Rule ID]: [What they're doing well — be specific]

━━━ CHANGED SINCE LAST AUDIT ━━━   ← only if a previous report exists

- [Rule ID]: [old verdict] → [new verdict] ([site-changed / re-evaluation / procedure-changed])

Full report: ~/Documents/Inbox/[company]-saas-report-[date].md
```

### Terminal Output Rules

1. **Scorecard first** — the summary table is the first thing the user sees
2. **Only include FAILs** in the fix tiers — never PASSes, N/As, or UNVERIFIEDs
3. **Critical tier gets full detail** — Problem + Fix + Impact; Medium and Low get
   Problem + Fix
4. **Top Wins section** — 3-5 strongest PASSes (highest weight) to show what's working
5. **Be specific** — quote actual headlines, measured counts, actual CTAs
6. **If a tier has no FAILs, omit it**
7. **UNVERIFIED items** appear only as the count in the Evidence line of the terminal
   summary — their detail lives in the file report

---

## File Output

Write to `~/Documents/Inbox/[company]-saas-report-[YYYY-MM-DD].md` with this EXACT structure:

```markdown
# SaaS Optimization Report: [Company Name]

**URL:** [url]
**Date:** [date]
**Plugin version:** [version from plugin.json]
**Overall:** [raw pass]/[applicable] passing · weighted [w-pass]/[w-applicable] ([W%] — [grade])

## Classification

| Dimension | Value | Evidence |
|-----------|-------|----------|
| Audience | ... | ... |
| Buying motivation | ... | ... |
| Brand maturity | ... | ... |
| Monetization | ... | ... |
| Pricing model | ... | ... |
| Experience-related | ... | ... |

## Evidence Sources

| Source | Status |
|--------|--------|
| Rendered DOM (homepage) | captured / failed |
| Rendered DOM (pricing) | captured / failed / no pricing page |
| Screenshot (homepage) | captured / failed |
| Screenshot (pricing) | captured / failed |
| WebFetch fallback | used / not needed |

## Summary

| Section | Raw | Weighted | Grade |
|---------|-----|----------|-------|
| Brand & Messaging | X/Y | W% | [grade] |
| Page Design & Visuals | X/Y | W% | [grade] |
| Pricing Plans | X/Y | W% | [grade] |
| Free Trials (FT-1, FT-2) | X/Y | W% | [grade] |
| Freemium | X/Y | W% | [grade] |
| Referrals | X/Y | W% | [grade] |
| Practices Review (ungraded) | [n verified, n unverified] | — | — |

## Changes Since Last Audit
[Only if a previous report was found. One line per flip with cause; otherwise omit
the section. "First audit on record" if none found.]

---

## 1. Brand & Messaging ([X/Y] — [Grade])

### BM-1: Productize Your Headline

**What it is:** [Copy from reference — word for word]

**Why it matters:** [Copy from reference — word for word]

**Source:** [Copy full citation from reference — word for word]

**Recommendation:** [Copy from reference — word for word]

**Observation:** [What was actually measured/observed — quote headlines, counts from
the signals JSON, screenshot descriptions. Written BEFORE the verdict.]

**Compliance:** PASS | FAIL | N/A | UNVERIFIED — [criterion bullet that fired] (confidence: High/Medium/Low)

**How to fix:** [Only if FAIL. Specific, actionable, with effort class: copy/design/product.]

---

[...repeat for every graded rule in sections 1–6: BM, PD, PR, FT-1/FT-2, FM, RF...]

## 7. Practices Review (ungraded)

[FT-3, FT-4, CP-1..3, AF-1..2 — same per-rule format, but verdicts default to
UNVERIFIED phrased as the question the founder should answer. Score informationally
only when on-site evidence exists.]

## Machine-Readable Results

```json
{
  "plugin": "saas-grader",
  "version": "[plugin version]",
  "url": "[url]",
  "date": "[YYYY-MM-DD]",
  "classification": { "audience": "...", "motivation": "...", "maturity": "...", "monetization": "...", "pricingModel": "...", "experienceRelated": false },
  "evidence": { "domHomepage": true, "domPricing": true, "screenshotHomepage": true, "screenshotPricing": false, "webFetchFallback": false },
  "overall": { "rawPass": 0, "rawApplicable": 0, "weightedPass": 0, "weightedApplicable": 0, "grade": "" },
  "rules": [
    { "id": "BM-1", "verdict": "FAIL", "confidence": "High", "weight": 5, "criterion": "...", "evidence": "..." }
  ]
}
```
```

### File Output Rules

1. **Every single rule gets its own section** — no exceptions, no skipping, no grouping
2. **"What it is", "Why it matters", and "Recommendation" are copied word-for-word**
   from the reference files; **"Source"** is the full citation
3. **Observation precedes Compliance** and contains concrete evidence: verbatim quotes,
   measured counts from the signals JSON, or screenshot descriptions. No evidence → the
   verdict is UNVERIFIED, not FAIL
4. **Every verdict names the criterion bullet that fired** and its confidence level
5. **"How to fix" is actionable** — a concrete alternative plus its effort class
6. **N/A and UNVERIFIED rules are still listed** — with why they don't apply / what
   would verify them
7. **The JSON block is mandatory** — it is what enables the next run's delta section
8. **The horizontal rule `---` separates every rule** for clean readability
