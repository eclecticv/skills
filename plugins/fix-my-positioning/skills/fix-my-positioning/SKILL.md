---
name: fix-my-positioning
description: This skill should be used when the user invokes "/fix-my-positioning" or asks to "grade my positioning", "audit my homepage positioning", "audit my landing page", "score my SaaS homepage", "rewrite my B2B positioning", "fix my hero section", "score my homepage against Dunford", "generate positioning variants", or "give me a Fletch teardown of my homepage". Grades B2B startup positioning against five non-overlapping frameworks (Dunford, JTBD/ODI, Raskin, VPC, Challenger), runs the Fletch PMM execution-layer detector module against the homepage, and generates three positioning variants with H1 + subhead + features + 7-axis tradeoff analysis. Writes a structured markdown report to ~/Desktop/claude-code/.
argument-hint: <url> [--stage seed|A|B+] [--acv SMB|mid|enterprise] [--motion PLG|sales|hybrid] [--grade-only]
allowed-tools: ["Read", "Write", "Bash", "WebFetch", "Task"]
---

# Fix My Positioning — orchestrator

This skill runs a six-stage pipeline against a B2B startup URL — extraction → Fletch critique → 5-framework scoring → 3-variant generation → 7-axis pros/cons → recommendation/message-house — and finally writes a structured markdown report. Stages are numbered 1–6; the report-writing step is Stage 6's final substep.

## Inputs

Parse the user's invocation:

- **`<url>`** — required, the B2B startup homepage URL
- **`--stage`** — optional: `seed`, `A`, or `B+`. Shapes scoring thresholds (e.g., seed-stage gets cap on category-creation claims) and recommendation logic
- **`--acv`** — optional: `SMB`, `mid`, or `enterprise`. Adjusts Challenger framework rigor
- **`--motion`** — optional: `PLG`, `sales`, or `hybrid`. Adjusts buyer-committee axis weighting
- **`--grade-only`** — optional flag. If present, stop after Stage 3 (Scoring). Skip generation, pros/cons, and message house.

If the user provides no URL, ask once. Do not invent a URL.

## Pipeline

### Stage 1: Extraction (delegate to agent)

Dispatch the `positioning-extractor` agent with the URL. The agent returns a structured markdown document containing verbatim hero copy, social proof, category labels, and the Fletch detector module results (13 failure detectors + 7 positive detectors + 9-element clarity heatmap).

Use the Task tool with `subagent_type: "positioning-extractor"`. Pass the URL and any context flags. Wait for completion.

If the agent reports "fetch status: failed", relay the failure to the user with the agent's specific reason and stop the pipeline. Do not attempt to score on missing data.

### Stage 2: Fletch critique synthesis

Read the agent's output. The Fletch detector module already ran inside the agent. In this stage, organize the findings into:

1. **Critical findings** — failure-pattern detectors that are blocking (F1 with `--stage seed/A`, F2 with `--stage seed/A`, F10, F11)
2. **Standard findings** — other failure-pattern detectors that fired
3. **Positive signals** — positive-signal detectors that fired
4. **Clarity heatmap** — the 9-element scores

Apply the score boosts from positive-signal detectors (P1 → +0.5 to Dunford c5; P2 → +0.25 to Dunford c4; P3 → +0.5 to VPC; P4 → +0.25 split between Raskin and VPC; P5 → +0.5 to Dunford c1; P6 → +0.25 to Raskin; P7 → +0.25 to Challenger). Track these boosts — they apply during Stage 3.

Read `references/fletch-detectors.md` if rule details need clarification.

### Stage 3: Five-framework scoring

Read `references/frameworks.md` for the full rubrics. Score each framework independently, in this order:

1. **Dunford — Obviously Awesome** (0–2.0)
2. **JTBD + ODI overlay** (0–2.0)
3. **Raskin — Strategic Narrative** (0–2.0)
4. **Osterwalder — Value Proposition Canvas** (0–2.0)
5. **Challenger Sale** (0–2.0)

For each framework:

- Apply the rubric strictly. Read the 0 / 0.5 / 1.0 / 1.5 / 2.0 bands and choose the closest match.
- Quote 1–3 verbatim extracts from the agent's extraction as evidence.
- Identify the single weakest element (one phrase).
- Apply any positive-signal boosts from Stage 2.
- Apply stage-aware adjustments:
  - If `--stage seed/A` and Dunford is being held high because of a category-creation claim, cap Dunford at 1.0 (per `frameworks.md` Framework 1 stage-aware threshold)
  - If `--motion PLG` + `--acv SMB`, soften the Challenger ceiling (per `frameworks.md` Framework 5 stage-aware threshold)
- Write a one-sentence improvement recommendation.

Sum to a composite 0–10. Map to interpretive band (0–3 broken / 3–5 weak / 5–7 competent / 7–8.5 strong / 8.5–10 exceptional).

**If `--grade-only` was passed:** skip Stages 4 and 5 entirely. Proceed directly to Stage 6's report-writing substep. The report includes only sections 1, 2, and 3 of the output schema (composite scorecard, per-framework breakdown, Fletch findings) plus a closing note explaining that variants were skipped. Then stop.

### Stage 4: Three-variant generation

Read `references/exemplars.md` and `references/fletch-detectors.md` (especially the "Fletch generation rules" and "seven structural patterns" sections) before generating.

Generate exactly three variants:

- **Variant A — narrow-and-sharp** (Dunford-style; narrow ICP; explicit competitive alternative; fast sales cycle). Use the Who/What/Why or Outcome-first pattern.
- **Variant B — category-led** (Raskin + Play Bigger style; claims or reshapes a category; longer evangelism cycle; higher ambition). Use the Category-led or Mechanism-led pattern. **If `--stage seed/A`, do not generate a category-invention H1** — anchor to existing category + modifier instead.
- **Variant C — outcome-quantified** (JTBD + VPC style; leads with a specific measurable outcome on a high-importance under-satisfied job). Use the Outcome-first or Problem-first pattern.

