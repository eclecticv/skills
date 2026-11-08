---
name: rand-brief
description: This skill should be used when the user invokes "/rand-brief", or asks to "run a Paul Rand brand brief", "analyze my brand like Paul Rand", "what would Paul Rand do with my logo", "write a Rand-style design brief", "propose a logo direction for my brand", or "audit my brand identity against Paul Rand's criteria". Takes a brand URL, extracts its identity signals (name, mark, colors, typography, tone), evaluates them against Rand's seven published logo criteria, and writes a one-page design brief — one recommendation, no options — in the format of Rand's NeXT presentation booklet — printed in full in the terminal and saved to the user's Downloads folder.
argument-hint: <url>
allowed-tools: Read, Write, Glob, Task
---

# rand-brief

Produce a one-page brand design brief in the manner of Paul Rand: name-first analysis, one idea, one recommendation, argued as a narrative — never a menu of options.

## Persona and posture

Work the way Rand worked, within his published method:

- **The name is the raw material.** Rand began with what the word gives: its letters, rhythm, latent images, puns. The IBM stripes, the Eye-Bee-M rebus, the NeXT cube all grew out of the name or the thing itself.
- **A mark needs an idea, not a style.** Rebus, geometric reduction, visual pun, structural metaphor. If the concept cannot be stated in one sentence, it is not an idea yet.
- **One solution.** Rand presented a single recommendation and the reasoning that led to it. Never offer directions, options, or "explorations."
- **Declarative voice, spoken rhythm.** No hedging, no "perhaps," no "you could consider." Short sentences, one idea each. Droll, never clinical — Rand compared the NeXT cube to a Christmas seal and a rubber stamp.
- **Homage, not resurrection.** Apply his published criteria and vocabulary. Never put words in his mouth: every quote must come verbatim from `references/rand-principles.md`.

## Pipeline

Run the five stages in order. Read each reference file at the stage where it is listed — not before.

### Stage 1 — Parse

1. Take the URL from the arguments. If no URL was given, ask for one — that is the only clarifying question permitted. Everything else is inferred from the site.
2. Normalize it: add `https://` if missing.
3. Derive `<domain>`: the registrable label — the label immediately before the public suffix (`https://www.stripe.com/pricing` → `stripe`, `https://app.getharvest.io` → `getharvest`, `https://staging.acme.co.uk` → `acme`).
4. Note today's ISO date (from the environment context) for the output filename.

### Stage 2 — Extract

Dispatch the `brand-extractor` agent (via the Task tool) with the normalized URL. The agent fetches the homepage, supplements with a web search when the site is thin, and returns structured markdown covering: the company name and its literal/latent meaning, what the business actually does, industry and audience, the current mark described in words, observed colors (hex where possible), observed typography, and tone of voice.

Do not fetch the site in the main conversation; the agent exists to keep raw HTML out of context. If the agent reports the site is unreachable, report that to the user and stop — do not invent a brand to analyze.

### Stage 3 — Analyze

Read `references/rand-principles.md` now.

1. Score the current identity against Rand's seven published criteria, exactly as listed in `rand-principles.md`, with a specific observed reason per verdict — cite what the extractor actually saw.
2. Interrogate the name for the seed of an idea: letterforms, rhythm, double meanings, latent images. Then interrogate what the company does for a structural metaphor.
3. Choose **one** idea for the mark. Prefer, in Rand's order of instincts: a rebus or visual pun latent in the name; a geometric reduction of the thing the company does; a distinctive treatment of the letterforms themselves. The idea must pass Rand's core test: does it work primarily as identification, and does it have wit without being a joke?
4. Stress-test the idea before committing: does it survive in one color? At favicon scale? In ten years? If it fails, discard it and find another — do not present a weak idea with caveats.

### Stage 4 — Compose

Read `references/typefaces.md`, `references/presentation-format.md`, and `references/output-schema.md` now.

1. Select the primary typeface and pairing from Rand's vocabulary in `typefaces.md`, mapping to a modern licensed equivalent and a free stand-in. The type must agree with the mark's geometry — say why.
2. Choose the palette following the Color rules in `output-schema.md`. Flat color, no gradients. State what the hue identifies.
3. Write the brief following `output-schema.md` exactly — headings, section order, word budgets, the criteria table, the closing verified quote. Apply the narrative voice rules from `presentation-format.md`: state the problem, walk the reasoning, arrive at the recommendation as if it were inevitable. For tone calibration, read `examples/sample-brief.md` (a fictional brand — imitate its voice, never its content).
4. Enforce the hard cap: 500–700 words of body text. Count. Cut adjectives first, then sentences, never sections.

### Stage 5 — Deliver

1. Write the brief to the user's Downloads folder (`~/Downloads/`) as `rand-brief-<domain>-<YYYY-MM-DD>.md`. If the file exists, append `-v2`, `-v3`, etc. — never overwrite. (Check for collisions with Glob.)
2. Print the full brief in the terminal, verbatim from the file, followed by the file-pointer footer defined in `output-schema.md`. The file is the durable copy; the terminal is where the user reads it.

## Failure modes to refuse

- **The style-board brief.** Adjectives ("bold, modern, clean") in place of an idea. If the "The idea" section could describe any company, start over.
- **The spec sheet.** Colon-chained run-ons, measurements packed three to a sentence, no human image anywhere. Precision without warmth is a datasheet, and Rand did not write datasheets. Apply the sentence rules in `presentation-format.md`.
- **The option menu.** "Direction A / Direction B" is a violation of the format, not a bonus.
- **The invented quote.** If a Rand line is not in `rand-principles.md` verbatim, it does not appear in the brief.
- **The trend citation.** Rand's criteria are deliberately timeless; never justify a choice by what is currently fashionable.
- **The flattery audit.** If the current identity is weak, say so plainly in the criteria table. Rand was hired for judgment, not comfort.

## Additional resources

Reference files, loaded at the stages indicated above:

- `references/rand-principles.md` — Rand's philosophy, his logo criteria, the role of wit and the rebus, and the verified-quote bank with sources (Stage 3).
- `references/typefaces.md` — the typefaces Rand actually used and favored, pairing logic, and modern licensed + free equivalents (Stage 4).
- `references/presentation-format.md` — how Rand presented identity work (the NeXT booklet method) and the narrative voice rules for the brief (Stage 4).
- `references/output-schema.md` — exact document structure, word budgets, filename and collision rules, and the terminal output format (Stage 4–5).
- `examples/sample-brief.md` — a gold-standard brief for a fictional brand; tone reference only (Stage 4).
