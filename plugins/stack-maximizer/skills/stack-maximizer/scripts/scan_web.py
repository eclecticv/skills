#!/usr/bin/env python3
"""Dump everything a website loads into one text file for detect.py.

Why a headless browser: most GTM tags are injected at runtime by a tag
manager, so raw HTML misses them. Why also fetch gtm.js: tags gated behind a
consent banner never fire in a headless visit, but the container script still
names their hosts, so reading it catches consent-gated pixels.

Usage: scan_web.py OUT.txt https://example.com [https://example.com/pricing ...]
Falls back to plain HTTP fetches when Playwright or its browser is missing,
and says so in the output header so the gap is visible.
"""
import re, sys, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception as e:  # keep going: one dead page must not sink the scan
        return f"# FETCH FAILED {url}: {e}\n"


def launch(p):
    """Python Playwright pins one Chromium build; machines often hold another.
    Try the pinned build, then any cached build, then a fresh headless system
    Chrome (a new process, never an attach to the user's running browser)."""
    import glob, os
    attempts = [dict()]
    pats = ["~/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
            "~/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
            "~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome", "/opt/pw-browsers/chromium*"]
    for pat in pats:
        attempts += [dict(executable_path=x) for x in sorted(glob.glob(os.path.expanduser(pat)), reverse=True) if os.path.isfile(x)]
    attempts.append(dict(channel="chrome"))
    err = None
    for kw in attempts:
        try:
            return p.chromium.launch(headless=True, **kw)
        except Exception as e:
            err = e
    raise err


def with_browser(urls):
    from playwright.sync_api import sync_playwright
    chunks = []
    with sync_playwright() as p:
        b = launch(p)
        ctx = b.new_context(user_agent=UA)
        for url in urls:
            reqs = []
            page = ctx.new_page()
            page.on("request", lambda r: reqs.append(r.url))
            try:
                page.goto(url, wait_until="networkidle", timeout=45000)
                page.wait_for_timeout(4000)  # late-firing pixels
                chunks.append(f"# PAGE {url}\n{page.content()}")
            except Exception as e:
                chunks.append(f"# PAGE FAILED {url}: {e}")
            chunks.append("# REQUESTS\n" + "\n".join(sorted(set(reqs))))
            page.close()
        chunks.append("# COOKIES\n" + "\n".join(f"{c['name']} {c['domain']}" for c in ctx.cookies()))
        b.close()
    return chunks, "browser"


def main():
    out, urls = sys.argv[1], sys.argv[2:]
    try:
        chunks, mode = with_browser(urls)
    except Exception as e:
        chunks, mode = [f"# PAGE {u}\n{fetch(u)}" for u in urls], f"http-only ({e.__class__.__name__}: runtime-injected tags may be missing)"
    text = "\n".join(chunks)
    for gtm in sorted(set(re.findall(r"GTM-[A-Z0-9]{4,9}", text))):
        text += f"\n# GTM CONTAINER {gtm}\n" + fetch(f"https://www.googletagmanager.com/gtm.js?id={gtm}")
    with open(out, "w") as f:
        f.write(f"# scan_web mode={mode}\n{text}")
    print(f"mode={mode} bytes={len(text)} -> {out}")


if __name__ == "__main__":
    main()
