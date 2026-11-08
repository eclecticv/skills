# Pricing Plan Optimization (PR-1 to PR-9)

<!-- Built: 2026-03-18 | Based on original peer-reviewed papers cited within each rule -->

## PR-1: Offer 3-5 Plans

**What it is:** The pricing page presents between 3 and 5 plan options (including any free tier).

**Recommendation:** To ease user decision-making, aim to offer between 3 and 5 plans. Offer a basic plan as a low-cost entry option, a standard plan as a balance between cost and functionality, and a premium plan focused on capturing a high-end market segment. Make sure the middle option is well-defined as a balance between the basic and high-end options — people will be most drawn toward this one. You can consider an optional enterprise plan for large organizations with custom needs. Finally, if you opt for a freemium model, you can include a free plan.

**Why it matters:** People tend to avoid options that are perceived as extreme or risky (e.g. the most expensive one) and prefer the middle or moderate options, thus most opt for the Standard plan. This effect is driven by people wanting to make a decision that is safer, reducing feelings of regret.

**Key stat:** Extremeness aversion drives most users to the middle plan.

**Source:** Simonson, I., & Tversky, A. Choice in Context: Tradeoff Contrast and Extremeness Aversion. *Journal of Marketing Research* (August 1992). **Universities:** Haas School of Business, University of California Berkeley, and Stanford University.

**Decision procedure:** A "plan" is a named tier card on the pricing page. COUNT:
free tiers and enterprise/"Contact us" tiers — both are choices the visitor weighs.
DON'T COUNT: add-ons, billing-period toggles (monthly/annual is one plan, not two),
or one-off services. State the count and list the plan names in the observation.
PASS iff 3 ≤ count ≤ 5.

**PASS criteria:**
- 3 to 5 distinct plans visible
- Clear basic/standard/premium progression
- Middle option well-defined as a balanced choice
- Enterprise/custom plan is acceptable as an addition

**FAIL criteria:**
- Fewer than 3 plans (insufficient choice)
- More than 5 plans (overwhelming)
- No clear middle option that feels balanced
- Plans not clearly differentiated from each other

---

## PR-2: Decoy Plan

**What it is:** One plan is positioned as a decoy — slightly better than the target plan but significantly pricier, making the target look like great value.

**Recommendation:** When presenting multiple plans, you can turn one of the plans into a decoy option that is slightly better but significantly pricier (e.g. make your middle plan a decoy). The goal is not to sell the decoy plan but to make the other plans (lower priced and higher priced) more attractive. Be sure to use just-below prices instead of rounded pricing on your main plan too (e.g. $49.99 vs. $50). A decoy option led people to buy the target (e.g. standard plan) option 62% of the time when using a just-below price (vs. 49% when using rounded prices).

**Why it matters:** The decoy effect relies on presenting an option that makes another choice seem superior by comparison. By introducing a decoy, precise pricing helps people identify the superior value of the target option, which then leads them to choose it over others.

**Key stat:** Decoy with just-below pricing: 62% chose the target option (vs. 49% with rounded prices).

**Source:** Cui, Y. G., Kim, S. S., & Kim, J. Impact of preciseness of price presentation on the magnitude of compromise and decoy effects. *Journal of Business Research* (August 2021). **Universities:** Auckland University of Technology and The Hong Kong Polytechnic University.

**PASS criteria:**
- A plan exists that makes another plan look like clearly better value
- Decoy is slightly better but disproportionately more expensive
- Target plan uses just-below pricing (e.g., $49.99 not $50)

**FAIL criteria:**
- All plans are evenly spaced in value and price
- No plan makes another look like an obvious deal

**N/A when:** Only 2 plans exist, or single-plan offering.

---

## PR-3: Left-to-Right Plan Ordering

**What it is:** Plans are ordered from cheapest (left) to most expensive (right), and prices are positioned on the left side of each plan card.

**Recommendation:** Display your plans left to right — from the cheapest to the most expensive one. Display product prices on the left side of each specific plan image or description (vs to the right) to make them appear more affordable. People assigned up to 9.49% higher prices for products that were placed on their right-hand side.

**Why it matters:** When people process items from left to right, they start with the smaller values on the left (e.g. 1, 2, 3, etc.), which influences people's perceptions of the prices displayed on the left as being "lower." So people associate smaller numerical values with the left side of a display, such layout flows more naturally indicating progression.

**Key stat:** Right-side price placement led to 9.49% higher price estimates.

**Source:** Cai, F., Shen, H., & Hui, M. K. The Effect of Location on Price Estimation: Understanding Number-Location and Number-Order Associations. *Journal of Marketing Research* (October 2012). **Universities:** Shanghai Jiao Tong University & Chinese University of Hong Kong.

