# Seven tradeoff axes for variant pros/cons analysis

When the GENERATION stage produces three positioning variants, each variant must be evaluated against these seven dimensions. The Pros/Cons stage of the report uses this scoring.

For each variant, score each axis on a scale:
- **+** strong fit / advantage
- **0** neutral
- **−** weak fit / liability

Then write a 1–2 sentence rationale per axis per variant.

---

## Axis 1: TAM vs. specificity

**The tradeoff.** Narrow positioning wins pre-PMF and crossing-the-chasm (Moore's bowling alley); Thiel's *Zero to One* rule is *"start small and monopolize."* Broad positioning wins post-PMF when the platform can straddle multiple segments.

**The trap.** Dunford's "Oh Crap" segmentation problem — the narrowest best-fit segment is sometimes too small to hit revenue goals. Fletch: *"refusing to choose use cases to anchor on, you'll always lose to someone who's willing to go that extra level of specificity."*

**Stage adjustment.**
- Seed / Series A → favor narrow (+ for narrow variants, − for broad)
- Series B+ → balanced
- Series C+ → favor expansion-readiness (+ for broader variants if defensibility holds)

---

## Axis 2: Category creation vs. category entry

**The tradeoff.** Play Bigger's dataset (~2,694 VC transactions) shows Category Kings capture ~76% of total category market cap and generate $5.6 of market cap per dollar of revenue — but *"a six-year-old startup that wasn't yet a king had almost zero chance of becoming one."* Category creation is expensive and fails frequently.

**Mike Troiano:** *"Don't try to create a category."*

**Stage adjustment.**
- Seed / Series A → category creation almost always − (rate as critical risk, not just a con)
- Series B+ → category creation can be 0 or + if there's genuine market shift
- Always +: anchoring to existing category with a modifier

---

## Axis 3: Competitive defensibility

**Frame:** Hamilton Helmer's *7 Powers* (Scale Economies, Network Economies, Counter-Positioning, Switching Costs, Branding, Cornered Resource, Process Power).

**Counter-positioning** is especially valuable for startups — it frames differences from incumbents as selling points incumbents can't copy without cannibalizing (E*Trade vs. Schwab; Figma vs. Sketch on cloud-native; HubSpot vs. Marketo on pricing/ease).

Helmer: tech startups typically move counter-positioning → scale → switching costs → network economies, in that chronological order.

**Score each variant:** does the positioning frame the company in a way that makes the incumbent's moat irrelevant or actively harmful?

---

## Axis 4: Messaging clarity vs. expansiveness

**The tradeoff.** Narrow positioning is memorable but limits expansion narrative. Platform positioning is expansive but vague.

**Dunford:** *"If I pitch you my product and all I tell you is that it's a CRM, you would assume my competition is Salesforce."* Category labels trigger assumptions — narrow triggers specific assumptions (good for clarity, bad for TAM); broad triggers vague assumptions (big TAM, but "compared to what?" question kills conversion).

**Score:** which variant is most memorable in one sentence vs. which leaves the most room to grow?

---

## Axis 5: VC-readable vs. customer-readable

**First Round Review:** *"A great pitch deck makes for an ineffective website. It also makes terrible outbound copy."*

**Lenny Rachitsky:** *"Don't copy the messaging of later-stage companies. You're not Stripe, Airbnb or Figma. No one knows what you do yet. You need to spell it out clearly."*

At Seed/Series A:
- Deck → emphasizes TAM, category-king ambition, network effects (VC-readable)
- Homepage → emphasizes concrete JTBD, named alternatives, ROI (customer-readable)

Only at growth stage do the two converge.

**Score each variant:** is this hero copy that wins VC pitch meetings, or copy that wins customer demos? Flag if it's confused for the wrong audience.

---

## Axis 6: Sales cycle and GTM fit

**Tradeoff.** Challenger / category-creation positioning produces longer sales cycles (9–18 months) but higher ACV and retention — requires MEDDPICC rigor, analyst relations, multi-quarter education.

Commoditized / comparable positioning produces faster cycles but price compression — requires PLG, self-serve, fast onboarding.

**6sense 2025 data:** average B2B cycle is 10.1 months (down from 11.3 in 2024).

**Motion adjustment.**
- `--motion PLG` → narrow user-persona positioning fits best; flag any variant that requires a 6-month sales cycle as − for PLG fit
- `--motion sales-led` + `--acv enterprise` → category-led and Challenger-style positioning fits best
- `--motion hybrid` → favor variants with dual-CTA-friendly framing

---

## Axis 7: Buyer committee multi-threading

**Gartner.** B2B buying groups average 6–10 decision-makers; 72% of deals fail when buyers don't see clear value.

**Dunford:** *"Your biggest competitor is 'no decision.'"*

Positioning must address:
- **End user** — ease, speed
- **Champion** — career safety, "this makes me look smart"
- **Economic buyer** — ROI, TCO, payback
- **IT / security** — compliance, implementation risk

**Score each variant:** how many of these four roles does the positioning give explicit ammunition to? Score:
- + → 3+ roles addressed
- 0 → 2 roles addressed
- − → 1 role addressed (or only end user)

`--acv SMB` softens this rule; `--acv enterprise` enforces it strictly.

---

## Coherence check (run after all 7 axes)

After scoring all three variants on all seven axes, run a coherence check. Flag any variant whose axis combination is **structurally infeasible** for the company's stage.

Examples of incoherent combinations:

- **Seed-stage + category-creation + enterprise buying-committee positioning + PLG motion** — infeasible. Flag with red severity.
- **PLG motion + dense buyer-committee multi-threading + 18-month sales cycle implication** — infeasible.
- **`--stage seed` + a variant that scores − on TAM specificity AND − on category risk** — infeasible.

When a variant is flagged as incoherent, recommend either modifying the variant or removing it from final consideration.

---

## How the recommendation is chosen (stage-aware logic)

After all three variants are scored, the plugin tags one as "recommended" if `--stage` was provided.

Default tagging rules:

| Stage flag | Default recommendation |
|---|---|
| `seed` | Variant A (narrow-and-sharp) — unless coherence-flagged |
| `A` | Variant A (narrow-and-sharp) or Variant C (outcome-quantified), whichever has higher coherence + better axis 1 (specificity) and axis 5 (customer-readable) scores |
| `B+` | Variant B (category-led) or Variant C (outcome-quantified), whichever has higher coherence + better axis 2 (category risk) and axis 4 (clarity vs. expansiveness) scores |

If `--stage` was NOT provided, present all three neutrally without a recommendation tag — but always print a "your stage matters" note explaining why a stage flag would help.
