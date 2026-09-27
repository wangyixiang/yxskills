对于**中大型软件项目**，真正有效的方法不是“让 AI 帮我们写更多代码”，而是把 AI 嵌入整个软件工程流程，让它参与：

**需求理解 → 系统设计 → 任务拆解 → 编码 → 测试 → Review → 集成 → 文档更新 → 后续演进**

我比较推荐把这套方法理解成：

> **Spec-driven + Agent-driven + Test-verified + Human-controlled Software Development**

核心思想只有一句：

> **人负责目标、约束和关键决策；AI 负责理解、拆解、实现、验证和维护。**

而且对于中大型项目，**“文档 + Agent 指南 + Skills + 计划 + 测试”本身就是 AI 的开发基础设施。**

---

# 一、先纠正一个最常见的思路

很多人用 AI 开发项目，是这样：

```text
我：帮我实现 XXX

AI：写了一堆代码

我：这里不对，再改一下

AI：继续改

我：又坏了

AI：再修

...
```

小项目还可以。

中大型项目很快就会变成：

```text
需求漂移
   ↓
AI 不知道整体架构
   ↓
开始局部优化
   ↓
破坏其他模块
   ↓
继续打补丁
   ↓
代码越来越复杂
   ↓
AI 更难理解
   ↓
重新开发
```

最终 AI 会从：

> **开发加速器**

变成：

> **代码混乱加速器**

所以真正重要的不是“怎么给 Coding Agent 更强的 Prompt”，而是：

# 怎么建立一个让 AI 能持续工作的工程系统。

---

# 二、我建议把整个项目分成 5 个层次

可以建立这样一个模型：

```text
┌───────────────────────────────┐
│       Product / Business      │
│       为什么做这个系统         │
├───────────────────────────────┤
│        Requirements           │
│       系统必须做什么           │
├───────────────────────────────┤
│        Architecture           │
│       系统应该怎么构成         │
├───────────────────────────────┤
│        Implementation         │
│       当前具体怎么实现         │
├───────────────────────────────┤
│        Verification           │
│       怎么证明它是正确的       │
└───────────────────────────────┘
```

AI 可以参与所有层，但是：

**越靠上，人类控制越强；越靠下，AI 自动化程度越高。**

比如：

| 层级     | 人类    | AI    |
| ------ | ----- | ----- |
| 产品目标   | ★★★★★ | ★     |
| 核心需求   | ★★★★★ | ★★    |
| 架构原则   | ★★★★  | ★★★   |
| 模块设计   | ★★★   | ★★★★  |
| 具体实现   | ★★    | ★★★★★ |
| 测试生成   | ★★    | ★★★★★ |
| Bug 分析 | ★★    | ★★★★★ |
| 文档维护   | ★     | ★★★★★ |

这非常重要。

**不要把“系统应该是什么”完全交给 Agent。**

---

# 三、第一步：先建立 AI 能读懂的“项目知识库”

从零开发一个中大型项目，我不会一开始让 Agent 写代码。

第一阶段反而应该是：

> **建立项目的 Source of Truth。**

例如：

```text
project/
│
├── AGENTS.md
├── README.md
│
├── docs/
│   ├── PRODUCT.md
│   ├── REQUIREMENTS.md
│   ├── ARCHITECTURE.md
│   ├── DESIGN_PRINCIPLES.md
│   │
│   ├── specs/
│   │   ├── PROTOCOL_SPEC.md
│   │   ├── WORKFLOW_SPEC.md
│   │   ├── API_SPEC.md
│   │   └── ...
│   │
│   ├── adr/
│   │   ├── ADR-001-xxx.md
│   │   ├── ADR-002-xxx.md
│   │   └── ...
│   │
│   └── guides/
│       ├── architecture-guide.md
│       ├── backend-guide.md
│       ├── frontend-guide.md
│       └── testing-guide.md
│
├── skills/
│   ├── ...
│
├── plans/
│   ├── roadmap.md
│   ├── milestones/
│   └── ...
│
├── work-items/
│   ├── feature-001/
│   ├── feature-002/
│   └── ...
│
├── src/
├── tests/
└── scripts/
```

这个结构的意义不是“文档好看”。

它实际上是在建立：

> **AI 的长期记忆和工作协议。**

---

# 四、其中最重要的不是 README，而是 AGENTS.md

例如：

```text
AGENTS.md
```

它应该回答：

