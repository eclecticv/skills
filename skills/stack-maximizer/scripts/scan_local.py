#!/usr/bin/env python3
"""Collect local telemetry into plain-text files for detect.py.

Writes into OUTDIR:
  apps.txt        installed macOS apps (+ Homebrew casks)
  extensions.txt  browser extension names (Chrome, Brave, Edge, Arc, Dia)
  history.txt     "host visits" for signed-in APP traffic (app./dashboard.
                  hosts, /settings-style paths) over the last --days. The best
                  usage signal there is: a paid tool nobody opens shows zero.
  history_site.txt all visits incl. marketing sites (research interest, weak)
  mcp.txt         MCP servers / connectors configured for AI agents
  envkeys.txt     env var NAMES (never values) from repos, underscores
                  turned into spaces so HUBSPOT_API_KEY name-matches
  repo_<n>.txt    dependency names + CI/deploy config per repo
  _report.txt     what was read, what was blocked (macOS privacy, missing)

Never reads secret values, never copies message bodies. History DBs are
copied to a temp file first because the browser holds a lock on them.

Usage: scan_local.py OUTDIR [--repos ~/code] [--days 90]
Works on macOS, Linux and Windows; sources missing on an OS are reported and skipped.
"""
import argparse, glob, json, os, pathlib, platform, re, shutil, sqlite3, subprocess, tempfile, time
from collections import Counter

H = pathlib.Path.home()
SYS = platform.system()
# Per-OS profile roots. Missing roots are skipped, so listing extras is free.
if SYS == "Darwin":
    AS = H / "Library" / "Application Support"
    CHROMIUMS = {"Chrome": AS / "Google/Chrome", "Brave": AS / "BraveSoftware/Brave-Browser",
                 "Edge": AS / "Microsoft Edge", "Arc": AS / "Arc/User Data", "Dia": AS / "Dia/User Data",
                 "Chromium": AS / "Chromium"}
    FIREFOX = AS / "Firefox/Profiles"
elif SYS == "Windows":
    AS = pathlib.Path(os.environ.get("APPDATA", H / "AppData/Roaming"))
    LAD = pathlib.Path(os.environ.get("LOCALAPPDATA", H / "AppData/Local"))
    CHROMIUMS = {"Chrome": LAD / "Google/Chrome/User Data", "Brave": LAD / "BraveSoftware/Brave-Browser/User Data",
                 "Edge": LAD / "Microsoft/Edge/User Data", "Chromium": LAD / "Chromium/User Data"}
    FIREFOX = AS / "Mozilla/Firefox/Profiles"
else:  # Linux and other XDG systems
    AS = pathlib.Path(os.environ.get("XDG_CONFIG_HOME", H / ".config"))
    CHROMIUMS = {"Chrome": AS / "google-chrome", "Brave": AS / "BraveSoftware/Brave-Browser",
                 "Edge": AS / "microsoft-edge", "Chromium": AS / "chromium"}
    FIREFOX = H / ".mozilla/firefox"
report = []


def note(msg):
    report.append(msg)


def apps(out):
    names = set()
    for d in ["/Applications", str(H / "Applications"), "/Applications/Setapp"]:
        for p in glob.glob(d + "/*.app"):
            names.add(pathlib.Path(p).stem)
    for d in ["/usr/share/applications", str(H / ".local/share/applications"), "/var/lib/flatpak/exports/share/applications"]:
        for p in glob.glob(d + "/*.desktop"):
            names.add(pathlib.Path(p).stem)
    if SYS == "Windows":
        for d in [os.environ.get("ProgramFiles", ""), os.environ.get("ProgramFiles(x86)", ""), str(H / "AppData/Local/Programs")]:
            if d:
                names.update(pathlib.Path(p).name for p in glob.glob(d + "/*"))
    try:
        casks = subprocess.run(["brew", "list", "--cask"], capture_output=True, text=True, timeout=60).stdout.split()
        names.update(casks)
    except Exception:
        note("brew casks: brew not available")
    out.write_text("\n".join(sorted(names)))
    note(f"apps: {len(names)}")


def ext_name(manifest):
    try:
        m = json.loads(manifest.read_text(errors="ignore"))
    except Exception:
        return None
    n = m.get("name", "")
    if n.startswith("__MSG_"):
        key = n[6:-2]
        for loc in ["en", "en_US", m.get("default_locale", "en")]:
            f = manifest.parent / "_locales" / loc / "messages.json"
            if f.exists():
                try:
                    msgs = {k.lower(): v for k, v in json.loads(f.read_text(errors="ignore")).items()}
                    return msgs.get(key.lower(), {}).get("message", n)
                except Exception:
                    pass
    return n


