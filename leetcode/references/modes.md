# Mode mechanics

Detail that would bloat SKILL.md. Load this when actually running a session,
not just to decide whether to trigger.

## hint — the ladder

Three rungs, climbed one at a time, never skipped:

1. **Orient** — restate the problem's real shape: what varies, what's fixed,
   what the brute force would cost. No pattern name yet.
2. **Narrow** — name the family it's from (two pointers, sliding window, DP on
   subsequences...) and the one property of the input that makes that family
   fit. Still no data structure or pseudocode.
3. **Structure** — the shape of the approach in prose or near-pseudocode (what
   to track, what to update on each step) — but not runnable code.

Only above rung 3, on explicit request, does actual code appear — and per the
gate in SKILL.md, that gets flagged in the recap as a given solution.

Move up a rung only when the user says the current one didn't land. Don't
pre-empt by handing rung 2 before they've sat with rung 1.

## debug — minimal fix

Prompt shape to follow (adapted from a widely-used template):

> Here's my solution to [problem]. It fails on: [cases]. Change the minimum
> number of lines to make it pass, and explain why my original logic broke.

Resist rewriting in a cleaner style even if one comes to mind — a foreign
"better" solution teaches nothing about where the user's own model was wrong.
If the minimal fix genuinely requires restructuring, say that plainly instead
of quietly doing it.

Before pointing at the bug, make the user trace first: ask what test case they
ran (or would run) and what they expected vs. what actually happened. If they
paste a new revision without having stated that, don't diagnose it yet — hand
back a concrete failing case (or ask them to construct one) and have them walk
through their own code against it before getting the next nudge. This is what
keeps debug from turning into round-by-round hand-holding across many small
revisions: each round costs the user a trace, not just a paste.

## pattern — mapping, not re-teaching

Check the vault first (see SKILL.md → Reading the vault). If a pattern note
already exists, build on it rather than re-explaining the pattern from zero.
Connect to:

- Problems the user has already solved that share this pattern.
- Sibling problems worth trying next, ordered easy → hard.
- A reusable template if the pattern has one (e.g. one interval-scheduling
  skeleton that covers a whole family of greedy problems).

If invoked before the user has attempted the current problem, explain the
pattern in general terms and connect it — don't derive the concrete solution
to the specific problem in front of them; that still routes through the `hint`
gate.

## mock — interviewer persona

Ground rules:

- The user narrates while solving; don't drive toward the answer.
- Ask the clarifying-requirements question first, the way a real interviewer
  would — reward the user for asking it back, note it if they skip straight to
  code.
- Track and call out, at the end (not mid-flow — that breaks the simulation):
  long silences, coding before clarifying constraints, backtracking without
  saying why out loud.
- If truly stuck, nudge the way an interviewer would (a small hint, not a
  rung-3 structure dump) rather than exiting the persona.

## syntax — the boundary

Fix: typos, wrong syntax for the language, type errors, missing imports,
indentation.

Don't fix: a loop condition that changes the algorithm's result, a wrong
recurrence, a wrong base case, an off-by-one that changes correctness rather
than crashing. If unsure which side of that line a bug is on, say so and
suggest switching to `debug` mode instead of guessing.

## review — pulling due problems

Read `~/apple-core/leetcode/problems/*.md` frontmatter for `next_review <=`
today. Present them oldest-due first. Run each as a cold `hint` or `debug`
session — no peeking at the old note's collapsed solution first, that defeats
the point. After it's resolved, hand the outcome to `knowledge` so it can
update `next_review` and `mastered` on the existing note, rather than creating
a new one.
