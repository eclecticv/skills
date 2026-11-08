# Output schema — the one-page brief

The brief is the product. It must read like a page from Rand's NeXT presentation booklet: calm, declarative, one recommendation argued from first principles. Not a consulting deck, not a list of options.

## File rules

- **Directory:** the user's Downloads folder (`~/Downloads/`). Do not create subdirectories.
- **Filename:** `rand-brief-<domain>-YYYY-MM-DD.md`
  - `<domain>`: the registrable label — the label immediately before the public suffix. `https://www.stripe.com/pricing` → `stripe`; `https://app.getharvest.io` → `getharvest`; `https://staging.acme.co.uk` → `acme`.
  - Date is today's ISO date.
- **Collision:** if the file exists, append `-v2`, then `-v3`, etc. Never overwrite.
- The file is the durable copy. The full brief is also printed in the terminal, where the user reads it.

## Hard constraints

- **One page.** 400–550 words of body text, total. Count before writing the file; cut adjectives first, then clauses, then sentences — never sections. Shorter is more Rand, not less.
- **One recommendation.** Never present alternatives, "options," or "directions to explore." Rand: one solution, argued.
- **No fabricated facts.** Every Rand quote must come verbatim from `rand-principles.md`. Never invent statistics about the analyzed brand.
- **No images.** The brief describes the mark in construction language precise enough that a designer could draw it. Words are the deliverable.
- Write in first person plural ("we") sparingly or in flat declaratives. Never "I think," never hedges ("perhaps," "could consider"). Rand did not hedge.

## Document structure (exact headings, in order)

```markdown
# <Company>: a design brief in the manner of Paul Rand

*<url> · <YYYY-MM-DD> · produced by rand-brief*

## The name
## The identity today
## The idea
## The mark
## Typography
## Color
## In use
```

### The name (~55 words)
What the company's name literally is, means, and evokes. Rand began with the material he was given: the word itself — its letters, its rhythm, any double meaning. If the name contains a latent image or pun, say so here; it becomes the seed of The idea.

### The identity today (~70 words)
What the current identity does and fails to do, judged against Rand's seven published criteria (see `rand-principles.md`). Include this table, scoring each criterion ✓ / ✗ / ~ with a five-or-fewer-word note:

| Criterion | Verdict | Note |
|---|---|---|
| Distinctiveness | | |
| Visibility | | |
| Useability | | |
| Memorability | | |
| Universality | | |
| Durability | | |
| Timelessness | | |

Be specific and fair: cite what was actually observed on the site (colors, mark, type), not generic criticism. A `~` verdict counts as not met in the summary tally but is reported separately ("3/7 met, 2 partial").

### The idea (~85 words)
The single concept for the mark. This is the heart of the brief. It must be an *idea* — a rebus, a geometric reduction, a visual pun, a structural metaphor drawn from what the company actually does — not a style. State it in one sentence first, then unpack why it is right for this business.

### The mark (~100 words)
Construction brief precise enough to draw from:
- Geometry (grid, angles, stroke weights, proportions)
- The one-color test: describe the mark in solid black — it must survive
- The scale test: legible as a 16px favicon and on the side of a truck
- Negative space: what the counter-forms do

### Typography (~70 words)
One primary typeface plus one pairing, drawn from Rand's vocabulary in `typefaces.md`. Name the historical face Rand would have reached for, then the modern licensed equivalent AND a free/Google-Fonts stand-in. One sentence on why this voice fits the name and the mark.

### Color (~45 words)
A flat, limited palette: one primary hue + black + white, at most one secondary. Give hex values. Rand used color as identification, not decoration — say what the hue is doing.

### In use (~45 words)
Three concrete applications: favicon/avatar, wordmark lockup rule (clear space, when the mark appears alone), and one application specific to this business (packaging, app icon, signage — whichever fits).

### Closing
End the document with one verified Rand quote from `rand-principles.md` (attributed, with source), set as a blockquote. Below it, one italic line:

*This brief is an exercise in Paul Rand's published method — his criteria, his vocabulary, his presentation format. It is homage, not resurrection.*

## Terminal output (printed to chat after writing the file)

Print the full brief in the terminal, verbatim from the file — every section, the criteria table, the closing quote, and the homage line. Do not paraphrase, summarize, or reformat it; the terminal rendering and the file must be identical.

Below the brief, one footer line pointing to the durable copy:

```
Saved → ~/Downloads/rand-brief-<domain>-<date>.md
```
