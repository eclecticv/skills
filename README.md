# Build in Public — Claude Code Plugin

Observe your Claude Code sessions and git commits, surface share-worthy moments, and draft algorithm-tuned X and LinkedIn posts in your voice. Everything stays local until you publish.

---

## Privacy model

**This plugin never auto-publishes.** The pipeline always ends at a human-reviewed draft file that you must explicitly approve before anything is queued or copied.

Three additional safeguards:

1. **Repo allowlist is opt-in and empty by default.** The commit scanner (`scan_commits.py`) never auto-discovers repositories. You add repos explicitly in `~/.build-in-public/config.md` or during `/build-in-public:setup`. If the allowlist is empty, no commits are scanned.

2. **Privacy gate blocks any draft with findings.** Before a draft is written, `secret_scan.py` checks for secrets (AWS keys, API tokens, high-entropy strings, PEM headers) and all terms in your denylist. Exit code 1 = hard block. The skill surfaces the full findings report and stops. Nothing is queued silently.

3. **Everything stays local until you run `/build-in-public:publish`.** The journal (`~/.build-in-public/journal.jsonl`), all draft files, and the posting history (`~/.build-in-public/posted.jsonl`) are local files. No data leaves your machine automatically.

---

## What it does

At the end of every Claude Code session, a `SessionEnd` hook runs `capture_session.py`. The script reads the session transcript, detects share-worthy signals (shipped, fixed, learned), and appends a compact digest to a local journal file.

When you run `/build-in-public:draft` (manually or via a weekly cron), the synthesizer:

