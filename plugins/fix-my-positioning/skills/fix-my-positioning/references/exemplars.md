# Homepage exemplars

Eight high-signal B2B SaaS hero sections, captured 2026-04-23. Use these as **calibration references** during scoring (what does a 1.5 or 2.0 actually look like?) and as **structural patterns** during generation (what does a category-led H1 sound like in practice?).

**Caveat.** These are snapshots. Live homepages change. If a quoted H1 turns up materially different at runtime, treat the exemplar as historical and rely on the structural lesson, not the verbatim copy.

---

## The eight exemplars

### 1. Linear — Category-led + contrarian
- **H1:** *The product development system for teams and agents*
- **Subhead:** *Purpose-built for planning and building products. Designed for the AI era.*
- **Pattern:** Category-led ("system" + "product development" + "for teams and agents")
- **H1 length:** 8 words
- **Why it works:** Names a category ("product development system"), names an audience ("teams and agents"), drops a trend hook ("AI era") without being lazy. Pairs with a contrarian "Issue tracking is dead" strip below.
- **Lesson:** A category-led headline can include a trend layer in the subhead without falling into vagueness.

### 2. Stripe — Mechanism-led
- **H1:** *Financial infrastructure to grow your revenue*
- **Subhead:** *Millions of companies use Stripe's software and APIs to accept payments, send payouts, and manage their businesses online.*
- **Pattern:** Mechanism-led ("financial infrastructure")
- **H1 length:** 6 words
- **Why it works:** "Financial infrastructure" is a mechanism frame Stripe earned over a decade. The subhead does proof + scope.
- **Lesson:** Mechanism framing is only legitimate when the company is a category leader. Do not generate this pattern for early-stage startups.

### 3. Notion — Category-led with trend layer
- **H1:** *The AI workspace that works for you.*
- **Subhead:** *One place where teams find every answer, automate the busywork, and get projects done.*
- **Pattern:** Category-led ("workspace") with trend modifier ("AI")
- **H1 length:** 7 words
- **Why it works:** Existing category ("workspace") + modifier ("AI"). Subhead does outcome triad.
- **Lesson:** Category + modifier is the safe play. Notion didn't invent "AI workspace" — they staked the strongest claim to it.

### 4. Gong — Category-led + social proof
- **H1:** *The #1 AI operating system for Revenue Teams*
- **Subhead:** *Trusted by 5,000+ customers. Built to help your revenue team crush goals, close with confidence, and keep growing.*
- **Pattern:** Category-led + superlative + named audience + social proof above fold
- **H1 length:** 9 words
- **Caution:** "AI operating system" is borderline category-invention — only legitimate because Gong is a Series F category leader. **Do not generate "operating system" for any pre-Series-B company.** This would trigger the F1 (category inflation) detector.
- **Lesson:** Superlative + audience + proof works at scale. Earlier-stage companies must earn the superlative differently.

### 5. Superhuman — Superlative + quantified outcome
- **H1:** *The most productive email app ever made*
- **Subhead:** *Save 4 hours every week with Superhuman Mail.*
- **Pattern:** Superlative + outcome (quantified)
- **H1 length:** 8 words
- **Why it works:** "4 hours every week" is a falsifiable claim. The subhead does the quantify-outcome job, single-purpose.
- **Lesson:** Pair a superlative H1 with a quantified outcome subhead — the proof in the subhead earns the superlative in the H1.

### 6. Attio — Emotional hook + rational positioning
- **H1:** *Customer relationship magic.*
- **Subhead:** *Attio is the AI CRM for GTM.*
- **Pattern:** Emotional hook H1 + category-led subhead
- **H1 length:** 3 words; Subhead: 6 words
- **Why it works:** "Magic" is emotional and unfalsifiable in isolation, but the subhead immediately rationalizes with a tight category + modifier ("AI CRM for GTM"). This is the **dual-line template** — emotional H1, rational subhead.
- **Lesson:** Short emotional H1s are allowed *only* when paired with a subhead that names a clear category and audience. Without the subhead, this would trigger F4 (abstract verb / vague claim) and F10 (missing ICP).

### 7. Vanta — Outcome-first verb triad
- **H1:** *Automate compliance, manage risk, and accelerate trust with AI*
- **Subhead:** *Vanta helps you get compliant fast… Trusted by 15,000+ customers.*
- **Pattern:** Outcome-first (verb triad) + social proof
- **H1 length:** 9 words
- **Caution:** Three verbs in one H1 risks triggering F7 (feature dump). Vanta gets away with it because the verbs are unified by a single product domain (compliance) and the trend modifier ("with AI") at the end. Do not generate this pattern unless the verbs unify around one domain.
- **Lesson:** Multi-verb H1s only work when there's one obvious unifying topic.

### 8. Clay — Outcome + proof
- **H1:** *Go to market with unique data — and the ability to act on it*
- **Subhead:** *Proof-led: OpenAI case (40% → 80% enrichment coverage).*
- **Pattern:** Outcome-first + proof-led
- **H1 length:** 13 words (over the recommended 12-word ceiling)
- **Caution:** 13 words is at the high end. Justified here because the dash creates two phrases; would not work as one continuous clause.
- **Lesson:** When breaking the 12-word ceiling, use punctuation to create two parseable phrases.

---

## Cross-pattern findings

- **Average H1 length:** 7–9 words across the exemplars
- **Every H1** names at least one of: category, audience, or quantified outcome. None use pure abstraction.
- **Every subhead** does exactly one or two clear jobs (proof, audience, mechanism, quantified outcome). No subhead tries to do three jobs at once.
- **Dual CTAs** (free/self-serve + sales/demo) are near-universal for PLG companies. Watch for this in extracted homepages.
- **Six of eight** surface social proof above the fold (Gong, Vanta, Linear, Notion, Stripe via "millions of companies," Clay via OpenAI case).

---

## How to use this file during the GENERATION stage

When generating a variant:

1. Pick the structural pattern that fits the variant strategy (see `fletch-detectors.md` → "The seven structural patterns").
2. Find the closest exemplar above. Match its structural shape, NOT its words.
3. Validate the generated H1 against:
   - Length (6–12 words preferred; 13+ requires punctuation justification)
   - Forbidden-words list (in `fletch-detectors.md`, rule G6)
   - Harry Dry test (visualizable / falsifiable / unique)
   - Fletch one-sentence test
4. Validate the subhead does exactly one of the six jobs.

Never quote an exemplar's headline verbatim in a generated variant. The exemplars are calibration anchors, not templates to mimic.
