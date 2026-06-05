---
title: "Harness Engineering — Agent 开箱即用完整手册"
created: 2026-05-29
updated: 2026-06-05
type: concept
tags: [concept, harness-engineering, architecture, method, agent-patterns, control-theory]
confidence: high
sources:
  - openai.com/index/harness-engineering (2026-02-11)
  - martinfowler.com/articles/harness-engineering.html (2026-04-02)
  - blog.langchain.com/the-anatomy-of-an-agent-harness (2026-03-10)
  - github.com/deusyu/harness-engineering (3.5k★)
  - github.com/openai/symphony (25k★)
  - github.com/snarktank/ralph (19.9k★)
---

# Harness Engineering — Agent 开箱即用完整手册

> **Agent = Model + Harness**。模型提供智能，Harness 让智能变得有用。本文是 Harness Engineering 的完整参考手册，任何 Agent 阅读后即可理解并应用其核心原则。

---

## TL;DR (30 秒掌握)

```
传统工程: 人类写代码 → 机器执行代码
Harness Engineering: 人类设计约束 → Agent 写代码 → 机器执行代码
```

**核心转变**: 工程师的产出从「代码」变成了「约束系统」—— AGENTS.md、架构规则、自定义 linter、反馈回路。

**一句话**: 如果它不是模型本身，它就是 Harness。系统提示词、工具、沙箱、编排逻辑、钩子、记忆、上下文管理……全是 Harness。

---

## 1. 起源与时间线

| 日期 | 事件 | 影响 |
|:-----|:-----|:-----|
| **2026-02-05** | Mitchell Hashimoto 发表 *"Engineer the Harness"* (6 步 AI 采纳之旅第 5 步) | 提出 Harness 的操作性定义：「每次 Agent 犯错，花时间工程化一个方案使其永不再犯」— 两种形式：改进 AGENTS.md + 编写程序化工具 |
| **2026-02-11** | OpenAI 发布 *"Harness Engineering: Harnessing Codex in an Agent-First World"* | 3 人团队 5 个月从零写完 ~100 万行代码，零手写代码。首次定义术语和六大核心概念 |
| **2026-02-17** | Martin Fowler / Birgitta Böckeler 发布初始备忘录 | 将概念引入传统软件工程社区 |
| **2026-03-10** | LangChain (Vivek Trivedy) 发布 *"The Anatomy of an Agent Harness"* | 严谨拆解 Harness 7 层组件构成 |
| **2026-04-02** | Fowler/Böckeler 发表完整文章 (martinfowler.com) | 用控制论（Guides × Sensors 2×2 矩阵 + 3 监管维度 + Ashby 定律）给出形式化框架 |
| **2026-03~06** | deusyu/harness-engineering 增长至 3.5k★ | 最完整的中文学习档案：19 篇原始文章、12 篇翻译、5 阶段学习路线 |
| **2026 Q1** | Symphony (OpenAI, 25k★) / Ralph (19.9k★) / Claude Code Harness (2.6k★) / ralph-orchestrator (2.9k★) 发布 | Harness Engineering 的旗舰实现密集涌现 |

---

## 2. 三视角全景框架

Harness Engineering 有三个互补的视角，分别回答 **What / How / Anatomy**：

### 2.1 OpenAI 六大核心概念（What — 哲学层）

| # | 概念 | 含义 | Agent 可行动项 |
|:--|:-----|:-----|:--------------|
| 1 | **仓库即记录系统** | 不在 repo 里的东西对 Agent 不存在（Slack、Google Docs、脑子里的知识 = 不可见） | 所有决策/规范/计划必须版本化提交到 repo |
| 2 | **地图而非手册** | AGENTS.md 是 ~100 行的目录页，不是百科全书；渐进式披露 | 从小入口开始，指向深层文档。巨型指令文件的三个死因：挤占上下文、无法维护、无法机械验证 |
| 3 | **机械化执行** | 文档会腐烂，lint 规则不会。自定义 linter + 结构测试 = 不变量守护者 | lint 错误消息里内嵌修复指令，Agent 可自我纠正 |
| 4 | **Agent 可读性** | 优先为 Agent 的推理能力优化（选"无聊"技术、稳定 API、良好训练覆盖） | 重新实现子集可能比包装不透明的上游行为更好；让应用可以按 git worktree 启动 |
| 5 | **吞吐量改变合并理念** | 纠错成本低，等待成本高。PR 生命周期很短 | 测试偶发失败通过后续重跑解决。在 Agent 吞吐量远超人类注意力的系统中默认成立 |
| 6 | **熵管理 = 垃圾回收** | Agent 会复现已有的模式——包括坏模式。技术债 = 高息贷款 | 定期后台任务扫描偏差、更新质量评分、发起重构 PR |

