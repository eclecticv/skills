# Build in Public Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a community Claude Code plugin that observes a developer's sessions and git commits, surfaces share-worthy moments, and drafts privacy-gated, algorithm-tuned X and LinkedIn posts in the user's voice — never auto-publishing.

**Architecture:** Five units — a `SessionEnd` capture hook writing to a local journal, a moment store, a weekly synthesizer skill (`/draft`), a privacy/redaction gate, and a publisher skill (`/publish`) — plus `setup` and `capture` skills. Deterministic mechanics live in three stdlib-only Python scripts (capture, secret-scan, commit-scan); all reasoning lives in SKILL.md instructions Claude executes.

**Tech Stack:** Claude Code plugin (markdown skills + `hooks.json`), Python 3 (stdlib only) for runtime scripts, pytest (dev-only) for tests, Aboudjem `humanizer-skill` as a dependency, Buffer (via the user's Buffer MCP or HTTP) as the optional scheduler.

## Global Constraints

- Runtime scripts MUST be Python 3, **stdlib only**, zero runtime dependencies. Tests may use `pytest` (dev-only).
- The pipeline MUST NEVER auto-publish. It always terminates at a human-reviewed draft.
- `repo_allowlist` MUST default to `[]` (empty) — git scanning is strictly opt-in.
- Humanizer AI-tell gate threshold default: **25** (refuse to queue posts scoring `> 25`).
- No hardcoded identities, voices, vault paths, or account IDs. All per-install config lives in `~/.build-in-public/config.md`.
- Scripts are config-free: they receive inputs via args/stdin. Skills read `config.md` and pass values to scripts.
- Use `${CLAUDE_PLUGIN_ROOT}` for all in-plugin paths referenced by hooks and skills.
- Output is markdown-first; Buffer is optional and uses the user's own Buffer MCP / HTTP fallback.
- Scripts honor the `BUILD_IN_PUBLIC_HOME` env var to override the base dir (used by tests).

---

### Task 1: Plugin scaffold + manifest

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.gitignore` (already exists from spec commit — verify/extend)
- Create: `requirements-dev.txt`

**Interfaces:**
- Produces: a valid plugin manifest discoverable by Claude Code.

- [ ] **Step 1: Write `.claude-plugin/plugin.json`**

```json
{
  "name": "build-in-public",
  "version": "0.1.0",
  "description": "Observes your Claude Code sessions and git commits, surfaces share-worthy moments, and drafts privacy-gated, algorithm-tuned X and LinkedIn posts in your voice. Never auto-publishes.",
  "author": { "name": "Build in Public" },
  "keywords": ["build-in-public", "social", "linkedin", "twitter", "x", "content", "devrel"]
}
```

- [ ] **Step 2: Ensure `.gitignore` covers state files**

```
node_modules/
.DS_Store
*.local.md
journal.jsonl
posted.jsonl
__pycache__/
.pytest_cache/
```

- [ ] **Step 3: Write `requirements-dev.txt`**

```
pytest>=8.0
```

- [ ] **Step 4: Verify the manifest parses**

Run: `python3 -c "import json; json.load(open('.claude-plugin/plugin.json'))" && echo OK`
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/plugin.json .gitignore requirements-dev.txt
git commit -m "feat: scaffold build-in-public plugin manifest"
```

---

### Task 2: Capture script (`capture_session.py`)

**Files:**
- Create: `scripts/capture_session.py`
- Test: `tests/test_capture_session.py`

**Interfaces:**
- Consumes: SessionEnd hook JSON on stdin (`session_id`, `transcript_path`, `cwd`).
- Produces: `detect_signals(text) -> list[str]`, `build_digest(hook_input, transcript_text, now=None) -> dict`, `append_journal(digest, path=None) -> None`, `journal_path() -> Path`. Appends one JSON line per session to `~/.build-in-public/journal.jsonl`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_capture_session.py
import json
import importlib.util
from pathlib import Path

def _load():
    p = Path(__file__).parent.parent / "scripts" / "capture_session.py"
    spec = importlib.util.spec_from_file_location("capture_session", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

cs = _load()

def test_detect_signals_finds_shipped_and_fixed():
    text = "We shipped the feature after we fixed the crash."
    assert cs.detect_signals(text) == ["fixed", "shipped"]

def test_detect_signals_empty_when_none():
    assert cs.detect_signals("just renamed a few variables") == []

def test_build_digest_extracts_repo_from_cwd():
    d = cs.build_digest({"session_id": "abc", "cwd": "/home/u/Developer/myrepo"}, "we shipped it")
    assert d["repo"] == "myrepo"
    assert d["session_id"] == "abc"
    assert d["signals"] == ["shipped"]

def test_append_journal_writes_one_line_each(tmp_path):
    jp = tmp_path / "journal.jsonl"
    cs.append_journal({"ts": "x", "signals": ["shipped"]}, path=jp)
    cs.append_journal({"ts": "y", "signals": []}, path=jp)
    lines = jp.read_text().strip().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["signals"] == ["shipped"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_capture_session.py -v`
Expected: FAIL — `ModuleNotFoundError`/`FileNotFoundError` (script doesn't exist yet).

- [ ] **Step 3: Write `scripts/capture_session.py`**

```python
#!/usr/bin/env python3
"""SessionEnd capture hook for Build in Public.

Reads hook JSON from stdin, derives a compact session digest with
share-worthy signals, and appends one JSON line to the local journal.
Stdlib only. No network calls; writes only to the local journal.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SIGNAL_PATTERNS = {
    "shipped": re.compile(r"\b(shipped|deployed|released|launched|went live|merged to main)\b", re.I),
    "fixed": re.compile(r"\b(fixed|bug|debugged|root cause|regression|crash)\b", re.I),
    "learned": re.compile(r"\b(learned|realized|turns out|TIL|gotcha|first time|never knew)\b", re.I),
}


def base_dir():
    return Path(os.environ.get("BUILD_IN_PUBLIC_HOME", str(Path.home() / ".build-in-public")))


def journal_path():
    return base_dir() / "journal.jsonl"


def detect_signals(text):
    return sorted(name for name, pat in SIGNAL_PATTERNS.items() if pat.search(text or ""))


def build_digest(hook_input, transcript_text, now=None):
    now = now or datetime.now(timezone.utc)
    cwd = hook_input.get("cwd", "") or ""
    return {
        "ts": now.isoformat(),
        "session_id": hook_input.get("session_id", ""),
        "cwd": cwd,
        "repo": Path(cwd).name if cwd else "",
        "signals": detect_signals(transcript_text),
    }


def read_transcript(path):
    try:
        return Path(path).read_text(errors="ignore") if path else ""
    except OSError:
        return ""


def append_journal(digest, path=None):
    path = path or journal_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(digest) + "\n")


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # never block session teardown
    transcript_text = read_transcript(hook_input.get("transcript_path"))
    digest = build_digest(hook_input, transcript_text)
    if digest["signals"] or digest["repo"]:
        append_journal(digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_capture_session.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add scripts/capture_session.py tests/test_capture_session.py
git commit -m "feat: add session capture script with signal detection"
```

---

### Task 3: Hook wiring (`hooks/hooks.json`)

**Files:**
- Create: `hooks/hooks.json`

**Interfaces:**
- Consumes: `scripts/capture_session.py` (Task 2).
- Produces: a `SessionEnd` hook that pipes hook JSON to the capture script.

- [ ] **Step 1: Write `hooks/hooks.json`**

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/capture_session.py"
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 2: Verify the hook JSON parses**

Run: `python3 -c "import json; json.load(open('hooks/hooks.json'))" && echo OK`
Expected: `OK`

- [ ] **Step 3: Smoke-test the hook end-to-end with a temp home**

Run:
```bash
BUILD_IN_PUBLIC_HOME=$(mktemp -d) bash -c '
echo "{\"session_id\":\"t1\",\"cwd\":\"/x/Developer/demo\",\"transcript_path\":\"\"}" \
  | python3 scripts/capture_session.py
cat "$BUILD_IN_PUBLIC_HOME/journal.jsonl"'
```
Expected: one JSON line containing `"repo": "demo"` and `"signals": []`.

- [ ] **Step 4: Commit**

```bash
git add hooks/hooks.json
git commit -m "feat: wire SessionEnd capture hook"
```

---

### Task 4: Secret-scan script (`secret_scan.py`)

**Files:**
- Create: `scripts/secret_scan.py`
- Test: `tests/test_secret_scan.py`

**Interfaces:**
- Consumes: text via `--file` or stdin; `--deny TERM` (repeatable).
- Produces: `scan(text, denylist=None) -> list[dict]`, `shannon_entropy(s) -> float`. CLI prints `{"clean": bool, "findings": [...]}` and exits `1` if any finding (so skills gate on exit code).

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_secret_scan.py
import importlib.util
from pathlib import Path

def _load():
    p = Path(__file__).parent.parent / "scripts" / "secret_scan.py"
    spec = importlib.util.spec_from_file_location("secret_scan", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ss = _load()

def test_scan_detects_openai_key():
    f = ss.scan("here is my key sk-abcdefghij1234567890XYZ token")
    assert any(x["type"] == "openai_key" for x in f)

def test_scan_detects_aws_key():
    assert any(x["type"] == "aws_access_key" for x in ss.scan("AKIAIOSFODNN7EXAMPLE in code"))

def test_scan_flags_denylist_case_insensitive():
    f = ss.scan("We helped AcmeCorp ship", denylist=["acmecorp"])
    assert any(x["type"] == "denylist" for x in f)

def test_scan_clean_text_returns_empty():
    assert ss.scan("Shipped a clean caching layer today. No secrets here.") == []

def test_entropy_of_repeated_char_is_zero():
    assert ss.shannon_entropy("aaaa") == 0.0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_secret_scan.py -v`
Expected: FAIL — script not found.

- [ ] **Step 3: Write `scripts/secret_scan.py`**

```python
#!/usr/bin/env python3
"""Privacy/redaction gate for Build in Public.

Scans candidate post text for secrets and denylisted terms. Prints a JSON
report and exits non-zero if any finding is present, so a skill can gate on
the exit code. Stdlib only.
"""
import argparse
import json
import math
import re
import sys

SECRET_PATTERNS = {
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "anthropic_key": re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    "vcs_token": re.compile(r"\b(?:ghp|gho|github_pat|xoxb|xoxp)_[A-Za-z0-9_\-]{10,}\b"),
    "bearer": re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{16,}\b"),
    "env_assignment": re.compile(r"(?m)^[A-Z][A-Z0-9_]{2,}\s*=\s*\S+"),
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


def shannon_entropy(s):
    if not s:
        return 0.0
    n = len(s)
    counts = {c: s.count(c) for c in set(s)}
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def find_high_entropy_tokens(text, min_len=28, threshold=4.2):
    out = []
    for token in re.findall(r"[A-Za-z0-9+/=_\-]{%d,}" % min_len, text):
        if shannon_entropy(token) >= threshold:
            out.append(token)
    return out


def scan(text, denylist=None):
    denylist = denylist or []
    findings = []
    for name, pat in SECRET_PATTERNS.items():
        for m in pat.findall(text):
            findings.append({"type": name, "match": m if isinstance(m, str) else m[0]})
    for token in find_high_entropy_tokens(text):
        findings.append({"type": "high_entropy", "match": token})
    for term in denylist:
        if term and re.search(re.escape(term), text, re.I):
            findings.append({"type": "denylist", "match": term})
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    ap.add_argument("--deny", action="append", default=[])
    args = ap.parse_args(argv)
    text = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    findings = scan(text, args.deny)
    json.dump({"clean": not findings, "findings": findings}, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_secret_scan.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add scripts/secret_scan.py tests/test_secret_scan.py
git commit -m "feat: add secret/denylist redaction scanner"
```

---

### Task 5: Commit-scan script (`scan_commits.py`)

**Files:**
- Create: `scripts/scan_commits.py`
- Test: `tests/test_scan_commits.py`

**Interfaces:**
- Consumes: `--repo PATH` (repeatable, allowlist), `--since "7 days ago"`.
- Produces: `signals_for(subject) -> list[str]`, `git_log(repo, since) -> list[dict]`, `scan(repos, since) -> list[dict]`. CLI prints commits as JSON. Only reads repos explicitly passed (never auto-discovers).

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_scan_commits.py
import importlib.util
import subprocess
from pathlib import Path

def _load():
    p = Path(__file__).parent.parent / "scripts" / "scan_commits.py"
    spec = importlib.util.spec_from_file_location("scan_commits", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

sc = _load()

def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)

def _make_repo(tmp_path):
    repo = tmp_path / "demo-repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "Tester")
    (repo / "f.txt").write_text("a")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "ship: release v1.2")
    return repo

def test_signals_for_detects_ship():
    assert "shipped" in sc.signals_for("ship: release v1.2")

def test_signals_for_detects_fix():
    assert "fixed" in sc.signals_for("fix: null pointer in parser")

def test_scan_returns_commit_with_signal(tmp_path):
    repo = _make_repo(tmp_path)
    commits = sc.scan([str(repo)], "1 year ago")
    assert len(commits) == 1
    assert commits[0]["subject"] == "ship: release v1.2"
    assert commits[0]["repo"] == "demo-repo"
    assert "shipped" in commits[0]["signals"]

def test_scan_nonexistent_repo_is_empty():
    assert sc.scan(["/no/such/repo/here"], "1 year ago") == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_scan_commits.py -v`
Expected: FAIL — script not found.

- [ ] **Step 3: Write `scripts/scan_commits.py`**

```python
#!/usr/bin/env python3
"""Scan allowlisted git repos for recent commits as Build in Public candidates.

Stdlib only (shells out to `git`). Prints commits as JSON. Only reads repos
explicitly passed in (allowlist); never auto-discovers.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SHIP_RE = re.compile(r"\b(ship|shipped|release|released|deploy|launch|v\d+\.\d+)\b", re.I)
FIX_RE = re.compile(r"\b(fix|fixed|bug|hotfix|patch|revert)\b", re.I)


def signals_for(subject):
    s = []
    if SHIP_RE.search(subject):
        s.append("shipped")
    if FIX_RE.search(subject):
        s.append("fixed")
    return s


def git_log(repo, since):
    fmt = "%H%x1f%an%x1f%aI%x1f%s"
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "log", f"--since={since}", f"--pretty=format:{fmt}"],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if out.returncode != 0:
        return []
    commits = []
    for line in out.stdout.splitlines():
        if not line.strip():
            continue
        h, author, date, subject = line.split("\x1f")
        commits.append({
            "repo": Path(repo).name,
            "hash": h,
            "short": h[:8],
            "author": author,
            "date": date,
            "subject": subject,
            "signals": signals_for(subject),
        })
    return commits


def scan(repos, since):
    out = []
    for r in repos:
        out.extend(git_log(r, since))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", action="append", default=[])
    ap.add_argument("--since", default="7 days ago")
    args = ap.parse_args(argv)
    json.dump(scan(args.repo, args.since), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_scan_commits.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add scripts/scan_commits.py tests/test_scan_commits.py
git commit -m "feat: add allowlisted git commit scanner"
```

---

### Task 6: Reference docs

**Files:**
- Create: `references/scoring-rubric.md`
- Create: `references/linkedin-algo.md`
- Create: `references/x-algo.md`
- Create: `references/redaction-rules.md`

**Interfaces:**
- Produces: knowledge files consumed by the `/draft` skill (Task 8).

- [ ] **Step 1: Write `references/scoring-rubric.md`**

Content MUST include: the four axes with 0–5 anchors and signal heuristics, verbatim:
- **Innovation** (novel approach / first use of a technology / clever solution) — signals: first-time deps/imports, new file types, unusual problem-solving arcs.
- **Insight** (a non-obvious learning) — signals: long exploration → concise conclusion, "TIL"-shaped arcs.
- **Lesson** (mistake → fix / debugging war story) — signals: extended debugging, revert→retry, fix commits after failures.
- **Shipped** (released/deployed/merged/launched) — signals: commit subjects matching ship/release/deploy/launch, tags, merges to main.
- Selection rule: composite score, pick top 1–2, enforce **axis variety** across weeks (don't post two "shipped" in a row).

- [ ] **Step 2: Write `references/linkedin-algo.md`**

Content MUST include these rules as a checklist: hook in first 1–2 lines (names the topic in plain nouns + the payoff); target 280–420 words; exactly one structurally-visible save-worthy artifact (named framework / numbered list / copy-paste line / rule of thumb); no engagement bait ("Agree?", "Thoughts?"); no hashtags; closing line is a sharpening reframe, not a question; embed the receipt (commit/PR reference).

- [ ] **Step 3: Write `references/x-algo.md`**

Content MUST include: first-line hook carries the whole value (assume no expand); single post by default; thread ONLY for shipped milestones (first post = the result, subsequent = the how); media bias (note v2 will add shipped-card images); concise, concrete, no hashtags; include the receipt link.

- [ ] **Step 4: Write `references/redaction-rules.md`**

Content MUST include: the secret categories `secret_scan.py` detects (AWS/Anthropic/OpenAI/VCS tokens, Bearer, env assignments, private keys, high-entropy); the never-post list (client/employer names via denylist, unreleased product names, internal URLs); and the rule that ANY finding blocks the draft pending human edit.

- [ ] **Step 5: Verify all four files exist and are non-empty**

Run: `for f in references/scoring-rubric.md references/linkedin-algo.md references/x-algo.md references/redaction-rules.md; do test -s "$f" && echo "OK $f" || echo "MISSING $f"; done`
Expected: four `OK` lines.

- [ ] **Step 6: Commit**

```bash
git add references/
git commit -m "docs: add scoring rubric, platform algo, and redaction references"
```

---

### Task 7: `/build-in-public:capture` skill

**Files:**
- Create: `skills/capture/SKILL.md`

**Interfaces:**
- Consumes: `scripts/capture_session.py` (Task 2).
- Produces: a user-invoked command that logs the current session as a moment on demand.

- [ ] **Step 1: Write `skills/capture/SKILL.md`**

Frontmatter (verbatim):
```yaml
---
name: capture
description: Manually log the current Claude Code session as a Build in Public moment. Use when the user says "capture this", "log this for build in public", or wants to save a notable session highlight to the journal right now.
argument-hint: "[optional note]"
allowed-tools: Bash, Read
---
```
Body MUST instruct Claude to: (1) determine the current `cwd` and transcript path; (2) invoke `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/capture_session.py` with a synthesized stdin JSON (`session_id`, `cwd`, `transcript_path`) OR append a hand-built digest including the user's optional note; (3) confirm the journal line written and which signals were detected. Instructions are written FOR Claude.

- [ ] **Step 2: Validate with skill-reviewer**

Dispatch the `plugin-dev:skill-reviewer` agent on `skills/capture/SKILL.md`; address any description/triggering/style findings inline.

- [ ] **Step 3: Commit**

```bash
git add skills/capture/SKILL.md
git commit -m "feat: add /build-in-public:capture skill"
```

---

### Task 8: `/build-in-public:draft` skill (core synthesizer)

**Files:**
- Create: `skills/draft/SKILL.md`

**Interfaces:**
- Consumes: `journal.jsonl`, `scripts/scan_commits.py`, `scripts/secret_scan.py`, all four `references/*.md`, the Humanizer dependency, and `config.md`.
- Produces: review-ready markdown drafts in the configured output dir; a notification.

- [ ] **Step 1: Write `skills/draft/SKILL.md`**

Frontmatter (verbatim):
```yaml
---
name: draft
description: Generate this week's Build in Public posts. Reads the moment journal and allowlisted git commits, scores the share-worthy moments, drafts algorithm-tuned X and LinkedIn posts in the user's voice, runs the privacy gate and Humanizer, and saves review-ready drafts. Use when the user says "draft my build in public posts", "run build in public", "what should I post this week", or when the weekly cron fires.
allowed-tools: Bash, Read, Write, Edit, Skill, AskUserQuestion
---
```
Body MUST instruct Claude, in order:
1. Read `~/.build-in-public/config.md` (output dir, platforms, voice preset + calibration, cadence, threshold, repo allowlist, denylist). If missing, tell the user to run `/build-in-public:setup` and stop.
2. Read the past week's entries from `~/.build-in-public/journal.jsonl`.
3. Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/scan_commits.py` with one `--repo` per allowlisted repo and `--since "7 days ago"`. (If allowlist is empty, note it and rely on the journal only.)
4. Score candidates using `references/scoring-rubric.md`; select top 1–2 with axis variety vs the most recent entries in `posted.jsonl`.
5. For each selected moment, draft per-platform posts following `references/linkedin-algo.md` and `references/x-algo.md`, in the configured voice preset/calibration, **embedding the receipt** (commit short hash/subject or PR link) — receipts-first is mandatory.
6. Run the privacy gate: pipe each draft to `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/secret_scan.py` with one `--deny` per denylist term. If exit code is non-zero, show findings and block that draft (offer to rewrite without the offending content); never proceed past a finding silently.
7. Run the Humanizer: invoke the `humanizer` skill in detect mode; if AI-tell `> threshold`, run rewrite/`--iterate` until `<= threshold`. If the dependency is absent, warn and continue with a clear "not humanized" marker.
8. Write each final draft as a markdown file to the configured output dir, filename `YYYY-MM-DD-<platform>-<slug>.md`, with frontmatter (moment id, axis, score, receipt, humanizer score).
9. Present a summary in chat and STOP for human review. Do NOT publish.

- [ ] **Step 2: Validate with skill-reviewer**

Dispatch `plugin-dev:skill-reviewer` on `skills/draft/SKILL.md`; address findings inline.

- [ ] **Step 3: Commit**

```bash
git add skills/draft/SKILL.md
git commit -m "feat: add /build-in-public:draft core synthesizer skill"
```

---

### Task 9: `/build-in-public:publish` skill

**Files:**
- Create: `skills/publish/SKILL.md`

**Interfaces:**
- Consumes: an approved draft file, `config.md` (Buffer creds optional), `posted.jsonl`.
- Produces: a queued/copied post; appends a record to `posted.jsonl`.

- [ ] **Step 1: Write `skills/publish/SKILL.md`**

Frontmatter (verbatim):
```yaml
---
name: publish
description: Publish or queue an approved Build in Public draft. Use when the user says "publish this draft", "queue my build in public post", or "send this to Buffer". Only acts on a draft the user has explicitly approved.
argument-hint: "<path-to-approved-draft.md>"
allowed-tools: Bash, Read, Edit, AskUserQuestion
---
```
Body MUST instruct Claude to: (1) read the approved draft file named in the argument; (2) confirm explicit approval before any external action; (3) if Buffer creds are configured, queue via the user's Buffer MCP tool `mcp__buffer__create_post` (org + channel from config), else fall back to the documented HTTP curl; if no scheduler configured, copy to clipboard (`pbcopy`/`xclip`) and tell the user to paste; (4) on success, append a line to `~/.build-in-public/posted.jsonl` with moment id, platform, axis, timestamp, and any returned post id; (5) NEVER queue without a returned success — surface errors verbatim and do not mark posted.

- [ ] **Step 2: Validate with skill-reviewer**

Dispatch `plugin-dev:skill-reviewer` on `skills/publish/SKILL.md`; address findings inline.

- [ ] **Step 3: Commit**

```bash
git add skills/publish/SKILL.md
git commit -m "feat: add /build-in-public:publish skill"
```

---

### Task 10: `/build-in-public:setup` skill

**Files:**
- Create: `skills/setup/SKILL.md`

**Interfaces:**
- Consumes: user answers; the Humanizer dependency; the host's cron/schedule mechanism.
- Produces: `~/.build-in-public/config.md`; an installed Humanizer dep; a registered weekly schedule.

- [ ] **Step 1: Write `skills/setup/SKILL.md`**

Frontmatter (verbatim):
```yaml
---
name: setup
description: Configure the Build in Public plugin. Use when the user says "set up build in public", "configure build in public", or on first run. Collects output destination, platforms, voice, cadence, repo allowlist, denylist, and optional Buffer credentials, then installs the Humanizer dependency and schedules the weekly run.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---
```
Body MUST instruct Claude to:
1. Use `AskUserQuestion` to collect: output dir (default `~/build-in-public-drafts`); platforms (X, LinkedIn); voice preset (changelog / teacher / story / honest-struggle) + optional path to writing samples for calibration; cadence/day; Humanizer threshold (default 25); **repo allowlist (default empty — explicit opt-in)**; denylist terms; optional Buffer org + channel ids.
2. Write `~/.build-in-public/config.md` with YAML frontmatter holding those values (this file is read by the other skills).
3. Check for the `humanizer` skill; if absent, offer to install Aboudjem `humanizer-skill` from its marketplace/repo (`https://github.com/Aboudjem/humanizer-skill`) and seed its `humanizer-context.md` from the user's voice preset/samples.
4. Register a weekly schedule that runs `/build-in-public:draft` (use the host's scheduling skill/cron); document the manual fallback if scheduling is unavailable.
5. Confirm what was written, installed, and scheduled.

- [ ] **Step 2: Validate with skill-reviewer**

Dispatch `plugin-dev:skill-reviewer` on `skills/setup/SKILL.md`; address findings inline.

- [ ] **Step 3: Commit**

```bash
git add skills/setup/SKILL.md
git commit -m "feat: add /build-in-public:setup skill"
```

---

### Task 11: README + full plugin validation

**Files:**
- Create: `README.md`

**Interfaces:**
- Produces: install/usage/privacy documentation; a validated plugin.

- [ ] **Step 1: Write `README.md`**

MUST include: overview; the never-auto-publish + repo-allowlist-opt-in privacy model up front; prerequisites (Python 3, git, optional Buffer account, Humanizer dependency); install steps; the four commands and the capture hook; config reference (`~/.build-in-public/config.md` fields); v2 roadmap (shipped-card images, build-log continuity, tease→payoff, Typefully, meta-distribution footer).

- [ ] **Step 2: Run the full test suite**

Run: `python3 -m pytest -v`
Expected: all tests pass (13 total across Tasks 2/4/5).

- [ ] **Step 3: Validate the whole plugin**

Dispatch the `plugin-dev:plugin-validator` agent on the plugin root; fix any critical issues inline (manifest, structure, naming, hook schema, security).

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add README and finalize v1 plugin validation"
```

---

## Self-Review

**Spec coverage:**
- Capture hook → Tasks 2, 3. Moment store → Tasks 2 (journal), 9 (posted). Weekly synthesizer → Task 8. Privacy gate → Tasks 4, 6 (redaction-rules), 8 (step 6). Publisher → Task 9. `setup`/`capture` commands → Tasks 10, 7. Scoring rubric → Task 6 + Task 8 step 4. Algo references → Task 6. Humanizer dependency → Tasks 8 (step 7), 10 (step 3). Buffer → Task 9. Cron via setup → Task 10 step 4. Receipts-first → Task 8 step 5. Defaults → Tasks 8/10. v2 deferrals → README (Task 11). All spec sections map to a task.

**Placeholder scan:** No "TBD/TODO/implement later". Script tasks contain complete code; markdown-component tasks specify exact required content + a concrete validation command. No fabricated symbols.

**Type consistency:** `journal_path`, `detect_signals`, `build_digest`, `append_journal` (Task 2) are referenced consistently. `scan`/`signals_for`/`git_log` (Task 5) and `scan`/`shannon_entropy` (Task 4) match their call sites. Scripts are config-free per the Global Constraints; skills pass `--deny`/`--repo`/`--since`, matching the CLIs defined in Tasks 4 and 5.
