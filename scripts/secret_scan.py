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
