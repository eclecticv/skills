---
name: capture
description: Manually log the current Claude Code session as a Build in Public moment. Use when the user says "capture this", "log this for build in public", or wants to save a notable session highlight to the journal right now.
argument-hint: "[optional note]"
allowed-tools: Bash, Read
---

You are capturing the current Claude Code session as a Build in Public journal entry on demand.

## Step 1: Gather session context

Run the following to locate the session transcript. The session id is available as the skill substitution `${CLAUDE_SESSION_ID}` (expanded before the bash runs — do NOT use it as a shell variable `$CLAUDE_SESSION_ID`):

```bash
transcript=$(find "$HOME/.claude/projects" -type f -name "${CLAUDE_SESSION_ID}.jsonl" 2>/dev/null | head -1)
echo "CWD: $(pwd)"
echo "SESSION_ID: ${CLAUDE_SESSION_ID}"
echo "TRANSCRIPT: $transcript"
```

- `cwd`: the current working directory (from `$(pwd)`)
- `session_id`: the value of the skill substitution `${CLAUDE_SESSION_ID}` (expanded in this file; not a shell env var)
- `transcript_path`: the result of the `find` above — may be empty if the transcript is not yet flushed to disk; that is acceptable graceful degradation

## Step 2: Invoke the capture script

Pipe a JSON object to the capture script via stdin. Build the JSON safely using Python's `json.dumps` to handle any special characters in the values. Substitute `${CLAUDE_SESSION_ID}` directly in the heredoc (it is expanded by the skill runtime before bash executes):

```bash
python3 -c "
import json, subprocess, os, sys
payload = {
    'session_id': '${CLAUDE_SESSION_ID}',
    'cwd': os.getcwd(),
    'transcript_path': os.environ.get('_TRANSCRIPT', ''),
}
proc = subprocess.run(
    ['python3', os.path.join(os.environ.get('CLAUDE_PLUGIN_ROOT', ''), 'scripts', 'capture_session.py')],
    input=json.dumps(payload),
    text=True,
    capture_output=True,
    env={**os.environ, '_TRANSCRIPT': '$transcript'},
)
sys.stdout.write(proc.stdout)
sys.stderr.write(proc.stderr)
sys.exit(proc.returncode)
"
```

If `transcript_path` is empty, the capture script will still run and record a repo-only digest from `cwd`. Tell the user "transcript signals were unavailable" in that case.

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
- `${CLAUDE_PLUGIN_ROOT}` is a skill substitution (not a shell env var) expanded by the Claude Code plugin runtime to the directory containing `plugin.json`. The capture script lives at `${CLAUDE_PLUGIN_ROOT}/scripts/capture_session.py`.
- `${CLAUDE_SESSION_ID}` is likewise a skill substitution, expanded in this file before bash executes. Do NOT reference it as `$CLAUDE_SESSION_ID` in shell — it will be empty. There is no `$CLAUDE_TRANSCRIPT_PATH` env var in Claude Code; the transcript is located via `find "$HOME/.claude/projects" -name "${CLAUDE_SESSION_ID}.jsonl"`.
- Do not pass the user's note into the stdin JSON — the script has no `note` field. The note is for your confirmation message only.
