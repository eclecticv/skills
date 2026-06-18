---
name: capture
description: Manually log the current Claude Code session as a Build in Public moment. Use when the user says "capture this", "log this for build in public", or wants to save a notable session highlight to the journal right now.
argument-hint: "[optional note]"
allowed-tools: Bash, Read
---

You are capturing the current Claude Code session as a Build in Public journal entry on demand.

## Step 1: Gather session context

Run the following to collect the values you need:

```bash
echo "CWD: $(pwd)"
echo "SESSION_ID: ${CLAUDE_SESSION_ID:-unknown}"
echo "TRANSCRIPT: ${CLAUDE_TRANSCRIPT_PATH:-}"
```

- `cwd`: the current working directory (from `pwd` or `$PWD`)
- `session_id`: use `$CLAUDE_SESSION_ID` if set; otherwise use `"unknown"`
- `transcript_path`: use `$CLAUDE_TRANSCRIPT_PATH` if set; otherwise pass an empty string `""`

## Step 2: Invoke the capture script

Pipe a JSON object to the capture script via stdin. Build the JSON safely using Python's `json.dumps` to handle any special characters in the values:

```bash
python3 -c "
import json, subprocess, os, sys
payload = {
    'session_id': os.environ.get('CLAUDE_SESSION_ID', 'unknown'),
    'cwd': os.getcwd(),
    'transcript_path': os.environ.get('CLAUDE_TRANSCRIPT_PATH', ''),
}
proc = subprocess.run(
    ['python3', os.path.join(os.environ.get('CLAUDE_PLUGIN_ROOT', ''), 'scripts', 'capture_session.py')],
    input=json.dumps(payload),
    text=True,
    capture_output=True,
)
sys.stdout.write(proc.stdout)
sys.stderr.write(proc.stderr)
sys.exit(proc.returncode)
"
```

## Step 3: Read the journal to confirm

After the script exits, read the last line of the journal to confirm the entry was written:

```bash
tail -1 "${BUILD_IN_PUBLIC_HOME:-$HOME/.build-in-public}/journal.jsonl"
```

Parse the JSON line and extract `ts`, `repo`, and `signals`.

## Step 4: Confirm to the user

Report back with a one-line summary in this format:

> Captured — repo: **`<repo>`**, signals: `[<signal1>, <signal2>]`, logged at `<ts>`.

If the user provided an optional `[note]` argument, append it as a parenthetical:

> Captured — repo: **`<repo>`**, signals: `[shipped]`, logged at `<ts>`. *(Note: "<their note>")*

If the journal line was not written (i.e., `tail -1` returns a line older than now, or the file doesn't exist), tell the user: "Nothing was captured — no signals were detected and no repo could be determined from the current directory. Try running from inside a project directory, or make sure the session transcript contains share-worthy keywords (shipped, fixed, learned, etc.)."

## Notes

- The script appends a journal entry only when it detects at least one signal keyword OR can derive a repo name from `cwd`. If neither condition holds, no line is written and you should surface the guidance above.
- The `$CLAUDE_PLUGIN_ROOT` variable is set by the Claude Code plugin runtime to the directory containing `plugin.json`. The capture script lives at `${CLAUDE_PLUGIN_ROOT}/scripts/capture_session.py`.
- Do not pass the user's note into the stdin JSON — the script has no `note` field. The note is for your confirmation message only.
