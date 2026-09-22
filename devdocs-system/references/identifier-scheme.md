# Identifier scheme

A devdocs set lives or dies on its identifiers. They are what turns twenty
documents into one reviewable object: a finding gets a name, every doc that
touches it cites that name, and a script can prove nothing dangles.

## 1. Allocate by axis, not by document

An **axis** is a question type. Different questions get different prefix
families, and one family never carries two meanings.

| Axis (question) | Example family | Owner doc |
| --- | --- | --- |
| What must the product do? | `FR-*`, `NFR-*` | PRD |
| Who does what, in what order? | `SC-*`, `UC-*` | scenarios doc |
| What is true in the code right now that shouldn't be? | `DEBT-*` | assessment |
| Where does the implementation disagree with a frozen contract? | `GAP-*` | assessment |
| What does the target need and the current system lack? | `TGAP-*` | gap analysis |
| Where does the target contradict a frozen decision? | `CF-*` | gap analysis |
| What has not been decided yet? | `OD-*` / `OQ-*` | gap analysis / risk register |
| What could go wrong? | `RISK-*` | risk register |
| What is known broken? | `DEF-*` | risk register |
| What did we decide, and why? | `ADR-*` | decision record |
| What package of work? | `W*` | refactor plan |
| What checkpoint? | `M*` | roadmap |
| What is the hard numeric limit? | `LIM-*` | **one** spec doc, nowhere else |

**The test for a new family:** can you fill in the sentence "`XX-nn` is a
___"? If the blank is fuzzy ("some issue"), you are about to create a family
nobody can use.

**Do not reuse a family for a nearby question.** `GAP-` (implementation vs
contract) and `TGAP-` (target vs current) look similar and are genuinely
different: the first says "fix this", the second says "decide whether to build
this". Merging them lets a decision item hide inside a bug list.

## 2. Format rules

- Shape: `PREFIX-NNN`, or `PREFIX-N.N` for hierarchical families
  (`FR-9.11`, `NFR-P.6`).
- **Be consistent about zero-padding inside a family.** This is not cosmetic:
  a set that defines `ADR-002` but cites `ADR-02` produces references a reviewer
  will read as valid and a validator will flag as dangling. Pick one width and
  hold it across the whole set.
- Prefix: 2–8 uppercase letters, no lowercase, no digits.
- Never encode meaning in the number beyond grouping (`FR-1.*` = the identity
  group). Ordering by number is a feature; making the number a checksum is not.
- Single-letter families (`W*`, `M*`, `C*`) are convenient and dangerous — see
  the collision rule below. If you use one, keep the numbers short and reserve
  the letter explicitly.

## 3. Keep a registry, and keep it honest

The index carries two tables. Both are load-bearing.

**Table A — prefix registry.** Every family, what it means, and which doc owns
it. Nothing enters a document that is not in this table.

```markdown
| Prefix | Meaning | Owner doc |
| --- | --- | --- |
| `DEBT-<n>` | Technical debt | assessment §4 |
| `TGAP-<n>` | Target capability gap | gap analysis §4 |
```

**Table B — occupied prefixes.** Short tokens already spoken for, including ones
that are *not* identifier families. This is what stops a future author from
re-inventing a collision.

```markdown
| Prefix | Already used by | Note |
| --- | --- | --- |
| `C0`–`C4` | data-classification levels in the security/domain docs | `C0 public … C4 credentials`. |
|   |   | Therefore the conflict family uses `CF-`, not `C1`. |
| `C0`–`C6`, `E0`–`E16`, `G1`–`G8` | historical task numbering in archived plans | not used for live work |
```

### The collision, in full (a real one)

`C1` was used for two things at once: a data-classification level
(`C1 internal`) and the first "principle conflict" (`C1 · session identity vs
audit attribution`). Both read perfectly well inside their own document. The
problem only surfaced when a validator asked "is every referenced `C1` defined?"
— and the answer depended on which meaning you had in mind.

Resolution: the **older allocation wins**. Data classification kept `C0–C4`;
the conflict family was renamed `CF-1…CF-9` across every doc that cited it, and
the collision was written into Table B so it cannot recur.

Two generalisable lessons:

1. **The older allocation wins**, because renaming it invalidates more history.
2. **Dangling-reference checking is collision detection.** You do not need a
   special tool; a validator that flags undefined references surfaces the same
   signal, because a token used with two meanings is undefined for one of them.

## 4. One owner per fact family

Pick the single document that owns each *value*, and make every other document
cite the ID.

- **Numbers** (size caps, timeouts, retry counts) get a `LIM-*` family owned by
  one spec doc. Other docs write "see `LIM-36`" — never the number.
  Why: a number copied into five documents is five chances to drift, and the one
  that drifts is always the one a reader trusts.
- **Enums and state names** belong to the domain-model doc. Specs cite them.
- **The permission matrix** belongs to one doc; security and scenario docs point
  at it.

Rule of thumb: **if you are about to type a digit that also appears elsewhere,
you are about to create a drift site.**

## 5. Placeholder forms

Registry tables need to show shapes, not instances: `DEBT-xx`, `FR-x`,
`ADR-0xx`. Mark them so tooling ignores them, and treat any of these as
placeholders:

```
PREFIX-x      PREFIX-xx      PREFIX-xxx      PREFIX-0xx
```

The bundled validator ignores them automatically. If you write your own,
reproduce that behaviour, or your registry table will report as a page of
dangling references.

## 6. Referencing across documents

- Always pair the ID with a link: `[04 §7](04-domain-model.md)` or
  `**`TGAP-10`** in [22](22-gap-analysis.md) §4`.
- Include the section, not just the file. Files get reorganised; sections are
  what a reviewer actually needs.
- When you cite an ID, cite the *owner's* ID, not a paraphrase of it. "the write
  capability gap" is unsearchable; `TGAP-10` is not.

## 7. Deprecation

Never delete or renumber. Mark it:

```markdown
| `DEBT-12` | [已消除 @M2] merged into `DEBT-19` | ... |
```

Renumbering breaks every historical citation and every commit message that
mentioned the old number. A tombstone row costs one line and preserves the
trail — which is the whole point of having identifiers.

## 8. A minimal viable scheme

If the project is small, four families carry most of the value:

```
FR-*      what the product must do
DEBT-*    what is wrong right now
RISK-*    what could go wrong
ADR-*     what we decided and why
```

Add `TGAP-*` / `CF-*` / `OD-*` the moment a *target* distinct from the current
contract appears — that is the point where "what we have" and "what we want"
start needing different vocabularies.
