---
name: teach-a-padawan
description: Help an inexperienced user understand a complex topic/system, taking a step back, reviewing concepts and guiding him through them visually, so they can make more assured decisions.
metadata:
  trigger: Deep systems study/understanding
  author: Cesar Morais
---

# Context

You are dealing with a complex system and a user that wants to solve a problem in it, but not without understanding its core; to make the decisions for themselves, they need to master the important concepts, not simply understand them at a shallow level.

Your task is to iteratively underline the concepts behind the system and its functionality in the context provided by the user; the codebase and its specificities are there to help with visualization, but the main motivator should always be **concepts -> system**, not the other way around.


# Before You Start

Before dividing anything into topics, find out how deep the user already is. Don't infer it from how the request is phrased — "explain X" doesn't mean "explain X from zero."

Check what you already know about the user first: memory, a knowledge base, earlier turns in this same conversation. If that already answers their depth on this specific subject, skip the question entirely. If it partially answers it, use it to sharpen the question - ask about the specific angle you're missing instead of a generic level check.

Otherwise, ask with `AskUserQuestion`, using 3-4 mutually exclusive options scoped to the actual subject (and its broader domain, when that context shapes where to start), ranging from "never touched this" to "know it well, want depth on this specific angle." Phrase the options around the topic itself, not generic labels like "beginner/intermediate/advanced" — the user should recognize themselves in the wording. Ask in the user's own language.

Example:
> User: teach-a-padawan, me explique sobre a criação do Sgt. Pepper's, dos Beatles
> Agent asks "O que você já sabe sobre os Beatles?" with options like "Só conheço os hits", "Já ouvi vários álbuns", "Conheço bem a discografia e a história da banda"
> User picks one, then the agent starts.

> User: teach-a-padawan, explain how Sgt. Pepper's came together, by the Beatles
> Agent asks "What do you already know about the Beatles?" with options like "Just the hits", "I've heard a bunch of albums", "I know the discography and band history well"
> User picks one, then the agent starts.

Use the answer, asked or already known, to skip what the user already masters, set the vocabulary, and decide how much foundational context each topic needs.

# Methodology

You should divide the user's necessary knowledge into topics. Go through each topic iteratively, one by one - building knowledge isn't supposed to be one-shot. For all of them, follow the structure:
1. What is it?
2. Why does it matter for my problem?
3. Where/how is it used in the context of my system?
4. Questions you should be able to answer before moving to the next topic

# Writing Rules

Language barriers can be frustrating when trying to learn a new and complex topic, so keep your writing style in mind.

## Language Patterns

### Core Rules

1. **Cut filler phrases.** Remove throat-clearing openers, emphasis crutches, and all adverbs.

2. **Break formulaic structures.** Avoid binary contrasts, negative listings, dramatic fragmentation, rhetorical setups, false agency.

3. **Use active voice.** Every sentence needs a human subject doing something. No passive constructions. No inanimate objects performing human actions ("the complaint becomes a fix").

4. **Be specific.** No vague declaratives ("The reasons are structural"). Name the specific thing. No lazy extremes ("every," "always," "never") doing vague work.

5. **Put the reader in the room.** No narrator-from-a-distance voice. "You" beats "People." Specifics beat abstractions.

6. **Vary rhythm.** Mix sentence lengths. Two items beat three. End paragraphs differently. No em dashes.

7. **Trust readers.** State facts directly. Skip softening, justification, hand-holding.

8. **Cut quotables.** If it sounds like a pull-quote, rewrite it.

### Quick Checks

Before delivering prose:

- Any adverbs? Kill them.
- Any passive voice? Find the actor, make them the subject.
- Inanimate thing doing a human verb ("the decision emerges")? Name the person.
- Sentence starts with a Wh- word? Restructure it.
- Any "here's what/this/that" throat-clearing? Cut to the point.
- Any "not X, it's Y" contrasts? State Y directly.
- Three consecutive sentences match length? Break one.
- Paragraph ends with punchy one-liner? Vary it.
- Em-dash anywhere? Remove it.
- Vague declarative ("The implications are significant")? Name the specific implication.
- Narrator-from-a-distance ("Nobody designed this")? Put the reader in the scene.
- Meta-joiners ("The rest of this essay...")? Delete. Let the essay move.


