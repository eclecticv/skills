# Shared Procedures

Common procedures used by the `/saas-grader:saas` command.

## Step 0: Classify the Site (BEFORE scoring anything)

Roughly half the rules are conditional on what kind of product this is. Decide these
questions ONCE, up front, record them in the report, and score every conditional rule
against this declared classification. Never re-decide a classification inside an
individual rule.

Record each answer WITH its evidence:

| Dimension | Values | Evidence to cite |
|-----------|--------|------------------|
| Audience | B2B / B2C / both | who the copy addresses, pricing structure, logos shown |
| Buying motivation | utilitarian (effective/reliable) / hedonic (fun/exciting) / mixed | product category, copy tone |
| Brand maturity | new (<5 years) / established | founding signals, copyright years, funding news, domain age |
| Monetization | free trial / freemium / paid-only / sales-led | signup CTAs, pricing page |
| Pricing model | flat / per-seat / usage-based / hybrid / opaque | pricing page structure |
| Experience-related | yes / no (travel, booking, lifestyle) | product category |

Rules that depend on classification: BM-4 (maturity), PD-1/PD-2 (motivation, audience),
PD-3 (maturity, experience), PD-9 (motivation), PR-8 (pricing model), FT-* (monetization),
FM-* (monetization). Their verdicts must reference the classification, e.g.
"Classified utilitarian → structured design expected."

## Evidence Collection Procedure

Evidence is collected in three passes, best-first. Record which pass produced each
piece of evidence — it determines the confidence level of every verdict.

### 1. Rendered DOM extraction (primary — measured evidence)

Find a Chromium binary (first hit wins):

```bash
CHROME=$(for c in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "$(which google-chrome-stable 2>/dev/null)" \
  "$(which google-chrome 2>/dev/null)" \
  "$(which chromium 2>/dev/null)" \
  "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
  "/Applications/Arc.app/Contents/MacOS/Arc" \
  "/Applications/ego lite.app/Contents/MacOS/ego lite" \
  $HOME/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell \
  ; do [ -x "$c" ] && echo "$c" && break; done)
```

Dump the rendered DOM (JS-rendered — works on SPA sites where plain fetches return an
empty shell), then distill it to a signals JSON:

```bash
( "$CHROME" --headless --disable-gpu --virtual-time-budget=8000 --dump-dom "[url]" > homepage.html 2>/dev/null & \
  CP=$!; ( sleep 30 && kill $CP 2>/dev/null ) & W=$!; wait $CP 2>/dev/null; kill $W 2>/dev/null )
node "${CLAUDE_PLUGIN_ROOT}/scripts/extract-signals.mjs" homepage.html > homepage-signals.json
```

The signals JSON contains measured facts: title, headings in order, CTA button texts,
nav links, price tokens with context, per-unit pricing mentions, numeric social proof,
star ratings, trial-length mentions, freemium signals ("$0", "free plan"), video/GIF
presence, font-family declarations, testimonial candidates, paragraph-length stats,
and founding-year signals. Rules marked `dom` in the scoring table MUST be scored from
this JSON, not from prose impressions.

Then find the pricing page in `navLinks` (href containing pricing/plans) and repeat
both commands for it (`pricing.html` → `pricing-signals.json`).

If Node is unavailable, read the dumped HTML directly for the same signal patterns and
note the fallback. If no Chromium binary exists, fall back to WebFetch (pass 3).

### 2. Screenshots (visual evidence)

Screenshot BOTH the homepage and the pricing page (position/shape rules need the
pricing page too — do not score PR-3/PR-4 from text):

```bash
( "$CHROME" --headless --disable-gpu --no-sandbox --disable-extensions --disable-background-networking --disable-sync --disable-translate --disable-default-apps --js-flags="--max-old-space-size=256" --screenshot="[company]-homepage.png" --window-size=1280,900 "[url]" 2>/dev/null & CHROME_PID=$!; ( sleep 30 && kill $CHROME_PID 2>/dev/null ) & WATCHDOG=$!; wait $CHROME_PID 2>/dev/null; kill $WATCHDOG 2>/dev/null ); if [ ! -f "[company]-homepage.png" ]; then echo "Screenshot failed or timed out — proceeding without it"; fi
```

- Read each screenshot with the Read tool, then delete it
- Never retry a failed screenshot; never use heights above 900px
- If screenshots fail, rules marked `screenshot` in the scoring table are scored from
  DOM/text at reduced confidence, or UNVERIFIED if the DOM can't answer them

### 3. WebFetch (fallback only)

If both passes above fail, crawl homepage and pricing page via WebFetch (50KB limit).
All verdicts from this pass are Low confidence; visual rules become UNVERIFIED.

### Reference files

Read reference files in batches as you score each section (do NOT load all 8 at once):
brand-messaging.md (BM), page-design.md (PD), pricing-plans.md (PR), free-trials.md (FT),
freemium.md (FM), churn-prevention.md (CP), affiliates.md (AF), referrals.md (RF).

