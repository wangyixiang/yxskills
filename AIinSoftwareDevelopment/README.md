# AI-Native 软件工程方法论

**如何把 AI 真正嵌入中大型项目的研发流程,而不是让它变成一个更快的破坏者**

---

## 核心论点

对于中大型软件项目,真正有效的方法不是"让 AI 帮我们写更多代码",而是把 AI 嵌入整个软件工程流程,参与：

**需求理解 → 系统设计 → 任务拆解 → 编码 → 测试 → Review → 集成 → 文档更新 → 后续演进**

一句话概括：

> **人负责目标、约束和关键决策；AI 负责理解、拆解、实现、验证和维护。**

需要先说明一点：Spec-driven development、ADR、CI 自动化门禁、任务拆解——这些构件本身都不是新发明,而是软件工程里已经存在十几年的成熟实践。这套方法论真正的价值,是**针对"AI 作为主要执行者"这个新变量,把这些构件重新组合成一套闭环**。它不是凭空创造出来的方法,而是一次面向 AI 时代的重构。这个区分很重要,因为它意味着大部分风险和边界条件其实是有先例可循的,不需要摸着石头过河。

对于中大型项目,**"文档 + Agent 指南 + Skills + 计划 + 测试"本身就是 AI 的开发基础设施**——这套基础设施的建设成本和维护成本,本文会在最后专门讨论,而不是假装它是免费的。

---

## 一、先纠正一个最常见的思路

很多人用 AI 开发项目是这样的：

```text
我：帮我实现 XXX
AI：写了一堆代码
我：这里不对，再改一下
AI：继续改
我：又坏了
AI：再修
...
```

小项目还撑得住。中大型项目很快会滑向：

```text
需求漂移 → AI 不知道整体架构 → 局部优化 → 破坏其他模块
    → 继续打补丁 → 代码越来越复杂 → AI 更难理解 → 重新开发
```

AI 会从"开发加速器"变成"代码混乱加速器"。真正重要的不是"怎么给 Coding Agent 更强的 Prompt",而是：

> **怎么建立一个让 AI 能持续正确工作的工程系统。**

---

## 二、五层控制模型

把项目理解成五个层次,越靠上人类控制越强,越靠下 AI 自动化程度越高：

```text
┌───────────────────────────────┐
│  Product / Business  为什么做  │
├───────────────────────────────┤
│  Requirements       必须做什么 │
├───────────────────────────────┤
│  Architecture      应该怎么构成 │
├───────────────────────────────┤
│  Implementation     具体怎么实现 │
├───────────────────────────────┤
│  Verification       怎么证明正确 │
└───────────────────────────────┘
```

| 层级 | 人类 | AI |
|---|---|---|
| 产品目标 | ★★★★★ | ★ |
| 核心需求 | ★★★★★ | ★★ |
| 架构原则 | ★★★★ | ★★★ |
| 模块设计 | ★★★ | ★★★★ |
| 具体实现 | ★★ | ★★★★★ |
| 测试生成 | ★★ | ★★★★★ |
| Bug 分析 | ★★ | ★★★★★ |
| 文档维护 | ★ | ★★★★★ |

**不要把"系统应该是什么"完全交给 Agent。** 这条原则会在后面的验证闭环一节里被具体化成一条可执行的合并门禁规则,而不只是一句口号。

---

## 三、建立 AI 能读懂的项目知识库

从零开发中大型项目,不该一上来就让 Agent 写代码。第一阶段应该是建立项目的 **Source of Truth**：

```text
project/
├── AGENTS.md
├── README.md
├── docs/
│   ├── PRODUCT.md
│   ├── REQUIREMENTS.md
│   ├── ARCHITECTURE.md
│   ├── DESIGN_PRINCIPLES.md
│   ├── specs/          （PROTOCOL_SPEC.md, WORKFLOW_SPEC.md, API_SPEC.md ...）
│   ├── adr/             （ADR-001-xxx.md ...）
│   └── guides/          （architecture-guide.md, backend-guide.md ...）
├── skills/
├── plans/
│   ├── roadmap.md
│   └── milestones/
├── work-items/
├── src/
├── tests/
└── scripts/
```

