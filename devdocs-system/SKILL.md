---
name: devdocs-system
description: Build or maintain a grounded, cross-linked development documentation system (PRD, specs, architecture, engineering standards, delivery plan) for an existing codebase. Use whenever the user asks for a PRD, spec, design doc, architecture doc, refactor plan, roadmap, or asks "这个项目缺什么 / what's missing", "把项目文档写下来", "建立文档体系", "写文档" — even if they never say the word "documentation". Also use when extending an existing doc set, when docs and code have drifted, or when a target product direction must be checked against frozen design decisions.
---

# Building a devdocs system

This skill produces a **numbered, cross-linked documentation set** for an existing
codebase: an index with role-based reading paths, a requirements doc, specs,
engineering standards, a delivery plan, and the reference docs that keep it
maintainable — plus a validator that proves the set is internally consistent.

The defining property is **grounding**: every non-obvious claim carries a
`file:line` citation or an explicit "unverified" marker. A doc set written from
plausible-sounding summaries is worse than no doc set, because reviewers act on
it.

## When this is the right tool

- "Write a PRD / spec / design doc for this project."
- "Analyse what this project is missing" / "现状和目标的差距" / "缺了什么".
- "Turn this plan / refactor / target product into proper documents."
- Extending an existing doc set, or finding that docs disagree with code.
- A target product direction has appeared and must be checked against decisions
  that were frozen earlier.

## When it is NOT the right tool

- A single README, CHANGELOG, API reference, or user manual → just write it.
- Pure code comprehension with no document deliverable → that is a
  knowledge-graph / exploration task, a different artifact.
- No access to the code → grounding is the whole value here; without source you
  are writing generic prose that will read as authoritative and be wrong.

---

## The pipeline

### Phase 0 — Find the axis

Read the existing docs **before** writing anything. The question to answer:
**what question do the existing docs not answer?**

Common findings:

| Existing docs are… | The missing axis is usually… |
| --- | --- |
| A changelog of batches/commits | "What is true now" as a stable fact list |
| Frozen contracts / historical plans | "What should it become" and "how do we get there" |
| Scattered per-module notes | Cross-cutting: requirements ↔ tests ↔ milestones |
| Aimed at a completed phase | The product beyond that phase |

Decide two things and write them down:

1. The **axis statement** — one sentence, in the index: what this set answers
   that the existing docs do not.
2. **Where new docs live, and what stays read-only.** Never rewrite frozen or
   historical documents. Put living docs in a new directory and register
   discrepancies as findings instead of editing history.

### Phase 1 — Ground in code

Two sources, both required.

**1a. Parallel exploration agents, fanned out by subsystem.** Each prompt must be
self-contained and must:

- name the exact files or directories to read;
- demand `file:line` for every claim;
- impose a report length budget (a number of words) so you get density, not dumps;
- ask for absence explicitly: *"state the exact scenario where X breaks or confirm
  it does not exist"*. **Absence claims are the highest-value output and the
  easiest to get wrong.**

A good agent prompt names what *not* to do as well: no full code dumps, no
speculation about intent.

**1b. Verify load-bearing facts yourself.** Numbers, limits, orderings,
cardinalities, and anything you will phrase as "already done" or "impossible
today" — read them at the source. Agents paraphrase; a paraphrased constant
becomes a confidently wrong spec.

**Anti-pattern:** writing docs from agent summaries alone. It is fast and it
produces numbers that are subtly wrong, which is the worst failure mode for a
spec.

### Phase 2 — Design the identifier system before writing prose

This is what makes the set maintainable instead of a pile of essays. Detail in
`references/identifier-scheme.md`. The short version:

- Each **axis** gets its own prefix family. Do not mix two questions in one series.
- **Register every prefix in the index before first use.**
- Keep an **occupied-prefix table** for short tokens already spoken for, so a new
  family cannot silently collide.
- Pick **one owner document per fact family**; other docs cite the ID and never
  restate the value. Numbers especially: one doc owns the limits, everyone else
  cites `LIM-xx`.

### Phase 3 — Write in dependency order

```
index  →  assessment  →  requirements  →  architecture  →  specs
       →  engineering  →  delivery  →  reference (glossary, traceability, decisions)
```

Writing the index first forces you to commit to the shape. Later docs cite
earlier ones, so this order minimises backtracking.

Per-document conventions (templates in `references/doc-set-template.md`):

- a header block: version, status, upstream, one-line purpose;
- an explicit **scope** section *and* a "not in this document" line;
- numbered change/finding lists with IDs, not prose paragraphs;
- a verification or acceptance section.

### Phase 4 — The three docs that make it survive

