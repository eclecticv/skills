# Build in Public — Design Spec

**Date:** 2026-06-18
**Status:** Approved design, pre-implementation
**Type:** Community Claude Code plugin

## Problem

Developers and builders who ship constantly often have no habit or system for "showing
their work" publicly. The raw material for great build-in-public content already exists in
their day-to-day output (Claude Code sessions, git commits, things they learned and shipped),
but turning that into platform-optimized posts is friction they never get around to.

## What it is

A community Claude Code plugin that observes a developer's work, detects genuinely
share-worthy moments, and turns 1–2 of them per week into platform-optimized X and LinkedIn
drafts. Posts are written in the user's voice, de-AI'd through a Humanizer dependency, passed
through a privacy/redaction gate, logged as markdown, and **never auto-published** — the human
always presses "post."

### Target user

The *installer* of the plugin — any dev/builder, not a specific person. Everything is generic
and configurable per installation. There are no hardcoded vault paths, voices, or account IDs.

### Non-goals

- Not a personal tool for any one person. No hardcoded identities.
- Does not auto-publish. Ever. The pipeline always terminates at a reviewed draft.
- Does not invent accomplishments. Posts are grounded in real session/commit artifacts.
- v1 does not generate images, multi-post narratives, or tease→payoff pairings (deferred to v2).

## Core principles

1. **Never auto-publish.** A tool that reads private session logs (secrets, client names,
   unreleased work, API keys) and writes to public social media must end at a human-reviewed
   draft, behind a redaction/secret-scan gate. This is both an ethics requirement and the
   trust feature that makes the plugin shareable.
2. **Receipts-first.** Every post is grounded in a real artifact (commit / PR / before-after).
   Verifiable build-in-public beats opinion content and is the plugin's authenticity spine.
3. **Generic and configurable.** Works for any installer out of the box; personalization is
   opt-in via `setup`.
4. **Don't overbuild.** v1 proves the core loop (capture → score → draft → gate → review →
   publish). Extensions are deferred until the core is validated.

## Architecture — 5 units

Each unit has one clear purpose, a defined interface, and is independently testable.

### 1. Capture hook (`SessionEnd`)
Runs after every Claude Code session. Cheap; does **no** heavy LLM scoring. Appends a compact
*session digest* to the local journal: what was worked on, files/commits touched, and
lightweight signals (`shipped` / `fixed` / `learned` / `first-time-using-X`). Preserves the
moment while context is fresh. Work done outside Claude Code is caught later by the commit scan.

**Interface:** reads session context → appends one JSON line to `journal.jsonl`.
**Depends on:** moment store path from config.

### 2. Moment store
- `~/.build-in-public/journal.jsonl` — captured candidate moments.
- `~/.build-in-public/posted.jsonl` — history of posted moments (dedup + variety enforcement).

Local only. Nothing leaves the machine until a reviewed draft is explicitly published.

**Interface:** append-only journal; read by the synthesizer; posted.jsonl updated by publisher.

