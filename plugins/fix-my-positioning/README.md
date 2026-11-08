# Fix My Positioning

**A B2B positioning audit and rewrite, grounded in the five frameworks that actually move the needle.**

Most positioning tools grade homepages against a single rubric — usually a watered-down version of one famous framework — and tell you to "be more specific." `Fix My Positioning` does the opposite: it scores your positioning across **five orthogonal diagnostic frameworks**, runs the most battle-tested public methodology for B2B homepage execution against your hero section, and writes you three alternative positioning variants you can put in front of customers tomorrow.

```bash
/fix-my-positioning https://your-startup.com --stage A --acv enterprise --motion sales
```

A markdown report lands in `~/Desktop/claude-code/`. Composite score, per-framework breakdown, structural critique, three rewrites, and a message house for the recommended variant.

---

## Why another positioning tool

Most positioning audits collapse into one of two failure modes:

1. **Single-rubric tunnel vision.** They use one framework (usually a stripped-down Dunford or a cargo-culted "value prop canvas") and miss the four other axes that actually decide whether positioning lands.
2. **Generic conversion advice.** "Lead with the benefit, not the feature." "Use action verbs." "Add social proof." None of which tells you whether your *strategic positioning* is broken or whether your *homepage execution* is broken — or both.

This plugin separates the two layers explicitly.

**Diagnostic layer (strategic):** Five frameworks, each evaluating a genuinely distinct dimension. None of the five is a substitute for any of the other four — they could each score a maximum while the others score zero. That's the test of orthogonality.

**Execution layer (tactical):** Fletch PMM's detector module — 13 failure-pattern detectors and 7 positive-signal detectors — applied to your actual homepage hero. This is the same methodology Anthony Pierri and Rob Kaminski have used to rewrite 400+ B2B SaaS homepages.

You get a number, you get evidence, you get specific things to change, and you get three different rewrites with their tradeoffs spelled out.

---

## The five diagnostic frameworks

Each framework scores 0–2.0 in 0.5 increments. Composite score: 0–10.

| # | Framework | Source | Dimension scored |
|---|---|---|---|
| 1 | **Obviously Awesome** (5 components) | April Dunford, *Obviously Awesome* (2019) | Competitive differentiation against real alternatives — including status quo |
| 2 | **Jobs-to-Be-Done + ODI** | Christensen + Ulwick (HBR 2016 / 2005) | Customer job clarity across functional / emotional / social dimensions |
| 3 | **Strategic Narrative** (5-part) | Andy Raskin (2016, 2.5M+ views) | Narrative arc — change, enemy, Promised Land, obstacles, proof |
| 4 | **Value Proposition Canvas** | Osterwalder, *Value Proposition Design* (2014) | Value-map fit to ranked pains and gains |
| 5 | **Challenger Sale** | Dixon & Adamson (2011) — CEB/Gartner research | Commercial insight + buying-committee multi-thread |

Composite bands: **0–3** broken, **3–5** weak, **5–7** competent, **7–8.5** strong, **8.5–10** exceptional.

