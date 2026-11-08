# Report template

Fill every section from `scored.json` plus the gap and value research. Numbers come from the script output, never re-derived by hand. Write plain verdicts, each with a number or a mechanism. No em dashes.

```markdown
# <Company> GTM stack: keep, kill, build

<date> · stage <stage> · motion <motion> · coverage: <sources read> (blocked: <sources and why>)

## Verdict
- <N> tools found, <K> keep, <A> activate, <X> kill, <G> essential gaps.
- Spend: $<now>/mo → $<after>/mo (<savings>/mo saved; <n> tools with unknown cost).
- One paragraph: the shape of the stack today (for example "two CRMs, three email tools, nothing reveals who visits the site") and the shape after.

## Stack after cleanup
| Core function | Tool | Also owns | $/mo | Why it stays |
One row per kept tool, ordered by capability priority. Every essential capability appears exactly once
across Core function and Also owns, or appears in Gaps.

## Kill list
| Tool | Reason | Replaced by | $/mo | Exit steps |
Exit steps are concrete: export what (contacts, sequences, recordings), where it moves, remove the tag / SPF
include / integration / seats, cancel before <renewal date if known>.

## Activate
Tools that are paid for, unused, and the only cover for an essential capability: the 30-day switch-on plan,
or replace.

## Gaps
| Capability | Tier | Recommendation | Alt | Cost (verified, source URL) | Connects to |
"Native: switch on <feature> in <kept tool>" beats a new tool. Essentials first.

## How it connects
A mermaid flowchart of data flow across the kept and recommended tools, for example:
website → deanonymization → enrichment → CRM → MAP / sales engagement → scheduling → call recording → CRM,
with analytics and attribution reading from the site and CRM. Mark missing links as dashed edges.

## Get full value from every kept tool
### <Tool>: <core function>
- 3-5 actions, each specific to their plan and evidence (wire X to Y, turn on Z, fix consent on pixel W),
  each with the expected effect.

## Roadmap
### Week 1: cut and connect
Kills that need no migration, removal of dead tags and SPF includes, critical integrations.
### Days 8-30: fill essential gaps
### Days 31-60: activate value plays
### Days 61-90: measure and tighten
Each phase: numbered actions, and a done-when check (for example "every form submission lands in CRM within
1 minute with source attribution").

## Assumptions
Every default or inference that the user didn't confirm, one line each.
```