For each variant:

1. Generate an **H1** — 6–12 words, ~55–70 characters. Apply Fletch generation rules: category + modifier (G1), capability over benefit (G2), single-line constraint (G3), named ICP (G5), no forbidden words (G6).
2. Generate a **subhead** — 12–25 words, doing exactly one job (elaborate / specify audience / name mechanism / provide proof / contrast status quo / quantify outcome). Apply pairing rules from `fletch-detectors.md` (G4).
3. Identify the variant's **best-fit ICP** — persona + company type + context.
4. Derive **2–4 value pillars** for the variant using Dunford's "list every feature, ask 'so what?', group by value outcome" method.
5. Select **3 reinforcing features** mapped to the pillars. Each feature must be:
   - Differentiated vs. named competitive alternatives
   - Directly enable a pillar's outcome
   - Demonstrable in a sales pitch or demo
   - Expressible as a Fletch capability statement (verb + concrete object — what the user *does*)

Validate each generated H1 against:
- Length (6–12 words; 13+ requires punctuation justification)
- Forbidden-words list (G6)
- Harry Dry test (visualizable / falsifiable / unique)
- Fletch one-sentence test

If a generated H1 fails validation, regenerate it. Do not ship a flagged H1.

### Stage 5: Seven-axis pros/cons

Read `references/tradeoff-axes.md` for the full axis descriptions.

For each variant, score all seven axes (+ / 0 / −) and write a 1–2 sentence rationale per axis:

1. TAM vs. specificity
2. Category creation vs. category entry
3. Competitive defensibility (Hamilton Helmer's 7 Powers)
4. Messaging clarity vs. expansiveness
5. VC-readable vs. customer-readable
6. Sales cycle and GTM fit
7. Buyer committee multi-threading

Apply stage / ACV / motion adjustments per the rules in `tradeoff-axes.md`.

After all three variants are scored, run the **coherence check**: flag any variant whose axis combination is structurally infeasible for the company's stage (e.g., seed-stage + category-creation + enterprise-buying-committee + PLG motion).

### Stage 6: Recommendation, message house, and surface adaptations

**Recommendation logic:**

- If `--stage` was provided, tag one variant as recommended per the table in `tradeoff-axes.md` ("How the recommendation is chosen"):
  - `seed` → Variant A (unless coherence-flagged; if flagged, fall back to Variant C)
  - `A` → Variant A or C (whichever has higher coherence + stronger axis 1 and axis 5 scores; if tied, prefer A)
  - `B+` → Variant B or C (whichever has higher coherence + stronger axis 2 and axis 4 scores; if tied, prefer C)
- If `--stage` was NOT provided, present all three variants neutrally with no recommendation tag, and add the "your stage matters" note.

**Message house** (only for the recommended variant — skip if no recommendation):
- **Roof** — single-sentence positioning combining category + audience + capability + outcome
- **Three pillars** — pillar names from Stage 4, each with a one-sentence pillar statement and 2–4 proof points
- **Tagline** (optional, 3–7 words)

**Surface adaptations** (only for the recommended variant — skip if no recommendation):
- Pitch deck title slide
- LinkedIn company tagline
- Sales cold-email opener
- Product Hunt launch
- Sales one-liner ("elevator")

Read `references/output-schema.md` for surface-specific constraints (character limits, format).

#### Stage 6 (final substep): Write report and print summary

Read `references/output-schema.md` for the exact report structure.

1. **Determine output filename:**
   - Extract domain from URL (strip `https://`, `www.`, take everything before the first `.`)
   - Use today's date (ISO `YYYY-MM-DD`)
   - Filename: `positioning-<domain>-YYYY-MM-DD.md`
   - If the file already exists for today's date and same domain, append `-v2`, `-v3`, etc.
2. **Ensure directory exists:** run `mkdir -p ~/Desktop/claude-code/`
3. **Write the report** using the Write tool, following the schema in `references/output-schema.md` exactly. Do not add or omit sections.
4. **Print the terminal summary** following the format in `references/output-schema.md` "Terminal summary structure".

## Defaults and conventions

- Do not weight the five frameworks. The orthogonality argument depends on equal weighting.
- Score in 0.5 increments only. Do not output 0.3 or 0.7.
- Quote homepage copy verbatim — never paraphrase, never invent.
- When in doubt between two adjacent score bands, choose the lower one. Generous scoring corrupts the signal.
- Generated H1s and subheads must pass all Fletch generation rules and both ruthless tests before being included in the report.
- The report file is the canonical output. The terminal summary is a pointer.

## Additional resources

### Reference files

For detailed rubrics, detectors, exemplars, and output structure, consult:

- **`references/frameworks.md`** — Five scoring rubrics with all 0–2.0 bands, diagnostic questions, and stage-aware thresholds
- **`references/fletch-detectors.md`** — 13 failure-pattern + 7 positive-signal detectors, the 9-element clarity heatmap, the seven structural patterns, the Fletch generation rules (G1–G6), and the two ruthless tests (Harry Dry + Fletch one-sentence)
- **`references/tradeoff-axes.md`** — Seven pros/cons dimensions, coherence-check rules, and stage-aware recommendation logic
- **`references/exemplars.md`** — Eight high-signal homepage exemplars (Linear, Stripe, Notion, Gong, Superhuman, Attio, Vanta, Clay) with H1, subhead, pattern, and per-exemplar lesson
- **`references/output-schema.md`** — Exact markdown report structure, terminal summary structure, file naming convention, and `~/Desktop/claude-code/` directory handling
