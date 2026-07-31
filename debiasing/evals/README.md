# debiasing — evals

Regex-based eval set for the `debiasing` skill. Two things are under test at once:

1. **The reversibility triage actually scopes the check** — a two-way-door decision
   gets the short form, a one-way-door decision gets the full checklist. This is
   the mechanism the skill is built around, so it's the most important thing to
   verify, not an afterthought.
2. **The trigger boundary against `interviews` holds.** Both skills touch
   architecture; `interviews` owns "what should this look like," `debiasing` owns
   "is this choice sound." `neg-cross-interviews` here checks debiasing doesn't
   fire on interviews' territory; a matching case in `interviews/evals/evals.json`
   checks the reverse.

## Run

```bash
# from ~/code/skills
python3 run_evals.py debiasing                       # default: claude -p on Haiku
python3 run_evals.py debiasing --case pos-one-way-door --case pos-two-way-door --trials 1
python3 run_evals.py debiasing --harness-cmd 'codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check -m gpt-5.4-mini {prompt}'
```

**The skill must be installed in whatever harness you test**, since each trial
runs in an isolated empty tempdir and only user-level skills load there:
Claude Code via `~/.claude/skills` (already symlinked to this repo), Codex via
`~/.agents/skills/debiasing` (symlink it manually — see the root README).

## What the checks mean

**Filesystem (`type: "files"`) first.** Every positive case expects
`workspace_clean: true` — pressure-testing a decision is a conversation, not code.
If the agent starts writing files, it skipped straight to implementation instead
of engaging.

**The contrast pair is the core of this eval set:**

- `pos-one-way-door` (irreversible migration) must name **≥3 biases** — proof the
  full five-step checklist ran.
- `pos-two-way-door` (reversible library swap) must recognize reversibility **and**
  stay under **4 questions** (`max`) — proof the short form actually stayed short.
  A skill that always runs the full checklist regardless of stakes passes the
  first case and fails this one; that's the point of pairing them.

**Bias vocabulary, positive vs negative.** Positives require bias-related
vocabulary (`min: 1`+); negatives negate it entirely. Five negative cases cover
the "don't fire" boundary from different angles: trivial choice, factual
question, bug fix, an explicit "don't question this," and the `interviews`
boundary.

## Calibration note

The `min`/`max` thresholds here are first-pass estimates, not measured values —
run a small trial batch first (`--trials 1` on the contrast pair) and read the
transcripts in `evals/results/<timestamp>/results.json` before trusting the
thresholds at scale. This is exactly how `interviews`' own eval set found its
first bugs (an over-tight question cap, a harness permission issue) — expect the
same here.
