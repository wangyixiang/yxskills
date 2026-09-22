# Doc set template

The shape of a full set, the minimum viable subset, and the section templates
worth reusing verbatim.

## 1. Set shape

A complete set for a multi-service product with frozen contracts. Fold away the
rows that the project does not earn.

| # | Document | Type | Answers |
| --- | --- | --- | --- |
| — | `README.md` | index | how to read this, how to maintain it |
| 00 | assessment | evaluation | what exists now, how real is it, where is the debt |
| 01 | PRD / requirements | requirements | what to build, for whom, what NOT to build |
| 02 | scenarios & use cases | requirements | who does what, in what order, with what permissions |
| 03 | target architecture | spec | how the system is structured |
| 04 | domain model & contracts | spec | entities, invariants, version rules |
| 05 | database design | spec | tables, constraints, migrations, retention |
| 06 | API / interface contract | spec | conventions, error model, compatibility |
| 07 | state machines & workflows | spec | states, transitions, concurrency, recovery |
| 08 | component spec (e.g. the edge agent) | spec | that component's design in depth |
| 09 | security & authorization | spec | threat model, trust chain, matrices, egress |
| 10 | UI / interaction | spec | information architecture, gates, error states |
| 11 | observability & operations | spec | logs, metrics, health, runbooks |
| 12 | test & acceptance strategy | engineering | what is tested how, gates, evidence |
| 13 | engineering standards | engineering | conventions, structure rules, review flow |
| 14 | change / refactor plan | delivery | gaps → workstreams → phases → rollback |
| 15 | milestones & roadmap | delivery | checkpoints, deliverables, exit criteria |
| 16 | risk register & open questions | delivery | risks, defects, undecided items |
| 17 | ADRs | decision | what we decided, why, and what we rejected |
| 18 | traceability matrix | reference | requirement ↔ state ↔ spec ↔ test ↔ milestone |
| 19 | glossary | reference | terms and where they live in code |
| 20 | doc governance | process | layers, ownership, sync, deprecation |
| 21 | evolution / version history | history | how the design changed and why; what was lost |
| 22 | target gap analysis | evaluation | target vs current, conflicts, open decisions |

**Minimum viable set (4):** index with an axis statement, assessment,
requirements-or-design, governance. Stop there unless the project earns more.

**Earn the set size.** Each document should be able to answer "what breaks if
this document didn't exist?" If nothing, delete it. Padding reads as diligence
and costs review time.

## 2. Index (`README.md`)

The index does five jobs. All five are necessary.

````markdown
# devdocs：<project> 开发与改造文档中心

| 项目 | 内容 |
| --- | --- |
| 适用仓库 | `<repo>` (package name) |
| 文档基线 | code commit `<sha>` |
| 建立日期 | YYYY-MM-DD |
| 文档状态 | 初版，待评审冻结 |

## 0. 这套文档解决什么问题

**轴声明 / axis statement** — what question this set answers that the existing
docs do not. Name the existing docs and their axis, then name this one.

| 目录 | 定位 | 时间性 |
| --- | --- | --- |
| `docs/source/` | 历史方案与规范性契约 | 已冻结，只读 |
| `devdocs/` | 产品、规格、工程与交付文档（活文档） | 随改造迭代 |

## 1. 阅读路径

### 路径 A ── 只想快速知道"现状与目标"
1. [assessment] — 代码级事实
2. [PRD] — 范围与功能需求
3. [architecture] — 目标态分层
4. [refactor plan] — 差距 → 工作流 → 阶段
5. [roadmap] — 里程碑与退出标准

### 路径 B ── 要动手改某个模块
### 路径 C ── 要评估风险与排期
### 路径 D ── 新人上手

> One path per real role. A path that nobody would actually follow is noise.

## 2. 文档地图
| 编号 | 文档 | 类型 | 回答的问题 |

## 3. 标识符约定
| 前缀 | 含义 | 定义位置 |     ← prefix registry
**已占用、不得复用的短前缀**            ← occupied prefix table

## 4. 状态与优先级标记
| `P0` | 阻塞级 … |  / `P1` / `P2`
| `已完成` / `部分` / `缺失` (define these!)

## 5. 文档维护规则（摘要）
1. 规格与代码同提交。
2. 数字只有一处来源。
3. 不改历史。
````

## 3. Per-document header block

Every document opens with the same table. It makes status and provenance
greppable.

