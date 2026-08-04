---
name: knowledge
description: Capture durable knowledge into the user's Obsidian vault. Trigger when the user says "knowledge", asks to save or record something learned, or when the conversation produces knowledge worth keeping — a LeetCode problem solved, a root cause debugged, a pattern or technique finally understood, "agora entendi", "isso é bom saber", "salva isso". Search the vault first and enrich an existing note rather than duplicating, then draft the note and confirm before writing. Do NOT trigger for passing explanations the user gave no signal of wanting to keep, for questions still being asked, for routine code edits, mid-way through an active `leetcode` tutoring session (wait for its own recap handoff), or when the user is pressure-testing a decision (that is `debiasing`) or scoping something to build (that is `interviews`).
---

# Knowledge

Capture what was learned into the vault, in the vault's own idioms, so it is findable
months later. Writing the note is the cheap part; the value is in it being found again
and connected to what is already there.

A note nobody finds again cost the writing and returned nothing.

## Where it lives

Vault root: **`~/apple-core`** (Obsidian). If that path does not exist, ask — do not
guess or create a vault elsewhere.

```
apple-core/
├── LeetCode.md          # MOC for the topic
├── leetcode/
│   ├── problems/        # one note per problem
│   └── patterns/        # one note per pattern; acts as the MOC for its problems
└── inbox/               # captured knowledge with no home yet
```

Folders are topics; links carry the relationships. Start minimal and let the taxonomy
emerge: new knowledge that fits no existing folder goes to `inbox/`. Once **three or
more** inbox notes share a theme, propose promoting them into their own folder with a
MOC. Do not invent empty folders in advance.

## When to engage

Engage when the exchange produced something worth keeping: a problem solved, a
non-obvious root cause, a technique understood, a decision's rationale worth revisiting.

Skip when:

- The user is still asking — capture after the understanding lands, not during.
- It was a passing explanation with no signal the user wants it kept.
- The knowledge is already fully in the repo or its docs; link to it, don't copy it.
- The user is weighing a decision (`debiasing`) or scoping a build (`interviews`).
- A `leetcode` tutoring session is still in progress — an "ah saquei" mid-hint-ladder
  is progress, not the recap. Wait for `leetcode`'s own Output step to hand it off.

If unsure whether something is worth a note, ask one question: *"Quer que eu guarde isso
na KB?"*

## How to capture

### 1. Search before writing

Search the vault for the topic first. If a note already covers it, **enrich that note**
— add the new insight, tighten what is now better understood, add links. Creating a
second shallow note on the same topic is the main way a vault rots.

### 2. Draft and confirm

Show the draft and wait for approval before writing anything to disk. Write only what
the user actually learned or confirmed — not a textbook dump on the topic.

### 3. Write, then wire it up

After writing, add the note to its folder's MOC and link it to related existing notes.
A note that nothing links to is nearly invisible in Obsidian.

## LeetCode

Two note types, both in play:

- **Problem note** (`leetcode/problems/`) — one per problem. Built for *re-practice*, not
  reference: the statement and the user's own insight stay visible, while the solution
  and complexity go inside a collapsed callout so the problem can be re-attempted later.
- **Pattern note** (`leetcode/patterns/`) — one per technique (Sliding Window, Two
  Pointers, BFS). This is where the transferable learning lives; it links to every
  problem that used it. Always link a problem note to its pattern note, creating the
  pattern note if it does not exist yet.

Set `next_review` when writing a problem note so a Bases view can surface what is due.
When a `leetcode` session hands off a recap, write it in whichever shape the recap is —
including whether a full solution was given, so the note stays honest about what was
earned versus handed over. On a review recap for a note that already exists, **update**
`next_review` and `mastered` on it rather than creating a new note.

See `references/templates.md` for both templates.

## Obsidian format

The vault is vanilla Obsidian — no Dataview. Structure comes from properties (queryable
via Bases) and wikilinks. Follow `references/obsidian-format.md` exactly; several rules
there are easy to get wrong and silently break (notably: a wikilink inside a property
must be quoted, and properties support no markdown and no nesting).