这个结构的意义不是"文档好看",而是在建立 **AI 的长期记忆和工作协议**。

---

## 四、三份文档,三种职责,不要混在一起

```text
AGENTS.md  →  告诉 Agent "如何工作"      （项目级工作规则）
SPEC       →  告诉 Agent "系统应该是什么" （实现与验收的契约）
PLAN       →  告诉 Agent "这次具体做什么" （当前任务范围）
```

`AGENTS.md` 应该回答：

```text
你是谁？正在开发什么系统？项目核心原则是什么？
目录结构是什么？哪些地方可以改，哪些不能改？
代码风格是什么？测试怎么跑？什么时候必须加测试？
架构边界是什么？如何提交代码？
什么情况下需要新增 ADR？什么情况下必须更新文档？
```

这三份文档混在一起，最常见的后果是：Agent 把"这次要做什么"的临时约束，误当成了"系统应该是什么"的永久规则，或者反过来，把一次性的任务范围写死进了项目级规则里，污染了以后所有任务的上下文。

---

## 五、Specification：实现与验收的契约

Specification 是中大型项目最关键的一层,它们不是普通说明文档,而应该成为：

> **实现与验收的契约。**

例如一个 Workflow Step 应该定义：

```text
Step 的目的 / 输入 / 输出 / 状态 / 生命周期
Step 的错误处理 / 重试规则
Step 的完成条件 / 失败条件
Step 与其他 Step 的关系
```

Agent 写代码时不应该被问：

> "你觉得这个 Step 应该怎么实现？"

而应该被要求：

> "按照 WORKFLOW_SPEC 中定义的行为实现这个 Step。"

这会极大降低 AI 的自由发挥空间——这也是为什么本文建议 Spec 要先于代码写出来,而不是等代码跑起来之后再补。

---

## 六、Architecture：显式的"禁止清单"

Specification 解决"系统需要表现成什么样",Architecture 解决"系统应该由什么构成"：

```text
                   ┌──────────────┐
                   │    Client    │
                   └──────┬───────┘
                          ▼
                ┌─────────────────┐
                │ Central          │
                │ Orchestrator     │
                └────────┬────────┘
             ┌───────────┼───────────┐
             ▼           ▼           ▼
         Context      Planner     Knowledge
         Engine       Engine       Engine
             └──────┬────┘
                    ▼
                 Executor
                    ▼
                  Edge
```

Architecture 文档应该说明组件是什么、为什么存在、如何通信、依赖关系、数据流、控制流、边界、扩展点、故障边界——但**最重要的是明确"禁止什么"**：

```text
Frontend MUST NOT access database directly.
Workflow Engine MUST NOT depend on UI.
Domain layer MUST NOT depend on infrastructure.
Edge MUST NOT make autonomous planning decisions.
```

对 AI 来说：

> **Negative constraints 往往比 Positive instructions 更重要。**

原因很直接：Agent 很容易"顺手"做出一个局部看起来完全合理、但破坏了整体架构的实现——它没有恶意,只是缺乏一个明确的边界告诉它"这条路不能走"。正面指令告诉 AI "该做什么",但中大型系统的复杂性大多来自"看似合理的例外",负面约束才是真正拦住这些例外的护栏。

---

## 七、从项目到 Work Item：不要让 Agent 处理"整个项目"

不要下发：

```text
Build the entire project.
```

而是逐层拆解：

```text
Project → Subsystem → Module → Feature → Work Item → Implementation Task
```

最后 Agent 接收到的任务应该长这样：

```text
Implement workflow step transition validation.

Read:
- WORKFLOW_SPEC.md
- architecture-guide.md
- current state implementation

Constraints:
- do not modify persistence layer
- preserve existing public API
- add unit tests, including invalid transition cases

Done when:
- ...
```

**真正的核心工作单位不是"Prompt",而是 Work Item。** 建议把每个任务标准化成一个目录：

