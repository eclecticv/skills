#!/usr/bin/env bash
# Offline smoke test: detect -> merge -> score on fixtures. No network, no
# access to the machine's mail, history or repos. Run before every release.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
S="$ROOT/skills/stack-maximizer/scripts"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
fail() { echo "FAIL: $*"; exit 1; }

python3 "$S/build_signatures.py" >/dev/null
git -C "$ROOT" diff --quiet -- skills/stack-maximizer/references/signatures.json 2>/dev/null \
  || fail "signatures.json is stale: commit the rebuilt file"

cat > "$T/web.txt" <<'X'
<script src="https://js.hs-scripts.com/123.js"></script>
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-ABC123"></script>
https://cdn.toolkit.com/x.js
X
cat > "$T/history.txt" <<'X'
app.hubspot.com 120
calendly.com 15
X
cat > "$T/billing.txt" <<'X'
2026-10-01 stripe.com | Your receipt from Calendly
2026-09-12 mailchimp.com | Your Mailchimp invoice
X
python3 "$S/detect.py" --source web --tokens "$T/web.txt" > "$T/d_web.json"
python3 "$S/detect.py" --source history --weighted "$T/history.txt" > "$T/d_history.json"
python3 "$S/detect.py" --source email --names --ci "$T/billing.txt" > "$T/d_email.json"

python3 - "$T" <<'X'
import json, sys
t = sys.argv[1]
web = {v["vendor"] for v in json.load(open(f"{t}/d_web.json"))["vendors"]}
assert {"HubSpot", "Google Tag Manager"} <= web, web
assert "Kit (ConvertKit)" not in web, "hostname boundary broken: toolkit.com matched kit.com"
hist = {v["vendor"]: v["hits"] for v in json.load(open(f"{t}/d_history.json"))["vendors"]}
assert hist.get("HubSpot") == 120, hist
mail = {v["vendor"] for v in json.load(open(f"{t}/d_email.json"))["vendors"]}
assert {"Calendly", "Mailchimp"} <= mail, mail
X

python3 "$S/merge.py" "$T/out" "$T"/d_*.json >/dev/null
python3 - "$T" <<'X'
import json, sys
rows = {r["vendor"]: r["inferred"] for r in json.load(open(f"{sys.argv[1]}/out/candidates.json"))}
assert rows["HubSpot"] == "in use", rows
assert rows["Calendly"] == "paid+used", rows
assert rows["Mailchimp"] == "paid, idle?", rows
X

python3 "$S/score.py" "$ROOT/examples/inventory.example.json" > "$T/scored.json"
python3 - "$T" <<'X'
import json, sys
r = json.load(open(f"{sys.argv[1]}/scored.json"))
d = {x["name"]: x["decision"] for x in r["decisions"]}
assert d == {"HubSpot": "keep", "Calendly": "keep", "Zapier": "keep", "Buffer": "kill",
             "Mailchimp": "kill", "Make": "kill", "Hotjar": "kill", "RB2B": "activate"}, d
assert r["spend"] == {"current_monthly": 146, "kill_savings_monthly": 84, "after_monthly": 62,
                      "unknown_cost_tools": ["RB2B"]}, r["spend"]
assert any(g["capability"] == "session_replay" and g["killed_tools_covering"] == ["Hotjar"] for g in r["gaps"])
X
echo "smoke: ok"
