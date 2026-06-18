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
    cwd = hook_input.get("cwd") or os.getcwd()
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