```text
你是谁？
你正在开发什么系统？
项目有哪些核心原则？
目录结构是什么？
哪些地方可以修改？
哪些地方不能随意修改？
代码风格是什么？
测试怎么跑？
什么时候必须增加测试？
架构边界是什么？
如何处理依赖？
如何提交代码？
什么情况下需要新增 ADR？
什么情况下必须更新文档？
```

也就是说：

```text
AGENTS.md
      ↓
告诉 Agent “如何工作”
```

而：

```text
SPEC
      ↓
告诉 Agent “系统应该是什么”
```

再：

```text
PLAN
      ↓
告诉 Agent “这次具体做什么”
```

这三个东西不要混在一起。

---

# 五、然后建立第二层：Specification

这是中大型项目最关键的一层。

比如：

```text
docs/specs/

PROTOCOL_SPEC.md
WORKFLOW_SPEC.md
API_SPEC.md
AUTH_SPEC.md
STORAGE_SPEC.md
```

这些不是普通说明文档。

它们应该成为：

> **实现与验收的契约。**

例如：

```text
Workflow Step
```

应该定义：

```text
Step 的目的
Step 的输入
Step 的输出
Step 的状态
Step 的生命周期
Step 的错误处理
Step 的重试规则
Step 完成条件
Step 失败条件
Step 与其他 Step 的关系
```

那么 Agent 写代码的时候，不应该是：

> “你觉得这个 Step 应该怎么实现？”

而应该是：

> “按照 WORKFLOW_SPEC 中定义的行为实现这个 Step。”

这会极大降低 AI 的自由发挥。

---

# 六、第三层：Architecture

Specification 解决：

> **系统需要表现成什么样。**

Architecture 解决：

> **系统应该由什么构成。**

例如：

```text
                   ┌──────────────┐
                   │  Client      │
                   └──────┬───────┘
                          │
                          ▼
                ┌─────────────────┐
                │ Central         │
                │ Orchestrator    │
                └────────┬────────┘
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
         Context      Planner     Knowledge
         Engine        Engine       Engine
             │           │
             └──────┬────┘
                    ▼
                 Executor
                    │
                    ▼
                  Edge
```

Architecture 文档应该说明：

```text
组件是什么
为什么存在
组件之间如何通信
依赖关系
数据流
控制流
边界
扩展点
故障边界
```

尤其重要的是：

# 明确“禁止什么”。

比如：

```text
Frontend MUST NOT access database directly.

Workflow Engine MUST NOT depend on UI.

Domain layer MUST NOT depend on infrastructure.

Edge MUST NOT make autonomous planning decisions.

```

对于 AI 来说：

> **Negative constraints 往往比 Positive instructions 更重要。**

因为 Agent 很容易“顺手”做出一个看似合理、但破坏架构的实现。

---

# 七、第四层：不要让 Agent 直接处理“整个项目”

这是 AI 开发中非常重要的一条。

不要：

```text
Build the entire project.
```

而是：

```text
Project
   ↓
Subsystem
   ↓
Module
   ↓
Feature
   ↓
Work Item
   ↓
Implementation Task
```

例如：

```text
项目
└── Workflow System
    ├── Workflow Definition
    ├── Workflow Runtime
    ├── Step Execution
    ├── Step State
    ├── Completion Evaluation
    └── Error Recovery
```

进一步：

```text
Workflow Runtime
    ↓
Implement Step Lifecycle
    ↓
Implement Step State Machine
    ↓
Implement transition validation
    ↓
Implement tests
```

最后 AI 接收到的任务应该是：

```text
Implement workflow step transition validation.

Read:
- WORKFLOW_SPEC.md
- architecture-guide.md
- current state implementation

Constraints:
- do not modify persistence layer
- preserve existing public API
- add unit tests
- add invalid transition cases

Done when:
- ...
```

这时候 Agent 的工作质量会明显提升。

---

# 八、所以真正的核心单位不是“Prompt”，而是 Work Item

我甚至建议把每个任务标准化成：

```text
work-items/
└── WF-023-step-transition-validation/
    ├── TASK.md
    ├── CONTEXT.md
    ├── DESIGN.md
    ├── TEST_PLAN.md
    └── ACCEPTANCE.md
```

例如：

```text
TASK.md

Goal:
Implement workflow step transition validation.

Related Spec:
docs/specs/WORKFLOW_SPEC.md

Scope:
workflow/runtime/

Out of Scope:
persistence
UI
API redesign

Required behavior:
...

Constraints:
...

Acceptance:
...
```