### 2.2 Fowler 控制论框架（How — 操作层）

#### Guides × Sensors 2×2 矩阵

| | **计算性** (CPU, 确定性, ms级) | **推理性** (LLM, 语义, 秒级) |
|---|---|---|
| **Guides 前馈** (行动前) | bootstrap 脚本、OpenRewrite 菜谱、LSP | AGENTS.md、Skills、ARCHITECTURE.md |
| **Sensors 反馈** (行动后) | linter、ArchUnit、类型检查、测试覆盖率 | AI code review、LLM-as-judge |

**关键原则**:
- 只有反馈 = 同错反复犯
- 只有前馈 = 不知道规则是否有效
- **两者必须组合使用**

#### 三个监管维度

| 维度 | 成熟度 | 现状 | 可用的 Agent 工具 |
|:-----|:------|:-----|:-----------------|
| **可维护性 Harness** | ✅ 最成熟 | linter / type-checker / formatter / 复杂度检查 | 已有丰富工具链，廉价且确定 |
| **架构适配性 Harness** | 🟡 中等 | 适应度函数（Fitness Functions） | ArchUnit、性能测试、可观测性规范 |
| **行为正确性 Harness** | 🔴 最弱「房间里的大象」 | AI 生成的测试不够可靠 | approved fixtures 模式在特定领域有效，非通用解法 |

#### Ashby 必要多样性定律

> 调节器必须至少拥有与被调节系统同等的多样性。

- LLM 可以生成几乎任何东西（极高多样性）
- 选定的拓扑结构（框架、模块边界、类型系统）**减少**多样性
- → 综合 Harness 变得可行
- **推论**: 更紧的约束 = 更多的自主权

### 2.3 LangChain 组件解剖（Anatomy — 实现层）

```
                    ┌─────────────────────────────────┐
                    │           AGENT                  │
                    │  ┌──────────┐  ┌──────────────┐  │
                    │  │  Model   │  │   HARNESS    │  │
                    │  │ (权重)   │  │ (一切其他)   │  │
                    │  └──────────┘  │              │  │
                    │                │ System Prompts│  │
                    │                │ Tools / Skills│  │
                    │                │ MCP Servers   │  │
                    │                │ Sandboxes     │  │
                    │                │ Orchestration │  │
                    │                │ Hooks / MW    │  │
                    │                │ Memory/Search │  │
                    │                │ Context Mgmt  │  │
                    │                └──────────────┘  │
                    └─────────────────────────────────┘
```

**Harness 七层组件详解**:

| 层 | 组件 | 解决什么问题 | 实例 |
|:---|:-----|:-----------|:-----|
| 1 | **系统提示词** | 注入核心指令和行为约束 | "你是 XX Agent，遵守以下规则…" |
| 2 | **工具 / Skills / MCP** | 扩展能力边界 | bash、文件读写、web_search、API 调用 |
| 3 | **沙箱基础设施** | 安全隔离的执行环境 | 文件系统、Docker sandbox、浏览器 |
| 4 | **编排逻辑** | 多 Agent / 子任务协调 | sub-agent 孵化、handoff、模型路由 |
| 5 | **钩子 / 中间件** | 确定性执行保障 | 上下文压缩、自动继续、lint 检查 |
| 6 | **记忆与搜索** | 跨 session 知识持久化 | AGENTS.md 文件标准、web search、知识截止日桥接 |
| 7 | **上下文管理** | 对抗上下文腐烂 (Context Rot) | 渐进式披露、compaction、工具输出截断 |

---

## 3. Agent 决策树：何时应用哪个概念

```
你的 Agent 遇到了什么问题？
│
├─ 上下文窗口不够用？
│   ├─ → ❷ 地图而非手册：用 AGENTS.md 渐进式披露
│   ├─ → ❺ 上下文管理：compaction + 工具输出截断
│   └─ → Ralph Loop：每次迭代清空上下文，从文件系统读状态
│
├─ Agent 反复犯同样的错？
│   ├─ → ❸ 机械化执行：写自定义 linter + 内嵌修复指令
│   ├─ → Guides × Sensors：同时加前馈规则和反馈检查
│   └─ → ❻ 熵管理：定期背景扫描 + 自动修复 PR
│
├─ Agent 输出的代码质量差？
│   ├─ → ❸ Linter + 类型检查 + 测试覆盖率（计算性反馈）
│   ├─ → ❹ Agent 可读性：换"无聊"技术栈
│   └─ → AI code review（推理性反馈）
│
├─ 要长时间自主完成任务？
│   ├─ → Ralph Loop 模式：背压门控，持续到完成
│   ├─ → ❶ 仓库即记录系统：文件系统 = 交接面
│   └─ → Symphony：Issue 控制面 + 自动化实现
│
├─ Agent 不知道项目规范？
│   ├─ → ❶ 仓库即记录系统：把规范版本化到 repo
│   ├─ → ❷ AGENTS.md：目录页指向深层文档
│   └─ → Guides（前馈）：Skills + 约束文档
│
└─ 架构在悄悄漂移？
    ├─ → 计算性 Sensors：ArchUnit 结构测试
    ├─ → ❻ 熵管理：定期扫描偏差
    └─ → 推理性 Sensors：AI 审查 + 趋势检测
```

