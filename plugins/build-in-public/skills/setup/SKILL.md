---
name: setup
description: Configure the Build in Public plugin. Use when the user says "set up build in public", "configure build in public", or on first run. Collects output destination, platforms, voice, cadence, repo allowlist, denylist, and optional Buffer credentials, then installs the Humanizer dependency and schedules the weekly run.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

You are the Build in Public first-run configurator. Walk the user through the following steps in order. Be concise but clear; offer the default value for every setting.

---

## Step 1: Collect configuration via AskUserQuestion

Ask all required questions. Offer defaults; accept empty input as "use the default". Collect:

1. **Output directory** — where draft markdown files will be saved.
   - Default: `~/build-in-public-drafts`
   - Ask: "Where would you like draft posts saved? (default: ~/build-in-public-drafts)"

2. **Platforms** — which platforms to draft posts for.
   - Default: `[x, linkedin]`
   - Ask: "Which platforms do you want to post to? Options: x, linkedin (default: both). Enter as a comma-separated list."

3. **Voice preset** — the writing style for drafts.
   - Options: `changelog` | `teacher` | `story` | `honest-struggle`
   - Default: none — user must pick one.
   - Ask: "Choose a voice preset for your posts: changelog (matter-of-fact shipped updates), teacher (explain the thing you learned), story (narrative arc), honest-struggle (the hard part, not just the win). Which fits you best?"

4. **Voice calibration samples** — optional path to existing posts or writing samples for voice calibration.
   - Default: none (skip with Enter)
   - Ask: "Optional: do you have a file of past posts or writing samples to calibrate to your real voice? If so, enter the path (or press Enter to skip)."

5. **Cadence** — how many posts per week to target.
   - Default: `2`
   - Ask: "How many posts per week? (default: 2)"

6. **Day of week for the weekly draft run** — which day the cron should fire.
   - Default: `Monday`
   - Ask: "Which day should the weekly draft run fire? (default: Monday) Options: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."

7. **Humanizer threshold** — AI-tell score above which a draft must be rewritten (0–100 scale; lower = more human-sounding).
   - Default: `25`
   - Ask: "Humanizer threshold (0–100): drafts scoring above this will be auto-rewritten. (default: 25)"

8. **Repo allowlist** — which git repo paths to scan for commits. **Defaults to empty — you must explicitly add repos.**
   - Ask: "Which git repo paths should be scanned for share-worthy commits? Enter full paths separated by commas, or press Enter to skip (you can add repos later by editing ~/.build-in-public/config.md)."

9. **Denylist** — terms that must never appear in a published post (client names, employer, unreleased product names, secrets).
   - Default: empty
   - Ask: "Enter any terms that must never appear in your posts (client names, employers, confidential project names). Separate with commas, or press Enter for none."

10. **Buffer credentials** — optional, for auto-queuing posts.
    - Ask: "Do you want to configure Buffer for auto-queuing posts? (y/n, default: n)"
    - If yes, ask:
      - "Enter your Buffer organization ID:"
      - "Enter your Buffer channel ID for LinkedIn (or press Enter to skip):"
      - "Enter your Buffer channel ID for X (or press Enter to skip):"
      - "Where is your Buffer personal access token stored? Enter the path to a file containing the token (e.g., ~/.secrets/buffer-token), or press Enter to skip (you will need to add it to config.md manually)."

Use a **single `AskUserQuestion` call** per question above, waiting for each answer before proceeding to the next. After all answers are collected, proceed to Step 2.

---

## Step 2: Write `~/.build-in-public/config.md`

Create the directory if it does not exist:

```bash
mkdir -p ~/.build-in-public
```

Build the YAML frontmatter from the collected values. Apply defaults for any field the user left blank:

- `output_dir`: the entered value, or `~/build-in-public-drafts`
- `platforms`: parsed list, or `[x, linkedin]`
- `voice_preset`: the chosen preset (required — ask again if blank)
- `voice_calibration_samples`: the entered path, or omit the key if blank
- `cadence_per_week`: the entered integer, or `2`
- `cadence_day`: the entered day, or `Monday`
- `humanizer_threshold`: the entered integer, or `25`
- `repo_allowlist`: the entered paths as a YAML list, or `[]` (empty list — never pre-populate)
- `denylist`: the entered terms as a YAML list, or `[]`
- `buffer_org_id`: the entered value, or omit the key if blank
- `buffer_channel_id_linkedin`: the entered value, or omit the key if blank
- `buffer_channel_id_x`: the entered value, or omit the key if blank
- `buffer_token_path`: the entered path, or omit the key if blank

Write `~/.build-in-public/config.md` with this structure. Replace each `<value>` with the actual collected value:

```markdown
---
output_dir: <output_dir>
platforms:
  - x
  - linkedin
voice_preset: <voice_preset>
voice_calibration_samples: <path or omit>
cadence_per_week: <integer>
cadence_day: <day>
humanizer_threshold: <integer>
repo_allowlist: []
denylist: []
---

# Build in Public — Config

Edit the YAML frontmatter above to change your settings at any time.
Re-run `/build-in-public:setup` to re-configure interactively.
```

Adjust the `platforms` list to match exactly what the user selected. Adjust `repo_allowlist` and `denylist` to contain only what the user explicitly entered (keep as `[]` if they pressed Enter). Include Buffer keys only if the user provided values for them. Omit `voice_calibration_samples` if the user left it blank.

