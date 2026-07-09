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

- **Positive cases** (`should_trigger: true`): the transcript must contain several
  questions (`\?` ≥ 3) **and** architecture vocabulary. That is the signature of the
  skill firing — an opening batch of design questions instead of diving into code.
- **Negative cases** (`should_trigger: false`): the transcript must **not** open an
  architecture interview (architecture vocab negated, question count capped).

## Known limitation

Trigger detection here reads the **final stdout**, not the tool trace — it infers
"the skill fired" from interview-shaped behavior. That is cheap and cross-harness but
approximate: a model could ask architecture questions without the skill loading, or
load it and phrase things unusually.

For a deterministic signal, add a trace-based check per harness where the trace
exposes skill invocations, e.g. Claude Code:

```bash
claude -p '<prompt>' --output-format stream-json --verbose
# then grep the trace for the skill being loaded / the Skill tool call
```

Keep the regex behavior checks as the portable baseline; layer trace checks on top
where a given harness supports them.
