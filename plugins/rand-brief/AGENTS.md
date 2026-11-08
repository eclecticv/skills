# rand-brief — agent instructions

This repo is a brand-analysis tool for AI coding agents. Given a brand URL, it produces a **one-page design brief in the manner of Paul Rand**: name-first analysis, one idea for the mark, typeface pairings from Rand's vocabulary, a flat limited palette — argued as a single confident recommendation, never a menu of options.

## If you are an AI agent working in this repo or asked to use it

When the user asks for a Rand-style brand brief, a logo direction, or "what would Paul Rand do with my brand":

1. Read `skills/rand-brief/SKILL.md` and follow its five-stage pipeline exactly.
2. Read each file in `skills/rand-brief/references/` at the stage where the pipeline tells you to — not before:
   - `rand-principles.md` — Rand's logo criteria and verified quotes (the only quotes you may use)
   - `typefaces.md` — his typeface vocabulary and modern equivalents
   - `presentation-format.md` — the NeXT-booklet narrative voice
   - `output-schema.md` — the exact brief structure and file rules
3. Write the finished brief to the user's current working directory as `rand-brief-<domain>-<YYYY-MM-DD>.md`.

If your environment supports subagents, delegate website fetching per `agents/brand-extractor.md`. If it does not, perform the extraction step yourself following that file's report format, then continue the pipeline.

## Hard rules (all environments)

- **One recommendation.** Never present design options.
- **Verified quotes only.** If a Paul Rand quote is not in `rand-principles.md`, it does not exist for your purposes.
- **One page.** 500–700 words of body text in the brief.
- Never overwrite an existing brief; add `-v2`, `-v3` suffixes.

## Repo layout

- `skills/rand-brief/SKILL.md` — the orchestrator (Agent Skills format; also a Claude Code plugin skill)
- `agents/brand-extractor.md` — website extraction subagent definition
- `.claude-plugin/` — Claude Code plugin + marketplace manifests
- `assets/` — social image and its regeneration source
