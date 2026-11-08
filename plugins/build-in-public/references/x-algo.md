# X (Twitter) Algorithm & Post Checklist

Reference for the `/draft` skill. Apply every rule before finalising an X draft.
X rewards concise, concrete, standalone value — not teasers that require a click.

---

## Core Principles

1. **First line carries the whole value.** Assume the reader never expands.
   If the first line is not worth reading on its own, rewrite it.
2. **Concrete over abstract.** Numbers, names, specific tools beat generalisms.
3. **No hashtags.** They signal noise; the algorithm surfaces posts via
   engagement and follow graph, not hashtag subscription.
4. **No engagement bait.** "RT if you agree" and variants are penalised.

---

## Format Rules

### Single post (default)
- [ ] Default to a single post unless the moment is a shipped milestone (see Thread section)
- [ ] Hard cap: 280 characters including the receipt link
- [ ] No trailing "🧵" unless you are actually writing a thread

### Thread (shipped milestones only)
Use a thread **only** when posting about a shipped milestone that has a meaningful
"how" story worth telling. Rules:

- [ ] **Post 1 = the result.** State what shipped, the concrete outcome, and the receipt.
      Do not bury the lede in the second post.
- [ ] **Posts 2–N = the how.** One idea per post. Stop when the how is told.
- [ ] Maximum 5 posts for a thread. If you need more, cut.
- [ ] Each post must stand alone — do not write "continued from above"

### Media
- [ ] Prefer attaching media when available (screenshot, graph, demo GIF)
- [ ] Media increases impressions; a relevant image outperforms text-only by default
- [ ] **v2 note:** shipped-card images (auto-generated deploy previews) will be
      attached automatically in a future release. For now, use a terminal screenshot
      or browser screenshot of the deployed result.

---

## Post Checklist

- [ ] First line is the full payload: topic + outcome in ≤ 100 characters
- [ ] No hashtags anywhere in the post or thread
- [ ] No engagement bait ("Retweet if…", "What do you think?", "Agree?")
- [ ] The receipt is included: short commit SHA + subject, or a deploy URL
- [ ] Single post unless it is a shipped milestone thread
- [ ] If thread: Post 1 = result, subsequent posts = the how
- [ ] Concrete detail present (tool name / file path / metric / version number)
- [ ] No "I" opener — start with the subject or a verb

---

## Receipt Format for X

Because character counts are tight, use the short form:

```
abc12345 "fix: remove N+1 query in feed loader"
```

Or a URL if it fits:

```
github.com/you/repo/commit/abc12345
```

Place the receipt at the end of the post (or end of Post 1 in a thread).

---

## Anti-patterns (auto-fail)

| Pattern | Why it fails |
|---------|-------------|
| "Thread 🧵 on X" with no result in Post 1 | Buries the value; readers bounce |
| Hashtag block | Down-ranked; signals spam |
| "RT if you agree" | Engagement bait penalty |
| Vague first line ("Big news today…") | Low impression-to-engagement ratio |
| Thread for a non-shipped moment | Thread format implies magnitude; use single post |

---

## Quick format templates

**Single post:**
```
[Concrete outcome or finding — ≤ 100 chars]

[One sentence of context, optional]

[Receipt: short SHA + subject or URL]
```

**Thread (shipped milestone):**
```
Post 1: [What shipped + concrete outcome + receipt URL]
Post 2: [The biggest challenge or decision]
Post 3: [What you'd do differently]
(Posts 4–5 only if genuinely necessary)
```
