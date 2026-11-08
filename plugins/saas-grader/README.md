# saas-grader

Score SaaS websites against 47 research-backed optimization rules from peer-reviewed marketing science. Every rule cites its source. No opinions.

## Install

```bash
claude /install saas-grader@andorlabs
```

Or load for a single session:
```bash
claude --plugin-dir /path/to/saas-grader
```

## Usage

```
/saas-grader:saas <url>
```

One command does everything: classifies the site, extracts measured evidence from the rendered DOM, screenshots the homepage and pricing page, scores all 47 rules with cited evidence and confidence levels, prints a prioritized scorecard to the terminal, and writes a full detailed report (with a machine-readable JSON block for run-over-run deltas) to `~/Documents/Inbox/`.

## What It Checks

### SaaS Optimization (47 rules)

| Category | Rules | Source |
|----------|-------|--------|
| Brand & Messaging | 8 | Journal of Marketing, Journal of Consumer Research |
| Page Design & Visuals | 14 | Marketing Science, Journal of Retailing |
| Pricing Plans | 9 | Journal of Consumer Psychology, Quarterly Journal of Economics |
| Free Trials | 4 | Management Science, Information Systems Research |
| Freemium | 2 | Journal of Marketing Research |
| Churn Prevention | 3 | Journal of the Academy of Marketing Science |
| Affiliates | 2 | International Journal of Research in Marketing |
| Referrals | 5 | Journal of Marketing, American Economic Review |

## Output Format

Every rule produces:
- **What it is** — from the reference (word for word)
- **Why it matters** — the research rationale
- **Source** — full citation (authors, journal, year)
- **Observation** — the measured evidence (quotes, counts, screenshot reads), stated before the verdict
- **Compliance** — PASS / FAIL / N/A / UNVERIFIED, naming the criterion that fired, with confidence
- **How to fix** — actionable recommendation with effort class (FAIL only)

Grades are weighted by each rule's research strength and effect size. Operational
practices that can't be seen from the website (churn tactics, affiliate terms, trial
ops) are reported in an ungraded Practices Review instead of being guessed at.

## Requirements

- Claude Code CLI
- A Chromium-based browser for DOM extraction and screenshots — Chrome, Chromium, Brave,
  Edge, Arc, or a Playwright-installed headless shell are all auto-discovered
- Node.js (for the zero-dependency signal extractor; graceful fallback without it)
- WebFetch (built-in, used only as a last-resort fallback)

## License

MIT