def extensions(out):
    rows = set()
    for browser, root in CHROMIUMS.items():
        for mf in glob.glob(str(root / "*" / "Extensions" / "*" / "*" / "manifest.json")):
            n = ext_name(pathlib.Path(mf))
            if n:
                rows.add(f"{browser}: {n}")
    for mf in glob.glob(str(FIREFOX / "*/extensions.json")):
        try:
            for a in json.loads(pathlib.Path(mf).read_text()).get("addons", []):
                rows.add(f"Firefox: {a.get('defaultLocale', {}).get('name')}")
        except Exception:
            pass
    out.write_text("\n".join(sorted(rows)))
    note(f"extensions: {len(rows)}")


def read_sqlite(path, sql, params=()):
    tmp = tempfile.mktemp(suffix=".db")
    try:
        shutil.copy2(path, tmp)
        con = sqlite3.connect(tmp)
        rows = con.execute(sql, params).fetchall()
        con.close()
        return rows
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def host_of(url):
    m = re.match(r"https?://([^/:?#]+)", url or "")
    return m.group(1).lower() if m else None


APP_SUBS = {"app", "apps", "dashboard", "my", "console", "admin", "login", "auth", "studio", "secure",
            "account", "accounts", "portal", "web", "manage", "platform", "cloud", "ui", "us", "eu"}
APP_PATHS = {"app", "apps", "dashboard", "login", "signin", "settings", "billing", "account", "workspace",
             "workspaces", "w", "projects", "files", "file", "design", "inbox", "campaigns", "contacts",
             "home", "org", "team", "u", "reports", "admin", "studio", "editor", "board", "boards"}


def is_app(url, host):
    """Signed-in product traffic vs marketing-site reading. Visiting copper.com
    to compare CRMs is research; app.attio.com is usage."""
    sub = host.split(".")[0]
    seg = (re.match(r"https?://[^/]+/([^/?#]*)", url) or [None, ""])[1].lower()
    return sub in APP_SUBS or seg in APP_PATHS


def history(out, days):
    c, app = Counter(), Counter()
    since = time.time() - days * 86400
    chrome_epoch = int((since + 11644473600) * 1_000_000)  # WebKit microseconds
    for browser, root in CHROMIUMS.items():
        for db in glob.glob(str(root / "*" / "History")):
            try:
                for url, n in read_sqlite(db, "SELECT u.url, COUNT(*) FROM visits v JOIN urls u ON u.id=v.url "
                                              "WHERE v.visit_time > ? GROUP BY u.url", (chrome_epoch,)):
                    h = host_of(url)
                    if h:
                        c[h] += n
                        if is_app(url, h):
                            app[h] += n
                note(f"history {browser}: ok ({db})")
            except Exception as e:
                note(f"history {browser}: blocked {e.__class__.__name__}")
    safari = H / "Library/Safari/History.db"
    if safari.exists():
        try:
            mac_since = since - 978307200  # Core Data epoch
            for url, n in read_sqlite(str(safari), "SELECT i.url, COUNT(*) FROM history_visits v JOIN history_items i "
                                                   "ON i.id=v.history_item WHERE v.visit_time > ? GROUP BY i.url", (mac_since,)):
                h = host_of(url)
                if h:
                    c[h] += n
                    if is_app(url, h):
                        app[h] += n
            note("history Safari: ok")
        except Exception as e:
            note(f"history Safari: blocked {e.__class__.__name__} (macOS: grant Full Disk Access to the terminal to include it)")
    for db in glob.glob(str(FIREFOX / "*/places.sqlite")):
        try:
            for url, n in read_sqlite(db, "SELECT p.url, COUNT(*) FROM moz_historyvisits v JOIN moz_places p ON p.id=v.place_id "
                                          "WHERE v.visit_date > ? GROUP BY p.url", (int(since * 1_000_000),)):
                h = host_of(url)
                if h:
                    c[h] += n
                    if is_app(url, h):
                        app[h] += n
            note("history Firefox: ok")
        except Exception as e:
            note(f"history Firefox: blocked {e.__class__.__name__}")
    out.write_text("\n".join(f"{h} {n}" for h, n in app.most_common()))
    (out.parent / "history_site.txt").write_text("\n".join(f"{h} {n}" for h, n in c.most_common()))
    note(f"history: {len(app)} app hosts, {len(c)} hosts total over {days}d")


