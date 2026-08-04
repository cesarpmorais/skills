# knowledge — evals

8 cases (4 positive / 4 negative) for a proactive, trigger-heavy skill. Run from the
repo root:

```bash
python3 run_evals.py knowledge                       # default: claude -p on Haiku
python3 run_evals.py knowledge --case pos-leetcode-solved --trials 1
```

See the [root README](../../README.md#testing-a-skill-evals) for flags, exit codes, and
the ERROR-vs-fail distinction.

## Why the vault path matters for these evals

The vault (`~/apple-core`) is an **absolute path outside the isolated trial tempdir**,
unlike `interviews`, where "did it write a file" is checked directly in the workspace.
Here the `workspace_clean: true` check proves something narrower: the agent didn't
create a vault or stray notes *in the current directory* — it says nothing about whether
it correctly wrote (or refrained from writing) to the real vault.

The real safety net is the **confirm-before-write step** in the skill itself: the agent
must draft and ask before touching disk. That's why several positive cases assert a
confirmation signal (`\?`, "posso", "quer que") in the transcript rather than a file
write — for this skill, *asking* is the correct terminal behavior for a trial, not
writing.

## What the checks mean

- **Positives** assert the Obsidian idioms actually used correctly: a wikilink
  (`\[\[`), a collapsed callout for LeetCode solutions (`\[!success\]-`), correct folder
  routing (`leetcode/problems` vs `leetcode/patterns`), and — critically — that the
  agent asks before writing rather than just doing it.
- **Negatives** cover the two ordinary false-trigger shapes (mid-question, routine code
  edit) **and** three sibling-skill boundaries: `neg-cross-interviews` (scoping a
  build is `interviews`' job), `neg-cross-debiasing` (weighing a decision is
  `debiasing`'s job), and `neg-cross-leetcode-midsession` (an "ah saquei" mid-hint-ladder
  is progress inside a `leetcode` session, not that session's recap — jumping in early
  would write a shallow note before the session even reached its own Output step). All
  four skills load together in CI, so this is where cross-triggering between them
  actually gets caught — see the root README's CI section.

## Known gap

None of these cases assert the agent *searched the vault first* before drafting
(step 1 of the skill) — that would need a vault fixture with a pre-existing note and a
check that the agent referenced/updated it rather than drafting a duplicate. Worth
adding once the skill has run for real and there's a natural case to model it on.
