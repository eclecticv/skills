# Source playbooks

`W` = work dir, `S` = scripts dir. Every collector is read-only. If a source is blocked, record `blocked: <reason>` for the coverage line and move on.

## Website (installed on site)

```
python3 $S/scan_web.py W/web.txt https://<domain> https://<domain>/pricing https://<domain>/blog <a page with a form>
python3 $S/detect.py --source web --tokens W/web.txt > W/d_web.json
```
- Captures rendered HTML, every network request, cookies, and the full `gtm.js` for each GTM container found. Tags gated behind a consent banner never fire in a headless visit, but the container script still names their hosts.
- Header line `mode=http-only` means no browser was available, so runtime-injected tags may be missing. Note it in coverage.
- Include subdomains that run other tools: `help.`, `docs.`, `community.`, `go.`/`info.` (often MAP landing pages), `book.`/`meet.`.

## DNS (connected to domain)

```
bash $S/scan_dns.sh <domain> [<other sending domains>] > W/dns.txt
python3 $S/detect.py --source dns --tokens W/dns.txt > W/d_dns.json
```
- SPF `include:` lists every platform allowed to send as the domain. An include for a tool nobody uses is also a deliverability and security cleanup item; put it on the kill action list.
- Verification TXT records (google-site-verification, facebook-domain-verification, ahrefs-site-verification, docusign=, brevo-code...) show a tool was connected at some point. On their own they don't prove a current subscription.

## Email (paying)

Preferred order:
1. **Mail connector** (Gmail or Outlook MCP, or the google-workspace skill) when one is connected. Search the last 400 days, headers and subjects only:
   `subject:(receipt OR invoice OR renewal OR "your subscription" OR "trial ends" OR "payment received")`
   and `from:(stripe.com OR paddle.com OR chargebee.com OR lemonsqueezy.com OR fastspring.com OR billing OR invoice)`.
   Write one line per message as `<date> <from-domain> | <subject>` to `W/mail/billing.txt`.
2. **Apple Mail local store (macOS):** `python3 $S/scan_mail.py W/mail --days 400`. It needs Full Disk Access for the terminal; if blocked, it says so.
3. **Thunderbird or other local clients, or an `.mbox` export:** grep the `From:` and `Subject:` header lines into the same `billing.txt` format.

```
python3 $S/detect.py --source email --names --ci W/mail/billing.txt > W/d_email.json
```
- Amounts in subjects ("Your $49.00 receipt") give `monthly_cost`. Annual charges are divided by 12.
- Seat counts in receipts help infer company stage.

## Local telemetry (usage, wiring, product vs GTM)

```
python3 $S/scan_local.py W/local --repos <folder holding the company repos, e.g. ~/code> --days 90
python3 $S/detect.py --source history --weighted W/local/history.txt > W/d_history.json
python3 $S/detect.py --source apps --all-names --ci W/local/apps.txt W/local/extensions.txt > W/d_apps.json
python3 $S/detect.py --source mcp --names --ci W/local/mcp.txt W/local/envkeys.txt > W/d_mcp.json
python3 $S/detect.py --source repo --names --ci W/local/repo_*.txt > W/d_repo.json
```
- `history.txt` counts **signed-in app traffic only** (app./dashboard. hosts, /settings-style paths). `history_site.txt` holds all visits including vendor marketing sites. Use it to explain interest, never as proof of use.
- Browsers covered: Chrome, Brave, Edge, Chromium and Firefox on macOS, Linux and Windows, plus Arc, Dia and Safari on macOS (Safari needs Full Disk Access). Only one person's machine is visible. Say so in coverage, and for teams note that seat usage needs the vendor's admin console.
- Repos: a dependency in the **product** repo means product. A dependency in the **marketing-site** repo means GTM. Read each `# REPO` header and remote to tell them apart.
- `envkeys.txt` holds variable NAMES with underscores turned into spaces. Values are never read.

## AI chat logs (interest, weak)

```
python3 $S/detect.py --source chat --names --since 180 --ext .jsonl \
  ~/.claude/projects ~/.codex/sessions ~/.gemini/tmp > W/d_chat.json
```
- Add a ChatGPT or Claude.ai data export (`conversations.json`) if the user has one; pass its path.
- Files that mention `stack-maximizer` are skipped automatically, so past audits don't feed back in.
- Chat hits alone never put a tool in the main table. They often reflect research, competitor work or the product domain. Their value is the evidence snippets: "my Clay table", "our HubSpot workflow" point to real use.

## Optional strong sources (use when available, never block on them)

- **Card or bank statement export** (CSV/PDF the user drops in): write the merchant lines to `W/card.txt`, then run `detect.py --source card --names --ci W/card.txt`. This is the most complete paying source.
- **SSO / OAuth app list:** Google Workspace Admin (Security > API controls > App access control) or Okta/Entra app lists, exported or read through a logged-in browser session. Save the names to `W/sso.txt` and run `--source sso --names --ci`.
- **1Password CLI** (only if `op` is signed in): `op item list --categories Login --format json | python3 -c "import json,sys;[print(i.get('title',''),' '.join(u.get('href','') for u in i.get('urls',[]))) for i in json.load(sys.stdin)]" > W/pw.txt`. This lists titles and URLs only, never fields. Then run `--source sso --names --ci`.
- **Calendar:** recurring vendor QBRs or renewal calls are a signal of paid contracts. Use a calendar connector if one exists.
