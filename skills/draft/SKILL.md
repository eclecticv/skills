---
name: draft
description: Generate this week's Build in Public posts. Reads the moment journal and allowlisted git commits, scores the share-worthy moments, drafts algorithm-tuned X and LinkedIn posts in the user's voice, runs the privacy gate and Humanizer, and saves review-ready drafts. Use when the user says "draft my build in public posts", "run build in public", "what should I post this week", or when the weekly cron fires.
allowed-tools: Bash, Read, Write, Edit, Skill, AskUserQuestion
---

You are the Build in Public weekly synthesizer. Execute the following 9 steps in order. Do NOT publish anything — stop at review-ready drafts.

---

## Step 1: Load config

Read `~/.build-in-public/config.md`. Parse the YAML frontmatter to extract:
- `output_dir` — where to write draft files
- `platforms` — list of target platforms (e.g., `[x, linkedin]`)
- `voice_preset` — voice style identifier
- `voice_calibration_samples` — optional calibration notes
- `cadence_per_week` / `cadence_day` — posting cadence (informational; do not enforce here)
- `humanizer_threshold` — AI-tell score threshold (default: 25 if absent)
- `repo_allowlist` — list of repo paths to scan (empty list is valid)
- `denylist` — list of terms to block

If `~/.build-in-public/config.md` does not exist, tell the user:
> Config not found. Run `/build-in-public:setup` to initialise the plugin, then re-run `/build-in-public:draft`.

Then STOP — do not proceed.

---

## Step 2: Read the journal

Read `~/.build-in-public/journal.jsonl`. Each line is a JSON object:
`{ts, session_id, cwd, repo, signals[]}`.

Collect all entries where `ts` is within the past 7 days (compare ISO timestamps to now). If the file does not exist or has no entries in the window, note "no journal entries this week" and continue — the commit scan (Step 3) may still surface moments.

Also read `~/.build-in-public/posted.jsonl` if it exists — you will need the most recent posted entries for axis-variety checking in Step 4.

---

## Step 3: Scan allowlisted commits

If `repo_allowlist` is non-empty, run the commit scanner once with all repos:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scan_commits.py" \
  --repo <REPO_1> --repo <REPO_2> ... \
  --since "7 days ago"
```

Build the command dynamically: one `--repo <path>` argument per entry in `repo_allowlist`. The script prints a JSON array of objects:
`{repo, hash, short, author, date, subject, signals[]}`.

If `repo_allowlist` is empty, note: "No repos in allowlist — relying on journal only." and skip this step's script invocation.

Merge commit objects and journal entries into a single candidate list for scoring. De-duplicate by commit hash where a journal entry and a scan result refer to the same commit.

---

## Step 4: Score and select moments

Read `${CLAUDE_PLUGIN_ROOT}/references/scoring-rubric.md` for the full axis definitions and selection rules. Do not re-implement them here — apply them as written.

For each candidate:
1. Score on Innovation, Insight, Lesson, Shipped (0–5 each).
2. Compute composite score = sum of the four axes.
3. Discard any candidate with composite < 6 ("no strong moment" threshold).

After scoring, apply the selection rules from the rubric:
- Pick top 1–2 candidates by composite score.
- Enforce axis variety: if the most recent entry in `posted.jsonl` was Shipped-dominant (Shipped ≥ 4 and Shipped is the highest axis), prefer the next candidate whose dominant axis differs.
- Tie-break: prefer Insight or Lesson over Innovation or Shipped.

If no candidates meet composite ≥ 6, report:
> No strong moments this cycle (all candidates scored below 6). Nothing to draft. Check back after more commits land, or use `/build-in-public:capture` to manually log a session highlight.

Then STOP.

Assign each selected moment an `id` using the format: `<repo-slug>-<short-hash>` (or `journal-<ts-epoch>` for journal-only moments).

---

## Step 5: Draft per-platform posts

For each selected moment, draft a post for every platform in the config's `platforms` list.

Read the platform references:
- `${CLAUDE_PLUGIN_ROOT}/references/linkedin-algo.md` — LinkedIn rules and checklist
- `${CLAUDE_PLUGIN_ROOT}/references/x-algo.md` — X rules and checklist

Apply every rule from the relevant reference before finalising each draft. Write in the configured `voice_preset` and `voice_calibration_samples`.

**Receipts are mandatory.** Every post must embed the real receipt:
- For a commit: `Commit: <short-hash> — "<subject line>"`
- For a PR: the PR link or number
- Place the receipt at the end of the post body (LinkedIn: closing paragraph or final standalone line; X: end of post or Post 1 in a thread)

Do not fabricate anecdotes. Every claim must be traceable to the receipt.

---

## Step 6: Privacy gate

For each draft, pipe its text to `secret_scan.py`. Build the `--deny` flags from the config's `denylist`:

```bash
echo "<DRAFT_TEXT>" | python3 "${CLAUDE_PLUGIN_ROOT}/scripts/secret_scan.py" \
  --deny "<TERM_1>" --deny "<TERM_2>" ...