1. Reads the journal entries from the past 7 days.
2. Scans your allowlisted git repos for recent commits.
3. Scores each candidate on four axes (Innovation, Insight, Lesson, Shipped) and selects the top 1–2 moments above a composite threshold of 6/20.
4. Drafts one post per selected moment per configured platform, grounded in a real commit receipt.
5. Runs the privacy gate. Any finding blocks the draft.
6. Runs the [Humanizer](https://github.com/Aboudjem/humanizer-skill) to score and rewrite AI-tells down to your configured threshold.
7. Writes review-ready markdown files to your `output_dir`.

Drafts are stored as plain markdown with YAML frontmatter. You review them, edit freely, then run `/build-in-public:publish` on each approved file.

---

## Prerequisites

- **Python 3** (stdlib only; no pip requirements for runtime scripts)
- **git** (for commit scanning — only needed if you add repos to the allowlist)
- **[Humanizer skill](https://github.com/Aboudjem/humanizer-skill)** — an external Claude Code plugin/skill that scores posts for AI-tells and rewrites them toward a target threshold. Install it following that repo's README, then re-run `/build-in-public:setup`. Without it, the de-AI pass is skipped and drafts are flagged `not-humanized: true`.
- **Buffer account** (optional) — for auto-queuing posts to X or LinkedIn. Requires an org ID, channel IDs, and a personal access token. Without Buffer, posts are copied to the clipboard.

---

## Install

1. Install this plugin via Claude Code:

   ```
   claude plugin install <owner>/build-in-public
   ```

2. Run setup:

   ```
   /build-in-public:setup
   ```

   Setup collects your output directory, platforms, voice preset, posting cadence, repo allowlist, denylist, and optional Buffer credentials. It writes `~/.build-in-public/config.md`, checks for the Humanizer dependency, and registers (or documents) the weekly cron.

3. (Optional) Install the Humanizer dependency from [github.com/Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) and re-run `/build-in-public:setup` to seed the voice profile.

---

## Commands

### `/build-in-public:setup`

First-run configurator. Walk through all settings interactively, write `~/.build-in-public/config.md`, check the Humanizer dependency, and register the weekly draft schedule. Re-run any time to reconfigure.

**When to use:** On first install, after changing platforms or Buffer credentials, or after installing the Humanizer.

---

### `/build-in-public:draft`

Weekly synthesizer. Reads the journal and allowlisted commits, scores and selects the best moments, drafts algorithm-tuned posts per platform, runs the privacy gate and Humanizer, and writes markdown draft files to `output_dir`.

**When to use:** Manually at any time (`/build-in-public:draft`), or let the weekly cron trigger it. Always ends at draft files — never publishes.

---

### `/build-in-public:capture [optional note]`

On-demand journal entry. Invokes `capture_session.py` against the current session and confirms what was logged. Use this when something notable just happened and you don't want to wait for the automatic `SessionEnd` hook.

**When to use:** Right after shipping something significant mid-session, or when you want to annotate a moment with a note.

---

### `/build-in-public:publish <path-to-approved-draft.md>`

Publisher. Reads the draft file, shows you the full post body, and asks for explicit approval before acting. Then queues the post via Buffer (MCP or HTTP fallback) or copies it to the clipboard. Appends a record to `~/.build-in-public/posted.jsonl` only on success.

**When to use:** After reviewing and editing a draft file produced by `/build-in-public:draft`.

---

### SessionEnd capture hook (`hooks/hooks.json`)

Runs automatically at the end of every Claude Code session. Calls `scripts/capture_session.py`, which detects signal keywords in the session transcript (shipped, fixed, learned, and related variants) and appends a digest to `~/.build-in-public/journal.jsonl`. Writes an entry only when at least one signal is detected or a repo name can be derived from `cwd`. No network calls; no side effects beyond the local journal file.

---

## Config reference (`~/.build-in-public/config.md`)

Settings live in the YAML frontmatter of `~/.build-in-public/config.md`. Edit the file directly or re-run `/build-in-public:setup` to reconfigure interactively.

| Key | Description | Default |
|-----|-------------|---------|
| `output_dir` | Directory where draft markdown files are saved | `~/build-in-public-drafts` |
| `platforms` | List of target platforms — valid values: `x`, `linkedin` | `[x, linkedin]` |
| `voice_preset` | Writing style for drafts — options: `changelog` \| `teacher` \| `story` \| `honest-struggle` | *(required — no default; must set during setup)* |
| `voice_calibration_samples` | Path to a file of past posts or writing samples used to calibrate the Humanizer voice profile | *(omit if not using)* |
| `cadence_per_week` | Target number of posts per week (informational; used for cron scheduling) | `2` |
| `cadence_day` | Day of the week the weekly draft cron runs | `Monday` |
| `humanizer_threshold` | AI-tell score ceiling (0–100); drafts scoring above this are rewritten by the Humanizer before review | `25` |
| `repo_allowlist` | List of absolute git repo paths to scan for commits — **empty by default; opt-in only** | `[]` |
| `denylist` | Terms that must never appear in a draft (client names, employers, unreleased product names) — blocks the draft on match | `[]` |
| `buffer_org_id` | Buffer organization ID — omit if not using Buffer | *(optional)* |
| `buffer_channel_id_linkedin` | Buffer channel ID for your LinkedIn account | *(optional)* |
| `buffer_channel_id_x` | Buffer channel ID for your X account | *(optional)* |
| `buffer_token_path` | Path to a local file containing your Buffer personal access token (e.g., `~/.secrets/buffer-token`) | *(optional)* |

**Buffer note:** All four Buffer keys must be present and the token file must be readable for the Buffer route to activate. If any are missing, `/build-in-public:publish` falls back to clipboard copy.

---

## v2 Roadmap

These were deferred from v1 and are planned for a future release:

- **Shipped-card images** — auto-generate a shareable image (e.g., a "just shipped" card) to attach to posts. Blocked on a reliable, local image-generation path.
- **Build-log continuity** — link related posts across cycles so followers can follow a multi-week arc (e.g., "last week I started X, this week it shipped").
- **Tease → payoff pairing** — when a moment scores high on Innovation, automatically draft a follow-up "shipped" post for the same thread.
- **Typefully scheduler** — add Typefully as an optional scheduler alongside Buffer, for X thread scheduling.
- **Meta-distribution footer** — an optional, off-by-default footer line ("surfaced by Build in Public") that can be toggled on in config for posts where attribution is welcome.

---

## Development

```bash
pip install pytest          # or: pip install -r requirements-dev.txt
python3 -m pytest -v        # 13 tests across capture_session, secret_scan, scan_commits
```

All scripts are Python 3 stdlib-only. No external dependencies at runtime.
