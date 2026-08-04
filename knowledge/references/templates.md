# Note templates

Shapes, not rigid forms. Drop sections that would be empty — an empty heading is worse
than no heading. Property names must stay consistent across notes, since Bases views
query them.

## LeetCode problem

Lives in `leetcode/problems/`. Filename: `<number>. <Title>.md` (e.g.
`3. Longest Substring Without Repeating Characters.md`) so it sorts and searches the way
the site does.

Built for **re-practice**: statement and the user's own insight stay visible; solution
and complexity are collapsed so the problem can be re-attempted months later.

```markdown
---
tags:
  - leetcode
difficulty: medium
pattern: "[[Sliding Window]]"
source: https://leetcode.com/problems/longest-substring-without-repeating-characters/
solved_on: 2026-07-30
next_review: 2026-08-06
mastered: false
---

## Enunciado

One-paragraph restatement in the user's own words, plus the constraints that actually
drive the solution (input size, value ranges).

## Como reconheci

The tell — what in the problem signals this pattern. This is the part that transfers to
an unseen problem, so it matters more than the code.

> [!success]- Solução
> ```python
> # the solution the user actually wrote
> ```
> **Complexidade:** O(n) tempo, O(min(n, m)) espaço

> [!warning]- Onde eu tropecei
> Wrong turns, off-by-ones, the edge case that broke it. Skip this callout if the
> problem went cleanly.

## Relacionados

- [[Sliding Window]]
- [[438. Find All Anagrams in a String]]
```

## LeetCode pattern

Lives in `leetcode/patterns/`. Filename is the pattern name (`Sliding Window.md`). This
is both the teaching note and the MOC for its problems — it is where the transferable
learning accumulates.

```markdown
---
tags:
  - leetcode
  - pattern
---

## Quando usar

The recognition signals: what a problem looks like when this pattern applies.

## A ideia

The mechanic in a few lines — the invariant the pattern maintains and why it beats brute
force.

## Armadilhas

Where it commonly goes wrong.

## Problemas

- [[3. Longest Substring Without Repeating Characters]] — medium
- [[438. Find All Anagrams in a String]] — medium
```

## General knowledge note

Lives in its topic folder, or `inbox/` when no folder fits yet.

```markdown
---
tags:
  - <topic>
created: 2026-07-30
source: <url or conversation, when there is one>
---

## O que eu aprendi

The insight itself, stated so it makes sense with no memory of the conversation that
produced it.

## Por que importa

The situation this changes. Without this, a note is trivia.

## Relacionados

- [[Related note]]
```

## MOC (Map of Content)

One per topic folder, named after the topic (`LeetCode.md`). It is the curated entry
point — a reader's path through the folder, not a dump of every file. Keep the grouping
meaningful and update it whenever a note is added.

```markdown
---
tags:
  - moc
---

## Padrões

- [[Sliding Window]] — janela que cresce e encolhe sobre uma sequência
- [[Two Pointers]] — dois índices convergindo ou em velocidades diferentes

## Em progresso

- [[Backtracking]] — ainda não consolidado
```