def mcp(out, repo_root=None):
    rows = []
    cands = [H / ".claude.json", H / ".cursor/mcp.json", AS / "Claude/claude_desktop_config.json",
             H / ".codeium/windsurf/mcp_config.json", H / ".codex/config.toml", H / ".gemini/settings.json",
             AS / "Code/User/mcp.json"]
    if repo_root:
        cands += [pathlib.Path(p) for p in glob.glob(str(pathlib.Path(repo_root).expanduser() / "*/.mcp.json"))]
        cands += [pathlib.Path(p) for p in glob.glob(str(pathlib.Path(repo_root).expanduser() / "*/.cursor/mcp.json"))]
    for f in cands:
        if not f.exists():
            continue
        txt = f.read_text(errors="ignore")
        if f.suffix == ".toml":
            rows += [f"{f}: {m}" for m in re.findall(r"\[mcp_servers\.([^\]]+)\]", txt)]
            continue
        try:
            d = json.loads(txt)
        except Exception:
            continue
        servers = dict(d.get("mcpServers", {}))
        for proj in (d.get("projects") or {}).values():
            servers.update(proj.get("mcpServers", {}) or {})
        for name, cfg in servers.items():
            # name + url/command only; env blocks hold secrets and are skipped on purpose
            rows.append(f"{f.name}: {name} {cfg.get('url', '')} {cfg.get('command', '')} {' '.join(map(str, cfg.get('args', [])))[:200]}")
    out.write_text("\n".join(rows))
    note(f"mcp servers: {len(rows)}")


MANIFESTS = ["package.json", "requirements.txt", "pyproject.toml", "Gemfile", "go.mod", "composer.json",
             "wrangler.toml", "wrangler.jsonc", "vercel.json", "netlify.toml"]


def repos(outdir, root, envkeys):
    root = pathlib.Path(os.path.expanduser(root))
    keys = set()
    n = 0
    for repo in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")):
        lines = [f"# REPO {repo}"]
        try:
            remote = subprocess.run(["git", "-C", str(repo), "remote", "get-url", "origin"], capture_output=True, text=True, timeout=10).stdout.strip()
            lines.append(f"# REMOTE {remote}")
        except Exception:
            pass
        for mf in MANIFESTS:
            for f in list(repo.glob(mf)) + list(repo.glob(f"*/{mf}")) + list(repo.glob(f"apps/*/{mf}")) + list(repo.glob(f"packages/*/{mf}")):
                if "node_modules" in f.parts:
                    continue
                txt = f.read_text(errors="ignore")
                if f.name == "package.json":
                    try:
                        d = json.loads(txt)
                        deps = list((d.get("dependencies") or {})) + list((d.get("devDependencies") or {}))
                        lines.append(f"## {f.relative_to(repo)} ({d.get('name', '')})\n" + "\n".join(deps))
                    except Exception:
                        pass
                else:
                    lines.append(f"## {f.relative_to(repo)}\n" + txt[:20000])
        for wf in repo.glob(".github/workflows/*.y*ml"):
            lines.append(f"## {wf.relative_to(repo)}\n" + wf.read_text(errors="ignore")[:10000])
        for envf in list(repo.glob(".env*")) + list(repo.glob("*/.env*")) + list(repo.glob(".dev.vars")) + list(repo.glob("apps/*/.dev.vars")) + list(repo.glob("apps/*/.env*")):
            if envf.is_file():
                for line in envf.read_text(errors="ignore").splitlines():
                    m = re.match(r"\s*(?:export\s+)?([A-Z][A-Z0-9_]{2,})\s*=", line)
                    if m:  # NAME only, the value is never read into output
                        keys.add(f"{repo.name}: {m.group(1).replace('_', ' ')}")
        if len(lines) > 2:
            (outdir / f"repo_{repo.name}.txt").write_text("\n".join(lines))
            n += 1
    envkeys.write_text("\n".join(sorted(keys)))
    note(f"repos with manifests: {n}; env key names: {len(keys)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("--repos", default=None, help="folder holding the company's repos (each subfolder scanned); omit to skip")
    ap.add_argument("--days", type=int, default=90)
    a = ap.parse_args()
    out = pathlib.Path(os.path.expanduser(a.outdir))
    out.mkdir(parents=True, exist_ok=True)
    for fn, args in [(apps, (out / "apps.txt",)), (extensions, (out / "extensions.txt",)),
                     (history, (out / "history.txt", a.days)), (mcp, (out / "mcp.txt", a.repos))]:
        try:
            fn(*args)
        except Exception as e:  # a blocked source is reported, never fatal
            note(f"{fn.__name__}: failed {e.__class__.__name__}: {e}")
    if a.repos and pathlib.Path(os.path.expanduser(a.repos)).is_dir():
        repos(out, a.repos, out / "envkeys.txt")
    else:
        (out / "envkeys.txt").write_text("")
        note(f"repos: skipped ({'not found: ' + a.repos if a.repos else 'no --repos given'})")
    (out / "_report.txt").write_text("\n".join(report))
    print("\n".join(report))


if __name__ == "__main__":
    main()