```text
work-items/
└── WF-023-step-transition-validation/
    ├── TASK.md
    ├── CONTEXT.md
    ├── DESIGN.md
    ├── TEST_PLAN.md
    └── ACCEPTANCE.md
```

这样 Agent 面对的不再是"帮我把这个东西做出来",而是**一个可以验证的工程任务**。

---

## 八、Coding Agent 的角色分工,以及一个容易被忽视的风险

把 Coding Agent 的工作模式拆成几个不同职责（不要求真的创建五个独立 Agent 实例）：

```text
Planner → Architect → Implementer → Tester → Reviewer
```

* **Planner**：需求 → 任务拆解 → 实施计划
* **Architect**：架构影响、依赖、接口、数据流、边界
* **Implementer**：真正修改代码
* **Tester**：测试、边界情况、失败路径、回归验证
* **Reviewer**：是否满足 Spec、是否破坏架构、是否 scope creep、是否缺少测试

### 一个容易被忽视的风险：AI 互审的相关性问题

这个分工模型有一个结构性的弱点,原始版本的方法论没有讨论：**如果 Implementer 和 Reviewer 是同一个模型（甚至只是同系列的不同实例）,它们大概率共享相同的盲点。** 一个模型看不出自己犯的某类错误时,让"另一个自己"去审查,往往也看不出来——这不是提示词写得不够好的问题,而是相关性失败（correlated failure）的问题：两个高度相似的判断源在同一类错误上同时失灵的概率,远高于两个独立的判断源。

这意味着 AI Reviewer 不能被当作和人工 Review 等价的关卡,尤其是在下面这几类判断上：

* 是否真正符合 Spec 的**意图**,而不只是字面吻合
* 是否引入了架构层面的坏味道,而不是局部正确但整体不协调
* 是否存在"看起来测试通过,但测试本身没有覆盖到关键场景"这种自我欺骗式的验证

**实践建议**：AI Reviewer 适合做机械性、可枚举的检查（是否缺测试、是否改了 Out of Scope 的文件、是否符合命名规范）；涉及架构判断和 Spec 意图判断的审查,应该保留人工介入点,或者至少用不同厂商/不同代际的模型交叉审查,降低相关性。

---

## 九、验证闭环：代码只是流水线的一个阶段

传统开发常是 `Code → Done`。AI 开发应该是：

```text
Code → Build → Unit Test → Integration Test
     → Spec Verification → Architecture Review → Done
```

以及一道"自动验证门"：

```text
Agent → git diff → format → lint → type check
      → unit tests → integration tests
      → architecture checks → security checks → commit
```

Agent 不能自己宣布"完成了",而应该输出可核查的状态：

```text
Implementation Status: PASS
Tests: 124 passed
Architecture checks: PASS
Spec checks: PASS
Changed: 7 files
Unrelated changes: none
```

### 明确合并门禁：自动化检查通过 ≠ 可以自动合并

这里需要修正原始方法论里一个容易被忽视的矛盾：如果"人负责关键决策"是核心原则,那自动化检查全部 PASS 之后,不应该无条件直接走向 Merge——那样"人类决策"就没有真正的落点。建议把合并门禁明确拆成两条路径：

```text
Automated Checks PASS
        │
        ▼
   变更分类
   ├── 局部实现 / bug fix / 测试补全
   │        → 满足门禁即可自动合并
   │
   └── 涉及架构边界 / 核心数据模型 / 对外接口 / 安全策略
            → 无论自动检查是否 PASS，必须经过人工 Review 才能合并
```

这条分类规则本身应该写进 `ARCHITECTURE.md` 或 `AGENTS.md`,而不是留给每次 PR 临时判断——否则"人类控制关键决策"就只是一句没有执行机制的口号。

**Requirement → Test → Implementation 的顺序也值得强调**：把需求先转成可执行的测试用例,再让 Agent 实现,而不是反过来先写代码再想怎么测。这样测试成为 AI 的"第二个程序员"——第一个负责写,第二个负责验证。

---

## 十、AI 真正擅长什么,不该负责什么

AI 的优势并不主要在"写代码"，而在：

