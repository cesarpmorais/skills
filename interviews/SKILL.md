---
name: interviews
description: Before implementing any non-trivial feature, system, or refactor, interview the user first to surface the decisions that would change the architecture. Trigger when the user asks to build, design, or architect something whose shape is not already pinned down ("build me X", "crie um app que...", "how should I structure Y", "add feature Z"). Prioritize questions that change the design over cosmetic ones; stop once the architecture-shaping decisions are settled. Do NOT trigger for small edits, bug fixes, simple questions, or when the user already specified the architecture or said to just build it.
---

# Interviews

Before building something non-trivial, run a short interview. The goal is not to
collect requirements — it is to find the few decisions that would change the
architecture if answered differently, and settle them before any code is written.

One architecture-changing question is worth ten cosmetic ones.

## When to engage

Engage when the user asks to build, design, refactor, or architect something whose
shape is not already decided.

Skip when:

- The change is small, mechanical, or a bug fix.
- The user already described the architecture, or said to just build it.
- The answer is in the code — read the repo instead of asking.

If unsure whether it is worth interviewing, ask one question: *"Want me to interview
you quickly before building, or is it already clear?"*

## How to run it

### 1. Opening batch

Ask 4-6 questions at once to map the terrain. Weight them toward decisions that fork
the design. Good territory:

- **Data & state** — what is the source of truth, who owns state, what is the shape of the core model.
- **Boundaries** — what is in scope vs out, what talks to what, sync vs async.
- **Constraints that bind the design** — scale, latency, offline, cost, existing systems to fit into.
- **Failure & lifecycle** — what happens when it breaks, how it is deployed, who maintains it.
- **Build vs buy** — is there an existing tool/skill/library that removes the need to build.

Skip anything you can infer from the repo or the request. Do not ask about colors,
naming, or details that are cheap to change later.

### 2. Follow-ups

Read the answers. Wherever an answer opens an architectural fork, go one question
deeper — one at a time, adapting to what was said. Chase only the threads that change
the design.

### 3. Stop when the architecture is locked

Stop as soon as the decisions that would change the design are resolved. Do not pad
the interview with low-value questions. When you stop, say so and move to output.

## Output

Match the project's convention:

- Repo uses **specs** (`specs/`, `spec/`) → write the decisions as a spec in that format.
- Repo uses **ADRs** (`docs/adr/`, `decisions/`, `*/adr/`) → write an ADR.
- Neither → give a short recap of the architecture decisions in the chat.

Detect the convention by looking at the repo before choosing. When in doubt, ask
which the user prefers.