## Verdicts

Four verdicts. Every rule gets exactly one:

- **PASS / FAIL** — only when evidence exists. The verdict MUST cite which specific
  PASS/FAIL criterion bullet fired, quoting the evidence (headline text, measured
  count, screenshot observation).
- **N/A** — the rule genuinely doesn't apply to this site (e.g. video speed with no
  video, freemium decoy with no freemium). Excluded from the denominator.
- **UNVERIFIED** — the rule applies but the available evidence can't answer it.
  Excluded from the denominator, and the report states what would verify it
  (e.g. "requires seeing the cancellation flow"). NEVER convert uncertainty into a
  FAIL: a FAIL is a claim about the site, not about our visibility into it.

**Evidence before verdict:** in the report, the Observation (quotes, measurements)
comes BEFORE the Compliance verdict, and the verdict line names the criterion that
fired. If you cannot write a concrete observation, the verdict is UNVERIFIED.

**Confidence:** each PASS/FAIL carries a confidence level determined by its evidence
source: **High** = measured from signals JSON or read directly off a screenshot;
**Medium** = inferred from rendered DOM text; **Low** = inferred from WebFetch text.

## Rigor Protocol (symmetric)

Before finalizing ANY verdict — PASS or FAIL — argue the other side:

1. **Re-read the opposite criteria** — for a PASS, does any FAIL bullet apply, even
   partially? For a FAIL, does the evidence actually satisfy the PASS bullets?
2. **Apply the "stranger test"** — would a first-time visitor with no industry
   knowledge understand this? Don't project your own familiarity onto the visitor.
3. **Separate headline from page** — if the headline alone doesn't pass but supporting
   copy below the fold does, note the gap. The headline carries most of the weight.
4. **Watch for borrowed positioning** — "X for Y" comparisons can mask weak
   self-description. Evaluate whether messaging stands on its own.
5. **No cheerleading, no pessimism ratchet** — observations are analytical in both
   directions. Note what could be stronger on PASSes, and what is genuinely fine on
   FAILs. A FAIL must identify a real defect, not a theoretical one.

## Scoring Table

Every rule has a fixed tier, evidence grade, impact grade, and weight. These are
static — do not re-derive them at runtime.

- **Tier:** `mech` = scored from measured data (signals JSON / screenshot) via the
  rule's decision procedure · `judg` = anchored model judgment · `prac` = operational
  practice not reliably observable from the website — reported in the Practices Review
  appendix, EXCLUDED from all grades (scored informationally only when evidence happens
  to be visible)
- **Evidence grade** (of the underlying research): 3 = field experiment / large-scale
  observational · 2 = lab experiments or industry eyetracking · 1 = practitioner consensus
- **Impact grade:** 3 = large measured effect (>30%) or conversion-critical placement ·
  2 = moderate · 1 = small or indirect
- **Weight = evidence + impact** (range 2–6)