---

## 4. Agent 自检清单："我的 Harness 有多完善？"

每个 Agent 或项目都应该定期评估这 15 项。打分：✅ 已实现 / 🟡 部分 / ❌ 缺失。

### 基础层（可维护性）

| # | 检查项 | 状态 |
|:--|:------|:----|
| 1 | 有 AGENTS.md 且 ≤ 200 行（渐进式披露） | |
| 2 | 有 pre-commit / CI linter 且消息内嵌修复指令 | |
| 3 | 有类型检查作为提交通关门禁 | |
| 4 | 有结构测试（ArchUnit 或等价物）检查模块边界 | |
| 5 | 所有规范/决策以版本化文件存在于仓库中 | |

### 进阶层（架构 + 行为）

| # | 检查项 | 状态 |
|:--|:------|:----|
| 6 | 有适应度函数监控架构特征（性能/可观测性/安全） | |
| 7 | 有自动化的"漂移扫描"定期检查技术债积累 | |
| 8 | 有 approved fixtures 或其他行为正确性验证 | |
| 9 | 有 mutation testing 验证测试质量 | |
| 10 | 有 CI 流水线中分布在正确位置的反馈检查（快→慢） | |

### 编排层（自主执行）

| # | 检查项 | 状态 |
|:--|:------|:----|
| 11 | 支持 Agent 通过 git worktree 独立启动 | |
| 12 | 有 Ralph Loop 或等价长时间自主执行机制 | |
| 13 | 有 Builder-Validator 分离（生成≠审查） | |
| 14 | 有子 Agent 孵化 / 任务分解机制 | |
| 15 | 有 Harness 性能度量（误报率/覆盖率/修复率） | |

---

## 5. 实现模式目录

### 5.1 Ralph Loop — 长时间自主执行

**机制**: bash 脚本反复启动 AI，每次迭代清空上下文，从文件系统读取状态。

```
┌─────────────────────────────────────────────────┐
│  ralph.sh                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │ Iter 1   │ →  │ Iter 2   │ →  │ Iter 3   │…  │
│  │ 干净上下文│    │ 干净上下文│    │ 干净上下文│   │
│  │ 读 prd.json│   │ 读 prd.json│   │ 读 prd.json│  │
│  │ 读 progress│   │ 读 progress│   │ 读 progress│  │
│  │ 写 commit │    │ 写 commit │    │ 写 commit │   │
│  └──────────┘    └──────────┘    └──────────┘   │
│       ↑ git / progress.txt / prd.json ↑          │
└─────────────────────────────────────────────────┘
```

**六大信条** (与 Harness Engineering 的映射):

| Ralph 信条 | Harness Engineering 对应 |
|:-----------|:------------------------|
| Fresh Context Is Reliability | ❹ Agent 可读性 |
| Backpressure Over Prescription | ❸ 机械化执行 |
| The Plan Is Disposable | ❻ 熵管理 |
| Disk Is State, Git Is Memory | ❶ 仓库即记录系统 |
| Steer With Signals, Not Scripts | 人类掌舵 |
| Let Ralph Ralph | Agent 执行 |

**实战项目**: snarktank/ralph (19.9k★), ralph-orchestrator (2.3k★), bmad-ralph (2★)

### 5.2 Symphony — Issue 作为控制面

> "Symphony turns project work into isolated, autonomous implementation runs."

**机制**:
1. 监控 Linear/Jira board 上的 Issues
2. 每个 Issue 自动孵化一个 Agent 实现运行
3. Agent 产出: CI 状态 + PR 审查反馈 + 复杂度分析 + walkthrough 视频
4. 人类只需审批 → 自动合并

**与 Harness Engineering 映射**:

| Symphony 概念 | Harness Engineering 对应 |
|:--------------|:------------------------|
| SPEC.md | Guide（前馈约束） |
| WORKFLOW.md | 程序化 Guide |
| 多语言验证 | Sensor（计算性反馈） |
| Issue 控制面 | ❶ 仓库即记录系统 |

**关键**: Symphony 需要代码库**已经**采用 Harness Engineering 才能工作（读它的 README: "Symphony works best in codebases that have adopted harness engineering"）

### 5.3 Builder-Validator 模式