这样 Agent 不再面对：

> “帮我把这个东西做出来。”

而是面对：

> **一个可以验证的工程任务。**

---

# 九、然后才是 Coding Agent

我比较推荐把 Coding Agent 分成几个不同职责。

不是必须真的创建五个 Agent，而是让它们拥有不同的工作模式：

```text
                 ┌──────────────┐
                 │   Planner    │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │  Architect   │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │ Implementer  │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │   Tester     │
                 └──────┬───────┘
                        ↓
                 ┌──────────────┐
                 │   Reviewer   │
                 └──────────────┘
```

职责分别是：

### Planner

负责：

```text
需求
 ↓
任务拆解
 ↓
实施计划
```

### Architect

负责：

```text
架构影响
依赖
接口
数据流
边界
```

### Implementer

负责：

```text
真正修改代码
```

### Tester

负责：

```text
测试
边界情况
失败路径
回归验证
```

### Reviewer

负责：

```text
是否满足 Spec
是否破坏架构
是否产生 scope creep
是否缺少测试
```

---

# 十、最重要的一件事：AI 写完代码不能算完成

传统开发经常是：

```text
Code → Done
```

AI 开发应该是：

```text
Code
  ↓
Build
  ↓
Unit Test
  ↓
Integration Test
  ↓
Spec Verification
  ↓
Architecture Review
  ↓
Done
```

也就是说：

# “生成代码”只是整个任务的一部分。

---

# 十一、最好让测试反过来约束 AI

例如定义：

```text
Requirement
      ↓
Acceptance Criteria
      ↓
Test Case
      ↓
Implementation
```

而不是：

```text
AI 写代码
      ↓
后来再想怎么测
```

例如：

```text
Requirement:

Workflow Step completes only when all required evidence
has been collected.
```

可以变成：

```text
Test:

missing evidence
→ NOT completed

partial evidence
→ NOT completed

all evidence
→ completed

invalid evidence
→ failed
```

然后：

```text
Agent implementation
```

再去满足这些测试。

这样：

> **Tests 成为 AI 的“第二个程序员”。**

第一个程序员是 AI。

第二个程序员是验证系统。

---

# 十二、再进一步：建立“自动验证门”

例如：

```text
Agent
 ↓
git diff
 ↓
format
 ↓
lint
 ↓
type check
 ↓
unit tests
 ↓
integration tests
 ↓
architecture checks
 ↓
security checks
 ↓
commit
```

Agent 不能自己宣布：

> “完成了。”

而应该是：

```text
Implementation Status:
PASS

Tests:
124 passed

Architecture checks:
PASS

Spec checks:
PASS

Changed:
7 files

Unrelated changes:
none
```

这会比单纯依赖 Agent 自我判断可靠很多。

---

# 十三、AI 最擅长的，其实不是“写代码”

这是很多人一开始容易误判的地方。

AI 真正有优势的是：

### 1. 理解大量上下文

例如：

```text
10 个模块
50 个接口
100 个测试
几十个配置
大量文档
```

人很难一直保持全局上下文。

AI 比较适合做：

```text
cross-module reasoning
```

---

### 2. 快速生成大量机械代码

例如：

```text
CRUD
DTO
serialization
validation
tests
mocks
adapters
boilerplate
```

---

### 3. 分析代码关系

例如：

```text
这个 API 谁调用？

这个状态在哪里修改？

这个对象为什么会出现？

某个字段还有哪些引用？
```

---

### 4. Debug

尤其是：

```text
log
stack trace
test output
diff
code
configuration
```

同时交给 AI。

这是非常适合 AI 的工作。

---

### 5. 维护文档

代码变化：

```text
code
 ↓
AI
 ↓
detect impacted docs
 ↓
update spec / guide / ADR
```

这件事情非常适合自动化。

---

# 十四、AI 不应该负责什么？

至少在项目早期，以下事情不要完全放给 AI：

```text
产品最终目标
核心业务规则
关键架构决策
安全边界
兼容性策略
核心数据模型
关键性能指标
重大技术选型
是否改变产品行为
```

AI 可以提出：

```text
Option A
Option B
Option C
```

但最终决策应该来自人。

然后：

```text
human decision
      ↓
ADR
      ↓
future AI behavior
```

这非常重要。

---

# 十五、ADR 是 AI 项目里非常有价值的东西

例如：

