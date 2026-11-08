# LinkedIn Algorithm & Post Checklist

Reference for the `/draft` skill. Apply every rule before finalising a LinkedIn
draft. These rules are derived from 360Brew ranking signals and content-quality
patterns — not engagement bait.

---

## Mandatory Checklist

### Hook (first 1–2 visible lines)
- [ ] Names the topic in plain nouns — no vague teasers, no "This changed everything"
- [ ] States the payoff immediately: what the reader will get or learn
- [ ] Fits entirely above the "…see more" fold (~140 chars on desktop)
- [ ] Does **not** open with "I", "We", or the company name

### Length
- [ ] Target 280–420 words (sweet spot for dwell-time signals)
- [ ] Under 280 words only if the entire value is contained in ≤ 3 lines + one artifact
- [ ] Over 420 words only with explicit justification; hard cap at 550 words

### Save-worthy artifact (exactly one)
A structurally-visible element the reader would save or copy:
- Named framework (e.g., "The X/Y/Z Rule")
- Numbered list (3–7 items; each item ≤ 15 words)
- Copy-paste command / snippet / template
- Bolded rule of thumb (a single sentence, standalone)

Rules:
- [ ] Exactly **one** artifact per post — do not stack frameworks
- [ ] The artifact must be visually distinct from body prose (line breaks before/after)
- [ ] It must be extractable out of context and still make sense

### Tone & engagement
- [ ] No engagement bait: no "Agree?", "Thoughts?", "Drop a comment below", "Tag someone who…"
- [ ] No hashtags (the algorithm no longer boosts them; they signal low-effort)
- [ ] No emoji spam; at most one structural emoji used for visual chunking, not decoration

### Closing line
- [ ] A **sharpening reframe** — restate the core tension or implication differently
- [ ] Not a question (questions prompt shallow comments, not saves/shares)
- [ ] Not a CTA ("Follow me for more…")
- [ ] Examples of valid closes: "The hard part isn't the tool — it's knowing when to stop." / "Most teams ship the fix. Few ship the understanding."

### The receipt
- [ ] Embed the commit reference, PR link, or deploy URL that proves the work happened
- [ ] Format: plain text reference in the closing paragraph or as a final standalone line
- [ ] Example: `Commit: abc123 — "fix: remove N+1 query in feed loader"`
- [ ] Do **not** use a hyperlink anchor (LinkedIn strips or penalises external links in body)

---

## Anti-patterns (auto-fail)

| Pattern | Why it fails |
|---------|-------------|
| "Excited to share…" opener | Vague; delays the value |
| "5 lessons I learned" with no artifact | Teases without delivering |
| Hashtag block at the end | Signals spam; 360Brew down-ranks |
| Closing question | Invites noise, not signal |
| Two save-worthy artifacts | Dilutes attention; reader saves neither |
| Fabricated or generalised anecdote | Must be traceable to the receipt commit |

---

## Quick format template

```
[Hook: topic noun + payoff — ≤ 140 chars]

[1–2 sentences of context: why this moment matters]

[The artifact — named framework / numbered list / rule]

[2–3 sentences unpacking the lesson or insight]

[Closing reframe — one sentence, not a question]

[Receipt: Commit abc123 — "subject line"]
```
