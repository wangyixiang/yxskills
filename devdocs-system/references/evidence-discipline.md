# Evidence discipline

The failure mode this file exists to prevent: **a confident, plausible, wrong
number.** It survives review because everyone believes it, and it surfaces
months later as a spec violation that nobody can trace. Everything below is
aimed at that.

## 1. Two sources, both required

| Source | Gives you | Fails at |
| --- | --- | --- |
| Exploration agents (fanned out) | breadth, "where is this", absence claims | precise numbers, exact orderings |
| Your own reading of the source | precision on load-bearing facts | finding things you did not think to look for |

Use both. Never write a document from agent summaries alone.

**What you must read yourself, not delegate:**

- every number you will state (limits, timeouts, counts, sizes);
- every claim of the form "already done" or "impossible today";
- every ordering that is semantically load-bearing (e.g. "idempotency is checked
  *before* lease expiry" — the order is the behaviour);
- the exact wording of any frozen clause you are about to characterise.

## 2. Absence claims are the highest-value output

"This concept does not exist anywhere" is the strongest thing a gap analysis can
say, and the easiest to get wrong — a single differently-named field invalidates
it.

How to make absence claims safe:

1. Search for the **concept**, not the word. A "solved/unsolved verdict" can hide
   behind `outcome`, `resolution`, `verdict`, `closed_reason`, `effectiveness`,
   `workaround`.
2. Report near-misses explicitly and explain why they are not the thing. Example:
   `unresolved_items` is not a resolution verdict — it counts executions missing
   an accepted result, which is an evidence-completeness problem.
3. State the search performed so a reviewer can repeat it.
4. Give the absence a boundary: *"not merely unimplemented — there is no column,
   enum, endpoint, or UI action to attach such a judgement to."*

## 3. Evidence levels

Tag what backs each acceptance claim. Use whatever numbering you like; what
matters is that a reader can tell a test from a sentence.

| Level | Meaning | May be used as |
| --- | --- | --- |
| **E1** automated assertion | repeatable assertion in CI | acceptance evidence |
| **E2** measured script | script run against a real deployment, machine-readable output | acceptance evidence |
| **E3** human verification record | a person operated the real thing and recorded it, with reproduction steps | acceptance evidence, if second-person reviewable |
| **E4** statement | prose only | **not** acceptance evidence |

Rule: any acceptance conclusion cites E1–E3 and names the evidence path plus the
generation time, bound to a specific commit.

## 4. Claim calibration

The same underlying fact supports very different sentences. Pick the one your
evidence actually supports.

| What you verified | You MAY write | You may NOT write |
| --- | --- | --- |
| Unit tests pass | "unit tests pass" | "the feature works" |
| Ran on this machine | "validated on `<machine>`" | "validated" |
| Ran in a container | "validated in a container" | "validated on the target platform" |
| Stub/fixture returned correctly | "the flow branches correctly" | "the integration works" |
| Two agents ran locally | "two agents ran on one machine" | "cross-machine validated" |
| Docs say X is required | "the contract requires X" | "X is implemented" |
| Code reads X | "the code reads X" | "X behaves correctly under load" |

**Write the not-covered part into the record.** A `limitations` field that is
empty is a red flag, not a clean bill of health.

## 5. Status vocabulary

Define these in the index and use them with exactly one meaning.

| Status | Means | Does NOT mean |
| --- | --- | --- |
| `已完成` / done | implemented and covered by the required tests | shipped |
| `部分` / partial | the mechanism exists but the product surface or a precondition is missing | "mostly fine" |
| `缺失` / missing | the concept does not exist anywhere (verified by search) | "we haven't looked" |
| `原型` / prototype | works for its original validation purpose only | safe to build on |
| **`范围反转` / reversal** | a previously **explicit exclusion** is now requested | unfinished work |

The last one is the most consequential. Never file a reversal as a bug:

> ❌ "Missing: RAG / external knowledge base."
>
> ✅ "Explicitly excluded in v1.2 §27 and v1.5 §13, with a stated reason
> ('small knowledge volume; exact revision references are sufficient; retrieval
> would break traceability'). This target reverses that decision. The stated
> reason needs an explicit answer — the reason only holds when retrieved content
> is not frozen; freeze it and both properties hold."

The second version tells a reviewer that a **decision** is required, and gives
them the reasoning they need to make it. The first looks like a task.

## 6. Verifying a "reversal" claim

Before calling something a reversal, find and quote the original exclusion. Then
re-read it for scope: exclusions are often narrower than they read.

Worked example: "no RAG" was written as *retrieval would break traceability*.
That is a conditional objection, not a flat prohibition — it fails only if
retrieved results are not pinned. Retrieval at selection time plus freezing the
selected revision into the existing snapshot mechanism satisfies both. Reporting
it as "RAG is excluded" would have hidden a viable design.

So: **quote the clause, then test whether its stated reason actually applies.**

## 7. How to disagree with the user's target

You are expected to push back when the target is incomplete or contradictory.
Do it with structure, not assertion:

1. **Restate their intent** in a line, so it is clear you heard it.
2. **Name the specific gap**, with the consequence: *"the loop has no failure
   exit; without one it can't converge, and the knowledge base will only ever
   receive successes — survivorship bias."*
3. **Offer options**, including one they may not have considered.
4. **Recommend one**, with the reason.
5. **Make it decidable** — an `OD-*` entry, not a debate.

What not to do:

- Silently designing around the problem (they will not learn it existed).
- Refusing to recommend ("it depends") — that pushes your work back onto them.
- Over-engineering the fix in a way that inflates the ask. If the user says "just
  solved or not solved", a five-value enum is you showing off, not serving them.

Expect correction and take it cheaply. Real examples from the run this skill came
from: an enum was cut to two values; a cross-machine pairing design was deleted
outright once the user pointed out the browser and the agent are on the same
machine. Both were improvements, and both were visible only because the design
was written down where a human could see it.

## 8. What to do with what you cannot verify

Not everything can be resolved during documentation. Do not guess, and do not
bury it in a modifier like "likely".

Route it to one of three places:

| Situation | Goes to |
| --- | --- |
| Needs a person's decision | open decision (`OD-*`) with options + recommendation |
| Needs the real environment | measured-not-assumed list, with a verification method |
| Needs work but is low confidence | risk register, with a trigger condition |

Every one of these keeps the uncertainty **visible and owned**. "We think this
works" is the only outcome that is never acceptable.