| Doc | Job |
| --- | --- |
| **Governance** | Doc layers, who updates what when, templates, deprecation, evidence format |
| **Evolution / history** | How the design changed across versions and **why**; where information was lost |
| **Gap analysis** | Target vs current, conflicts with frozen decisions, open decisions, and what must be **measured rather than assumed** |

The gap doc is where you are allowed to disagree with the user's stated target —
with evidence and recommended options, never with bare assertions. See
`references/evidence-discipline.md` for how to phrase that.

### Phase 5 — Validate, then stop

Run `scripts/check_docs.py <docs-dir>`. It checks internal links and dangling
identifier references, and prints the family inventory. Fix everything before
declaring the set done.

A dangling reference usually means one of two things: a real typo/inconsistency,
**or a prefix collision** — the same token meaning two different things in two
docs. Both are worth fixing immediately, and neither is visible by reading.

Add a `docids.json` in the docs dir so the check is one command with no arguments.

### Phase 6 — Backfill discipline

When you discover something later:

1. allocate the ID,
2. register the prefix if it is new,
3. add the entry in its **owner** doc,
4. cross-reference from the docs that led you there.

A finding that lives only in the document where it was discovered will be lost.
Findings discovered while writing doc 22 that belong to doc 00 and doc 16 must
be written into 00 and 16.

---

## Rules that matter, and why

1. **Separate the axes.** "Implementation vs frozen contract" and "target vs
   current" are different questions with different owners and different
   consequences. Merging them produces entries nobody can act on. Give each axis
   its own prefix and keep the axes from borrowing each other's tokens.

2. **Mark scope reversals as reversals.** When a target contradicts something
   that was *explicitly excluded* earlier, say so in those words: "this is not
   unfinished work, it is a deliberate decision being reversed." Framing it as a
   bug list hides the fact that **a decision must be made**, and reviewers will
   under-weight it.

3. **Never claim verification you do not have.** Grade evidence and say which
   grade you have (see `references/evidence-discipline.md`). Machine-local
   validation ≠ cross-machine; container ≠ native; a stub response ≠ a real
   integration; unit tests passing ≠ end-to-end works.

4. **One owner per fact family.** Limits, enums, state names, cardinalities. If a
   value appears in two docs, one of them will drift.

5. **Every doc set needs an explicit "what we will NOT do".** Without it, scope
   creeps silently and nobody notices the boundary moved.

6. **Prefer ID'd tables over prose.** Tables are reviewable, traceable, and
   machine-checkable; prose paragraphs are none of those.

7. **Do not invent the user's preferences.** When a decision is genuinely theirs,
   write it as an **open decision**: the options, the impact of each, and your
   recommendation with reasoning. Silently picking is the failure here — and so
   is refusing to recommend.

8. **Record "why not" as well as "why".** Rejected alternatives with the reason
   are the most valuable content six months later, and the first thing lost.

9. **Calibrate the set size to the project.** A 20+ document set is right for a
   multi-service product with frozen contracts; it is waste for a small library.
   Minimum viable set is four: index (with the axis statement), assessment,
   requirements-or-design, governance. Everything else is earned by complexity.
   Do not pad to look thorough.

---

## Bundled files

| File | Read it when |
| --- | --- |
| `references/identifier-scheme.md` | Phase 2 — designing prefixes, registries, collision handling |
| `references/doc-set-template.md` | Phase 3/4 — doc-set shape and section templates |
| `references/evidence-discipline.md` | Whenever you write a claim, a status, or an acceptance record |
| `scripts/check_docs.py` | Phase 5 — validate links, identifiers, family inventory |

## A worked instance

The pattern this skill was extracted from: a two-package product (central service +
edge agent) with frozen interface contracts, where the existing docs were a
55-batch implementation log and a set of frozen v1.x plans.

The set that resulted: 22 numbered docs + index — assessment with a debt register,
PRD, scenarios, target architecture, domain model, DB/API/state-machine specs,
security, UI, observability, test strategy, engineering standards, refactor plan,
milestones, risk register, ADRs, traceability matrix, glossary, doc governance,
a version-evolution history, and a target-gap analysis. The gap analysis is the
one that changed the plan: it found the target loop was ~70% already supported,
that the missing parts were product semantics rather than plumbing, and that one
requested capability (device writes) **contradicted a frozen decision** and
therefore needed a decision, not a task.

Two habits from that run are worth copying directly: many small ID'd rows instead
of paragraphs, and running the validator after every batch of edits — it caught a
two-digit/three-digit reference mismatch (`ADR-02` vs `ADR-002`) that ten minutes
of reading had missed.