```markdown
# NN · <标题>

| 项目 | 内容 |
| --- | --- |
| 文档版本 | v1.0 |
| 状态 | 草稿 / 待评审 / 已冻结 |
| 上游 | <what this depends on> |
| 相关 | [NN doc](file.md)（why it is related） |
| 作用 | <one sentence: what this doc is for> |
```

Then, near the top, both halves of the boundary:

```markdown
## 范围
…
## 明确不做 / 不在本文范围
…
```

A doc with no "not in this document" line will slowly absorb everything.

## 4. Section templates

### 4.1 Gap register row

```markdown
### TGAP-10 · <short name>

| 项 | 内容 |
| --- | --- |
| **缺口** | what is missing, in one sentence |
| **影响** | what goes wrong if it stays missing |
| **现状证据** | `path/file.py:120` — quote the actual mechanism |
| **改造性质** | 新增 / 扩展 / **范围反转** (say which — the third one needs a decision) |
| **要建什么** | ① … ② … ③ … |
```

The `改造性质` row is the one reviewers skip and shouldn't. "New capability" and
"reversal of a frozen decision" have completely different approval paths.

### 4.2 Conflict analysis entry

Use when the target contradicts something already decided.

```markdown
### CF-7 · <target> vs <frozen decision>

| 项 | 内容 |
| --- | --- |
| **冲突点** | the two things that cannot both be true |
| **为什么不能默默改** | which frozen clause is affected, quoted |
| **事实** | code/docs evidence for the current state |
| **取舍** | option ① … option ② … |
| **推荐** | which, and the reasoning |
| **要补的语义** | what must be defined for the recommendation to work |
```

Always include the quote of the frozen clause. It converts "I think this is
risky" into "v1.2 §17.3 says recovery is safe *because* actions are read-only",
which is a claim a reviewer can check.

### 4.3 Open decision

```markdown
### OD-04 · <question>

| 项 | 内容 |
| --- | --- |
| **要定什么** | the decision, narrowly |
| **选项 A / B** | with the consequence of each |
| **推荐** | your recommendation + why (including why not the others) |
| **影响面** | which docs/specs/milestones change |
```

Never leave this as a question with no recommendation. The user decides; you
narrow the decision to something decidable.

### 4.4 Measured-not-assumed list

For anything that cannot be known without touching the real environment.

```markdown
| # | 待实测项 | 为什么不能假设 | 验证方式 | 影响 |
| --- | --- | --- | --- | --- |
| M3 | external KB version history retrieval | decides whether we must keep a local copy | update an entry, fetch the old version | CF-3 |
```

This table exists because "should work" becomes "works" in the retelling. Every
row names a **verification method**, not just a question.

### 4.5 Evidence manifest

```json
{
  "commit": "<git sha>",
  "environment": { "machine": "…", "os": "…", "platform": "native|container" },
  "executor": "…",
  "started_at": "<UTC ISO 8601>",
  "conclusion": "pass|fail",
  "scope": ["what this run actually covered"],
  "limitations": ["what it did NOT cover — required, must not be empty"],
  "artifacts": ["raw/…"]
}
```

`limitations` is mandatory. It exists because "validated locally" gets read as
"validated" and the difference has bitten every project once.

### 4.6 Traceability matrix

One row per requirement, columns for state → spec → milestone → test → related
IDs. Cheap to keep, and the only mechanical proof that nothing was dropped.

```markdown
| 需求 | 现状 | 规格 | 里程碑 | 验收 | 债/风险 |
| --- | --- | --- | --- | --- | --- |
| FR-4.2 结构化抽取不虚构 | 可用（未接真实模型） | [07 §3] | M4 | 人工核对 + E2E | RISK-14 |
```

### 4.7 Governance doc contents

Doc layers and which are read-only; who updates what when; the sync rule
(spec changes ship with the code change); ID allocation authority; evidence
format; deprecation; a short "start here" checklist.

## 5. Writing order

```
index (forces the shape)
  → assessment (grounds everything)
    → requirements (what for)
      → architecture / domain (how organised)
        → specs (detail per area)
          → engineering (how we work)
            → delivery (plan, milestones, risk)
              → reference (ADR, traceability, glossary, governance)
                → history + gap analysis (last: they cite everything above)
```

The history and gap docs come last deliberately: both are cross-cutting and
read better once every detail document exists.