Confirm the file was written:

```bash
cat ~/.build-in-public/config.md
```

---

## Step 3: Check for and optionally install the Humanizer dependency

The Humanizer is an external skill dependency from https://github.com/Aboudjem/humanizer-skill that scores posts for AI-tells (0–100) and rewrites them toward a target threshold.

**Check if it is already installed** by invoking the `humanizer` skill via the Skill tool with `--score` and a one-sentence test string. If the Skill tool returns a `[Score: NN/100]` result, the dependency is present — skip the install offer.

If the Skill tool reports the `humanizer` skill is not found (not installed), inform the user:

> The `humanizer` skill is not installed. It is needed to score and de-AI your drafts before review. Install it from: https://github.com/Aboudjem/humanizer-skill (follow the repo's README to add it as a Claude Code plugin/skill, then re-run `/build-in-public:setup`).

Then use `AskUserQuestion` to ask:

> Would you like to continue setup now and install the humanizer later? Or would you prefer to pause, install it, and re-run setup? (continue / pause)

If the user chooses to continue, proceed to Step 4. Note that `/build-in-public:draft` will warn about the missing humanizer at runtime until it is installed.

**If the humanizer IS installed**, seed its voice profile. The humanizer reads a `humanizer-context.md` file for brand-voice instructions so it preserves the user's style instead of defaulting to a generic rewrite. Locate the humanizer skill's root directory using:

```bash
claude skill list 2>/dev/null | grep humanizer || echo "not found via CLI"
```

If you can determine the humanizer skill's root path, write or update its `humanizer-context.md`. Construct the content from the user's voice preset and calibration samples:

- For `changelog` preset: focus on factual, low-hype language; short sentences; specific shipped artifacts.
- For `teacher` preset: clear explanations; concrete examples; reader benefit first.
- For `story` preset: narrative arc; opening hook; earned conclusion; avoid drama for its own sake.
- For `honest-struggle` preset: transparent about difficulty; no forced positivity; lessons over victories.

If `voice_calibration_samples` was provided, read the file at that path and append a `## Writing samples` section with up to 3 representative excerpts (first 200 chars each).

Write the `humanizer-context.md` to the humanizer skill's root directory. If the path cannot be determined automatically, tell the user the content to paste in manually:

> Humanizer voice profile (paste into `<humanizer-skill-root>/humanizer-context.md`):
> <content>

---

## Step 4: Register the weekly schedule and confirm the SessionEnd hook

### SessionEnd capture hook

The `SessionEnd` hook is shipped in `${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json` and is activated when the plugin is installed. Confirm it is active by checking that the file exists:

```bash
ls "${CLAUDE_PLUGIN_ROOT}/hooks/hooks.json" && echo "hooks.json present"
```

If the file is present, confirm to the user:

> SessionEnd capture hook: active — journal entries will be written automatically at the end of each Claude Code session.

If the file is missing, warn:

> Warning: hooks/hooks.json was not found at the expected path. The SessionEnd capture hook may not be active. Reinstall the plugin or check that the plugin directory is intact.

### Weekly schedule

Try to register the weekly draft schedule using the `schedule` skill (Claude Code's built-in scheduling mechanism):

Invoke the `schedule` skill via the Skill tool with args describing the job: run `/build-in-public:draft` on the configured `cadence_day`, weekly.

If the `schedule` skill is available and reports success, confirm:

> Weekly schedule registered — `/build-in-public:draft` will run automatically each <cadence_day>.

**Manual fallback (always document this regardless of whether the schedule skill succeeds):**

Tell the user the exact cron entry they can add manually if the automatic schedule is not available or if they prefer a system-level cron:

```
# Run Build in Public draft every <cadence_day> at 09:00 local time
# Add with: crontab -e
0 9 * * <weekday_number>  /path/to/claude -p "/build-in-public:draft" >> ~/.build-in-public/cron.log 2>&1
```

Where `<weekday_number>` is: Sunday=0, Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5, Saturday=6.

Replace `/path/to/claude` with the output of `which claude` (run it to get the real path). Display the cron entry with the correct weekday number for the user's chosen day so they can copy-paste it directly.

Also mention the manual trigger command:

> To run a draft anytime: `/build-in-public:draft`

---

## Step 5: Confirm what was written, installed, and scheduled

Present a compact summary to the user:

---

**Build in Public — Setup complete**

| Item | Status | Detail |
|------|--------|--------|
| Config file | Written | `~/.build-in-public/config.md` |
| Output dir | Configured | `<output_dir>` |
| Platforms | Configured | `<platforms>` |
| Voice preset | Set | `<voice_preset>` |
| Cadence | Set | `<cadence_per_week>` posts/week, <cadence_day> |
| Humanizer threshold | Set | `<humanizer_threshold>` |
| Repo allowlist | `<count>` repos | `<list or "empty — add repos to config.md to enable commit scanning">` |
| Denylist | `<count>` terms | `<list or "none">` |
| Buffer | `<configured / not configured>` | `<org + channel IDs if set, else "clipboard route will be used">` |
| Humanizer skill | `<installed / not installed>` | `<"voice profile seeded" or install URL>` |
| SessionEnd hook | `<active / missing>` | `hooks/hooks.json` |
| Weekly schedule | `<registered / manual fallback>` | `<day and time or cron entry>` |

---

Next step: run `/build-in-public:draft` to generate your first week's posts, or wait for the weekly cron to fire.
