# interviews — evals

Regex-based eval set for the `interviews` skill. This is a trigger-heavy preference
skill, so the biggest risk is **over-triggering** — half the cases are negative on
purpose.

## Run

Use the shared runner at the repo root, pointing it at this skill by name:

```bash
# from ~/code/skills
python3 run_evals.py interviews                       # default: claude -p on Haiku
python3 run_evals.py interviews --model claude-sonnet-5
python3 run_evals.py interviews --case pos-add-auth --trials 1
python3 run_evals.py interviews --harness-cmd 'codex exec --full-auto {prompt}'
```

Exit code is `0` only if every case clears `--min-pass-rate` (default 0.6 over 5
trials), `3` if the harness errored (see below), `1` on real failures. Per-trial
transcripts land in `evals/results/<timestamp>/results.json`.

Requires the `claude` CLI on PATH and logged in (`claude` → `/login`), or another
harness via `--harness-cmd`. A harness that exits non-zero (not authenticated,
crash, timeout) is reported as **ERRORED**, never as pass/fail.

## What the checks mean

Two layers. Each trial runs in a fresh, empty temp workspace.

**1. Filesystem (`type: "files"`) — the deterministic layer.**
Interviewing writes nothing; building writes files. So:

- `{"type": "files", "workspace_clean": true}` — positives must leave the workspace
  empty (the agent asked, it did not code).
- `{"type": "files", "workspace_clean": false}` — `neg-just-build` must produce the
  endpoint file (it was told to just build).
- `{"type": "files", "exists": "path"}` — assert one exact artifact.

Hidden files/dirs are ignored (so a harness dropping `.claude/` scratch does not read
as dirty); pass `"include_hidden": true` to count them.

**2. Regex over the transcript — the corroborating layer.**
Positives ask several questions (`\?` ≥ 3) **and** hit architecture vocabulary.
Negatives must **not** open an architecture interview (vocab negated, question count
capped). `min` defaults to 1, but to 0 when only `max` is set (so "at most one
question" passes on zero questions).

Where the filesystem is ambiguous — a typo fix or rename in an *empty* workspace has
nothing to change, so a well-behaved agent writes nothing either way — those negative
cases rely on regex alone.

## Going further: trace-based trigger detection

The filesystem layer proves *behavior*, not that the skill file loaded. For a signal
that the skill itself fired, parse the harness trace where it exposes invocations —
e.g. Claude Code:

```bash
claude -p '<prompt>' --output-format stream-json --verbose
# then grep the trace for the skill being loaded / the Skill tool call
```

Add that as an extra check per harness that supports it; keep the files + regex layers
as the portable baseline.
