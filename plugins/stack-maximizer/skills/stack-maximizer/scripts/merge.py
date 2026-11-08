#!/usr/bin/env python3
"""Merge detect.py outputs into one candidate inventory for user confirmation.

Usage: merge.py OUTDIR detect_web.json detect_dns.json detect_email.json ...

Writes OUTDIR/candidates.json and OUTDIR/candidates.md (numbered table).

Inferred status is a pre-fill the user corrects, not a verdict:
  paid+used     billing email AND >= 10 app visits in the history window
  paid, idle?   billing email, < 3 visits: the classic zombie subscription
  in use        >= 10 visits, no billing seen (free tier, or billed elsewhere)
  on site       loads on the website / in DNS, no human usage seen
  product?      product_risk vendor whose only evidence is repos/env/MCP
  weak          chat mentions, a few site visits, a single app/extension
Weak rows go to a separate "low confidence" list so the confirmation table
stays short; the user can still pull any of them in.
"""
import json, pathlib, sys

STRONG = {"web", "dns", "email", "history", "billing", "sso", "card"}


def main():
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    cands = {}
    for f in sys.argv[2:]:
        d = json.loads(pathlib.Path(f).read_text())
        src = d["source"]
        for v in d["vendors"]:
            c = cands.setdefault(v["vendor"], {"vendor": v["vendor"], "caps": v["caps"],
                                               "product_risk": v["product_risk"], "sources": {}, "evidence": []})
            s = c["sources"].setdefault(src, {"hits": 0, "files": 0, "last_seen": None})
            s["hits"] += v["hits"]; s["files"] += v["files"]
            s["last_seen"] = max(filter(None, [s["last_seen"], v["last_seen"]]), default=None)
            c["evidence"] += [dict(e, source=src) for e in v["evidence"][:2]]

    rows = []
    for c in cands.values():
        src = c["sources"]
        visits = src.get("history", {}).get("hits", 0)
        billed = "email" in src or "card" in src
        if billed and visits >= 10:
            status = "paid+used"
        elif billed and visits < 3:
            status = "paid, idle?"
        elif visits >= 10:
            status = "in use"
        elif {"web", "dns"} & set(src):
            status = "on site"
        elif c["product_risk"] and {"repo", "mcp"} & set(src) and set(src) <= {"repo", "mcp", "chat", "apps"}:
            status = "product?"
        else:
            status = "weak"
        strong = len(STRONG & set(src))
        # Chat mentions prove interest, not a subscription (research, comparisons,
        # this very audit). With no strong source a row is low confidence.
        low = status == "weak" and (strong == 0 or visits < 5)
        rows.append(dict(c, inferred=status, visits=visits, strong_sources=strong, low_confidence=low))

    order = {"paid+used": 0, "paid, idle?": 1, "in use": 2, "on site": 3, "product?": 4, "weak": 5}
    rows.sort(key=lambda r: (r["low_confidence"], order[r["inferred"]], r["caps"][0], -r["visits"], r["vendor"]))
    for i, r in enumerate(rows, 1):
        r["n"] = i
    (out / "candidates.json").write_text(json.dumps(rows, indent=1))

    def line(r):
        flag = " (product?)" if r["product_risk"] else ""
        return (f"| {r['n']} | {r['vendor']}{flag} | {r['caps'][0]} | {r['inferred']} | {r['visits']} | "
                f"{', '.join(sorted(r['sources']))} |")
    hdr = "| # | Tool | Category | Inferred | Visits | Seen in |\n|---|---|---|---|---|---|"
    main_rows = [line(r) for r in rows if not r["low_confidence"]]
    low_rows = [line(r) for r in rows if r["low_confidence"]]
    md = f"## Candidates ({len(main_rows)})\n\n{hdr}\n" + "\n".join(main_rows)
    if low_rows:
        md += f"\n\n## Low confidence ({len(low_rows)}): seen only in chat logs, apps or repos, no billing or usage\n\n{hdr}\n" + "\n".join(low_rows)
    (out / "candidates.md").write_text(md + "\n")
    print(f"{len(main_rows)} candidates, {len(low_rows)} low-confidence -> {out}/candidates.md")


if __name__ == "__main__":
    main()