**Decision procedure:** This is a visual-position rule — score it ONLY from the
pricing-page screenshot (or an unambiguous DOM ordering of plan cards with prices).
Without that evidence the verdict is UNVERIFIED, never a text-inferred FAIL.

**PASS criteria:**
- Plans arranged left to right from cheapest to most expensive
- Price displayed on the left side of each plan card
- Natural left-to-right progression

**FAIL criteria:**
- Plans ordered right to left (expensive first)
- Plans in random order
- Price displayed on the right side of plan cards

---

## PR-4: Price Below Features

**What it is:** The price is displayed below the features list and above the CTA button, not at the top of the plan card.

**Recommendation:** Position the price below the features list and above the CTA button. This makes people perceive the price as lower and makes them more likely to subscribe. The "down = less" metaphor is deeply ingrained in people, so a lower vertical position makes the price seem smaller.

**Why it matters:** The "down = less" metaphor is deeply ingrained — a lower vertical position makes the price seem smaller and increases likelihood of subscribing. People read features first, building perceived value before encountering the price.

**Key stat:** Lower vertical position for price increases subscription likelihood.

**Source:** Cai, F., Shen, H., & Hui, M. K. The Effect of Location on Price Estimation: Understanding Number-Location and Number-Order Associations. *Journal of Marketing Research* (October 2012). **Universities:** Shanghai Jiao Tong University & Chinese University of Hong Kong.

