# And/or Labs skills

Agent skills for go-to-market work: audit the stack, fix the positioning, grade the site, brief the brand, ship the story. Each one runs in Claude Code as a plugin and in any other agent through [skills.sh](https://skills.sh).

| Skill | What it does | Command |
|---|---|---|
| [stack-maximizer](plugins/stack-maximizer) | Finds every GTM tool you pay for from local evidence, kills duplicates, fills gaps, writes a 30/60/90 roadmap | `/stack-maximizer` |
| [fix-my-positioning](plugins/fix-my-positioning) | Grades B2B positioning on five frameworks (0-10), critiques the homepage hero, writes three rewrites | `/fix-my-positioning <url>` |
| [saas-grader](plugins/saas-grader) | Scores a SaaS site against 47 rules from peer-reviewed marketing research, each one cited | `/saas-grader:saas <url>` |
| [rand-brief](plugins/rand-brief) | Reads a brand the way Paul Rand would and writes a one-page brief: one idea, one mark, one palette | `/rand-brief <url>` |
| [build-in-public](plugins/build-in-public) | Turns your Claude Code sessions and commits into reviewed X and LinkedIn drafts; never auto-posts | `/build-in-public:draft` |

## Install

**Claude Code**, all skills from one marketplace:

```
/plugin marketplace add eclecticv/skills
/plugin install stack-maximizer@andorlabs
```

Swap in any skill name from the table.

**Any agent** (Codex, Cursor, Gemini CLI and others) via [skills.sh](https://skills.sh):

```bash
npx skills add eclecticv/skills --skill stack-maximizer
npx skills add eclecticv/skills          # pick from the list
```

## Layout

```
.claude-plugin/marketplace.json   the "andorlabs" marketplace, one entry per plugin
plugins/<name>/                   a complete plugin: manifest, skills, agents, scripts, README
```

Each plugin keeps its own README with usage and requirements. Histories from the original single-skill repos are preserved; `git log -- plugins/<name>` shows them.

## License

MIT. Built by [And/or Labs](https://andorlabs.ca).
