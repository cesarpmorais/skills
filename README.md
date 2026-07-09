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
python3 run_evals.py interviews                    # default: claude -p, Haiku
python3 run_evals.py interviews --model claude-sonnet-5
python3 run_evals.py interviews --harness-cmd 'codex exec -s workspace-write -m gpt-5-mini {prompt}'
```

Requires the `claude` CLI to be logged in (`claude` → `/login`), or another harness
via `--harness-cmd`. If the harness breaks (not logged in, crash, timeout) the case
is marked **ERRORED**, never pass/fail — a broken tool never becomes a result. Each
skill keeps its own `evals/evals.json` next to its `SKILL.md`.

## CI

`.github/workflows/evals.yml` runs `run_evals.py` for every skill that has an
`evals/evals.json`, on every push/PR touching `evals.json`, `SKILL.md`, or the runner
itself. CI uses the **Codex CLI** (`@openai/codex`) on a cheap/fast OpenAI model
(the Codex-side equivalent of Haiku) rather than the local default — Codex is
easier to authenticate headlessly in Actions. Needs one repo secret:

- **Settings → Secrets and variables → Actions → New repository secret**
- Name: `OPENAI_API_KEY` — an OpenAI API key from [platform.openai.com](https://platform.openai.com), used by `codex login --with-api-key` for headless auth (no interactive login)

Results from each run are attached as a workflow artifact.

## Principles

- **English only.** Every skill in this repo is written in English (frontmatter and body); this README is the exception.
- **The description is what triggers the skill.** Write the what / when / when-not.
- **Lean.** Goals and constraints, not a step-by-step that boxes the agent in.
- **Human-written.** The draft can come out of a conversation, but I decide the
  content — a bad skill file encodes a bad process forever.