```text
ADR-007

Decision:
Workflow state is persisted centrally.

Why:
...

Rejected alternatives:
...

Consequences:
...

```

几个月以后，你再让 AI 改系统，它就不会问：

> “为什么不直接放客户端？”

因为 ADR 已经告诉它：

> **这是一个历史架构决策。**

所以：

```text
Human decision
      ↓
ADR
      ↓
AI institutional memory
```

---

# 十六、Skill 的作用又是什么？

这个和你之前研究的 `AGENTS.md + skills + agent guides` 正好能够组合起来。

我建议区分：

### AGENTS.md

解决：

> **项目级工作规则**

比如：

```text
architecture principles
coding conventions
test requirements
git rules
directory rules
```

---

### Skill

解决：

> **某一类任务怎么做**

比如：

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

例如：

```text
add-workflow-step

Input:
step requirement

Process:
1. inspect workflow spec
2. inspect state machine
3. identify extension point
4. update implementation
5. update tests
6. run workflow suite
7. update docs
```

于是：

```text
AGENTS.md
= How the project works

Skill
= How to perform a class of tasks

SPEC
= What the system must do

PLAN
= What we are doing now
```

这个分层我认为非常关键。

---

# 十七、最终应该形成一个 AI 开发闭环

完整流程可以变成：

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
                 AI Reviewer
                      │
                      ▼
              Automated Checks
                      │
             ┌────────┴────────┐
             │                 │
            PASS              FAIL
             │                 │
             ▼                 ▼
          Merge             Diagnose
                               │
                               ▼
                            Fix
                               │
                               └───────→ Tests
