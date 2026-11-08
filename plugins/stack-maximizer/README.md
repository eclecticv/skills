# Stack Maximizer

**Find every GTM tool you pay for, kill the duplicates, fill the gaps.**

An agent skill that audits a company's internal go-to-market stack from evidence already on the machine: receipts in your inbox, tags on your website, records in your DNS, logins in your browser history, dependencies in your repos. You confirm the list once. It then scores every tool, keeps one owner per job, and writes the plan.

```
/stack-maximizer
```

## What you get

- **Inventory.** Every marketing, sales, RevOps and CS tool found, with the evidence for each one: billed, used, installed on the site, or only mentioned.
- **Keep / kill.** A deterministic score per tool. Each capability gets exactly one owner; the losers get a reason ("Mailchimp duplicates HubSpot email; 1 send in 90 days") and exit steps.
- **One core function per kept tool.** HubSpot is the CRM. Calendly books meetings. Nothing does two people's jobs by accident.
- **Gaps.** Missing essentials for your stage and sales motion, checked against 42 capabilities of a modern B2B stack: visitor deanonymization, workflow builder, social scheduling, enrichment, conversation intelligence and more. A feature you already own beats a new tool, and every recommended price is verified on the vendor's site.
- **Roadmap.** Concrete actions per kept tool to get its full value, a data-flow diagram, and a week-1 / 30 / 60 / 90 day plan with done-when checks.
- **Spend.** Monthly cost before and after.

## Install

**Any agent, via [skills.sh](https://skills.sh):**

```bash
npx skills add eclecticv/skills --skill stack-maximizer
```

**Claude Code plugin:**

```
/plugin marketplace add eclecticv/skills
/plugin install stack-maximizer@andorlabs
```

**Manual:** copy `skills/stack-maximizer/` into your agent's skills folder (for Claude Code, `~/.claude/skills/`).

Requirements: Python 3.9+ (standard library only). Optional: `dig` for DNS checks, Playwright for rendered website scans (falls back to plain HTTP). Works on macOS, Linux and Windows; the Apple Mail and Safari collectors are macOS-only.

## How it works

1. **Intake.** It infers company, domain, stage (founder, growth, scale) and motion (PLG, sales-led, hybrid) from your site and repos.
2. **Scan.** Collectors dump each source to text; one signature matcher (about 200 vendors) reads all of them.
3. **Merge.** Evidence is combined into one numbered table with an inferred status: `paid+used`, `paid, idle?`, `in use`, `on site`, `product?`.
4. **Confirm.** One question round. You reply with corrections only, for example `unused 7, 12 · product 4 · add: Clay $149`.
5. **Score.** `score.py` picks one winner per capability and computes gaps and spend. Same input, same verdict.
6. **Research and report.** Gap picks, value plays per tool, roadmap.

## What it reads

Everything runs locally and read-only. Nothing is uploaded. The only network calls are to your own website, public DNS, and vendor pricing pages.

| Source | What is read | What is never read |
|---|---|---|
| Website | Rendered HTML, network request URLs, cookie names, the Google Tag Manager container | Anything behind a login |
| DNS | SPF, verification TXT records, DKIM selectors, subdomain CNAMEs | |
| Email | Sender domain, subject and date of receipt and renewal emails | Message bodies, attachments |
| Browser history | Hostnames and visit counts of signed-in app pages, last 90 days | Page content, form data, cookies |
| Apps and extensions | Names | |
| AI agent configs | MCP server names and URLs | `env` blocks, tokens |
| Repos | Dependency names, CI and deploy config, env var **names** | Env var values, source code |
| AI chat logs | Vendor mentions with redacted snippets | |

Raw dumps are deleted when the report is written. The skill never cancels, downgrades or changes a subscription; the output is a plan.

**Scope.** Internal GTM tools only. Tools that are runtime dependencies of your product (billing APIs, transactional email, data APIs) are excluded. Tools that can go either way (PostHog, Segment, Sanity) are classified from the evidence or asked about.

## Scoring

```
score = 4·usage + 2·min(integrations, 5) + min(capabilities − 1, 3) + 2·lock_in − log2(1 + monthly_cost / 25)
```

Per capability, the highest score among tools in active use wins; ties go to the cheaper tool. A tool that wins nothing is killed. A paid, unused tool that is the only cover for an essential capability becomes **activate**: switch it on within 30 days or replace it. To change a verdict, change the facts (a missing capability, the wrong cost) and rerun. You can also pin a tool with `"keep": true`; the redundancy is still reported.

Try it on the bundled example:

```bash
python3 skills/stack-maximizer/scripts/score.py examples/inventory.example.json
```

## Repository layout

```
skills/stack-maximizer/
  SKILL.md                     agent instructions
  scripts/                     scan_web.py, scan_dns.sh, scan_mail.py, scan_local.py,
                               detect.py, merge.py, score.py, build_signatures.py
  references/
    capabilities.json          42 capabilities, tiered by stage and motion
    signatures.json            vendor detection signatures (generated)
    sources.md                 per-source playbooks
    report-template.md         report structure
examples/inventory.example.json
tests/smoke.sh                 offline end-to-end test
```

## Contributing

Missing a vendor? Add a row to `scripts/build_signatures.py`, run it to regenerate `references/signatures.json`, then run `bash tests/smoke.sh`. Capability ids must exist in `references/capabilities.json`. Mark `product_risk` for vendors that are often part of a company's product rather than its GTM.

## License

MIT. Built by [And/or Labs](https://andorlabs.ca).