```

If `denylist` is empty, omit all `--deny` flags (the script still checks built-in secret patterns).

**Interpret exit codes strictly (per `references/redaction-rules.md`):**
- Exit code 0: draft is clean — proceed.
- Exit code 1: findings present — BLOCK this draft immediately.

On a finding:
1. Show the full JSON findings report to the user.
2. Offer to rewrite the draft removing the offending content.
3. If the user accepts a rewrite, re-run the gate on the rewritten draft before proceeding.
4. Never silently auto-redact and continue. Never proceed past a finding without a clean re-scan.

A draft is not ready until its scan returns exit code 0.

---

## Step 7: Humanize

For each draft that passed the privacy gate, follow this procedure exactly. Flag names and modes below match the `humanizer` skill's own SKILL.md — consult that file if an argument spelling is ever in doubt.

**7a. Detect pass.** Invoke the `humanizer` skill via the Skill tool:
- skill name: `humanizer`
- args: the draft text, `--score`, `--purpose marketing`

Parse the `[Score: NN/100]` header from the response. This is the AI-tell score (lower = more human).

**7b. Rewrite if needed.** If score > `humanizer_threshold` (from config, default 25):
1. Invoke `humanizer` via the Skill tool again with the draft text, mode `rewrite`, `--iterate 3`, `--purpose marketing`, and `--voice <voice_preset>` if a voice profile is configured.
2. The skill runs up to 3 detect→rewrite→detect loops internally and returns the best (lowest-scoring) version.
3. Re-read the score from the returned `[Score: NN/100]` header.
4. If score is still > threshold after the iterate run, use the lowest-scoring version produced; log a note that the threshold was not met.

**7c. Record score.** Set `humanizer_score` in the draft frontmatter to the final integer score.

**7d. Absent-dependency fallback.** If the Skill tool reports no `humanizer` skill is available (skill not found / not installed):
- WARN the user:
  > Warning: `humanizer` skill is not installed. The de-AI pass did not run. Install the humanizer dependency and re-run `/build-in-public:draft` before publishing.
- Set `humanizer_score: null` in the frontmatter.
- Add `not-humanized: true` to the frontmatter so the skipped pass is unambiguous.
- Continue writing the draft file — do NOT silently skip the warning or omit the frontmatter flags.

---

## Step 8: Write draft files

For each final draft (passed privacy gate and humanizer), write a markdown file to `output_dir`:

**Filename:** `YYYY-MM-DD-<platform>-<slug>.md`
- `YYYY-MM-DD`: today's date
- `<platform>`: `x` or `linkedin` (lowercase)
- `<slug>`: kebab-case summary of the moment (max 5 words, derived from the commit subject or journal signal)

**File format:**

```markdown
---
moment_id: <id from Step 4>
axis: <dominant axis: Innovation | Insight | Lesson | Shipped>
score: <composite score integer>
receipt: "<short-hash> — <commit subject>" or "<PR link>"
humanizer_score: <integer score, or "not_run">
platform: <x | linkedin>
draft_date: <YYYY-MM-DD>
---

<post body>
```

Write one file per platform per selected moment. If `output_dir` does not exist, create it:

```bash
mkdir -p "<output_dir>"
```

---

## Step 9: Summary and stop

Present a chat summary in this format:

---
**Build in Public drafts ready for review**

| # | Platform | File | Score | Axis | Receipt |
|---|----------|------|-------|------|---------|
| 1 | linkedin | `<filename>` | <score> | <axis> | `<short receipt>` |
| 2 | x | `<filename>` | <score> | <axis> | `<short receipt>` |

Drafts written to: `<output_dir>`

Tell the human: review the files above, edit as needed, then run `/build-in-public:publish` to queue them.

---

**STOP here. Do NOT publish, queue, or schedule anything.**
