# skills

Source of truth for my agent skills. Model-agnostic by design: each skill is a
`SKILL.md` (markdown + YAML frontmatter), the format shared by Claude Code, Codex,
Cursor, and dozens of other coding agents.

## Skills

| Skill | What it does | Evals |
|---|---|---|
| [`find-skills`](find-skills) | Discovers and installs skills from the open agent-skills ecosystem (`npx skills`). | — |
| [`interviews`](interviews) | Before a non-trivial build, interviews you to lock down the decisions that would change the architecture. | [evals](interviews/evals) |
| [`slidev`](slidev) | Creates and presents technical slide decks with Slidev (markdown + Vue). Installed from [`slidevjs/slidev`](https://github.com/slidevjs/slidev) (official). | — |

## How agents use this repo

Each agent reads skills from its own directory. Instead of copying files, I point a
symlink here — this repo stays the single copy and every agent sees the same thing:

```bash
# Claude Code
ln -s ~/code/skills ~/.claude/skills

# other agents (adjust the target per each one's docs)
# Codex   → ~/.codex/skills
# Cursor  → ~/.cursor/skills
```

Alternative (no symlink): install via the ecosystem's package manager —
`npx skills add <owner/repo@skill> -g`.

## Structure

```
skills/
  run_evals.py        # shared eval runner (points at a skill by name)
  find-skills/
    SKILL.md
  <skill>/
    SKILL.md           # frontmatter (name, description) + body
    references/        # optional: files that load on demand
    evals/              # optional: evals.json (+ results/, gitignored)
```

One skill = one capability. `SKILL.md` stays lean; long details move to
`references/` and only load when the agent needs them.

## Testing a skill (evals)

The runner is a single script at the root; the skill is the argument. Runs on
`claude -p` with Haiku by default:

```bash
python3 run_evals.py interviews                    # default: Haiku
python3 run_evals.py interviews --model claude-sonnet-5
python3 run_evals.py interviews --harness-cmd 'codex exec --full-auto {prompt}'
```

Requires the `claude` CLI to be logged in (`claude` → `/login`), or another harness
via `--harness-cmd`. If the harness breaks (not logged in, crash, timeout) the case
is marked **ERRORED**, never pass/fail — a broken tool never becomes a result. Each
skill keeps its own `evals/evals.json` next to its `SKILL.md`.

## CI

`.github/workflows/evals.yml` runs `run_evals.py` (Haiku, default) for every skill
that has an `evals/evals.json`, on every push/PR touching `evals.json`, `SKILL.md`,
or the runner itself. Needs one repo secret:

- **Settings → Secrets and variables → Actions → New repository secret**
- Name: `ANTHROPIC_API_KEY` — used by the `claude` CLI in headless mode (no interactive `/login`)

Results from each run are attached as a workflow artifact.

## Principles

- **English only.** Every skill in this repo is written in English (frontmatter and body); this README is the exception.
- **The description is what triggers the skill.** Write the what / when / when-not.
- **Lean.** Goals and constraints, not a step-by-step that boxes the agent in.
- **Human-written.** The draft can come out of a conversation, but I decide the
  content — a bad skill file encodes a bad process forever.
