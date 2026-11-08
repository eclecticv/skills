#!/usr/bin/env python3
"""Billing-signal extraction from the local Apple Mail store.

Reads HEADERS ONLY (From, Subject, Date) of .emlx files: never bodies, never
attachments. Writes:
  senders.txt   "<from-domain> <count>"         -> detect.py --weighted
  billing.txt   "<date> <from-domain> | <subject>" for receipts, invoices,
                renewals, trials, plan changes  -> detect.py --names
Receipts sent through Stripe/Paddle/Chargebee name the vendor only in the
subject, which is why billing.txt keeps subjects.

If the terminal lacks Full Disk Access, macOS blocks ~/Library/Mail. The
script reports that instead of failing; use the Gmail/Outlook connector path
in references/sources.md then.

Usage: scan_mail.py OUTDIR [--days 400]
"""
import argparse, email.parser, email.utils, glob, os, pathlib, re, time
from collections import Counter

# Transactional wording only. Marketing mail ("upgrade your SEO", "welcome
# to our webinar") also names vendors and would mark free newsletters as paid.
BILLING = re.compile(r"\breceipt\b|\binvoice\b|payment (?:received|confirm|failed|success|due)|"
                     r"\brenew(?:al|ed|s)\b|subscription (?:confirm|renew|cancel|receipt|activated|updated)|"
                     r"your (?:subscription|plan|trial|bill)|trial (?:ends|ending|expir|has ended)|"
                     r"\bcharged\b|billing (?:statement|receipt|update)|card (?:was )?declined", re.I)
PARSER = email.parser.HeaderParser()


def headers(path):
    with open(path, "rb") as f:
        f.readline()  # emlx first line is the byte count
        raw = b""
        for line in f:
            if line in (b"\n", b"\r\n"):
                break
            raw += line
            if len(raw) > 65536:
                break
    return PARSER.parsestr(raw.decode("utf-8", "ignore"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("--days", type=int, default=400, help="covers one annual renewal cycle plus slack")
    a = ap.parse_args()
    out = pathlib.Path(os.path.expanduser(a.outdir)); out.mkdir(parents=True, exist_ok=True)
    root = pathlib.Path.home() / "Library" / "Mail"
    try:
        stores = [p for p in root.iterdir() if p.name.startswith("V")]
    except PermissionError:
        print("BLOCKED: ~/Library/Mail needs Full Disk Access for this terminal. Use a mail connector instead.")
        return
    except FileNotFoundError:
        print("NO APPLE MAIL STORE. Use a mail connector instead.")
        return
    cutoff = time.time() - a.days * 86400
    senders, billing, n = Counter(), [], 0
    for store in stores:
        for path in glob.iglob(str(store / "**" / "*.emlx"), recursive=True):
            try:
                if os.path.getmtime(path) < cutoff:
                    continue
                h = headers(path)
            except (OSError, PermissionError):
                continue
            n += 1
            addr = email.utils.parseaddr(h.get("From", ""))[1].lower()
            dom = addr.split("@")[-1] if "@" in addr else ""
            if not dom:
                continue
            senders[dom] += 1
            subj = " ".join(str(h.get("Subject", "")).split())
            if BILLING.search(subj):
                d = email.utils.parsedate_to_datetime(h["Date"]).date().isoformat() if h.get("Date") else "?"
                billing.append(f"{d} {dom} | {subj[:160]}")
    (out / "senders.txt").write_text("\n".join(f"{d} {c}" for d, c in senders.most_common()))
    (out / "billing.txt").write_text("\n".join(sorted(billing, reverse=True)))
    print(f"messages={n} sender_domains={len(senders)} billing_lines={len(billing)} -> {out}")


if __name__ == "__main__":
    main()
