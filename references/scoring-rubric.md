# Scoring Rubric

Reference for the `/draft` skill. Score each candidate commit on four axes,
pick the top 1–2 moments per post cycle, and enforce variety rules.

---

## The Four Axes

### 1. Innovation (0–5)
**Definition:** Novel approach, first use of a technology, or a clever solution
that differs from the obvious path.

| Score | Anchor |
|-------|--------|
| 0 | Routine CRUD / config change / boilerplate |
| 1 | Minor adaptation of a known pattern |
| 2 | Combines existing tools in a slightly unusual way |
| 3 | First-time use of a library/service in this project |
| 4 | Novel architecture decision or previously unseen workflow |
| 5 | Genuinely new approach; the technique itself is the story |

**Signal heuristics (from commit diff):**
- First-time deps or imports not seen in prior commits
- New file types added to the project (`.wasm`, `.proto`, new framework config)
- Unusual problem-solving arc: detour → dead end → pivot to different tool
- Commits that introduce an abstraction nobody asked for but that clearly pays off

---

### 2. Insight (0–5)
**Definition:** A non-obvious learning — something that surprised you and will
surprise a reader.

| Score | Anchor |
|-------|--------|
| 0 | Expected outcome, no learning |
| 1 | Confirms prior assumption |
| 2 | Slightly counterintuitive but well-known to experts |
| 3 | Non-obvious to intermediate practitioners |
| 4 | Long exploration that distills to a concise, portable rule |
| 5 | Challenges a common mental model; "TIL" shaped |

**Signal heuristics:**
- Long exploration branch → single short commit ("turns out…")
- "TIL"-shaped commit subjects or PR descriptions
- Commit that deletes more lines than it adds after a research detour
- Comment or commit body that starts with "Actually…" or "Turns out…"

---

### 3. Lesson (0–5)
**Definition:** A mistake → fix arc or debugging war story with a transferable
takeaway.

| Score | Anchor |
|-------|--------|
| 0 | Clean implementation, no friction |
| 1 | Trivial typo fix |
| 2 | Minor bug caught quickly |
| 3 | Multi-commit debugging session with a clear resolution commit |
| 4 | Extended debug war (revert → retry → eventual fix) with root-cause insight |
| 5 | The mistake and its fix permanently change how you'd approach this class of problem |

**Signal heuristics:**
- Extended debugging session: multiple `fix:` / `debug:` commits in a row
- Revert commits followed by re-implementation (`revert … then …`)
- `git log` subject sequences: failure → hotfix → re-fix
- `scan_commits.py` `signals` array includes `"fixed"` on a commit that follows a failed earlier attempt

---

### 4. Shipped (0–5)
**Definition:** Something was released, deployed, merged, or launched and is
now real in the world.

| Score | Anchor |
|-------|--------|
| 0 | WIP / draft / stashed |
| 1 | Internal branch merge, no external impact |
| 2 | Merged to main but not yet deployed |
| 3 | Deployed to staging / preview URL |
| 4 | Deployed to production or TestFlight / App Store |
| 5 | Public launch with users; version tag + announcement |

**Signal heuristics:**
- Commit subject matches `scan_commits.py` SHIP_RE: `ship`, `shipped`, `release`,
  `released`, `deploy`, `launch`, `v\d+\.\d+`
- Git tag on the commit (`git describe --exact-match`)
- Merge commit into `main` / `master`
- Commit references a PR number that is now closed/merged

---

## Composite Score

```
composite = Innovation + Insight + Lesson + Shipped
```

- Each axis is 0–5; maximum composite = 20.
- Score each candidate commit independently.
- Rank candidates descending by composite score.

---

## Selection Rules

1. **Pick top 1–2** commits by composite score for the post cycle.
2. **Axis variety:** Do not post two "Shipped"-dominant moments in a row across
   consecutive post cycles. If the previous post was Shipped-dominant
   (Shipped ≥ 4 and Shipped is the highest axis), prefer the next candidate
   whose dominant axis differs.
3. **Minimum bar:** Only post moments with composite ≥ 6. Below that threshold,
   flag "no strong moment this cycle" and skip rather than post weak content.
4. **Tie-breaking:** Prefer Insight or Lesson over Innovation or Shipped when
   composite scores are equal — teaching beats announcing.
