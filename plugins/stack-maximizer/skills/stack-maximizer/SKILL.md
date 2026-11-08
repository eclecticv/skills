---
name: stack-maximizer
description: Audit a company's internal go-to-market software stack and turn it into a lean, integrated one. Scans email receipts, the website's tags and DNS, AI chat logs, connected repos, browser history, installed apps, extensions and MCP connectors to inventory every GTM tool the team pays for or uses (internal use only, not the product's own runtime dependencies), has the user confirm the list in one pass, then scores keep/kill deterministically, assigns each kept tool one core function, flags missing essentials of a modern B2B stack (visitor deanonymization, workflow builder, social scheduling and more), and delivers an action list and 30/60/90 roadmap. Use when the user asks to audit, rationalize, consolidate, simplify, de-duplicate or "maximize" their GTM, marketing, sales or martech stack, find unused SaaS subscriptions, or asks "what tools are we paying for".
license: MIT
compatibility: Python 3.9+ (stdlib). Optional dig for DNS and Playwright for rendered website scans. Collectors cover macOS, Linux and Windows; Apple Mail and Safari scans are macOS-only.
metadata:
  author: And/or Labs
  version: "0.1.0"
  repository: https://github.com/eclecticv/skills
---

# Stack Maximizer

Goal: a functional, integrated, non-redundant GTM stack. Every kept tool owns one core function, every essential capability has exactly one owner, nothing is paid for and unused.

Pipeline: **intake → scan → merge → confirm (the only question round) → score → research gaps → report.** Run straight through. The user is asked exactly once, at the confirm step, with everything batched.

Scripts live in `scripts/` next to this file (resolve the absolute path first: `S=<this skill dir>/scripts`). All are stdlib Python 3.9+ except `scan_web.py`, which uses Playwright when installed and falls back to plain HTTP, and `scan_dns.sh`, which needs `dig`. Use `python3` (on Windows, `py`).

## Scope rules (apply everywhere)

- **In scope:** tools the company uses to run marketing, sales, RevOps, customer success and GTM analytics. The marketing website counts: its tags, CMS, forms and pixels are GTM.
- **Out of scope:** the product's own runtime (billing APIs, transactional email, infra, data APIs the product calls), personal subscriptions, and engineering-only tools. Signatures flagged `product_risk` (PostHog, Segment, Sanity, Loops, DataForSEO, BuiltWith...) can be either. Decide from the evidence: a dependency in the product repo or an MCP server used for product work means product. The marketing-site repo or app logins by GTM staff mean GTM. If the evidence doesn't settle it, put it in the confirm table as `product?`.
- **Privacy:** everything runs locally and read-only. Collectors read headers, hostnames, names and dependency lists, never message bodies, secret values or tokens. Never print an env var value, API key or email body. Raw dumps stay in the work dir and are deleted at the end (step 7). Nothing is sent to third-party services except public lookups: the website, DNS, and vendor pricing pages.
- **Never cancel, downgrade or change any subscription or setting.** The output is a plan.

## 1. Intake (infer, don't ask)

Infer these from the repo, website, the agent's instruction files (AGENTS.md, CLAUDE.md and similar) and email signatures before scanning. Anything still unknown is added to the confirm round, not asked now.

- Company name, primary domain(s), and marketing-site URLs (homepage, pricing, blog, a form page).
- Stage: `founder` (1-10), `growth` (10-50), `scale` (50+). Infer from the team page, LinkedIn headcount or seat counts on receipts.
- Motion: `plg`, `sales_led` or `hybrid`. Infer from the website: a self-serve signup suggests PLG, "book a demo" only suggests sales-led.
- Repos folder: the folder holding the company's repos, if any (passed as `--repos`).
- Work dir: a project scratch folder if the user's instructions define one, else a fresh temp dir such as `$TMPDIR/stack-maximizer-<date>/`. It holds private data, so never put it inside a git-tracked folder.
- Deliverables: the user's documented deliverables folder if they have one, else `./stack-maximizer-<date>/` in the current directory.

## 2. Scan

Run the collectors, then `detect.py` on each output. Fan these out in parallel; they're independent. Each source has a playbook with exact commands and fallbacks in `references/sources.md`. Read it before scanning.

| Source | Collector | Detect flags | Signal |
|---|---|---|---|
| Website tags, network, cookies, GTM container | `scan_web.py W/web.txt <urls>` | `--source web --tokens` | installed on site |
| DNS: SPF, verification TXT, DKIM, CNAMEs | `scan_dns.sh <domains> > W/dns.txt` | `--source dns --tokens` | connected to domain |
| Email receipts and renewals | a mail connector, or `scan_mail.py W/mail` (Apple Mail) | `--source email --names --ci W/mail/billing.txt` | **paying** |
| Browser history, app logins only | `scan_local.py W/local --repos <dir>` (history.txt) | `--source history --weighted` | **usage** |
| Installed apps and extensions | `scan_local.py` (apps.txt, extensions.txt) | `--source apps --all-names --ci` | weak |
| MCP connectors and env key names | `scan_local.py` (mcp.txt, envkeys.txt) | `--source mcp --names --ci` | wired up |
| Repos: dependencies, CI, deploy config | `scan_local.py --repos <dir>` (repo_*.txt) | `--source repo --names --ci` | product vs GTM |
| AI chat logs | none; point detect at the log dirs | `--source chat --names --since 180 --ext .jsonl` | weak, interest only |
| Card statement, SSO app list, password manager | user-provided export or CLI, see sources.md | `--source card` / `sso` | **paying** / **access** |

Save each detect result as `W/d_<source>.json`. Chat logs are large, so run that scan in the background first.

A blocked source (OS privacy controls, no connector, no repos, a missing `dig`) is noted in the report's coverage line and the scan moves on. Never stop to ask for access.

Vendors not in `references/signatures.json` still count. If the email or history dumps show recurring billing or app logins for an unlisted vendor, add it to the inventory by hand.

## 3. Merge

```
python3 $S/merge.py W/out W/d_*.json
```

This writes `candidates.md` (numbered table) and `candidates.json` with an inferred status per tool: `paid+used`, `paid, idle?`, `in use`, `on site`, `product?`, `weak`, plus a low-confidence section. Before showing it, read the evidence snippets and fix obvious misreads. Typical misreads: a vendor's newsletter caught as a receipt, a competitor researched in chat, the user's own product. Move such rows to low confidence and note why.

## 4. Confirm: the one question round

Show the main table plus the low-confidence count, then ask for corrections in one reply. Statuses default to the inference, so silence means agreement:

```
Defaults: paid+used / in use / on site = using · paid, idle? = unused · product? = product
Reply with corrections only, e.g.
  unused 7, 12     not ours 14     product 4     using 22 (from low-confidence)
  add: Clay $149/mo, Lemlist      cost: 1=$29 13=$90      keep: 9 (never kill)
Also confirm: stage = growth, motion = hybrid   [only if inferred, else ask]
```

If the harness has a structured multiple-choice question tool, use it only when there are 12 or fewer rows and nothing else to confirm. Otherwise ask in plain text. Don't ask a second round: anything still unclear after the reply gets a stated assumption in the report.

## 5. Score

Build `W/inventory.json` (schema in the `score.py` docstring) from the confirmed rows:

- `capabilities`: ids from `references/capabilities.json` that the team actually uses this tool for, plus ones their current plan includes at no extra cost. Check the vendor's plan page. HubSpot Starter does not include social publishing, for example. The first id is the primary. Don't list capabilities from a higher tier they don't pay for.
- `usage`, mapped from app visits in the history window (90 days by default): 0 = none, 1 = 1-9, 2 = 10-59, 3 = 60+. If history is blocked, use the user's words or 1 for confirmed-used.
- `monthly_cost`: from receipt subjects/amounts or the user's reply. Annual plans divided by 12. Otherwise `null`; don't guess.
- `integrations`: other inventory tools it is actually connected to, from MCP configs, env keys, Zapier/Make evidence or native-integration mentions.
- `lock_in`: 2 for systems of record holding contacts or deals, 1 for tools with workflows or content, 0 otherwise.

```
python3 $S/score.py W/inventory.json > W/scored.json
```

The scores are the verdict. Don't override them by judgement. If a result looks wrong, fix the input (a missing capability, the wrong cost) and rerun. A user `keep` override is respected and the redundancy is flagged.

## 6. Research gaps and value plays

For each gap in `scored.json` (essential first, then recommended):

1. **Native first.** Check whether a kept tool already offers it on the current plan, from the vendor's docs. If it does, the action is "switch on X in Y", not a new tool.
2. Otherwise recommend **one pick and one alternative**. Prefer free tiers or low entry pricing, native integration with the kept CRM and workflow tool, and fit for the stage. Verify current pricing and integration claims on the vendor's site and cite the URL. Don't quote prices from memory.
3. If the gap has `killed_tools_covering`, say plainly whether to re-activate that tool or use the cheaper or native option.

For each kept tool, find the highest-value features and integrations the team isn't using yet. Base it on their plan and the evidence: no CRM sync, an unwired form, a pixel without conversion events, consent missing on pixels.

## 7. Report

Write `report.md` from `references/report-template.md` in the deliverables folder, plus `inventory.csv` (tool, decision, core function, cost, evidence sources). If the user asked for HTML or a PDF, render it too. Keep the work-dir `inventory.json` and `scored.json` for reruns, then **delete the raw dumps** (`web.txt`, `local/`, `mail/`, `d_chat.json`); they contain private browsing and mail metadata.

Report voice: plain verdicts with a number or a mechanism attached ("Mailchimp duplicates HubSpot email; $30/mo, 1 send in 90 days"). No hedging and no filler.

Finish with a short status in chat: spend now → after, keep/kill/gap counts, the top 3 actions, and the report path.

## Files

- `scripts/scan_web.py`, `scan_dns.sh`, `scan_mail.py`, `scan_local.py`: collectors
- `scripts/detect.py`: one signature matcher for every source (trie-compiled regex, redacted snippets, skips its own past runs in chat logs)
- `scripts/merge.py`: candidates and inferred status · `scripts/score.py`: keep/kill, core function, gaps, spend
- `scripts/build_signatures.py` → `references/signatures.json` (~200 vendors) · `references/capabilities.json` (42 capabilities, tiers by stage and motion)
- `references/sources.md`: per-source playbooks · `references/report-template.md`: report structure
