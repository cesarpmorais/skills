# interviews — evals

Regex-based eval set for the `interviews` skill. This is a trigger-heavy preference
skill, so the biggest risk is **over-triggering** — half the cases are negative on
purpose.

## Run

No default harness — you pass one. The `{prompt}` token is replaced per case:

```bash
# Claude Code
python run_evals.py --harness-cmd 'claude -p {prompt}'

# Codex
python run_evals.py --harness-cmd 'codex exec --full-auto {prompt}' --trials 5

# single case
python run_evals.py --harness-cmd 'claude -p {prompt}' --case pos-add-auth
```

Exit code is `0` only if every case clears `--min-pass-rate` (default 0.6 over 5
trials). Per-trial transcripts land in `results/<timestamp>/results.json`.

Must run in a terminal where the harness CLI is on PATH.

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
