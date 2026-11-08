#!/usr/bin/env python3
"""Deterministic keep/kill + gap analysis for a confirmed GTM inventory.

The LLM gathers and confirms facts. This script does the arithmetic, so the
same inventory always yields the same verdicts and reruns are comparable.

Input (inventory.json):
{
  "company": "Acme", "stage": "founder|growth|scale", "motion": "plg|sales_led|hybrid",
  "tools": [{
    "name": "HubSpot",
    "status": "using|unused|trial|not_ours|product",   # confirmed by the user
    "capabilities": ["crm", "map", "forms"],           # ids from capabilities.json, the ones THIS team uses it for
    "primary": "crm",                                  # optional, defaults to capabilities[0]
    "monthly_cost": 90,                                # USD, 0 if free, null if unknown
    "usage": 3,                                        # 0 none, 1 monthly, 2 weekly, 3 daily
    "integrations": ["Calendly", "Zapier"],            # live connections to other tools in the inventory
    "lock_in": 1,                                      # 0 easy to leave, 1 some data/process, 2 system of record
    "keep": false                                      # user override: never kill
  }]
}

Rules, in order:
 1. not_ours / product -> excluded (company product runtime, personal, other team).
 2. Per capability, candidates are using/trial tools that list it. Unused tools
    only compete when nobody else covers the capability.
 3. Winner = highest score, then lower cost, then name. A tool is kept if it
    wins at least one capability. Its core function is its primary capability
    if it won it, else its highest-priority win.
 4. Losers that win nothing are killed, pointed at the tool that replaces them.
 5. An unused tool that is the only cover for an essential capability is
    "activate" (pay for it only if it gets switched on in 30 days).
 6. Gaps = capabilities at tier E (essential) or R (recommended) for the stage
    and motion that no kept tool covers.

Score = 4*usage + 2*min(integrations,5) + min(capabilities-1,3) + 2*lock_in
        - cost_penalty, cost_penalty = log2(1 + monthly_cost/25)  (unknown cost = 1)
"""
import json, math, pathlib, sys

CAPS = json.loads((pathlib.Path(__file__).resolve().parent.parent / "references" / "capabilities.json").read_text())["capabilities"]
CAP = {c["id"]: c for c in CAPS}


def tier(cap, stage, motion):
    c = CAP[cap]
    return (c.get("motion", {}).get(motion) or c["tier"])[stage]


def score(t):
    cost = t.get("monthly_cost")
    pen = 1.0 if cost is None else math.log2(1 + cost / 25)
    integ = t.get("integrations") or []
    n_int = integ if isinstance(integ, int) else len(integ)
    s = 4 * t.get("usage", 0) + 2 * min(n_int, 5) + min(len(t["capabilities"]) - 1, 3) + 2 * t.get("lock_in", 0) - pen
    if t["status"] == "trial":
        s -= 2  # unproven: an established tool should win ties
    return round(s, 2)


def main():
    inv = json.loads(pathlib.Path(sys.argv[1]).read_text())
    stage, motion = inv.get("stage", "founder"), inv.get("motion", "hybrid")
    unknown = sorted({c for t in inv["tools"] for c in t.get("capabilities", []) if c not in CAP})
    if unknown:
        sys.exit(f"unknown capability ids: {unknown} (see references/capabilities.json)")

    tools = {}
    excluded = []
    for t in inv["tools"]:
        if t["status"] in ("not_ours", "product") or not t.get("capabilities"):
            excluded.append({"name": t["name"], "status": t["status"]})
            continue
        t = dict(t)
        t.setdefault("primary", t["capabilities"][0])
        t["score"] = score(t)
        tools[t["name"]] = t

    def rank(cands):
        return sorted(cands, key=lambda t: (-t["score"], t.get("monthly_cost") or 0, t["name"].lower()))

    winners = {}
    for cap in sorted({c for t in tools.values() for c in t["capabilities"]}, key=lambda c: CAP[c]["priority"]):
        active = [t for t in tools.values() if cap in t["capabilities"] and t["status"] in ("using", "trial")]
        pool = active or [t for t in tools.values() if cap in t["capabilities"]]
        winners[cap] = rank(pool)[0]["name"]

    decisions = []
    for t in sorted(tools.values(), key=lambda t: -t["score"]):
        won = sorted([c for c, w in winners.items() if w == t["name"]], key=lambda c: CAP[c]["priority"])
        d = {"name": t["name"], "score": t["score"], "monthly_cost": t.get("monthly_cost"), "status": t["status"]}
        if won:
            core = t["primary"] if t["primary"] in won else won[0]
            d.update(core_function=core, also_owns=[c for c in won if c != core])
            if t["status"] == "unused":
                essential = any(tier(c, stage, motion) == "E" for c in won)
                d.update(decision="activate" if essential else "kill",
                         reason=("only cover for an essential capability; switch it on within 30 days or replace"
                                 if essential else "paid and unused; capability is not essential at this stage"))
            else:
                d.update(decision="keep", reason=f"owns {', '.join(CAP[c]['name'] for c in won)}")
        elif t.get("keep"):
            d.update(decision="keep", core_function=t["primary"], also_owns=[],
                     reason=f"user override; redundant with {winners[t['primary']]} for {CAP[t['primary']]['name']}")
        else:
            repl = winners[t["primary"]]
            d.update(decision="kill", core_function=None, also_owns=[],
                     reason=("paid and unused" if t["status"] == "unused" else "redundant") +
                            f"; {repl} covers {CAP[t['primary']]['name']}", replaced_by=repl)
        decisions.append(d)

    kept = {d["name"] for d in decisions if d["decision"] in ("keep", "activate")}
    covered = {c for c, w in winners.items() if w in kept}
    covered |= {d["core_function"] for d in decisions if d["decision"] == "keep" and d.get("core_function")}
    gaps = [{"capability": c["id"], "name": c["name"], "tier": tier(c["id"], stage, motion)}
            for c in CAPS if c["id"] not in covered and tier(c["id"], stage, motion) in ("E", "R")]
    # A gap whose only tool was just killed for non-use reads as a contradiction
    # unless the report says so: name the killed tool so the write-up can pick
    # "re-activate" vs "use a free/native alternative" explicitly.
    for g in gaps:
        g["killed_tools_covering"] = [d["name"] for d in decisions if d["decision"] == "kill"
                                      and g["capability"] in tools[d["name"]]["capabilities"]]
    gaps.sort(key=lambda g: (g["tier"] != "E", CAP[g["capability"]]["priority"]))

    def total(ds):
        return round(sum(d["monthly_cost"] or 0 for d in ds), 2)
    killed = [d for d in decisions if d["decision"] == "kill"]
    result = {"company": inv.get("company"), "stage": stage, "motion": motion,
              "decisions": decisions, "gaps": gaps, "excluded": excluded,
              "spend": {"current_monthly": total(decisions), "kill_savings_monthly": total(killed),
                        "after_monthly": round(total(decisions) - total(killed), 2),
                        "unknown_cost_tools": [d["name"] for d in decisions if d["monthly_cost"] is None]},
              "capability_owner": {c: w for c, w in winners.items() if w in kept}}
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
