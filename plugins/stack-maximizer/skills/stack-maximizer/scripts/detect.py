#!/usr/bin/env python3
"""Match vendor signatures against local text sources.

Every collector (website HTML/network hosts, DNS records, email headers,
browser history, chat logs, repo files) dumps plain text, then pipes it or
points it here. One matcher keeps detection deterministic and comparable
across sources.

Usage:
  detect.py --source web  [--tokens]          FILE|DIR|- ...
  detect.py --source chat [--names] [--since 180] DIR ...
  detect.py ... --table          human-readable instead of JSON

Matching:
  domains  always on, case-insensitive, hostname-boundary anchored so
           "kit.com" never matches "toolkit.com".
  --tokens case-sensitive literals (JS globals, DNS verification keys,
           dkim:<selector> markers). Use for web and dns sources only: short
           tokens like "AW-" are noise in prose.
  --names  vendor names as whole words. Use for chat logs and email
           subjects (receipts from Stripe/Paddle name the vendor in text).
           Names that are common English words are skipped; those vendors
           need a domain hit.

Snippets are redacted (long opaque strings, email local parts) because chat
logs and repo files can contain keys. Output never includes secrets on purpose.
"""
import argparse, datetime as dt, json, os, re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SIGS = HERE.parent / "references" / "signatures.json"

# Names that collide with ordinary words or other products. Name-matching them
# in prose would flood the inventory, so they only count via domain hits.
AMBIGUOUS = {"make", "close", "front", "later", "plain", "writer", "hex", "grain",
             "circle", "kit", "loops", "clay", "dub", "folk", "twenty", "vector",
             "unify", "koala", "census", "shield", "orum", "nooks", "relay.app",
             "otter", "luma", "moz", "tally", "buffer", "notion", "segment",
             "copper", "crisp", "heap", "wix", "ghost", "g2", "hunter", "zoom webinars",
             "gong", "fathom", "drift", "mutiny", "attio", "granola", "sanity",
             "framer", "riverside", "metabase", "outreach", "reply.io", "later"}

SECRETISH = re.compile(r"[A-Za-z0-9_\-+/=]{28,}")
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@([A-Za-z0-9.\-]+\.[A-Za-z]{2,})")


def redact(s: str) -> str:
    s = SECRETISH.sub("<redacted>", s)
    return EMAIL.sub(r"…@\1", s)


def build(vendors, use_tokens, use_names, all_names=False, ci_names=False):
    dom_map, tok_map, name_map = {}, {}, {}
    for v in vendors:
        for d in v["domains"]:
            dom_map[d.lower()] = v["name"]
        if use_tokens:
            for t in v["tokens"]:
                tok_map[t] = v["name"]
        if use_names:
            for alt in re.split(r"\s*/\s*", v["name"].split(" (")[0]):
                if all_names or (alt.lower() not in AMBIGUOUS and len(alt) >= 4):
                    name_map[alt] = v["name"]
    def alt(keys):
        # Trie-shaped regex: Python's re does not factor common prefixes out of
        # a plain alternation, so ~400 flat branches were retried at every
        # character (5+ minutes for 30 days of chat logs). Shared prefixes make
        # each position cheap. Longer branches are tried first, so the longest
        # key wins ("us.i.posthog.com" before "posthog.com").
        trie = {}
        for k in keys:
            node = trie
            for ch in (k.lower() if ci_flag[0] else k):
                node = node.setdefault(ch, {})
            node[""] = True
        def emit(node):
            end = node.get("", False)
            branches = [re.escape(ch) + emit(sub) for ch, sub in sorted(((c, v) for c, v in node.items() if c), key=lambda kv: -depth(kv[1]))]
            if not branches:
                return ""
            body = branches[0] if len(branches) == 1 else "(?:" + "|".join(branches) + ")"
            return "(?:" + body + ")?" if end else body
        return emit(trie)
    def depth(node):
        return 1 + max((depth(v) for k, v in node.items() if k), default=0)
    ci_flag = [True]
    dom_re = re.compile(r"(?<![a-z0-9\-])(" + alt(dom_map) + r")(?![a-z0-9])", re.I) if dom_map else None
    ci_flag[0] = False
    tok_re = re.compile("(" + alt(tok_map) + ")") if tok_map else None
    if ci_names:
        name_map = {k.lower(): v for k, v in name_map.items()}
    ci_flag[0] = ci_names
    name_re = re.compile(r"\b(" + alt(name_map) + r")\b", re.I if ci_names else 0) if name_map else None
    return [(dom_re, dom_map, "domain", True), (tok_re, tok_map, "token", False),
            (name_re, name_map, "name", ci_names)]