1. **理解大量上下文**：跨模块推理，人很难长期保持全局视野，AI 更适合。
2. **快速生成机械代码**：CRUD、DTO、序列化、校验、mocks、adapters、boilerplate。
3. **分析代码关系**：这个 API 谁在调用？这个状态在哪里被修改？某个字段还有哪些引用？
4. **Debug**：日志、堆栈、测试输出、diff、配置同时交给 AI 分析，是它最擅长的场景之一。
5. **维护文档**：代码变化 → 检测受影响的文档 → 更新 spec / guide / ADR（但这一点在第十四节会补充一个重要的前提）。

至少在项目早期，以下事项不应完全交给 AI：

```text
产品最终目标 / 核心业务规则 / 关键架构决策
安全边界 / 兼容性策略 / 核心数据模型
关键性能指标 / 重大技术选型 / 是否改变产品行为
```

AI 可以提出 Option A / B / C，但最终决策应该来自人，然后沉淀为 ADR，指导未来的 AI 行为。

---

## 十一、ADR：不只是怎么产生,还要有生命周期

ADR（Architecture Decision Record）是 AI 项目里非常有价值的制度记忆：

```text
ADR-007
Decision: Workflow state is persisted centrally.
Why: ...
Rejected alternatives: ...
Consequences: ...
```

几个月后再让 AI 改系统时，它不会问"为什么不直接放客户端"，因为 ADR 已经告诉它：**这是一条历史架构决策。**

### 补充：ADR 需要状态,而不只是存档

原始方法论只讲了 ADR 如何产生,没有讲 ADR 如何失效。这是一个真实的风险：如果某条决策后来被推翻，但对应的 ADR 没有被标记，AI 会把一份**已经不成立的历史决策**当作现在仍然有效的约束继续遵守——这比完全没有 ADR 更危险，因为它看起来权威可信。

建议给每条 ADR 加一个显式状态字段：

```text
Status: ACCEPTED | SUPERSEDED-BY-ADR-0XX | DEPRECATED
```

Agent 在读取 ADR 作为上下文时，应该只把 `ACCEPTED` 状态的决策当作当前有效约束；被取代或废弃的 ADR 仍然保留（作为历史记录和"为什么当初这样想"的参考），但不再具有约束力。

---

## 十二、Skill：某一类任务怎么做

如果说 SPEC 定义"系统必须做什么"、PLAN 定义"这次做什么"，那 Skill 定义的是：

> **某一类任务怎么做。**

```text
skills/
├── implement-api/
├── create-migration/
├── add-workflow-step/
├── debug-test/
├── refactor-module/
├── write-integration-test/
└── update-spec/
```

例如 `add-workflow-step` 可以固化成一个可重复的流程：

```text
Input: step requirement
Process:
1. inspect workflow spec
2. inspect state machine
3. identify extension point
4. update implementation
5. update tests
6. run workflow suite
7. update docs
```

四层分工至此完整：

```text
AGENTS.md = 项目怎么运作
Skill     = 一类任务怎么做
SPEC      = 系统必须做什么
PLAN      = 现在具体做什么
```

---

## 十三、Context Engineering：三级上下文

项目大到一定程度后，最大的问题往往不是"AI 不聪明"，而是 **Context 太多**。一个有 50 万行代码、3000 个源文件、200 篇文档、1000 个测试的项目，不可能每次都把整个仓库扔给 AI。

应该建立分级的、可组装的上下文，而不是"整个仓库"：

```text
                 ┌──────────────────┐
                 │ Project Context   │  AGENTS / Architecture / Principles
                 └────────┬─────────┘
                 ┌────────▼─────────┐
                 │ Module Context    │  module guide / interfaces / local rules
                 └────────┬─────────┘
                 ┌────────▼─────────┐
                 │ Task Context      │  task / spec / tests / relevant code
                 └──────────────────┘
```

例如一个任务 `WF-023` 的精确 Context Package：

```text
Global:   AGENTS.md
Architecture: workflow architecture
Spec:     WORKFLOW_SPEC.md
Module:   workflow/runtime/README.md
Task:     TASK.md
Relevant code:  state_machine.ts, transition.ts
Relevant tests: transition_test.ts
```

