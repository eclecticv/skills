# Output schema

The OUTPUT stage writes a structured markdown report to `~/Desktop/claude-code/positioning-<domain>-YYYY-MM-DD.md` and prints a tight summary to the terminal.

The full report follows this exact section order. Do not invent additional sections. Do not omit sections (when a section has no content, print "Not applicable" and the reason).

---

## Full report structure

```markdown
# Fix My Positioning — <Company name>
**URL:** <url>
**Audited:** YYYY-MM-DD
**Context flags:** stage=<value> · ACV=<value> · motion=<value> (or "none provided")

---

## 1. Composite scorecard

**Overall: X.X / 10 — <interpretive band>**

| Framework | Score | Weakest element |
|---|---|---|
| Dunford — Obviously Awesome | X.X / 2.0 | <one phrase> |
| JTBD + ODI overlay | X.X / 2.0 | <one phrase> |
| Raskin — Strategic Narrative | X.X / 2.0 | <one phrase> |
| Osterwalder — VPC | X.X / 2.0 | <one phrase> |
| Challenger Sale | X.X / 2.0 | <one phrase> |

---

## 2. Per-framework breakdown

### Dunford — Obviously Awesome (X.X / 2.0)

**Evidence (verbatim from homepage):**
> "<quoted hero copy>"
> "<additional quoted copy if relevant>"

**Findings:**
- <specific gap or strength>
- <specific gap or strength>

**Improvement recommendation (one sentence):**
<recommendation>

### JTBD + ODI overlay (X.X / 2.0)
[same structure]

### Raskin — Strategic Narrative (X.X / 2.0)
[same structure]

### Osterwalder — Value Proposition Canvas (X.X / 2.0)
[same structure]

### Challenger Sale (X.X / 2.0)
[same structure]

---

## 3. Fletch execution-layer findings

### Failure-pattern detectors triggered

(Only list rules that fired. If none, write "No failure patterns detected.")

| Rule | Verbatim copy | Suggested fix |
|---|---|---|
| F<n>. <Rule name> | "<quoted offending copy>" | <fix> |

### Positive signals detected

(Only list rules that fired. If none, write "No positive signals detected.")

| Rule | Verbatim copy |
|---|---|
| P<n>. <Rule name> | "<quoted copy>" |

### Fletch 9-element clarity heatmap

| Element | Score (0–3) | Note |
|---|---|---|
| Persona | <0–3> | <one phrase or "absent"> |
| Company type | <0–3> | <note> |
| Context | <0–3> | <note> |
| Problem | <0–3> | <note> |
| Product category | <0–3> | <note> |
| Capability | <0–3> | <note> |
| Feature | <0–3> | <note> |
| Benefit | <0–3> | <note> |

### The two ruthless tests

**Harry Dry test:**
- Visualizable: <yes/no — one sentence>
- Falsifiable: <yes/no — one sentence>
- Unique: <yes/no — one sentence>

**Fletch one-sentence test:** <yes/no — one sentence>

---

## 4. Three positioning variants

(SKIP THIS SECTION ENTIRELY if `--grade-only` was passed. Stop after Section 3 and add a closing note.)

### Variant A — Narrow-and-sharp

- **H1 (X words):** <generated H1>
- **Subhead (X words):** <generated subhead>
- **Pattern used:** <one of the seven Fletch patterns>
- **Best-fit ICP:** <persona + company type + context>

**Three reinforcing features (mapped to value pillars):**

| Feature | Pillar | Capability statement |
|---|---|---|
| <feature 1> | <pillar 1> | <verb + concrete object — what the user does> |
| <feature 2> | <pillar 1 or 2> | <capability statement> |
| <feature 3> | <pillar 2 or 3> | <capability statement> |

**Pros / cons (7-axis):**

| Axis | Score | Rationale (1–2 sentences) |
|---|---|---|
| 1. TAM vs. specificity | + / 0 / − | <rationale> |
| 2. Category creation vs. entry | + / 0 / − | <rationale> |
| 3. Competitive defensibility | + / 0 / − | <rationale> |
| 4. Clarity vs. expansiveness | + / 0 / − | <rationale> |
| 5. VC-readable vs. customer-readable | + / 0 / − | <rationale> |
| 6. Sales cycle and GTM fit | + / 0 / − | <rationale> |
| 7. Buyer committee multi-threading | + / 0 / − | <rationale> |

**Coherence flag:** <none / specific incoherence noted>

### Variant B — Category-led
[same structure]

### Variant C — Outcome-quantified
[same structure]

---

## 5. Recommendation

(If `--stage` was provided, tag one variant as recommended. If not, present neutrally and add the "your stage matters" note.)

**Recommended variant:** <A / B / C — or "no recommendation without --stage flag">

**Why:** <2–3 sentences explaining the choice based on stage, ACV, motion, and the 7-axis tradeoff scores>

**Validation plan:**
1. <Customer segment to validate with — be specific about who and how many>
2. <Concrete validation method — interviews, message testing, landing-page split test, etc.>
3. <Timeline — typically 2–4 weeks for message validation>

---

## 6. Message house — recommended variant

(Only generate this section for the recommended variant. Skip if no recommendation.)

**Roof (single-sentence positioning):**
<one sentence pulling category + audience + capability + outcome>

**Three pillars:**

### Pillar 1: <pillar name>
**Pillar statement:** <one sentence>
**Proof points:**
- <feature or capability that delivers this pillar>
- <customer outcome or quantified evidence>
- <competitive contrast if available>

### Pillar 2: <pillar name>
[same structure]

### Pillar 3: <pillar name>
[same structure]

**Tagline (3–7 words, optional):** <tagline>

---

## 7. Surface adaptations

How the recommended positioning expresses across surfaces (using the same five inputs, varying emphasis):

| Surface | Constraint | Adapted copy |
|---|---|---|
| Pitch deck title slide | 1 line + subline (≤12 + ≤15 words); Moore-format acceptable | <copy> |
| LinkedIn company tagline | 120-char limit | <copy — H1 verbatim if it fits> |
| Sales cold-email opener | 1 sentence ≤25 words; first line <90 chars | <copy> |
| Product Hunt launch | 60-char limit; declarative; no jargon | <copy> |
| Sales one-liner ("elevator") | ≤20 seconds / ~50 words; Moore-format with competitor named | <copy> |

---

## Appendix: methodology and sources

- Five frameworks: Dunford (2019), Christensen + Ulwick (2016 / 2005), Raskin (2016), Osterwalder (2014), Dixon & Adamson (2011)
- Execution layer: Fletch PMM (Pierri & Kaminski) — 9-element model + 13 failure / 7 positive detectors + category-modifier and capability-over-benefit rules
- Composite-band thresholds and 0.5 increments derive from the *Fix My Positioning Research Foundation v2*
```

