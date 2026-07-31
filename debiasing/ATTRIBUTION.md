# Attribution

This skill vendors content from the
[Debiasing Decisions Toolkit](https://github.com/ddd-crew/debiasing-decisions-toolkit)
by **Evelyn van Kelle**, **Gien Verschatse**, and **Kenny Baas-Schwegler**,
co-authors of [Collaborative Software Design](https://collaborative-software-design.com)
(Manning, 2024).

Licensed under
[Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

## Scope

This license applies **only to this `debiasing/` directory** — specifically
`references/checklist.md`, `references/biases.md`, and `references/adr-snippet.md`,
which preserve the toolkit's original question wording, bias table, and ADR
template almost verbatim. The rest of this repo remains MIT.

## What was adapted

- Reorganized from a standalone README into an agent skill (`SKILL.md` +
  `references/`) that an AI coding agent loads on demand.
- Added a reversibility-based triage (`SKILL.md`, "Scope the check to
  reversibility") that decides how much of the checklist to run per decision —
  not part of the original toolkit, but built directly on its own Step 5
  principle ("spend time proportional to how hard this decision is to reverse").
- Adapted from team facilitation ("work through the checklist as a team") to
  individual use with an AI agent, including an explicit note (`SKILL.md`,
  "Being honest about what an agent can and can't do here") that the agent's own
  output does not count as independent advice — a gap the original toolkit
  doesn't need to address since it assumes a human team.

Per CC BY-SA 4.0, this derivative work is distributed under the same license.
