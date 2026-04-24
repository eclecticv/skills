# Fletch PMM detector module

The execution-layer authority for homepage critique is **Fletch PMM** (Anthony Pierri & Rob Kaminski), whose firm has rewritten 400+ B2B SaaS homepages and openly cites April Dunford as their positioning-strategy foundation.

This module runs against the extracted homepage and produces:
- 13 **failure-pattern detectors** (each either flags or doesn't)
- 7 **positive-signal detectors** (each either rewards or doesn't)
- Fletch 9-element positioning clarity heatmap (each element scored 0–3)

Detector outputs feed both the Dunford / VPC framework scores and a separate execution-layer findings list in the final report.

---

## Failure-pattern detectors (13)

For each, if the rule fires, emit a finding with: rule name, the verbatim offending copy, and the suggested fix.

### F1. Category inflation
**Rule:** H1 contains "platform," "OS," "operating system," "suite," or "ecosystem" without supporting evidence the product genuinely spans 3+ use cases, 3+ personas, or 3+ connected modules.
**Severity escalation:** if `--stage seed` or `--stage A`, treat as a critical flag.
**Fix:** Anchor to a real category + modifier instead.

### F2. Category invention
**Rule:** H1 uses a capitalized multi-word category name that returns <100 non-self-referential Google results (e.g., "Revenue Operating System," "Decision Intelligence Platform").
**Fix:** Apply Fletch's category + modifier rule (see Section "Fletch generation rules" below).

### F3. Vague benefit language without capability
**Rule:** H1 or subhead contains any of: "empowering," "seamless," "transform," "unlock," "streamline," "amplify," "supercharge," "reimagine," "revolutionize" without a named capability.
**Fix:** Replace with a verb + object describing what the user *does*.

### F4. Abstract verb without object
**Rule:** H1 uses a verb with no concrete object ("Streamline your workflow," "Transform your business," "Unlock growth").
**Fix:** "What does that actually mean?" test failure — rewrite with a concrete object.

### F5. Us-focused copy
**Rule:** H1 or subhead begins with "We build…", "We help…", "Our mission…".
**Fix:** Reframe to be about the buyer, not the company.

### F6. "For everyone" audience framing
**Rule:** H1 uses "for modern teams," "for businesses of all sizes," "for the enterprise and beyond," "for any company."
**Fix:** Choose a specific persona, company type, or context.

### F7. Feature dump in hero
**Rule:** H1 + subhead lists 3+ features separated by commas without a unifying capability or outcome.
**Fix:** Identify the unifying outcome and lead with it.

### F8. Superlatives without proof
**Rule:** "The fastest," "the smartest," "the most powerful," "the leading" with no customer count, growth metric, or third-party ranking visible above the fold.
**Fix:** Either add proof above the fold or remove the superlative.

### F9. Too-clever metaphor
**Rule:** H1 uses a metaphor that requires interpretation ("We slay email dragons," "Your GPS for growth," "The Swiss Army knife of X").
**Fix:** State the literal capability.

### F10. Missing ICP
**Rule:** No named persona (role/title), company type (firmographic), OR context (situation) in H1, subhead, or above-the-fold eyebrow text.
**Fix:** Add at least one ICP signal — the buyer must self-identify in <3 seconds.

### F11. Missing category anchor
**Rule:** No recognizable product-category word visible in hero (e.g., CRM, observability, analytics, compliance, data pipeline, testing platform). Even with a modifier play, the category word must be present.
**Fix:** Add the category word.

### F12. Fake social proof
**Rule:** "Trusted by thousands of companies" without named logos or a quantified number visible.
**Fix:** Either name logos, quantify, or remove the claim.

### F13. Internal-stakeholder ROI claims above the fold
**Rule:** "3x ROI," "$M saved," "200% productivity gain" as the primary hero message.
**Fix:** Hard ROI belongs in the deeper sales cycle, not the homepage hero. Replace with a capability statement.

---

## Positive-signal detectors (7)

For each, if the rule fires, emit a positive finding and apply the linked score boost.

### P1. Clear category + modifier
**Rule:** Existing category word + 1–2 word differentiator (e.g., "AI CRM for GTM," "Observability for serverless").
**Boost:** +0.5 to Dunford component 5 (market category).

### P2. Named ICP in hero
**Rule:** Persona OR company type OR context explicit in H1 or subhead.
**Boost:** +0.25 to Dunford component 4 (best-fit customers).

### P3. Capability-led headline or subhead
**Rule:** A concrete verb-plus-object describing what the buyer *does* ("See deals at risk before the forecast call," "Ship PRs without breaking production").
**Boost:** +0.5 to VPC.

### P4. Single-job subhead
**Rule:** Subhead doing exactly one of {elaborate, specify audience, name mechanism, provide proof, contrast status quo, quantify outcome}.
**Boost:** +0.25 narrative-clarity bonus (split between Raskin and VPC).

### P5. Named competitive alternative above the fold
**Rule:** "Unlike spreadsheets," "Replace your legacy CRM," "Built for teams outgrowing Notion."
**Boost:** +0.5 to Dunford component 1 (competitive alternatives).

### P6. Problem section directly after hero
**Rule:** Second section explicitly articulates the buyer's pain before introducing the product. Matches Fletch's Hero → Problem → Solution Intro → Value Propositions flow.
**Boost:** +0.25 narrative-coherence bonus to Raskin.

### P7. Dual CTA with role asymmetry
**Rule:** One CTA for self-serve/user ("Start free") + one for sales/buyer ("Book a demo").
**Boost:** +0.25 to Challenger (signals multi-stakeholder awareness).

---

## Fletch 9-element clarity heatmap

Score each element 0–3 based on how clearly it appears in the hero or above the fold:

| Element type | Element | What to look for |
|---|---|---|
| Market | **Persona** | Job title or role explicit (e.g., "for CFOs", "for engineering managers") |
| Market | **Company type** | Firmographic (e.g., "for B2B SaaS", "for fintech startups", "for mid-market") |
| Market | **Context** | Situation or trigger (e.g., "after Series A", "when scaling past 50 engineers") |
| Market | **Problem** | Functional or emotional pain explicit (e.g., "stop losing deals to slow follow-up") |
| Product | **Product category** | Recognizable category word (CRM, observability, etc.) |
| Product | **Capability** | What the user can *do* (verb + object) |
| Product | **Feature** | Mechanism or how it works |
| Product | **Benefit** | Outcome (e.g., "save 4 hours per week") |

Scoring per element:

- **0** — absent
- **1** — vague or implied
- **2** — clear but generic
- **3** — clear and specific

**Important.** Founders don't need 3s on all 9 elements — they need a **minimum viable positioning** anchored on the 2–3 they're clearest on. The plugin should report the heatmap as raw data, not as a 27-point score.

---

## Fletch generation rules (used during the GENERATION stage)

When generating any of the three positioning variants, every variant must satisfy:

### G1. Category + modifier rule (almost always)
Anchor to an existing category with a differentiating modifier. "AI CRM for GTM" works (existing category: CRM; modifier: AI + GTM-specific). "Revenue Operating System" does not.

The test: if the closest description of what the company does is "they use spreadsheets and manual processes to do this today," the company *may* be creating a new category — and in that rare case, Raskin's Strategic Narrative carries the weight, not the homepage category claim.

If `--stage seed` or `--stage A`, never generate a category-invention H1.

### G2. Capability over benefit
Every H1 or subhead must name a **capability** (verb + concrete object describing what the user does), not just a benefit. "AI-powered pipeline insights" is a benefit (vague, interchangeable). "See which deals are at risk before your forecast call" is a capability (concrete, demonstrable).

### G3. Length and readability targets
- **Headlines:** 6–12 words, ~55–70 characters, ≤2 lines on mobile (390px)
- **Subheadings:** 12–25 words, ~100–160 characters, ≤3 lines on mobile
- **Reading level:** Grade 6–8 (Flesch 60–70), even for executive audiences

### G4. Subhead does exactly one job
A subhead should do exactly one of:
- **Elaborate** the headline
- **Specify** target audience
- **Name** mechanism
- **Provide** proof
- **Contrast** with status quo
- **Quantify** outcome

Pairing rules:
- If the headline is category-led, subhead should elaborate + quantify
- If outcome-first, subhead should specify audience + name mechanism

### G5. Named ICP in hero
Persona OR company type OR context must be explicit in H1 or subhead. The buyer must self-identify in under 3 seconds.

### G6. Forbidden words list
Reject any generated headline containing: "empowering," "seamless," "transform," "unlock," "streamline," "amplify," "supercharge," "reimagine," "revolutionize," "leverage," "synergy," "best-in-class," "world-class," "next-generation," "cutting-edge," "industry-leading."

---

## The seven structural patterns

When generating variants, choose the pattern that fits the variant's strategic profile:

| Pattern | Template | When it works |
|---|---|---|
| **Who/what/why** | "[Category] for [audience] that [unique value]" | Real category + well-defined audience (Linear: "The product development system for teams and agents") |
| **Outcome-first** | "[Desired result] without [painful tradeoff]" | Product eliminates a known tradeoff |
| **Category-led** | "The [new category] for [audience]" | Only when you can credibly own a new category — rare (Gong: "The #1 AI operating system for Revenue Teams") |
| **Problem-first** | "Stop [pain]" or "[Bad status quo] is dead" | Aggressive repositioning |
| **Mechanism-led** | Name a proprietary approach (Stripe: "Financial infrastructure") | You have IP worth naming |
| **Social proof-led** | "Trusted by N" | Late-stage; weak early |
| **Contrarian/provocative** | Real POV + explicit enemy | Founder has a real POV; risks alienation if unsupported |

Variant strategy mapping (default):
- **Variant A — narrow-and-sharp** → Who/what/why or Outcome-first
- **Variant B — category-led** → Category-led or Mechanism-led
- **Variant C — outcome-quantified** → Outcome-first or Problem-first

---

## The two ruthless tests

Apply both to every generated H1 and to the existing homepage H1 during extraction:

**Harry Dry's three-rule test** (any failure → broken):
1. **Visualizable** — can a reader picture it?
2. **Falsifiable** — is it a verifiable claim?
3. **Unique** — could a competitor say the same sentence?

**Fletch's one-sentence test:**
*"Can the prospect tell a colleague what your product is in one sentence, using your language, without misrepresenting it?"*

If the answer is no, the hero is broken. Surface as a critical finding.