The execution-layer authority for the homepage critique is **[Fletch PMM](https://fletchpmm.com/)** — their 9-element positioning model runs as a clarity heatmap, their 13+7 detectors run as structural critique, and their category-modifier and capability-over-benefit rules constrain every generated variant.

---

## What you get

A single command produces a structured markdown report with:

1. **Composite scorecard** with per-framework scores and the weakest element of each
2. **Per-framework breakdown** — verbatim quotes from your homepage as evidence, the gap analysis, and a one-sentence improvement recommendation per framework
3. **Fletch execution-layer findings** — every triggered failure pattern with the offending copy and a suggested fix; every positive signal with the rewarded copy; the 9-element clarity heatmap
4. **Three positioning variants** — narrow-and-sharp, category-led, and outcome-quantified — each with:
   - An H1 (6–12 words, validated against forbidden-word and ruthless-test rules)
   - A subhead doing exactly one job
   - Three reinforcing features mapped to value pillars, each expressed as a Fletch capability statement
   - A 7-axis tradeoff matrix (TAM, category risk, defensibility, clarity, VC vs. customer legibility, sales cycle, buyer-committee fit)
   - A coherence flag if the variant is structurally infeasible for your stage
5. **Recommendation** — one variant tagged "recommended" if you provided `--stage`, with a validation plan
6. **Message house** for the recommended variant — roof, pillars, proof points, optional tagline
7. **Surface adaptations** — pitch deck title, LinkedIn tagline, cold-email opener, Product Hunt copy, sales one-liner — all derived from the recommended variant with surface-specific character constraints applied

---

## Install

```bash
# In Claude Code:
/plugin marketplace add eclecticv/skills
/plugin install fix-my-positioning@andorlabs
```

That's it. The slash command `/fix-my-positioning` becomes available in any Claude Code session.

---

## Usage

```bash
/fix-my-positioning <url> [--stage seed|A|B+] [--acv SMB|mid|enterprise] [--motion PLG|sales|hybrid] [--grade-only]
```

### Examples

**Quick audit only — no rewrite, lowest token cost:**
```bash
/fix-my-positioning https://attio.com --grade-only
```

**Full audit + three rewrites + recommendation, with context:**
```bash
/fix-my-positioning https://example.com --stage seed --acv SMB --motion PLG
```

**No context flags — get all three variants without an auto-recommendation:**
```bash
/fix-my-positioning https://example.com
```

### Why the context flags matter

`--stage`, `--acv`, and `--motion` shape **scoring thresholds** and **recommendation logic**:

- `--stage seed` caps the score on category-creation claims (Dunford and Play Bigger both warn against pre-Series-B category creation), and recommends the narrow-and-sharp variant by default
- `--motion PLG` + `--acv SMB` softens the Challenger-framework ceiling (multi-stakeholder commercial insight isn't required for bottom-up SMB PLG), and weighs the buyer-committee axis differently
- `--motion sales` + `--acv enterprise` enforces the full Challenger rubric and weighs category-led variants more favorably

Skip the flags if you want a neutral grade with no auto-recommendation.

---

## How it works

```
INPUT          →  /fix-my-positioning <url> [flags]
                  ↓
EXTRACTION     →  positioning-extractor agent fetches homepage (+ About / pricing if linked),
                  pulls hero H1 / subhead / CTAs / social proof / category claims verbatim,
                  runs the 13 Fletch failure detectors and 7 positive detectors,
                  scores the 9-element clarity heatmap
                  ↓
SCORING        →  five framework rubrics applied independently (Dunford, JTBD/ODI, Raskin,
                  VPC, Challenger), each 0–2.0 with verbatim evidence and weakest-element
                  diagnosis
                  ↓
                  IF --grade-only → write report (sections 1–3) + stop
                  ↓
GENERATION     →  three variants (narrow-and-sharp / category-led / outcome-quantified)
                  with H1 + subhead + 3 capability-led features per variant,
                  Fletch generation rules enforced (category + modifier; capability over
                  benefit; forbidden-word list; Harry Dry test; Fletch one-sentence test)
                  ↓
PROS/CONS      →  7-axis tradeoff matrix per variant + coherence check
                  ↓
RECOMMENDATION →  stage-aware tagging + message house + surface adaptations
                  ↓
OUTPUT         →  ~/Desktop/claude-code/positioning-<domain>-YYYY-MM-DD.md
```

The pipeline delegates homepage extraction to a sub-agent so raw HTML never pollutes the main scoring context. The five framework rubrics, the Fletch detector module, the seven tradeoff axes, the calibrated homepage exemplars, and the output schema all live in reference files that load on demand — keeping the orchestrator lean (~1,600 words) while making the underlying methodology fully inspectable.

---

## What's inside

```
fix-my-positioning/
├── .claude-plugin/
│   └── plugin.json               (manifest)
├── agents/
│   └── positioning-extractor.md  (homepage fetch + Fletch detector module)
└── skills/fix-my-positioning/
    ├── SKILL.md                  (six-stage pipeline orchestrator)
    └── references/
        ├── frameworks.md         (5 scoring rubrics, 0–2.0 bands, diagnostic questions)
        ├── fletch-detectors.md   (13 failure + 7 positive detectors, 9-element heatmap, generation rules)
        ├── tradeoff-axes.md      (7 pros/cons axes, recommendation logic)
        ├── exemplars.md          (8 calibrated homepage exemplars: Linear, Stripe, Notion, Gong, Superhuman, Attio, Vanta, Clay)
        └── output-schema.md      (exact markdown report structure)
```

---

## Methodology and credits

Built on a research foundation that synthesizes:

- **April Dunford** — *Obviously Awesome* (2019), *Sales Pitch* (2023), and the aprildunford.com positioning essays
- **Clayton Christensen** — *"Know Your Customers' Jobs to Be Done"* (HBR, Sept 2016) and *Competing Against Luck* (2016)
- **Tony Ulwick** — *What Customers Want* (2005) and Outcome-Driven Innovation
- **Andy Raskin** — *"The Greatest Sales Deck I've Ever Seen"* (Medium, 2016) and the strategic-narrative essays
- **Alexander Osterwalder, Yves Pigneur et al.** — *Value Proposition Design* (Wiley, 2014)
- **Matthew Dixon & Brent Adamson** — *The Challenger Sale* (Portfolio, 2011) and *The Challenger Customer* (2015)
- **Fletch PMM** (Anthony Pierri & Rob Kaminski) — methodology, 9-element positioning model, capability-over-benefit rule, and the failure-pattern teardowns
- **Hamilton Helmer** — *7 Powers* (2016)
- **Ramadan, Peterson, Lochhead, Maney** — *Play Bigger* (2016) for category-creation tradeoff data
- **Harry Dry** (marketingexamples.com), Nielsen Norman Group, CXL Institute — for hero-section structural patterns and conversion evidence

The plugin's defensibility lies in non-overlapping framework orthogonality at the diagnostic layer and in grounding execution in the most battle-tested public methodology for B2B homepages at the output layer.

---

## Status

**v0.1.0** — early. The five rubrics, twenty Fletch detectors, seven tradeoff axes, and eight calibration exemplars are all in place. Expect the first few audits to surface refinements you'll want to make to the detector aggressiveness or the variant generation prompts. Edit the reference files in `skills/fix-my-positioning/references/` — they're the source of truth.

Issues, feedback, and pull requests welcome.

---

## License

MIT — see [LICENSE](LICENSE).

---

*Built by [And/or Labs](https://andorlabs.ca) — distributed via the andorlabs Claude Code marketplace.*
