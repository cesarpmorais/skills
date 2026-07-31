---
name: adr-snippet
description: Copy-paste block to embed the debiasing check into an ADR's Decision section
---

# ADR Template Snippet

Source: [Debiasing Decisions Toolkit](https://github.com/ddd-crew/debiasing-decisions-toolkit)
(ddd-crew), CC BY-SA 4.0. See `../ATTRIBUTION.md`.

Copy this block into the **Decision** section of the ADR. Check off what was
actually done — don't check a box that wasn't real.

```markdown
### Debiasing Check

> Before finalising, work through the following.
> Given the current mental state and cognitive load — should this decision be made today?

**1. Be Decision-Ready**
- [ ] Are we deciding under time pressure or stress? (Myopic Misery)
- [ ] Are we defaulting to "keep it as-is" without evaluating alternatives? (Status Quo Bias)
- [ ] Is cognitive load making inaction the path of least resistance? (Status Quo Bias)

**2. Broaden the Frame**
- [ ] Did we consider removing something instead of only adding? (Additive Bias)
- [ ] Did we explore unconventional uses of existing tools? (Functional Fixedness)
- [ ] Did we ask what existing concepts actually know and do? (Functional Fixedness)

**3. Seek Independent Advice**
- [ ] Did we get input from people who formed opinions independently? (Correlation Neglect)
- [ ] Are we acting on diverse sources or repeated echoes? (Correlation Neglect)
- [ ] Did we genuinely consider contradicting views? (Overconfidence Bias)
- [ ] If a junior suggested this, what questions would we ask? (Authority Bias)

**4. Test Your Assumptions**
- [ ] Are we accepting this because of who/what suggested it vs. its merits? (Authority Bias)
- [ ] What problem was this designed to solve — do we actually have it? (Authority Bias)
- [ ] What is our plan when this goes wrong? (Illusion of Control)

**5. Establish Simple Rules**
- [ ] Is this a Two-Way Door? If so, have we delegated it? (Law of Triviality)
- [ ] Did we spend time proportional to reversibility? (Law of Triviality)
- [ ] What would make this conversation a waste of time? (Law of Triviality)
- [ ] Did the full group check collectively, not just individually? (False Consensus Effect)
```