| Rule | Tier | Verify via | Ev | Imp | Weight |
|------|------|-----------|----|-----|--------|
| BM-1 | judg | dom (h1/subhead) | 2 | 3 | 5 |
| BM-2 | judg | dom + screenshot | 2 | 2 | 4 |
| BM-3 | judg | dom text | 1 | 1 | 2 |
| BM-4 | mech | dom (brandAge) + classification | 1 | 1 | 2 |
| BM-5 | judg | dom text | 2 | 2 | 4 |
| BM-6 | mech | dom (socialProof.numbers) | 2 | 3 | 5 |
| BM-7 | mech | dom (starRatings) | 2 | 2 | 4 |
| BM-8 | judg | dom (testimonialCandidates) | 3 | 2 | 5 |
| PD-1 | judg | screenshot + classification | 2 | 2 | 4 |
| PD-2 | judg | screenshot + classification | 2 | 1 | 3 |
| PD-3 | judg | screenshot + classification | 2 | 2 | 4 |
| PD-4 | judg | screenshot | 2 | 1 | 3 |
| PD-5 | mech | screenshot | 3 | 3 | 6 |
| PD-6 | mech | screenshot + dom (fontFamilies) | 1 | 1 | 2 |
| PD-7 | mech | screenshot | 2 | 2 | 4 |
| PD-8 | mech | screenshot | 2 | 1 | 3 |
| PD-9 | mech | dom (video) + classification | 2 | 2 | 4 |
| PD-10 | judg | video content | 2 | 1 | 3 |
| PD-11 | mech | screenshot | 2 | 3 | 5 |
| PD-12 | mech | dom (textStats) | 2 | 2 | 4 |
| PD-13 | judg | dom (headings) | 2 | 2 | 4 |
| PD-14 | judg | dom + screenshot | 2 | 2 | 4 |
| PR-1 | mech | pricing dom/screenshot | 2 | 3 | 5 |
| PR-2 | judg | pricing dom | 2 | 2 | 4 |
| PR-3 | mech | pricing screenshot | 2 | 1 | 3 |
| PR-4 | mech | pricing screenshot | 2 | 1 | 3 |
| PR-5 | judg | pricing dom | 2 | 2 | 4 |
| PR-6 | judg | pricing dom | 2 | 3 | 5 |
| PR-7 | mech | pricing dom (arithmetic) | 2 | 1 | 3 |
| PR-8 | judg | pricing dom + classification | 2 | 2 | 4 |
| PR-9 | mech | pricing dom | 2 | 2 | 4 |
| FT-1 | judg | pricing/trial dom | 3 | 2 | 5 |
| FT-2 | mech | dom (trialMentions) | 3 | 3 | 6 |
| FT-3 | prac | site-ops (onboarding) | 3 | 2 | 5 |
| FT-4 | prac | site-ops (trial-end flow) | 2 | 2 | 4 |
| FM-1 | mech | pricing dom | 3 | 3 | 6 |
| FM-2 | judg | pricing dom | 3 | 2 | 5 |
| CP-1 | prac | site-ops | 2 | 2 | 4 |
| CP-2 | prac | site-ops | 3 | 2 | 5 |
| CP-3 | prac | site-ops (cancel flow) | 2 | 2 | 4 |
| AF-1 | prac | affiliate terms | 2 | 1 | 3 |
| AF-2 | prac | affiliate terms | 2 | 1 | 3 |
| RF-1 | judg | referral page | 3 | 3 | 6 |
| RF-2 | judg | referral flow | 3 | 2 | 5 |
| RF-3 | judg | referral page | 2 | 2 | 4 |
| RF-4 | judg | referral page | 3 | 2 | 5 |
| RF-5 | judg | referral page | 2 | 2 | 4 |

## Grades

Two numbers per section and overall:

1. **Raw:** passes / applicable (PASS+FAIL only; N/A and UNVERIFIED excluded)
2. **Weighted:** sum of weights of passing rules / sum of weights of applicable rules

The letter grade is computed from the **weighted** percentage. Practice-tier rules
(FT-3, FT-4, CP-*, AF-*) never enter either number — their sections (Churn Prevention,
Affiliates) appear as an ungraded Practices Review, and Free Trials is graded on
FT-1/FT-2 only.

| Grade | Weighted pass rate |
|-------|-----------|
| A+ | 100% |
| A | 90-99% |
| A- | 85-89% |
| B+ | 80-84% |
| B | 75-79% |
| B- | 70-74% |
| C+ | 65-69% |
| C | 60-64% |
| C- | 55-59% |
| D+ | 50-54% |
| D | 45-49% |
| D- | 40-44% |
| F | Below 40% |

Always print the denominators next to a grade ("weighted 41/58 across 14 applicable
rules") — grade movement caused by denominator changes is noise, not signal.

## Priority Computation

Priority is computed per FAIL, not looked up from a static list:

1. Classify the fix effort: **copy** change (+3) · **design** change (+2) ·
   **product/pricing** change (+0)
2. Priority points = rule weight + effort bonus
3. **Critical (Fix This Week)** ≥ 8 · **Medium (Fix This Month)** 5–7 · **Low (Backlog)** ≤ 4

This naturally ranks "add '10,000+ users' to the hero" (weight 5 + copy 3 = 8,
Critical) above "restructure trial length" (weight 6 + product 0 = 6, Medium).
Use judgment only to break ties or demote a technically-Critical item that the
classification makes marginal.

## Delta vs Previous Run

Before writing the report, look for the most recent previous report for the same
company in the output directory and read its `## Machine-Readable Results` JSON block.
If found, add a **Changes Since Last Audit** section listing every verdict flip, each
with a stated cause:

- **site-changed** — quote the before/after evidence
- **re-evaluation** — the site is unchanged; explain what the grader reads differently
  now (these are the flips to be suspicious of)
- **procedure-changed** — the rule's criteria or evidence pipeline changed between
  plugin versions

## Company Name Extraction

Extract the company name from the page title or domain, using the brand name only
(e.g., for `https://www.acme.com`, use `acme`; for a page titled "Acme - Project
Management", use `acme`).

## Notes

- **Screenshot memory safety:** keep the 30-second watchdog, 256MB JS heap, and
  1280×900 window. Never retry a failed screenshot.
- The signals JSON is the source of truth for `dom`-verified rules. If the model's
  impression of the page conflicts with an extracted signal, trust the signal or
  explain the discrepancy in the observation.
- Font evidence from a DOM dump is partial (external CSS is not included) — corroborate
  with the screenshot before failing PD-6.
- If no pricing page is found, note it; pricing rules that require pricing-page content
  become UNVERIFIED (not FAIL, not silently N/A).
