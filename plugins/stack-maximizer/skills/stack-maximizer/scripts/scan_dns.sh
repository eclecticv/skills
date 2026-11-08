#!/usr/bin/env bash
# DNS reveals SaaS the website never loads: SPF includes name every service
# allowed to send as the domain, verification TXT records name tools that were
# connected to it, DKIM selectors fingerprint email platforms. Read-only, public.
# Usage: scan_dns.sh example.com [more domains...] > dns.txt
set -u
if ! command -v dig >/dev/null 2>&1; then
  echo "# BLOCKED: dig not installed (macOS: built in; Debian/Ubuntu: apt install dnsutils; Windows: use WSL)" >&2
  exit 2
fi
SELECTORS="google selector1 selector2 k1 k2 k3 s1 s2 mandrill zendesk1 zendesk2 intercom kl kl2 cm hs1 hs2 pm mailjet krs smtp mxvault resend sendgrid"
for d in "$@"; do
  echo "# DOMAIN $d"
  echo "## TXT";   dig +short TXT "$d"
  echo "## MX";    dig +short MX "$d"
  echo "## DMARC"; dig +short TXT "_dmarc.$d"
  echo "## DKIM"
  for s in $SELECTORS; do
    r=$(dig +short TXT "$s._domainkey.$d"; dig +short CNAME "$s._domainkey.$d")
    # Emit a dkim:<selector> marker (matched as a token) plus the record head,
    # whose CNAME target usually names the vendor outright.
    [ -n "$r" ] && echo "dkim:$s -> $(echo "$r" | tr '\n' ' ' | cut -c1-160)"
  done
  echo "## SUBDOMAIN CNAMES"
  for sub in www go info email mail click links track learn blog help support docs community events book meet; do
    c=$(dig +short CNAME "$sub.$d" | head -1)
    [ -n "$c" ] && echo "$sub.$d -> $c"
  done
done