```

这才是比较理想的：

# AI-assisted Software Factory

而不是：

# ChatGPT + Copilot + 一堆 Prompt

---

# 十八、对于“从零开始”的项目，我建议分 8 个阶段

## Phase 0：Project Discovery

先回答：

```text
我们到底要解决什么问题？
谁使用？
核心场景？
非目标？
成功标准？
```

产物：

```text
PRODUCT.md
REQUIREMENTS.md
```

---

## Phase 1：System Modeling

建立：

```text
domain model
system boundaries
actors
major components
data flow
control flow
```

产物：

```text
ARCHITECTURE.md
DESIGN_PRINCIPLES.md
ADR/*
```

---

## Phase 2：Specification

把关键行为定义清楚：

```text
PROTOCOL_SPEC
WORKFLOW_SPEC
API_SPEC
DATA_SPEC
```

这里尤其应该避免“代码先跑起来再说”。

---

## Phase 3：Repository Bootstrap

让 Agent 建立：

```text
repo
build
CI
lint
test
dev environment
documentation structure
agent instructions
skills
```

这个阶段代码量不需要很多。

重点是：

> **把以后 AI 工作的环境建立起来。**

---

## Phase 4：Vertical Slice

不要一次做整个系统。

例如：

```text
User Request
      ↓
API
      ↓
Core Logic
      ↓
Storage
      ↓
Response
```

先打通一个**最小完整链路**。

这是验证 architecture 最有效的方法。

---

## Phase 5：Iterative Development

之后：

```text
Feature
 ↓
Spec
 ↓
Plan
 ↓
Implementation
 ↓
Test
 ↓
Review
 ↓
Merge
```

一个 Feature 一个 Feature 做。

---

## Phase 6：Hardening

重点：

```text
performance
concurrency
security
failure recovery
observability
compatibility
migration
```

---

## Phase 7：Evolution

后续开发就不是重新理解整个项目。

而是：

```text
Current State
   +
New Requirement
   ↓
Impact Analysis
   ↓
ADR / Spec Update
   ↓
Implementation Plan
   ↓
Implementation
   ↓
Verification
```

---

# 十九、还有一个非常重要的概念：Context Engineering

当项目大到一定程度以后，最大的问题不是 AI 不聪明。

而是：

> **Context 太多。**

比如项目有：

```text
500,000 lines
3,000 source files
200 docs
1,000 tests
```

你不可能每次：

```text
把整个 repo 扔给 AI
```

所以应该建立：

```text
Global Context
      +
Architecture Context
      +
Module Context
      +
Task Context
      +
Relevant Code
      +
Relevant Tests
```

而不是：

```text
整个仓库
```

例如一个任务：

```text
WF-023

Global:
AGENTS.md

Architecture:
workflow architecture

Spec:
WORKFLOW_SPEC.md

Module:
workflow/runtime/README.md

Task:
TASK.md

Relevant code:
state_machine.rs
transition.rs

Relevant tests:
transition_test.rs
```

这就是一个**精确 Context Package**。

Agent 的效率会高很多。

---

# 二十、所以未来的 Coding Agent 系统其实可以形成三级上下文

我会非常推荐：

```text
                 ┌──────────────────┐
                 │ Project Context  │
                 │                  │
                 │ AGENTS           │
                 │ Architecture     │
                 │ Principles       │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │ Module Context   │
                 │                  │
                 │ module guide     │
                 │ interfaces       │
                 │ local rules      │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │ Task Context     │
                 │                  │
                 │ task             │
                 │ spec             │
                 │ tests            │
                 │ relevant code    │
                 └──────────────────┘
```

这是比“一个超级 AGENTS.md”更可扩展的方式。

---

# 二十一、再往前一步：让 AI 自己维护项目知识

成熟以后，可以让 Agent 在开发过程中自动执行：

```text
Code changed
    ↓
Impact analysis
    ↓
Docs affected?
    ↓
Spec affected?
    ↓
ADR needed?
    ↓
Tests affected?
```

例如：

```text
修改 Workflow State Machine
        ↓
WORKFLOW_SPEC affected
        ↓
integration tests affected
        ↓
architecture guide unaffected
        ↓
ADR not needed
```

于是最终代码库会形成：

```text
Code
 ↕
Specs
 ↕
Tests
 ↕
Architecture
 ↕
Decisions
```

这才是真正的：

# Living Software Documentation

---

# 二十二、如果把这一整套体系压缩成一句公式

我会建议你记住：

```text
AI Development
=
Context
+
Specification
+
Task Decomposition
+
Agent Skills
+
Implementation
+
Automated Verification
+
Human Decisions
```

而不是：

```text
AI Development = Better Prompt
```

---

# 二十三、对于你现在正在探索的方向，我会进一步做成这样的总体架构

结合你之前在思考的 **Coding Agent 文档体系 / Skills / Agent Guide / Central Orchestrator / Client-Edge 协作**，其实可以自然演化成：

```text
                 ┌──────────────────────┐
                 │      Human           │
                 │ Product / Decisions  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Project Knowledge  │
                 │                      │
                 │ Specs                │
                 │ Architecture        │
                 │ ADR                 │
                 │ Guides              │
                 │ Skills              │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Central Planner    │
                 │   / Orchestrator     │
                 └──────────┬───────────┘
                            │
                ┌───────────┼────────────┐
                ▼           ▼            ▼
             Planner   Implementer    Reviewer
                │           │            │
                └───────────┼────────────┘
                            ▼
                     Local / Edge
                     Coding Agent
                            │
                            ▼
                         Repo
                            │
                            ▼
                  Build / Test / CI
                            │
                            ▼
                         Evidence
                            │
                            └───────────→ Central
```

这其实已经不是简单的：

> **“使用 AI 写软件”**

而是：

> **“建立一个 AI-native Software Engineering System。”**

这也是我认为中大型项目最值得研究的方向。

---

## 最重要的落地点

假如今天真的从零开始一个中大型项目，我**不会先写代码**，而会先建立下面这套最小系统：

```text
AGENTS.md

docs/
├── PRODUCT.md
├── REQUIREMENTS.md
├── ARCHITECTURE.md
├── DESIGN_PRINCIPLES.md
├── specs/
├── adr/
└── guides/

skills/
├── planning/
├── implementation/
├── testing/
├── debugging/
└── documentation/

plans/
└── roadmap.md

work-items/
```

然后规定每个功能必须经过：

```text
Requirement
    ↓
Spec
    ↓
Work Item
    ↓
Plan
    ↓
Implementation
    ↓
Test
    ↓
Review
    ↓
Evidence
    ↓
Merge
```

**代码只是这个流水线中的一个阶段。**

而且我认为你前面在做的 `PROTOCOL_SPEC.md`、`WORKFLOW_SPEC.md`、`AGENTS.md`、`skills`、`agent guides` 这些东西，实际上可以被统一放进这个更大的 **AI-native Software Development Framework** 里，而不是分别设计成几套孤立的文档。

下一步最值得做的，是直接把这套方法落成一个**可以复制到任意新项目里的标准工程模板**：包括目录结构、所有根文档模板、`AGENTS.md`、Skills、Agent Guides、Work Item 模板、Spec 模板、ADR 模板，以及从“需求 → 编码 → 验收”的 Agent 工作流。