---

## Terminal summary structure

After writing the full report, print this to the terminal:

```
✅ Fix My Positioning — <Company> · <url>

Score: X.X / 10  (<band>)
  Dunford X.X · JTBD X.X · Raskin X.X · VPC X.X · Challenger X.X

Fletch flags: <count> failure / <count> positive
Top critique: <one-sentence — the highest-leverage fix>

[If variants generated:]
3 variants generated — recommended: <A/B/C — or "see report for tradeoffs">
  A. <H1 — narrow-and-sharp>
  B. <H1 — category-led>
  C. <H1 — outcome-quantified>

[If --grade-only:]
Skipped variant generation (--grade-only).

📄 Full report: ~/Desktop/claude-code/positioning-<domain>-YYYY-MM-DD.md
```

---

## File naming convention

- **Domain extraction:** strip `https://` and `www.` → take the apex domain → use everything before the first `.` → fallback to the full hostname if extraction fails. Examples:
  - `https://www.example.com/about` → `example`
  - `https://app.gong.io` → `gong`
  - `https://fletchpmm.com` → `fletchpmm`
- **Date:** ISO `YYYY-MM-DD` (use today's date)
- **Final filename:** `positioning-<domain>-YYYY-MM-DD.md`

If the file already exists for today's date and same domain, append `-v2`, `-v3`, etc.

Always ensure `~/Desktop/claude-code/` exists before writing (mkdir -p if needed).