**原则**: 生成和审查必须分独立会话 — 同一个 Agent 不能既写代码又审代码。

**实施**:
- Builder Agent: 写代码（全能力，无审慎约束）
- Validator Agent: 仅审查（只读，Linter + 结构测试 + 语义审查）
- 循环直到通过所有门禁

### 5.4 模型-Harness 共演化

> 模型变强 → 工具约束可以放宽；模型变弱 → 约束必须收紧

这是一个持续反馈循环: Harness 中的有用原语 → 被吸收进模型训练 → 模型变强 → Harness 可以简化 → 新的缺口出现 → 新的 Harness 原语……

**副作用**: 模型可能过度拟合其训练时的 Harness（例如 Codex 在特定 patch 方法上的性能）。解决方案：为**你的**任务优化 Harness，而非盲目使用默认 Harness。

### 5.5 Anthropic 初始化器 + 编码 Agent — 长时间运行模式

**来源**: Anthropic Engineering, *"Effective harnesses for long-running agents"* (2025-11-26)

**核心问题**: Agent 在跨多个上下文窗口的长时间任务中会遭遇两种失败模式：
1. **试图一次性完成所有工作** — 上下文窗口不够，遗留半实现的 feature
2. **过早宣布胜利** — 看到已有进展就认为任务完成

**解决方案 — 双 Agent 模式**:

| Agent | 职责 | 产出物 |
|:------|:-----|:------|
| **初始化器 Agent** (仅首次运行) | 搭建环境、扩展需求 | `feature_list.json`（200+ 功能规格，全标 `passes: false`）、`init.sh`、`claude-progress.txt` |
| **编码 Agent** (每次迭代) | 每次只做一个 feature，留下干净状态 | 一个 feature 实现 + git commit + progress 更新 + `passes: true` |

**四个失败模式及对策**:

| 失败模式 | 初始化器行为 | 编码 Agent 行为 |
|:---------|:------------|:--------------|
| 过早宣布胜利 | 建立 feature 清单文件 (JSON，所有项初始 `passes: false`) | 每 session 开始读清单，只选一个 feature |
| 遗留 bug 或未记录进度 | 创建 git repo + progress 文件 | 开始: 读 progress + git log + 跑基础测试；结束: git commit + progress 更新 |
| 未充分测试就标记完成 | 建立 feature 清单 | 必须端到端自验证（浏览器自动化工具等），通过后才标记 `passes: true` |
| 不知道如何运行应用 | 写 `init.sh` 脚本 | 每 session 开始跑 `init.sh` |

**关键设计决策**:
- 使用 **JSON** 而非 Markdown 做 feature 清单（模型更不容易不当修改 JSON）
- 使用**强措辞指令**：「删除或修改测试是不可接受的」
- 每次启动必须跑 `pwd` → 读 git log → 读 progress → 读 feature 清单 → 跑基础 E2E 测试（标准化「获取方位」流程，节省 token）

### 5.6 Claude Code Harness — 生产级守卫引擎