这是一个精确的 Context Package，比"一个超级 AGENTS.md"更可扩展。但这里有一个实际问题原始方法论没有回答：**这个 Package 是谁组装的？** 如果靠人工每次手动挑选文件，规模上不去；如果靠 Agent 自己检索，检索质量直接决定了上下文质量。可行的做法是把"识别相关模块 / 相关代码 / 相关测试"本身也做成一个 Skill（比如 `assemble-context`），并且让它输出的清单可以被人快速核对，而不是完全黑盒。

---

## 十四、文档自维护：必须带一道审计机制

成熟以后，可以让 Agent 在开发过程中自动执行影响分析：

```text
Code changed → Impact analysis
  → Docs affected? → Spec affected? → ADR needed? → Tests affected?
```

例如：修改 Workflow State Machine → WORKFLOW_SPEC 受影响 → integration tests 受影响 → architecture guide 不受影响 → 不需要新 ADR。

这个闭环的目标是让代码库形成：

```text
Code ↔ Specs ↔ Tests ↔ Architecture ↔ Decisions
```

也就是 **Living Software Documentation**。

### 补充：AI 说"不需要更新"，本身也需要被校验

这一节的原始版本有一个隐藏的信任假设：AI 自己判断"这次不需要改文档"，然后这个判断就被直接采信了。问题在于，如果 AI 判断错了——遗漏了真正受影响的 Spec——没有任何机制能发现这个遗漏，文档会在看起来体系完整的情况下，悄悄和代码脱节，而且比人工维护的文档更难被察觉，因为团队会默认"这套自动化机制在正常工作"。

建议至少加一层校验，二选一或者两者都做：

* **抽样人工核对**：每隔一定数量的 PR，随机抽取几次"AI 判断为不受影响"的变更，人工复核是否真的不受影响。
* **交叉判断**：影响分析这一步单独用一次调用，明确要求 AI 只回答"哪些文档*可能*受影响"并倾向于宁可多报，而不是在同一次生成代码的上下文里顺带判断——顺带判断更容易被"我刚写完代码，应该没问题"的惯性带偏。

没有这道审计，"Living Documentation"很容易退化成"看起来在维护，实际上没人知道有没有维护对"的文档。

---

## 十五、从零开始：建议的八个阶段

**Phase 0 — Project Discovery**：回答"要解决什么问题、谁使用、核心场景、非目标、成功标准"。产物：`PRODUCT.md`、`REQUIREMENTS.md`。

**Phase 1 — System Modeling**：建立 domain model、系统边界、actors、主要组件、数据流、控制流。产物：`ARCHITECTURE.md`、`DESIGN_PRINCIPLES.md`、`ADR/*`。

**Phase 2 — Specification**：把关键行为定义清楚（`PROTOCOL_SPEC` / `WORKFLOW_SPEC` / `API_SPEC` / `DATA_SPEC`），尤其要避免"代码先跑起来再说"。

**Phase 3 — Repository Bootstrap**：搭建 repo、build、CI、lint、test、开发环境、文档结构、agent 指令、skills。这个阶段代码量不需要多，重点是把以后 AI 工作的环境建立起来。

**Phase 4 — Vertical Slice**：不要一次做整个系统，先打通一条最小完整链路（`User Request → API → Core Logic → Storage → Response`），这是验证架构最有效的方法。

**Phase 5 — Iterative Development**：`Feature → Spec → Plan → Implementation → Test → Review → Merge`，一个 Feature 一个 Feature 推进。

**Phase 6 — Hardening**：性能、并发、安全、故障恢复、可观测性、兼容性、迁移。

**Phase 7 — Evolution**：后续开发不再是重新理解整个项目，而是 `Current State + New Requirement → Impact Analysis → ADR/Spec Update → Implementation Plan → Implementation → Verification`。

---

## 十六、这套体系什么时候不该用

原始方法论只讲"该怎么做"，没有讲"什么时候不该这么做"。这是一个真实的缺口——过度工程化本身也是一种风险，而不是只有"没有流程"才是风险。