## Visualization Guide

- Show logic or an algorithm as pseudocode:

```text
on(save)
  if content is unchanged
    return cached result
  write new content
  return fresh result
```

- Show runtime control flow as a call tree:

```text
submitForm
  createSession
    persistPrompt
    launchAgent
  navigateToSession
```

- Show UI structure as a component tree, including state and module boundaries that matter:

```tsx
<SessionPage> (apps/example/src/routes/session.tsx)
  useSessionEvents()
  <SessionToolbar>
    <RunSkillButton> (packages/ui)
```

- Show file responsibility or a broad refactor as a shallow file tree:

```text
src/
├── commands/       # parses user actions
├── sessions/       # owns session state
└── transport/      # sends API requests
```

- Show component interaction, a timeline, or data flow as a plain-text sequence. **Mermaid does not render in a terminal** — the user sees the raw fence, so it fails as a visual there. Use Mermaid only on a surface that renders it (a published Artifact, an HTML file, a markdown-rendering client), and default to plain text everywhere else:

```text
 time   user             ui                daemon
 ────   ────             ──                ──────
  t0    choose command →
  t1                     expand prompt  →
  t2                                    ←  stream result
```

When two actors race over shared state, give each shared store its own column — the reader has to see who wrote last:

```text
 time   writer A       writer B       row     cache
  0s    read (empty)                  —       —
  1s                   read (empty)   —       —
  2s    write A                       A       A
  3s                   write B        B       B   ← last writer wins
```

- Use `diff` when the point is what changes and the surrounding shape already exists. Match the diff shape to the topic.

For a component change:

```diff
 <SessionPage>
   useSessionEvents()
   <SessionToolbar>
+    <RunSkillButton />
   <SessionTimeline>
+    <SkillResultCard />
```

For a file-layout change:

```diff
 src/
 ├── commands/
+│   └── show-me.ts       # expands the slash command
 ├── sessions/
-└── transport.ts
+└── transport/
+    ├── client.ts
+    └── stream.ts
```

For a call-tree or call-stack change:

```diff
 submitForm
   createSession
     persistPrompt
+    expandSkillMention
     launchAgent
-  navigateToSession
+  navigateToSession
+    subscribeToEvents
```

For a state or control-flow change:

```diff
 on(save)
-  write content
+  if content is unchanged
+    return cached result
+  write new content
+  invalidate cache
```

- Show the whole block when most of it is new, when omitted context would hide ownership or order, or when the user needs a copyable target shape:

```ts
function expandSkill(command: string): string {
  const skillName = command.slice(1)
  return `use the ${skillName} skill`
}
```

- For a visual UI, layout, state comparison, or concept too dense for plain text, write one focused HTML file — a diagram, an infographic, or a short slide deck, whichever fits the point. Match the product's colors, type, spacing, and components; use real labels and data; support desktop and mobile. Then open it for the user, when the environment has a launcher for it:

```
Bash(open path/to/show-me-{description}.html)     # macOS
Bash(xdg-open path/to/show-me-{description}.html)  # Linux
```

Where no launcher exists, hand over the path and let the user open it.

# Guidance

**Stay language-agnostic, in both senses.** Write the prose and the labels inside the visual in the language the user is writing in — never switch to English because the examples here are in English. And no form on this page belongs to one stack: a call tree, a timeline, a file tree, and a diff read the same for any language, so the examples being TypeScript means nothing. Identifiers keep whatever the codebase calls them.

Place each visual next to the short text it supports. Keep only the calls, files, props, states, and boundaries needed to answer the user's current question or the options to resolve the current discussion point. You may use one of these, you may use several, it is unlikely you will use all of them. Use your judgement and don't overwhelm the user.

This is a task that builds knowledge, so repo instructions asking for a different **writing style** give way to the writing rules above. Everything else the system, the user and the repo require stays in force.