**来源**: [Chachamaru127/claude-code-harness](https://github.com/Chachamaru127/claude-code-harness) (v4.14.0, 2.6k★, MIT)

**定位**: Claude Code 的生产级外置 Harness，用 Go 重写所有守卫逻辑。

**架构亮点**:

| 组件 | 实现 | 性能 |
|:-----|:-----|:-----|
| **守卫引擎** | Go 二进制 ~2.5MB，零 CGO 热路径，13 条声明式规则 (R01-R13) | 2-3ms/次 (bash 原版 40-60ms) |
| **钩子系统** | PreToolUse / PostToolUse / PermissionRequest 全部路由到单一 Go 二进制 | `hook-fastpath` 包 <5ms，零文件 I/O、零网络 |
| **5 动词技能** | `plan` → `work` → `review` → `sync` → `release` | 复杂计划自动启用 `team_validation_mode` 子 Agent 验证 |
| **Advisor 策略** | Planner/Critic/Worker 三 Agent 并行，git worktree 隔离，信号量控制并发 | 依赖解析 + 自动合并 |
| **PreCompact 钩子** | 压缩前保存 WIP 状态，压缩后恢复上下文 | 防止压缩破坏当前任务 |
| **跨会话记忆** | HTTP POST 到本地 daemon (port 37888) | daemon 不可用时降级到 JSONL 日志 |

**13 条守卫规则示例**:
- R01: 拒绝 `sudo`
- R03: 阻止受保护路径写入
- R05: `rm -rf` 需确认
- R06: 拒绝 `git push --force`
- T01-T12: 检测测试篡改（如 Agent 偷偷删掉失败测试）
- S01: 检测密钥泄露

**核心教训**: 将 Harness 逻辑从 shell 脚本迁移到编译型语言可带来 10-20x 性能提升，同时解锁静态分析和更好的可测试性。

### 5.7 ralph-orchestrator — Hat 角色系统 + 人在回路

**来源**: [mikeyobrien/ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) (v2.9.3, 2.9k★, MIT, Rust 81.7%)

**定位**: Ralph 的 Rust 进化版，为生产环境设计的编排层。

**核心创新**:

| 特性 | 说明 |
|:-----|:-----|
| **Hat 角色系统** | `code-assist` / `debug` / `research` / `review` / `pdd-to-code-assist` — 每个 Hat 有专门的角色描述和工具集 |
| **事件驱动协调** | Agent 发事件 → Hat 响应事件 → 循环直到 `LOOP_COMPLETE` 或达迭代上限 |
| **多后端支持** | Claude Code / Kiro / Gemini CLI / Codex / Amp / Copilot CLI / OpenCode |
| **背压门控** | 测试 / lint / typecheck 必须通过才能结束循环 |
| **持久记忆** | Memories & Tasks 系统支持跨会话持续学习 |
| **RObot (人在回路)** | Telegram 集成 — Agent 可在循环中途向人类提问并阻塞等待回答；人类可主动发送中途指导 |
| **MCP 服务器模式** | `ralph mcp serve` 作用域限定在单个 workspace root |
| **Web 仪表盘 (Alpha)** | Rust RPC API + 前端，监控编排循环 |

**与 Harness Engineering 的映射**: Hat = 前馈 Guides（角色约束），背压门控 = 反馈 Sensors（质量门禁），RObot = 人类掌舵，持久记忆 = 仓库即记录系统。

---

## 6. Harnessability 评估：你的代码库准备好了吗？

### 6.1 高 Harnessability 的特征

| 特征 | 为什么重要 | 评分 (1-5) |
|:-----|:---------|:----------|
| 强类型语言 | 类型检查 = 免费的计算性 Sensor | |
| 清晰模块边界 | 可定义结构约束规则 | |
| 成熟框架 (Spring/Rails 等) | 框架抽象掉细节，Agent 不需要担心它们 | |
| 良好测试覆盖率 | 计算性反馈的基础 | |
| CI/CD 已就绪 | 反馈循环已有运行场所 | |
| 文档在仓库中（非外部 wiki） | Agent 能读取 | |
| 无巨型单体 (monolith) | 拆分减少每次任务的多样性 | |

### 6.2 绿场 vs 棕场

| | 绿场（新项目） | 棕场（遗留项目） |
|:--|:-------------|:---------------|
| **优势** | 从第一天起 bake in harnessability | 已有业务逻辑可作为参考 |
| **劣势** | 需要同时建立项目 + Harness | 技术债多，Harness 最需要但最难建 |
| **策略** | 技术选型时优先考虑 harnessability | 先建传感器（先测量），再建前馈（再引导） |
| **Ambient Affordances** | 可人为设计 | 需要考古发现 |

---

## 7. 转向循环 (The Steering Loop)

Harness 不是一次性配置，而是**持续的工程实践**:

```
问题发生 → 改进前馈/反馈控制 → 问题变少 → 发现新问题 → 重复

         ┌──────────────────────────┐
         │     Steering Loop        │
         │                          │
         │  观察 Agent 失败模式 ──→  │
         │  设计新的 Guide/Sensor ──→│
         │  部署到 Harness ──→      │
         │  监控效果 ──→ 重复       │
         └──────────────────────────┘
```

**Mitchell Hashimoto 的操作化定义**:
> 「任何时候发现 Agent 犯了错，花时间工程化一个方案使其永不再犯。」

两种工程化形式：
1. **更好的隐式提示 (AGENTS.md)** — 每一行都基于一次 Agent 的不良行为。例：Ghostty 项目的 [AGENTS.md](https://github.com/ghostty-org/ghostty/blob/main/AGENTS.md)
2. **实际的编程工具** — 脚本截图、运行过滤测试等，与 AGENTS.md 更新配套

**关键**: 也可以用 AI 来改进 Harness —— Agent 可以:
- 生成结构测试
- 从观察到的模式草拟规则
- 脚手架自定义 linter
- 从代码库考古创建 how-to 指南

---

## 8. Harness 有效性度量

> Fowler 的开放问题：「如果传感器从不触发，是高质量还是检测不足？我们需要类似于代码覆盖率和 mutation testing 对测试所做的——对 Harness 覆盖率和质量的评估方式。」

### 8.1 Harness 健康度指标

| 指标 | 定义 | 健康值 | 危险信号 |
|:-----|:-----|:------|:--------|
| **传感器触发率** | 每次提交平均触发多少条传感器告警 | 低且稳定（说明前馈有效） | 零且无前馈 = 可能检测不足 |
| **误报率** | 传感器告警中人类审查后判定为「无需修复」的比例 | < 20% | > 40% → Agent 学会忽略告警 |
| **逃逸率** | 通过所有 Harness 但最终被人类发现缺陷的提交比例 | < 10% | > 30% → 传感器覆盖面不足 |
| **修复比例** | Agent 收到传感器告警后成功自我修复的比例 | > 70% | < 30% → 告警信息不够可操作 |
| **前馈/反馈比率** | Guides 数量 vs Sensors 数量 | 1:2 ~ 1:5 | 100% 前馈或 100% 反馈 |
| **Harness 惯性** | 添加一条新规则到生效的平均时长 | < 1 天 | > 1 周 → 转向循环断裂 |
| **传感器灵敏度** | 用 mutation testing 注入已知缺陷后传感器触发率 | > 80% | < 50% → 传感器需要校准 |

### 8.2 度量方法

```
1. 基线测量（Week 0）:
   - 记录当前所有传感器的触发基线
   - 人工审查最近 100 个 PR 中的逃逸缺陷

2. 注入测试（持续）:
   - 每月在代码库中注入 5-10 个已知缺陷类型
   - 检查哪些传感器触发、哪些漏过
   - 对漏过的添加新传感器或调整现有规则

3. Agent 满意度评分（定性）:
   - Agent 报告「传感器消息清晰可操作」的比例
   - Agent 在无传感器指导时主动请求添加规则的比例

4. Harness 覆盖率地图:
   - 将缺陷分类（类型安全 / 架构 / 业务逻辑 / 安全 / 性能）
   - 映射每个类别是否有 Guide + Sensor 覆盖
```

---

## 9. Harness 模板 (未来方向)

大多数企业有几种常见服务拓扑覆盖 80% 需求:
- 通过 API 暴露数据的业务服务
- 事件处理服务
- 数据仪表盘

**Harness 模板 = Guides + Sensors 的预制包**，将 Agent 约束到特定拓扑的结构、规范和技���栈。团队选技术栈时可能开始考虑 "什么 Harness 模板已可用"。

---

## 10. 反模式清单

| 反模式 | 后果 | 正确做法 |
|:-------|:-----|:---------|
| ❌ 把 AGENTS.md 写成万言书 | 挤占上下文 + 无法维护 + 无法机械验证 | → ❷ 地图而非手册：≤100 行入口 + 渐进式披露 |
| ❌ 只有前馈没有反馈 | 不知道规则是否有效 | → 同时部署 Guides + Sensors |
| ❌ 只有反馈没有前馈 | 反复犯同样的错 | → 从传感器数据中提取规则写入前馈 |
| ❌ 标准存在人脑中（Google Docs / Slack） | Agent 不可见 | → ❶ 仓库即记录系统 |
| ❌ 忽略行为正确性 Harness | 「房间里的大象」越来越大 | → 至少用 approved fixtures 覆盖关键路径 |
| ❌ 让同一个 Agent 写代码又审代码 | 认知盲点 | → Builder-Validator 分离 |
| ❌ Harness 之间相互矛盾 | Agent 无法做合理权衡 | → 定期审计 Harness 一致性 |
| ❌ 传感器从不触发就认为没问题 | 可能是检测不足而非质量高 | → 用 mutation testing 验证传感器灵敏度 |

---

## 11. 与其他概念的关系全景

```
                     Harness Engineering
                    （总体框架与哲学）
                          │
          ┌───────────────┼───────────────┐
          │               │               │
     Context          Control         Agent
    Engineering       Theory         Architecture
    （交付机制）      （形式化）      （实现模式）
          │               │               │
    ┌─────┴─────┐   ┌────┴────┐   ┌──────┴──────┐
    │           │   │         │   │             │
  渐进式    上下文  Guides  Sensors  Ralph     Symphony
  披露      压缩    ×        ×      Loop      （编排）
  (Skills) (LCM)  Sensors  (Linter,  (自主执行)  (Issue→PR)
                  (AGENTS  ArchUnit)
                   .md)
```

| 概念 | 与 Harness Engineering 的关系 |
|:-----|:---------------------------|
| **MCP (Model Context Protocol)** | Harness 的**工具/数据连接层**。MCP 服务器 = Harness 第 2 层的一种实现。Harness Engineering 更广，包含编排/上下文/钩子等 |
| **Symphony** | Harness Engineering **原则的具体编排实现**。把 6 大概念操作化为 SPEC.md + WORKFLOW.md + 多语言验证 |
| **Ralph/Loop** | Harness 中**长时间自主执行**的循环原语 |
| **Context Engineering** | Harness Engineering 的**交付手段**。为 coding Agent 设计 Harness 就是特定形式的 Context Engineering |
| **Hermes Workflow (P0-P4)** | Harness Engineering 的**Agent 端执行层实现**（本 wiki 体系内） |
| **AI-Harness-Exploration** | Harness Engineering 的**跨源分析方法**（本 wiki 体系内） |

---

## 12. Agent 可立即使用的模板

### 12.1 最小可行 AGENTS.md 模板

```markdown
# AGENTS.md — [项目名]

## TL;DR
[一句话项目描述 + 技术栈]

## 关键约定
- [最重要规则 1]
- [最重要规则 2]
- [最重要规则 3]

## 在哪里找更多信息
- 架构: [[ARCHITECTURE.md]]
- 规范: [[CONVENTIONS.md]]
- 当前任务: [[tasks/]]

## 质量门禁
- `npm run lint` → 0 错误
- `npm run typecheck` → 0 错误
- `npm run test` → 全绿

## 已知陷阱
- [陷阱 1]
- [陷阱 2]
```

### 12.2 最小可行 Harness 脚手架

```bash
# 1. 创建 AGENTS.md（≤ 100 行入口）
# 2. 配置 pre-commit hook:
#    - linter (eslint / ruff / clippy)
#    - typecheck (tsc / mypy / cargo check)
#    - formatter (prettier / black / rustfmt)
# 3. 添加结构测试 (ArchUnit / dependency-cruiser)
# 4. 设置 CI 流水线（快反馈在前，慢在后）
# 5. 启动漂移扫描 cron job（每周）
```

### 12.3 Ralph Loop 最小实现

```bash
#!/bin/bash
# ralph.sh — 最简 Harness 循环
MAX_ITER=10
for i in $(seq 1 $MAX_ITER); do
  echo "=== Iteration $i ==="
  # 每次迭代清空上下文，只注入:
  # - prd.json (当前任务状态)
  # - progress.txt (历史学习)
  # - AGENTS.md (项目规范)
  claude --prompt "$(cat prompt.md)" --allowedTools "bash,read,write,edit"
  # 检查退出码: 0 = 完成, 2 = 继续
  if [ $? -eq 0 ]; then break; fi
done
```

---

## 13. 完整来源索引（22 篇核心文章 + 5 个旗舰实现）

### 脉络一：AI 时代 Harness Engineering（19 篇）

| # | 文章 | 作者/来源 | 核心贡献 |
|:--|:-----|:---------|:---------|
| 1 | Harness Engineering: Harnessing Codex in an Agent-First World | OpenAI | 六大核心概念 + 100 万行代码实战 |
| 2 | Harness Engineering for Coding Agent Users | Fowler/Böckeler | Guides × Sensors 控制论框架 |
| 3 | Harness Engineering (初版备忘录) | Fowler/Böckeler | 首次社区引入 |
| 4 | The Anatomy of an Agent Harness | LangChain/Vivek | 7 层组件解剖 |
| 5 | Encoding Team Standards | Fowler/Garg | 团队标准机械化 |
| 6 | Feedback Flywheel | Fowler/Garg | 反馈循环工程 |
| 7 | How to Build a Custom Agent Harness | LangChain/Sydney | 实战教程 |
| 8 | Inside the Scaffold (论文) | Rombaut/Huawei/arXiv | 13 个开源 Agent 的源码分类 |
| 9 | Meta-Harness (论文) | Lee/Stanford/arXiv | 自动 Harness 设计：5 模型 +4.7pp |
| 10 | Continual Learning for AI Agents | LangChain/Chase | 3 层学习：权重/Harness/上下文 |
| 11 | Scaling Managed Agents | Anthropic/Lance | Anthropic 的 Agent 管理经验 |
| 12 | Harness Design for Long-Running App Dev | Anthropic Labs | GAN 式 3-Agent 架构 |
| 13 | Agent-driven Development | GitHub/McGoffin | Copilot 应用科学团队的实践 |
| 14 | Agent Evaluation Checklist | LangChain | Agent 评估清单 |
| 15 | Stripe Minions/Blueprints | Stripe | pre-push hook + "shift feedback left" |
| 16 | Symphony (SPEC.md) | OpenAI/Kotliarskyi | Spec-as-Product + 多语言验证 |
| 17 | Effective Harnesses for Long-Running Agents | Anthropic/Young | 初始化器 + 编码 Agent 双模式 / 4 失败模式 + 对策 / feature_list.json 设计 |
| 18 | Claude Code Harness (v4.14.0) | Chachamaru127 | Go 守卫引擎 (13 规则 2-3ms) / 5 动词技能 / Advisor 策略 / PreCompact |
| 19 | ralph-orchestrator (v2.9.3) | mikeyobrien | Rust Hat 系统 / RObot 人在回路 / 事件驱动 / MCP 服务器模式 |

### 脉络二：效率悖论与独立视角

| # | 文章 | 核心视角 |
|:--|:-----|:---------|
| 20 | 为什么 AI 写代码更快但交付没变 (YDD) | 约束理论 + Spec/Rule/Skill 架构 + 洗衣机悖论 |
| 21 | Engineer the Harness (Mitchell Hashimoto) | 操作性定义：「犯错→工程化方案使其永不再犯」+ 6 步 AI 采纳之旅 |
| 22 | Context Engineering | Context Engineering 独立视角 |

### 脉络三：5 个旗舰开源实现

| 项目 | Stars | 语言 | 核心创新 |
|:-----|:------|:-----|:---------|
| [openai/symphony](https://github.com/openai/symphony) | 25k★ | Elixir | Issue 控制面 / SPEC.md / 多语言验证 |
| [snarktank/ralph](https://github.com/snarktank/ralph) | 19.9k★ | Bash | 最简循环 / 干净上下文每次迭代 / prd.json |
| [deusyu/harness-engineering](https://github.com/deusyu/harness-engineering) | 3.5k★ | Shell | 学习档案 / 19 篇文章 + 12 篇翻译 / 5 阶段路线 |
| [mikeyobrien/ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) | 2.9k★ | Rust | Hat 角色 / RObot HITL / 事件驱动 / MCP 模式 |
| [Chachamaru127/claude-code-harness](https://github.com/Chachamaru127/claude-code-harness) | 2.6k★ | Go | 守卫引擎 2-3ms / 5 动词技能 / 13 规则 |

---

## 14. 关联 Wiki 页面

### 本 wiki 内直接关联

- [[concepts/harness-engineering]] — 速览页（本文的精简版）
- [[concepts/fowler-guides-sensors]] — Guides × Sensors 2×2 矩阵深入
- [[concepts/symphony-spec-as-product]] — Symphony：Spec-as-Product 实现
- [[methods/ralph-wiggum-loop]] — Ralph Loop 实战方法
- [[concepts/hermes-workflow]] — Hermes 端 P0-P4 工作流（Harness Engineering 深度融合）
- [[entities/hermes-skill-ai-harness-exploration|ai-harness-exploration]] — 跨源探勘技能
- [[entities/hermes-skill-hermes-workflow|hermes-workflow]] — 执行层技能
- [[concepts/mcp-ecosystem-2026]] — MCP 生态（Harness 第 2 层）
- [[methods/hermes-workflow-and-exploration]] — 双技能方法论

### 外部仓库

- [deusyu/harness-engineering](https://github.com/deusyu/harness-engineering) — 最完整中文学习档案 (3.5k★)
- [openai/symphony](https://github.com/openai/symphony) — 编排实现 (25k★)
- [snarktank/ralph](https://github.com/snarktank/ralph) — Ralph Loop 实现 (19.9k★)
- [harness/harness](https://github.com/harness/harness) — ⚠️ 同名但不同的 DevOps 平台 (36.4k★)，不是本文讨论的 Harness Engineering 范式
- [Chachamaru127/claude-code-harness](https://github.com/Chachamaru127/claude-code-harness) — Go 守卫引擎 (v4.14.0, 2.6k★)
- [mikeyobrien/ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) — Rust Hat 系统 (v2.9.3, 2.9k★)

---

## 15. 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-05-29 | 初始版：从 deusyu/harness-engineering 提取，11 核心概念 + Hermes 映射 |
| v2.0 | 2026-06-05 | **完全重写**: 整合 OpenAI 原文 + Fowler 完整文章 + LangChain 解剖 + 全网补充搜索；新增 Agent 决策树、自检清单、模板、反模式、22 篇完整来源索引；从 Hermes 特化改为框架无关的 Agent 通用手册 |

---

| v2.1 | 2026-06-05 | **深度优化**: 新增 Mitchell Hashimoto 操作性定义 + Anthropic 初始化器/编码 Agent 双模式 + Claude Code Harness v4.14.0 (Go 守卫引擎) + ralph-orchestrator v2.9.3 (Hat 系统 + RObot HITL) + Harness 有效性度量 7 指标 + 4 度量方法 |

---

> **核心领悟**: Harness Engineering 的精髓不是"给 Agent 更多约束"，而是"用正确的约束换取更多的自主权"。Ashby 定律告诉我们：减少系统的多样性，才能用有限的 Harness 有效治理它。这是控制论级别的深刻洞见。
>
> **Mitchell Hashimoto 的工程直觉**: 「给 Agent 快速、高质量的工具，让它能在犯错时自动知道。」这不是学术理论——这是每天花 5 分钟修一个 Harness 缺口，日积月累构建出的工程壁垒。