以下几种情况，建议有意识地简化或延后这套体系，而不是教条地全套照搬：

* **需求本身还不稳定的早期探索阶段**。如果产品方向每周都在变，先把 Spec 写死成"契约"，反而会造成 Spec 和现实脱节的速度比代码还快——这时候 `PRODUCT.md` 和一份轻量的 `ARCHITECTURE.md` 可能就够了，Spec 层可以推迟到核心行为稳定之后再补。
* **小型项目或单人项目**。Work Item 目录、五个 Agent 角色、完整的 ADR 流程，对一个几千行代码、一个人维护的项目来说，维护成本可能超过它带来的收益。这套体系的回报是随项目规模和团队规模超线性增长的，规模不够时不必强行套用。
* **一次性脚本或实验性原型**。不需要 SPEC、不需要 ADR，快速验证想法本身就是目的。

判断标准可以简化成一句话：**当"AI 因为不知道全局而破坏其他模块"这件事开始真实发生、并且造成了返工成本时，就是引入这套体系的时机；在那之前，过早引入的文档基础设施本身就是一种技术债。**

---

## 十七、整体闭环架构

```text
                    Human
                      │
                      ▼
               Product Intent
                      │
                      ▼
                 Requirements
                      │
                      ▼
                 Architecture
                      │
                      ▼
                    Specs
                      │
                      ▼
                  Roadmap
                      │
                      ▼
               Work Breakdown
                      │
                      ▼
                 Work Item
                      │
                      ▼
                 AI Planner
                      │
                      ▼
               AI Implementer
                      │
                      ▼
                   Tests
                      │
                      ▼
                 AI Reviewer（机械性检查）
                      │
                      ▼
              Automated Checks
                      │
             ┌────────┴────────┐
             │                 │
            PASS              FAIL
             │                 │
             ▼                 ▼
        变更分类              Diagnose
             │                 │
    ┌────────┴────────┐        ▼
    ▼                 ▼       Fix
局部/低风险        架构/高风险   │
    │                 │        └──→ Tests
    ▼                 ▼
  Merge          人工 Review
                       │
              ┌────────┴────────┐
              ▼                 ▼
            通过              打回
              │                 │
              ▼                 ▼
            Merge            重新实现
```

这才是比较理想的 **AI-assisted Software Factory**，而不是 "ChatGPT + Copilot + 一堆 Prompt"。相比原始版本，这里明确加入了"变更分类 → 人工 Review 分支"，让"人类控制关键决策"这句原则真正落到了流程图里的一个节点上，而不只是文字上的强调。

---

## 十八、压缩成一句公式

```text
AI Development
=
Context
+ Specification
+ Task Decomposition
+ Agent Skills
+ Implementation
+ Automated Verification
+ Human Decisions（有明确的合并门禁作为落点）
+ 审计与漂移校验（针对文档自维护和 AI 互审风险）
```

而不是：

```text
AI Development = Better Prompt
```

---

## 最重要的落地点

如果今天从零开始一个中大型项目，最小可用系统应该包括：

```text
AGENTS.md

docs/
├── PRODUCT.md
├── REQUIREMENTS.md
├── ARCHITECTURE.md（含"禁止清单"和"合并门禁分类规则"）
├── DESIGN_PRINCIPLES.md
├── specs/
├── adr/（每条 ADR 带 Status 字段）
└── guides/

skills/
├── planning/
├── implementation/
├── testing/
├── debugging/
├── documentation/
└── assemble-context/

plans/
└── roadmap.md

work-items/
```

然后规定每个功能必须经过：

```text
Requirement → Spec → Work Item → Plan → Implementation
   → Test → Review（按风险分类走自动或人工）→ Evidence → Merge
```

**代码只是这个流水线中的一个阶段。** 这套体系的价值不在于文档写得多漂亮，而在于它把"人类控制关键决策"从一句原则，变成了目录结构、合并门禁、ADR 状态字段这些可以被检查、被执行的具体机制——同时也诚实地承认它自身有成本，不是每个项目、每个阶段都值得全套引入。
