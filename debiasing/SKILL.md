---
name: debiasing
description: Before finalizing a hard or important decision, an ADR, or an architectural choice between named options, pressure-test it for cognitive bias using the ddd-crew Debiasing Decisions Toolkit. Trigger on "should we do X or Y", "I think we should...", "this feels like the right call", writing/finalizing an ADR, "everyone agrees", "senior/vendor/AI said to do X", "decidimos usar X", or similar. Scale the check to how reversible the decision is: a cheap-to-undo call gets 2-3 sharp questions, an irreversible one gets the full five-step checklist. Do NOT trigger for trivial choices (naming, formatting), factual questions, bug fixes, or when the user already decided and said to just execute. Do NOT trigger when the shape of what to build is still undecided — that is the `interviews` skill's territory; use this one once a decision or preferred option already exists.
---

# Debiasing

Pressure-test a decision before it locks in. The goal is not to overrule the user —
it is to catch the moment a bias is doing the deciding instead of judgment.

Core heuristic from the toolkit this is built on: whenever "this just feels right"
shows up, pause and ask — is this a genuinely good decision, or a bias in disguise?

## When to engage

Engage when the user is weighing named options, about to finalize an ADR, states a
preference with conviction, or invokes authority/consensus as the reason ("the
senior architect said...", "everyone agrees...").

Skip when:

- The choice is trivial or cheap either way (naming, formatting, a two-line change).
- It is a factual question, not a decision.
- It is a bug fix.
- The user already decided and said to just execute — pressure a decision once,
  not after it is made.
- **The shape of what to build is not decided yet.** That is `interviews` territory:
  if the user needs the design worked out, hand it there. Use this skill once a
  decision, a leaning, or a named set of options exists to press on.

## Scope the check to reversibility

This mirrors the toolkit's own Step 5 ("spend time proportional to how hard this is
to reverse") applied to the check itself — do not run the full checklist on a
decision that costs nothing to undo.

1. **Classify first.** Two-way door (cheap/fast to reverse) or one-way door
   (expensive, slow, or impossible to reverse)? If unclear, ask exactly one
   question to find out — do not guess on something that changes how much rigor
   follows. **Open with one explicit sentence naming the classification and why**,
   before the first question, in both directions — e.g. "This is a one-way door
   (hard/costly to reverse), so full checklist." Don't just let the depth of what
   follows imply it; say it.
2. **Two-way door → short form.** Ask the 2-3 highest-risk questions only (usually
   from Steps 1 and 4 — decision-readiness and untested assumptions). Say
   explicitly that it is reversible and does not need ceremony. Do not load
   `references/checklist.md` for this path.
3. **One-way door → full checklist.** Load `references/checklist.md` and work
   through all five steps: decision-readiness, broadening the frame, independent
   advice, testing assumptions, simple rules proportional to stakes. **Name the
   bias next to each question as you ask it** (checklist.md pairs every question
   with the bias it targets — surface that pairing, don't wait until you have
   answers to name anything). **Don't ask permission to proceed — launch straight
   into the questions.** Offering an opt-out ("want me to check?") on the
   highest-stakes case just hands Status Quo Bias an easy exit; that defeats the
   point.

## How to run it

Answer what you can from context; ask only what depends on the human.

- Read the code, the ADR draft, or the conversation and answer inferable questions
  yourself (e.g. "did we consider removing something instead of adding" — check
  the diff).
- Ask only what the repo can't tell you (e.g. "did the people who advised you form
  their opinions independently of each other?").
- When you find a real risk, **name the bias** (see `references/biases.md`) instead
  of a vague "consider reconsidering." "This reads like Authority Bias — the
  senior's suggestion isn't evaluated on its own merits yet" is useful; "have you
  considered other options?" is not.
- Close with what would change the decision, not a generic report.

### Being honest about what an agent can and can't do here

The toolkit itself names two biases this skill can accidentally cause:
**Authority Bias** ("blindly trusting AI-generated code or proposals without
scrutiny") and **Correlation Neglect** (mistaking repetition for validation). So:

- Don't present findings as a verdict. You are pressure-testing, not ruling.
- **Don't count "I asked an LLM" as independent advice** — if the user consulted
  ChatGPT, Claude, and a blog post, that is not three independent sources; note
  this directly when it comes up.
- You can offer the contrarian/steelman view as a partial substitute for
  independent advice, but say plainly that it doesn't replace a second human.

The toolkit is designed for teams checking each other; the user runs this alone.
That gap is exactly why the two points above matter — without them this becomes
theater instead of a real check.

## Output

Detect the project's convention before choosing:

- Repo uses **ADRs** (`docs/adr/`, `decisions/`) → embed the block from
  `references/adr-snippet.md` into the Decision section.
- No convention → give a short recap in the chat: risks found, by name, and what
  would resolve each.

Never rewrite the user's decision for them. This skill presses on it; the user
still decides.