**Decision procedure:** Visual-position rule — score ONLY from the pricing-page
screenshot. Describe the actual card layout (what's at top, middle, bottom) in the
observation. Without the screenshot the verdict is UNVERIFIED.

**PASS criteria:**
- Price appears below the feature list
- Price is above or near the CTA button
- Features are read before price is encountered

**FAIL criteria:**
- Price displayed at the very top of the plan card
- Price displayed above the feature list
- Price positioned far from the CTA button

---

## PR-5: Price Difference Framing

**What it is:** Upgrade messaging focuses on the price difference between plans ("$10 more") rather than the absolute price of the higher plan ("$25/mo").

**Recommendation:** When displaying prices of different plan options, upgrades, or add-ons (e.g. Starter to Premium plan), focus on the price difference (e.g. $10 more for Premium) not the total price (e.g. $15 Starter vs $25 for Premium). Your premium plan will seem cheaper, because $10 (the difference) is cheaper than $25 (the total price), so people will be more likely to buy it. This does not work for more expensive, high-involvement purchases, as people will stop and properly calculate the prices themselves.

**Why it matters:** People think of prices as they're shown to them. When people see the price difference for a premium plan, they focus on that number more than the total cost. "$5 per month, when buying the annual plan" makes people focus on the monthly, rather than the total yearly amount, making people consider the total cost as cheaper.

**Key stat:** Differential framing makes premium plans seem significantly cheaper.

**Source:** Allard, T., Hardisty, D.J. & Griffin, D. When "More" Seems Like Less: Differential Price Framing Increases the Choice Share of Higher-Priced Options. *Journal of Marketing Research* (July 2019). **Universities:** Nanyang Technological University, University of British Columbia.

**PASS criteria:**
- Upgrade prompts highlight the difference ("Just $10 more for Premium")
- Comparison language used between tiers
- N/A for single-plan offerings

**FAIL criteria:**
- Only absolute prices shown with no comparative framing
- Price difference not highlighted when upgrading
- No upgrade path messaging visible

**N/A when:** Single-plan offering or no visible upgrade path.

---

## PR-6: Simple Pricing

**What it is:** Pricing is easy to understand at a glance — no complex per-seat calculations, no multiple odd numbers combined, no compound formulas.

**Recommendation:** Avoid complex pricing, which is difficult to understand at a glance (when price components have many different odd numbers e.g. $2.7/per seat, $0.55/per GB of storage, and require different calculation types e.g. $20/month service fee plus 10 x $3 seats with 20% entry discount). People tend to choose simple price options. In experiments, even when a plan was more expensive (e.g. €35 vs €30 per month), 65.9% still chose the simple option. Stick to even endings, consider flat-rate prices, and ensure customers only need to make simple calculations to get the final price.

**Why it matters:** When the price is complex, people may not put in the effort, and simply assume the price is higher than a simpler option (even if it isn't). People may also feel like the company is being unfair and making it hard to figure out the cost. When the price is simple, people feel that the company is being more fair and transparent than competitors, so they are more likely to choose it.

**Key stat:** 65.9% chose the simpler pricing option even when it was more expensive.

**Source:** Homburg, C., Totzek, D., & Krämer, M. How price complexity takes its toll: The neglected role of a simplicity bias and fairness in price evaluations. *Journal of Business Research* (June 2013). **Universities:** University of Melbourne, University of Mannheim, and University of Passau.

**PASS criteria:**
- Price is immediately understandable (flat monthly/yearly fee)
- No complex math required to figure out the real cost
- Even number endings preferred
- Simpler than typical competitors

**FAIL criteria:**
- Complex per-seat or per-unit calculations
- Multiple pricing components that require math
- Odd numbers and different calculation types combined
- Final price unclear without a calculator

---

## PR-7: Easy-to-Divide Prices

**What it is:** Prices and quantities form easy arithmetic — multiples and divisions that are instantly calculable.

**Recommendation:** List the number of product attributes or the number of users the product plan is intended for as a multiple of the price (e.g. $36 team plan for 3 or 6 users), so it's easy to calculate. For instance: team subscriptions at $15 for 3 or 5 users ($5 or $3 each), cloud storage at $5 for 50GB or $10 for 100GB, usage limits for the $5 plan allow generating 25 AI images. You can also use this in your promotions, for example, "save $12" and include a tagline of 4 reasons why to choose your product.

**Why it matters:** People prefer to see numbers that are easily cognitively processed, especially resulting from common arithmetic problems. Exposure to multiples of a number (e.g. 2 and 6) immediately activates the sum (e.g. 8) along with their product (e.g. 12) which makes it easier for us to process and leads to greater liking.

**Key stat:** Easy arithmetic increases processing fluency and product liking.

**Source:** King, D., & Janiszewski, C. The Sources and Consequences of the Fluent Processing of Numbers. *Journal of Marketing Research* (April 2011). **Universities:** National University of Singapore & University of Florida.

**PASS criteria:**
- Per-user cost divides evenly (e.g., $36 for 3 users = $12 each)
- Usage tiers use round, divisible numbers
- Price relationships between tiers are clear

**FAIL criteria:**
- Awkward per-unit math (e.g., $47 for 7 users)
- Quantities that require a calculator
- Pricing that creates irrational-seeming numbers

---

## PR-8: Flat + Usage Hybrid

**What it is:** If usage-based pricing exists, it combines a fixed base fee with a per-usage component, rather than pure pay-per-use or pure flat-rate.

**Recommendation:** If you have sophisticated enough analytics and can constantly monitor usage, a fixed fee (e.g. $19/month) and pay-per-use (e.g. $10 per 1,000 visits) combination is more profitable. In this situation, two-part pricing plans lead to 36% and 49% higher profits compared to just pay-per-use and flat-rate plans, respectively. Use data to determine the optimal balance between the fixed fee and the marginal usage fee to maximize profits.

**Why it matters:** Customers adjust their usage based on marginal price changes. Two-part pricing plans efficiently capture surplus by separating the decision to subscribe from the decision on usage. The fixed fee secures a baseline revenue while the marginal price adjusts to their usage levels.

**Key stat:** Two-part pricing leads to 36% and 49% higher profits compared to pay-per-use and flat-rate respectively.

**Source:** Schlereth, C., Skiera, B., & Wolk, A. Measuring Consumers' Preferences for Metered Pricing of Services. *Journal of Service Research* (December 2011). **Universities:** Goethe-University Frankfurt.

**PASS criteria:**
- Base subscription fee + usage-based component
- Clear separation between fixed and variable costs
- N/A if pure flat-rate pricing

**FAIL criteria:**
- Pure pay-per-use with no base fee
- Complex tiered usage pricing that's hard to predict
- Usage component with unclear per-unit costs

**N/A when:** Pure flat-rate pricing model with no usage component.

---

## PR-9: Flat-Rate Option

**What it is:** At least one plan offers a simple flat-rate price — the same cost regardless of usage or seats.

**Recommendation:** If you prefer a simpler approach, want to reduce complexity (e.g. because other parts of your product are complex), and want to increase upselling or usage, stick with a flat fee (e.g. the same price no matter the number of seats and the usage intensity). In experiments in this study, 68% of people chose the flat-rate plan when the pay-per-use plan would have cost the same, and 23% chose the flat-rate plan even when it was 20% more expensive than pay-per-use.

**Why it matters:** People prefer flat-rate plans over pay-per-use plans, even if that means they pay more. Both B2C and B2B customers have this bias. People tend to overestimate how much they will use a product. It also feels convenient, and simple and gives a sense of insurance that people will not be charged more than they expect.

**Key stat:** 68% chose flat-rate when it cost the same. 23% chose it even when 20% more expensive.

**Source:** Kienzler, M., Kowalkowski, C., & Kindström, D. Purchasing professionals and the flat-rate bias: Effects of price premiums, past usage, and relational ties on price plan choice. *Journal of Business Research* (April 2021). **Universities:** Linköping University and Hanken School of Economics.

**PASS criteria:**
- At least one plan with a single, predictable price
- No surprises or variable costs on that plan
- Flat-rate plan clearly labeled and easy to understand

**FAIL criteria:**
- All plans require usage calculations
- No predictable-cost option available
- "Flat rate" plan that actually has hidden variable costs