def iter_files(paths, since_days, exts):
    cutoff = None
    if since_days:
        cutoff = dt.datetime.now().timestamp() - since_days * 86400
    for p in paths:
        if p == "-":
            yield "-", None
            continue
        p = pathlib.Path(os.path.expanduser(p))
        files = [p] if p.is_file() else (f for f in p.rglob("*") if f.is_file())
        for f in files:
            try:
                st = f.stat()
            except OSError:
                continue
            if cutoff and st.st_mtime < cutoff:
                continue
            if exts and f.suffix.lower() not in exts:
                continue
            yield str(f), st.st_mtime


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--source", required=True, help="label: web, dns, email, history, chat, repo, apps, mcp ...")
    ap.add_argument("--tokens", action="store_true")
    ap.add_argument("--names", action="store_true")
    ap.add_argument("--all-names", action="store_true", help="include ambiguous names; only for precise lists (apps, extensions, env keys, packages)")
    ap.add_argument("--ci", action="store_true", help="case-insensitive name matching (env keys, package names)")
    ap.add_argument("--weighted", action="store_true", help="lines end in a count (history.txt): add it to hits")
    ap.add_argument("--exclude-containing", default="stack-maximizer",
                    help="skip files containing this marker, so the skill's own past runs in chat logs do not count as evidence")
    ap.add_argument("--since", type=int, default=0, help="only files modified in the last N days")
    ap.add_argument("--ext", default="", help="comma list of extensions, e.g. .jsonl,.md")
    ap.add_argument("--max-bytes", type=int, default=300_000_000, help="skip files larger than this")
    ap.add_argument("--table", action="store_true")
    a = ap.parse_args()

    vendors = json.loads(SIGS.read_text())["vendors"]
    meta = {v["name"]: v for v in vendors}
    matchers = build(vendors, a.tokens, a.names or a.all_names, a.all_names, a.ci)
    exts = {e.strip().lower() for e in a.ext.split(",") if e.strip()}
    agg, scanned, skipped = {}, 0, []

    for path, mtime in iter_files(a.paths, a.since, exts):
        try:
            if path != "-" and os.path.getsize(path) > a.max_bytes:
                skipped.append(path); continue
            fh = sys.stdin if path == "-" else open(path, "r", errors="ignore")
        except (OSError, PermissionError) as e:
            skipped.append(f"{path} ({e.__class__.__name__})"); continue
        scanned += 1
        if path != "-":
            with open(path, "rb") as bh:
                if b"\x00" in bh.read(4096):
                    fh.close(); continue  # binary
            if a.exclude_containing and os.path.getsize(path) < 50_000_000:
                with open(path, "r", errors="ignore") as xh:
                    if a.exclude_containing in xh.read():
                        fh.close(); skipped.append(f"{path} (self-reference)"); continue
        with fh:
            for line in fh:
                w = 1
                if a.weighted:
                    m_w = re.search(r"\s(\d+)\s*$", line)
                    w = int(m_w.group(1)) if m_w else 1
                for rx, mp, kind, ci in matchers:
                    if not rx:
                        continue
                    for m in rx.finditer(line):
                        key = m.group(1).lower() if ci else m.group(1)
                        name = mp.get(key)
                        if not name:
                            continue
                        r = agg.setdefault(name, {"hits": 0, "files": set(), "kinds": set(),
                                                  "last_seen": 0, "evidence": []})
                        r["hits"] += w
                        r["files"].add(path)
                        r["kinds"].add(kind)
                        if mtime:
                            r["last_seen"] = max(r["last_seen"], mtime)
                        if len(r["evidence"]) < 3 and path not in [e["file"] for e in r["evidence"]]:
                            s = max(0, m.start() - 60)
                            r["evidence"].append({"file": path, "snippet": redact(line[s:m.end() + 60].strip())})

    rows = []
    for name, r in sorted(agg.items(), key=lambda kv: -kv[1]["hits"]):
        v = meta[name]
        rows.append({"vendor": name, "caps": v["caps"], "product_risk": v["product_risk"],
                     "source": a.source, "hits": r["hits"], "files": len(r["files"]),
                     "match_kinds": sorted(r["kinds"]),
                     "last_seen": dt.datetime.fromtimestamp(r["last_seen"]).date().isoformat() if r["last_seen"] else None,
                     "evidence": r["evidence"]})
    if a.table:
        print(f"# source={a.source} files_scanned={scanned} skipped={len(skipped)}")
        for r in rows:
            flag = " [product?]" if r["product_risk"] else ""
            print(f"{r['vendor']:<38} {r['caps'][0]:<20} hits={r['hits']:<5} files={r['files']:<4} last={r['last_seen']}{flag}")
    else:
        print(json.dumps({"source": a.source, "files_scanned": scanned, "skipped": skipped[:50], "vendors": rows}, indent=1))


if __name__ == "__main__":
    main()
