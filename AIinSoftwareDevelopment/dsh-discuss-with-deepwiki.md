https://deepwiki.com/deepseek-ai/deepseek-harness
https://deepwiki.com/search/-repoai-httpsgithubcomwangyixi_c30597c2-2396-478e-9c7a-f8ab6a9c18e0?mode=fast
---

# dsh repo的AI开发基建是不是和[README](README.md)很像?
**是的，非常像。** 文章的公式 `Context + Specification + Task Decomposition + Agent Skills + Implementation + Automated Verification + Human Decisions` 几乎每一项都能在dsh repo 找到对应实现，而且不少已经产品化成了 harness 的运行时机制，而不只是文档约定。

---

## 逐项对应

| 文章概念 | 本仓库对应物 |
|---|---|
| `AGENTS.md` = "如何工作" | 分层 `AGENTS.md`：根 `AGENTS.md` 只放 standing orders，`packages/`、`docs/`、`website/`、`notes/` 各有子树级规则 — 正好是文章的「三级上下文」结构 [1](#1-0)  |
| AGENTS.md 自动进上下文 | `dsh-agent-instructions` 插件按目录优先级加载 `AGENTS.md`/`CLAUDE.md`，以 `<system-reminder>` 注入，支持嵌套发现与增量刷新 [2](#1-1)  |
| ADR = AI institutional memory | Agent Notes：`{proposed,implemented,rejected,archived}/{class}/` 生命周期 + `## Alternatives considered` 强制记录被否决方案，正是文章说的「防止 re-litigation」 [3](#1-2) [4](#1-3)  |
| Skills = 某类任务怎么做 | `.agents/skills/`：`dsh-code-review`、`dsh-pre-push-checks`、`dsh-doc`、`dsh-find-simplifications`、`dsh-translate-docs` 等，每个是带流程的 `SKILL.md` [5](#1-4)  |
| 自动验证门 / "AI 不能自己宣布完成" | `scripts/` 下大量机械 gate：`verify-translation-pairing`、`verify-type-equiv`、`verify-agent-note-format`、`verify-doc-budgets`、`check-workspace-constraints`、`verify-archived-agent-notes`，加上 `dsh-pre-push-checks` skill [6](#1-5)  |
| Spec = 实现与验收的契约 | `docs/subsystems/` 每子系统一页承载类型定义与语义；` ```ts type-equiv ` 代码块由 `verify-type-equiv` 强制与源码同步，即「文档是契约、机器校验不漂移」 [7](#1-6)  |
| Negative constraints 更重要 | 根 `AGENTS.md` 多为禁令（"package bins... are forbidden"），文章「MUST NOT」条款的实例 [8](#1-7)  |
| Code ↔ Docs 双向维护（Living Documentation） | 双语配对三元组（`foo.md`/`foo.zh.md`/`foo.i18n.yaml`）+ blob hash + merge driver + `dsh-translate-docs`；Agent Note 要求「代码改动与 owning note 同一 PR 更新」 [11](#1-10)  |

## 差异 / 缺口

- **Work Item 目录没有。** 文章建议 `work-items/TASK.md + ACCEPTANCE.md` 的标准化任务包；本仓库最接近的是 `proposed/` Agent Note 的 `## Proposal + ## Acceptance criteria` 骨架，但它是决策记录而非任务载体 [12](#1-11) 
- **Specs 层级较薄。** 没有独立的 `docs/specs/` 行为规约层；契约主要由 `subsystems/` 类型页 + 包 README 承担，「协议级行为规约」这个 tier 不存在 [13](#1-12) 
- **测试先行约束是流程约定而非测试基建。** gate 验证文档/格式/依赖图，但没有「requirement → acceptance criteria → generated test」的强制链。

## Notes

dsh repo 本身就是文章理念的极端化版本：它既是「按这套基建开发的仓庫」，又是「给别的项目提供这套基建的运行时」。可以认为文章的 §3–§16 描述的是*仓库内约定*，而本仓库把其中一半做成了*代码强制*。

---

# 本仓库做了哪些你说的”代码强制“？也就是你说的gate?
**"代码强制"指：凡是能用脚本检查的规则，都做成非零退出的命令，交给 git hooks 和 CI 跑，而不是留在 AGENTS.md 里靠评审者或 agent 自觉。** 设计原则被记录在 "Mechanical quality gates over prose guidelines" 这篇 Agent Note 中：本仓库主要由 agent 开发，agent 遵守门禁远比遵守行文约定可靠，因此「每条机械可检查的 AGENTS.md 承诺都配一条命令」 [1](#2-0) 。

---

## 文档↔代码一致性（doc-sync 门禁族）

| 门禁 | 强制的承诺 |
|---|---|
| `doc-typecheck` | 文档里每个 ` ```ts ` 围栏块必须真正编译通过；草图需显式 `ts ignore-check` opt-out，且 opt-out 比例超一半即失败 [2](#2-1)  |
| `verify-type-equiv` | `docs/subsystems/` 粘贴的类型声明用 `ts type-equiv` / `ts public-api` 标记并登记 `type-equiv.manifest.json`；门禁用 TypeScript 解析器从源码提取符号断言两侧一致 — 文档里的类型**不许漂移** [3](#2-2)  |
| `verify-md-wrap` | 「一个段落一个物理行」写作规则，AST 解析后拒绝跨行段落 [4](#2-3)  |
| `verify-md-links` | 相对链接 + `#fragment` 锚点必须指向磁盘上存在的目标 — 改文件名会立即红 [5](#2-4)  |
| `verify-doc-budgets` | `doc-budgets.manifest.json` 给每篇 standing doc 设词数上限（根 `AGENTS.md` ≤1950 词等），超限要 relocate/condense/显式抬预算 — 文章说的「context 不能膨胀」被数值化 [6](#2-5)  |
| `verify-package-readme-limitations` | 每个包 README 必须有恰好一个规范标题 `## Known Limitations and Deferred Work`；真没有就进显式 `NO_LIMITATIONS` 白名单 — 「没写」和「确认没有」不可混淆 [7](#2-6)  |
| `verify-cordis-catalog` 等生成目录门禁 | `tool-catalog`、`config-catalog`、`module-graph` 等参考文档由源码重新生成 + freshness 门，手改生成区会被拒绝 [8](#2-7)  |

## 双语配对（最重的一套）

- `foo.md` / `foo.zh.md` / `foo.i18n.yaml` 三元组，sidecar 记录两侧 blob hash；任何一侧改动未重新确认即失同步，PR 必须整体合并 [9](#2-8) 
- `verify-translation-pairing` 校验完整性、hash、语言切换行、结构签名（标题深度、逐字节一致的代码块、表格行列数） [10](#2-9) 
- 自定义 Git merge driver `dsh-translation-pairing`：`.i18n.yaml` 冲突时自动验证两侧三文合并仍保持配对，可安全合并则生成新记录，否则保留冲突 [11](#2-10) 

## Git hooks 与 CI

- `lefthook.yml`：pre-commit 跑暂存配对校验、归档 note 校验、Oxlint 自动修复、THIRD_PARTY_NOTICES 重生成、空白检查、vendor manifest 守卫；pre-merge-commit 再查配对；pre-push 跑 typecheck [12](#2-11) 
- CI 侧是 `scripts/run-gates.ts` 有界调度器：`needs`/`after` 依赖边、`allowFailure`、`streamOutput`，覆盖 Node 22.19/24/26 矩阵与构建产物冒烟 [13](#2-12) 
- 配套 agent 流程 skill：`dsh-pre-push-checks` 要求先 `change-scope --base <ref>` 拿到确定性变更范围报告，再选最窄证据集 — 即文章说的「Agent 不能自己宣布完成，要交 evidence」 [14](#2-13) [15](#2-14) 

## Agent Note 本身也被门禁化

- `verify-agent-note-format` / `verify-archived-agent-notes` 把 `{lifecycle}/{class}/` 目录约定、必备小节（含 `## Alternatives considered`）、归档三元组完整性做成校验，连 hooks 都单独跑归档 note 检查 [16](#2-15) 
- 100% 覆盖率的 per-file 门（`packages/*/*/src`，v8）、jscpd 跨文件克隆检测、`check-workspace-constraints`（private、cordis peer+dev、统一版本、ESM）、publint、NodeNext 消费方 typecheck 都在同一套原则下 [17](#2-16) 

## 运行时层的"代码强制"（区别于仓库门）

对应文章里"人控制关键决策"的部分也做成了运行时机制：`dsh-plan-mode` 让 agent 只能读、规划、`exit_plan_mode` 交人审批后才实现；`tools/pre-execute` 的 `ask`→`ctx.approval` 审批 seam、landlock/sandbox-exec 沙箱后端都是代码级约束而非提示词约定 [18](#2-17) [19](#2-18) 

## Notes

- 刻意的边界：hooks 只跑便宜检查，全量归 CI；`check:all` 是可选本地演练、不是 agent 指令 [20](#2-19) 
- 门禁的已知盲区也被显式承认：配对 gate 只能证明 hash/结构一致，证明不了译文质量 — 语义仍归评审 [21](#2-20) 
- 一句话概括：dsh repo 把「agent 遵守门禁比遵守行文可靠」当作公理，AGENTS.md 里每条可机械化的承诺都有对应的 `scripts/verify-*.ts`。

---
# "AGENTS.md → 告诉 Agent "如何工作" （项目级工作规则） SPEC → 告诉 Agent "系统应该是什么" （实现与验收的契约） PLAN → 告诉 Agent "这次具体做什么" （当前任务范围）" dsh项目的SPEC和PLAN文档，都放哪里了？
**SPEC → `docs/subsystems/` + `docs/architecture.md` + 各包 README**（没有独立的 `specs/` 目录）；**PLAN → `.agents/notes/proposed/`** 是最接近的常驻载体，运行时任务级 plan 则由 `plan-mode` 插件的 `exit_plan_mode` 产生、只存会话不落盘为仓库文档。 [1](#3-0) [2](#3-1) 

---

## SPEC：拆散在多个 tier，而非一个 `docs/specs/`

| 文章角色 | 本仓库位置 | 契约性如何被保证 |
|---|---|---|
| 「系统应该是什么」的类型/语义契约 | `docs/subsystems/*.md` — 每子系统一页，承载类型定义、语义、生成的 Cordis API；如 `workflow.md` 定义 `WorkflowStartRequest`/`WorkflowRun`/`workflow/*` 事件、`plan.md` 定义 `plan/mode` 状态 | ` ```ts type-equiv `/`ts public-api ` 围栏 + `verify-type-equiv` 门禁：文档里的声明必须与源码逐字一致，漂移即红 [3](#3-2) [4](#3-3)  |
| 「系统应该怎么构成」（架构层） | `docs/architecture.md` — 组件/loop/seam/扩展点的有序地图；行为叙述归它，类型定义归 subsystems [1](#3-0)  |
| 模块级契约 | `packages/**/README.md` — 每包的 config、semantics、limitations、extension points；`## Known Limitations` 章节由门禁强制 [5](#3-4)  |
| 生成型规约 | `tool-catalog.md`、`config-catalog.md`、`module-graph.md` 等 — 从源码重新生成 + freshness 门，手改被拒 [6](#3-5)  |

关键区别：文章的 spec 是「先写行为规约再实现」（PROTOCOL_SPEC、WORKFLOW_SPEC）；本仓库的 subsystems 页是**描述已 ship 的当前现实**，且用 type-equiv 门禁强制「文档 = 源码投影」。协议级「尚未实现的验收契约」这个 tier 不存在。

## PLAN：两处，一近一远

- **仓库级 plan**：`.agents/notes/proposed/` — 未来时态的 `## Proposal` + `## Acceptance criteria` + `## Risks` 骨架就是文章的 work-item 载体；ship 后同一文件迁到 `implemented/`，`## Proposal` 改写成现在时 `## Decision`（`## Acceptance criteria` 在 implemented 里会被门禁拒绝） [2](#3-1) [7](#3-6) 
- **运行时 plan**：`dsh-plan-mode` — agent 在只读态探查后用 `exit_plan_mode` 交「decision-complete」的计划 markdown 给人审批；这份 plan 是会话产物，不写入仓库 [8](#3-7) [9](#3-8) 
- 没有 `plans/roadmap.md` 或 `work-items/` 目录；最细的"当前任务"是 proposed note 的 acceptance criteria。

## Notes

- 对应关系：`AGENTS.md`↔如何工作、`subsystems/+architecture.md`↔是什么、`proposed/ notes`↔要做什么 — 三分法都成立，但 SPEC 层是"描述现状的契约"而非"先于实现的规约"，PLAN 层粒度比文章的 work-item 粗。
- 还有个反向校验：implemented note 明确禁止 spec-speak（"should…"）——计划语气只能活在 `proposed/` [10](#3-9) 

---
# 你说的"SPEC 层是"描述现状的契约"而非"先于实现的规约"是指dsh项目是”描述现状的契约“， 而我们的文档里写的是”先于实现的规约“
**对，就是这个意思。** 在dsh仓库（deepseek-harness），`docs/subsystems/` 和 type-equiv 门禁保证文档**等于已交付源码的现状**——"先写规约再实现"的那一层不存在；而你们文章里的 `WORKFLOW_SPEC.md` 一类是先于实现、用来约束 agent 产出的契约。 [1](#4-0) 

---

## 证据：dsh仓库把"描述现状"写成了硬规则

- `docs/AGENTS.md` 的写作规则第一条就是 "**Document current state**"——历史留在 commit/Agent Note/postmortem 里，文档只描述现存机制 [1](#4-0) 
- `subsystems/` 页的职责被定义为"每子系统一页参考：类型定义、语义、生成的 Cordis API"，行为叙述都被划给 `architecture.md`——它是参考（reference），不是规约（specification） [2](#4-1) 
- `verify-type-equiv` 的方向也说明了因果：**源码是权威，文档是投影**。脚本从源码提取符号断言文档块与之逐字一致——如果文档先于实现，这个断言根本无从成立 [3](#4-2) 
- 配套的义务同样是"代码变了→同一变更里更新 owning subsystems 页"，即文档跟随实现，不是实现跟随文档 [4](#4-3) 

## 时态被门禁强制分开

dsh仓库甚至把"先于实现的语气"隔离到了一个专门目录，并用 `verify-agent-note-format` 门禁执行：

| 目录 | 语气 | 角色 |
|---|---|---|
| `.agents/notes/proposed/` | `## Proposal` 可以用将来时，`## Acceptance criteria` 定义"什么算完成" | **最接近你们文章的 SPEC/Work Item** [5](#4-4)  |
| `.agents/notes/implemented/` | `## Decision` 必须用现在时；`## Proposal`、`## Acceptance criteria` 这类标题会被门禁直接拒绝，称为 "spec-speak" | 交付后的现状记录 [6](#4-5)  |

即：**"先于实现的规约"在本仓库只存在于 `proposed/` Agent Note 里，且 ship 后必须改写成现在时**——`proposed/` → `implemented/` 迁移时 `## Proposal` 重写为 `## Decision`、`## Acceptance criteria` 折叠进 `## Consequences` [7](#4-6) 。

## 所以差异的本质

你们文章的 SPEC 是**独立的、先于代码的 source of truth**（"按照 WORKFLOW_SPEC 实现这个 Step"）；本仓库的选择是：**源码是唯一 source of truth，文档层用机械门保证不漂移，"规约"只在决策记录生命周期里短暂存在**。两种都能防止 agent 自由发挥，但约束的锚点不同——一个锚在先写的文档上，一个锚在源码 + 已交付决策记录上。

## Notes

- 值得注意：这套"现状即契约"体系自己也承认盲区——一份 proposed note 指出门禁能证明结构与新鲜度，但证明不了行文仍指向活的机制（例如曾有 implemented note 描述了已不存在的行为） [8](#4-7) 。
- 如果你们想把"先于实现的规约"引入这类仓库，自然的位置就是 `proposed/` Agent Note 的 `## Proposal` + `## Acceptance criteria` 骨架——它已经是门禁化的、最接近 work-item 的载体。

Wiki pages you might want to explore:
- [Documentation & Internationalization (deepseek-ai/deepseek-harness)](/wiki/deepseek-ai/deepseek-harness#9)

