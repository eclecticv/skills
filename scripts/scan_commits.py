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
