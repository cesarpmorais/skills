# Obsidian format rules

Rules verified against the official Obsidian docs (help.obsidian.md). The vault is
vanilla — no community plugins — so structure must come from properties and wikilinks,
both of which Obsidian indexes natively.

## Properties (YAML frontmatter)

Must be the **very first thing in the file**, delimited by `---`. Name and value are
separated by a colon **followed by a space**. Property names are unique per note.

```yaml
---
tags:
  - leetcode
  - arrays
difficulty: medium
solved_on: 2026-07-30
mastered: false
---
```

Seven supported types: **text**, **list**, **number**, **checkbox** (`true`/`false`),
**date** (`2026-07-30`), **date & time** (`2026-07-30T10:30:00`), and **tags**.

Three names Obsidian treats specially: `tags`, `aliases`, `cssclasses` — all list type.

### Gotchas that silently break things

- **A wikilink in a property must be quoted.** `pattern: "[[Sliding Window]]"` works;
  `pattern: [[Sliding Window]]` does not. Same inside lists:
  ```yaml
  related:
    - "[[Two Pointers]]"
    - "[[438. Find All Anagrams in a String]]"
  ```
- **No markdown inside properties.** Bold, code spans, and links-as-text will not
  render. Keep values atomic.
- **No nested properties.** Flatten instead (`review_next` rather than `review.next`).
- **Numbers must be literal** — no expressions.
- Tags in the `tags` property are written **without** the `#`.

## Internal links

- Basic: `[[Note name]]`
- In a folder: `[[leetcode/patterns/Sliding Window]]` — always forward slashes
- Custom display text: `[[Sliding Window|the sliding window pattern]]`
- To a heading: `[[Note#Heading]]`, subheading `[[Note#Heading#Subheading]]`
- To a block: `[[Note#^block-id]]`
- Embed (renders inline): `![[Note name]]`

Linking to a note that does not exist yet is normal and useful — Obsidian creates it at
that path when clicked. Prefer wikilinks over markdown links; they are the vault default.

## Callouts

Blockquote syntax with a type identifier. Adding `-` makes the callout **collapsed by
default**, `+` makes it expanded and foldable.

```markdown
> [!success]- Solução
> Collapsed until clicked — this is what keeps a problem re-practicable.

> [!warning]- Onde eu tropecei
> Also collapsed.

> [!tip] Insight
> No dash, so always visible.
```

Useful types here: `note`, `tip` (`hint`), `success` (`check`, `done`), `question`
(`help`, `faq`), `warning`, `failure`, `danger`, `bug`, `example`, `quote`.

Nest by adding another `>` level.

## What this vault does NOT have

No Dataview, no Templater, no spaced-repetition plugin. Do not write queries or syntax
that depend on them. Structured views come from **Bases** (a core plugin, enabled),
which reads the same properties defined above — which is exactly why property names must
stay consistent across notes.
