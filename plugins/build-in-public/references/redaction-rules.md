# Redaction Rules

Reference for the `/draft` skill. The `secret_scan.py` script is the enforcement
gate. These rules explain what it detects, what is never posted regardless of
detection, and what happens when any finding is present.

---

## Secret Categories `secret_scan.py` Detects

These regex patterns and heuristics are checked against every draft before
publishing. Category names match the `type` field in the JSON report.

| Category | Pattern / Heuristic | Example match |
|----------|---------------------|---------------|
| `aws_access_key` | `AKIA` followed by 16 uppercase alphanums | `AKIAIOSFODNN7EXAMPLE` |
| `anthropic_key` | `sk-ant-` followed by 20+ alphanums/dash/underscore | `sk-ant-api03-…` |
| `openai_key` | `sk-` followed by 20+ alphanums | `sk-proj-abc123…` |
| `vcs_token` | GitHub PAT prefixes: `ghp_`, `gho_`, `github_pat_`, Slack tokens `xoxb_` / `xoxp_` | `ghp_abc123…` |
| `bearer` | `Bearer ` followed by 16+ chars of a token-like string | `Bearer eyJhbGci…` |
| `env_assignment` | All-caps env var name `=` non-whitespace value at line start | `DATABASE_URL=postgres://…` |
| `private_key` | PEM header `-----BEGIN … PRIVATE KEY-----` | RSA / EC / PKCS8 private keys |
| `high_entropy` | Token ≥ 28 chars with Shannon entropy ≥ 4.2 bits/char | Any long random string |

**High-entropy detection specifics:**
- Scans all alphanumeric+base64+underscore+dash tokens ≥ 28 characters
- Shannon entropy threshold: 4.2 bits/character
- Catches tokens that do not match known prefixes (custom API keys, JWTs, etc.)

---

## Never-Post List (Denylist)

These terms are blocked via the `--deny` flag passed to `secret_scan.py`.
Even if no secret pattern fires, a denylist match blocks the draft.

### Client and employer names
- Add the names of current clients, employers, or partner organisations to the
  denylist in the plugin's configuration.
- Include both full legal name and common short name (e.g., "Acme Corp" and "Acme").
- These are never auto-discovered — the installer maintains this list.

### Unreleased product names
- Any product, feature, or codename that has not been publicly announced.
- Add to the denylist before the product enters any public channel.
- Remove from denylist after the public announcement commit is shipped.

### Internal URLs
- Hostnames or paths for internal tooling, staging environments, admin panels,
  or private infrastructure (e.g., `internal.example.com`, `admin.corp/`, `10.0.0.`).
- Add base hostname patterns to the denylist; partial matches are caught by
  `re.escape` + `re.search`.

---

## Blocking Rule

> **ANY finding from `secret_scan.py` — whether a secret pattern match, a
> high-entropy token, or a denylist hit — BLOCKS the draft from being posted.**

The skill MUST:
1. Surface the full findings report to the user (the JSON from `secret_scan.py`).
2. Halt and request human review before any post is queued or published.
3. Never auto-redact and re-post silently. The human must approve the edited draft.

There are no warnings, partial passes, or override flags for the `/draft` skill.
Clean means `"clean": true` in the JSON report with an empty `"findings": []` array.

---

## How `secret_scan.py` Is Invoked

```bash
# Scan draft text from stdin
echo "$DRAFT_TEXT" | python3 scripts/secret_scan.py --deny "ClientName" --deny "UnreleasedThing"

# Scan a draft file
python3 scripts/secret_scan.py --file draft.md --deny "ClientName"
```

Exit code `0` = clean. Exit code `1` = findings present. The skill gates on exit code.

---

## Denylist Configuration

The installer populates the denylist at setup time via `/build-in-public:setup`.
The denylist is stored in the plugin's local configuration and passed as `--deny`
arguments at scan time. Do not hardcode names in `secret_scan.py` itself — keep
patterns in configuration so they can be updated without touching the script.