### 3. Weekly synthesizer (`/build-in-public:draft`) — the core
The scheduled run:
1. Gathers the week's journal entries + scans git commits across **allowlisted repos only**.
2. Scores each candidate on the 4-axis rubric (see Scoring). Selects the top 1–2 *peaks*,
   enforcing variety (won't post two "shipped" in a row; rotates axes week to week).
3. Drafts **platform-specific** posts: LinkedIn long-form (algo-tuned), X single (thread only
   for shipped milestones). Each draft embeds its receipt (commit/PR link or reference).
4. Runs the **privacy gate** (unit 4).
5. Runs the **Humanizer loop** until AI-tell score < threshold (default 25).
6. Writes review-ready drafts to the configured markdown folder and notifies the user.

**Interface:** in = journal + git history + config; out = markdown draft files + notification.
**Depends on:** moment store, privacy gate, Humanizer dependency, scoring rubric, algo references.

### 4. Privacy / redaction gate
Non-negotiable. Applied to every draft before it can be surfaced for review:
- **Secret scan** — API keys, tokens, `.env`-shaped values, high-entropy strings.
- **User denylist** — client/employer/project names that must never appear publicly.
- **Repo allowlist** — only commits from opted-in repos are ever considered.
- **Human approval** — final gate; never bypassed.

Blocks anything suspicious and explains why. Never auto-publishes.

**Interface:** in = draft text + config denylist; out = pass/block + redaction report.

### 5. Publisher (`/build-in-public:publish`)
Takes an **approved** draft and either copies it to the clipboard / opens compose, or queues
it to **Buffer** if creds are configured. Marks the moment as posted in `posted.jsonl`.

**Interface:** in = approved draft + config; out = queued/copied post + posted.jsonl update.
**Depends on:** Buffer MCP (or HTTP fallback), moment store.

### Supporting commands
- **`/build-in-public:setup`** — interactive config. Sets output folder, platforms (X/LinkedIn),
  voice preset + optional calibration samples, cadence, Humanizer threshold, repo allowlist +
  denylist, optional Buffer creds. Installs/verifies the Humanizer dependency. Registers the
  `SessionEnd` hook and the weekly cron.
- **`/build-in-public:capture`** — manual "log this moment now" for the current session.

## Data flow

```
session ends
   └─> capture hook ──> journal.jsonl            [continuous, cheap]

weekly cron fires /build-in-public:draft
   ├─ gather journal entries (past week)
   ├─ scan git commits across allowlisted repos
   ├─ score candidates (4-axis rubric) ──> select top 1–2 peaks (variety-enforced)
   ├─ draft platform-specific posts (+ embed receipts)
   ├─ privacy gate (secret scan + denylist) ──> block or pass
   ├─ Humanizer loop until AI-tell < threshold
   └─ write drafts to markdown folder + notify user

user reviews / edits draft
   └─> /build-in-public:publish ──> Buffer queue OR clipboard/compose
        └─> mark posted in posted.jsonl
```

## Scoring rubric (4 axes)

Each candidate scored 0–5 on each axis; composite picks the peaks.

- **Innovation** — novel approach, first use of a technology, a clever solution.
  Signals: first-time imports/deps, new file types, unusual problem-solving arcs.
- **Insight** — a learning worth sharing, a non-obvious realization.
  Signals: long exploration → concise conclusion, "TIL"-shaped session arcs.
- **Lesson** — a mistake → fix, a debugging war story.
  Signals: extended debugging, revert→retry cycles, fix commits after failures.
- **Shipped** — released / deployed / merged / launched.
  Signals: commit messages matching ship/release/deploy/launch, tags, merges to main.

**Selection:** top 1–2 by composite score, with axis variety enforced across weeks (rotates
so the feed isn't all "shipped" posts).

## Voice

Hybrid: ship build-in-public tone presets (changelog / teacher / story / honest-struggle);
optionally calibrate to the user's real voice from samples or past posts they point to in
`setup`. The Humanizer strips AI tells after the draft is written.

## Platform algorithm references (kept current)

- `references/linkedin-algo.md` — hook in first 1–2 lines, 280–420 words, one structurally
  visible save-worthy artifact, no engagement bait, no hashtags, closing reframe not a question.
- `references/x-algo.md` — first-line hook, single vs thread rules, media bias, brevity.
- `references/scoring-rubric.md` — the rubric above, with signal heuristics.
- `references/redaction-rules.md` — secret patterns and never-post rules.

## Dependency

**Aboudjem `humanizer-skill`** (https://github.com/Aboudjem/humanizer-skill) — 43 patterns,
0–100 AI-tell score, `--iterate` loop. Used as a scored gate: default refuse to queue any post
scoring **> 25/100**; `--iterate` auto-fixes failures. Voice preserved via its
`humanizer-context.md` brand-voice file (seeded from the user's voice preset/calibration), so
fixed profiles don't flatten the user's voice.

## Component plan

| Type | Count | Purpose |
|------|-------|---------|
| Skills (commands) | 4 | `setup`, `draft`, `capture`, `publish` |
| Hooks | 1 | `SessionEnd` capture |
| References | 4 | LinkedIn algo, X algo, scoring rubric, redaction rules |
| Config / state | 1 | `config.md` (YAML frontmatter) + `journal.jsonl` + `posted.jsonl` |
| MCP | 0 | scheduler via existing Buffer MCP / HTTP fallback (optional) |

## Defaults (all editable in `setup`)

- Cadence: weekly, up to 2 posts.
- LinkedIn: 280–420 words. X: single post (thread only for shipped milestones).
- Humanizer threshold: AI-tell < 25.
- Output: markdown folder (Obsidian vault or any dir).
- Scheduler: Buffer (opt-in creds).

## v1 scope

- 5 architecture units + 2 supporting commands.
- Receipts-first grounding (default behavior).
- Buffer scheduler integration.
- Cron registered via `setup`.

## Deferred to v2

- Shipped-card images (auto-generated shareable graphics).
- Build-log continuity (week-N narrative threading).
- Tease → payoff post pairing.
- Typefully scheduler.
- Meta-distribution footer ("surfaced by Build in Public"), off by default, only if honest.

## Open questions / risks

- **Capture-hook cost:** must stay cheap. If `SessionEnd` extraction is non-trivial, fall back
  to recording raw session metadata only and defer all interpretation to the weekly run.
- **git scan scope:** allowlist must default to *empty* (opt-in), so the plugin never reads
  repos the user didn't approve.
- **Humanizer install:** `setup` must handle the dependency not being present gracefully
  (offer to install from the marketplace, or degrade with a clear warning).
