---
title: Wiki as Second Brain — Agent 怎么用 Wiki + 怎么做好 Wiki
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [wiki, multi-agent, second-brain, meta, knowledge-management, progressive-disclosure, blackboard, PARA]
sources:
  - https://gurusup.com/blog/best-multi-agent-frameworks-2026
---
  - https://medium.com/@Micheal-Lanham/multi-agent-in-production-in-2026-what-actually-survived-f86de8bb1cd1
  - https://openlayer.com/blog/post/multi-agent-system-architecture-guide
  - https://medium.com/online-inference/best-practices-for-building-effective-ai-agents-and-multi-agent-systems-2c7fe11c9605
  - https://solace.com/blog/analysts-say-mas-needs-real-time-context-eda
  - https://www.mindstudio.ai/blog/what-is-ai-second-brain
  - https://www.myyearindata.com/posts/obsidian-second-brain-ai-agents
  - https://medium.com/@AnalyticsAtMeta/how-we-built-an-ai-second-brain-for-60k-knowledge-workers-78c507dd795b
  - https://ericmjl.github.io/blog/2026/3/6/mastering-personal-knowledge-management-with-obsidian-and-ai
  - https://news.ycombinator.com/item?id=48283108
  - https://dev.to/imaginex/ai-agent-memory-management-when-markdown-files-are-all-you-need-5ekk
  - https://jumpcloud.com/it-index/understanding-shared-memory-in-multi-agent-systems
  - https://fme.safe.com/guides/ai-agent-architecture/multi-agent-systems
  - https://medium.com/mongodb/why-multi-agent-systems-need-memory-engineering-153a81f8d5be
  - https://www.nxcode.io/resources/news/obsidian-ai-second-brain-complete-guide-2026
  - https://volodymyrpavlyshyn.substack.com/p/obsidian-supercharged-the-ai-revolution
  - https://www.buildingasecondbrain.com
  - https://workflowy.com/help/para-method
  - https://evernote.com/learn/what-is-the-building-a-second-brain-method-a-practical-guide
  - internal-synthesis
confidence: high
---

# Wiki as Second Brain — Agent 怎么用 Wiki + 怎么做好 Wiki

> **来源**:5 路 web 搜索(2026 多 Agent / 第二大脑 / Obsidian / 文件通信 / PARA) + 11 份内部产物合成。
> **结论**:我的 wiki 设计**部分对、部分错**。7 个真改进点要立刻执行。

## 1. 核心论点(一句话)

**Wiki = 多 Agent 共享第二大脑** = **3 类节点**(registry + scratchpad + tasks) + **1 套协议**(CLAUDE.md 5 层) + **1 套原语**(6 个 communication primitives)。但**对的不代表够** — 2026 业界共识显示 3 个我没做的关键事:**progressive disclosure**、**typed schema 验证**、**A2A-compatible 协议层**。

## 2. Agent 怎么用 Wiki(读协议 — 我的设计 vs 业界)

### 2.1 我的 4 步启动序列

```
Step 1: 读 CLAUDE.md(13K)        → schema + 5 层协议
Step 2: 读 index.md(3.8K)         → catalog
Step 3: 读 agents/README.md(2.6K) → 谁存在 + 怎么注册
Step 4: 读 scratchpad/index.md + tasks/index.md → in-flight
```

### 2.2 业界 2026 共识 vs 我的设计(8 维度)

| 维度 | 业界共识 | 我现在 | 我的差距 |
|---|---|---|---|
| **Progressive Disclosure** | Root CLAUDE.md 5-8K lean,按需 drill 到 per-section (Meta 60K workers 模式) | 13K 单文件 | ❌ Root 太大,违反 "lean context up front" |
| **Typed Schema 验证** | Agent 消息必须 YAML/JSON schema (FIPA-ACL, OACP, fme.safe.com) | Frontmatter 有字段,但**无 schema 校验** | 🟡 schema 文档化,无机械化验证 |
| **A2A-compatible 协议** | 2026 60% MAS 用标准协议 (Gartner 预测) | 6 原语是简化版 A2A | 🟡 命名不一致,缺 a2a-compatible 描述 |
| **Blackboard namespace** | 按 `/extraction/`、`/validation/` 隔离 (fme.safe) | scratchpad 扁平 | 🟡 scratchpad 需加 namespace 规范 |
| **PARA 维度** | Projects / Areas / Resources / Archives 按可操作性分类 (Tiago Forte) | 按主题分类(concepts/methods/...) | 🟡 可加"按可操作性"二级索引 |
| **Goal Alignment Feedback** | Agent 主动告警 "off track" (MyYearInData) | 我只被动响应 | 🟡 加"主动警告"协议 |
| **CODE 流程** | Capture → Organize → Distill → Express (Tiago Forte) | 写协议 2.x 涵盖前 2 步 | 🟡 缺 Distill(提炼)和 Express(表达)工作流 |
| **Tiered Memory** | 3 层 memory (project / org / cross-instance) (OACP, MongoDB) | 3 TTL(ephemeral/short/long)全在 scratchpad | 🟡 需拆 layer:scratchpad=sessions, memory/org=org-wide |

## 3. 怎么创建更好的 Wiki(写协议 — 我的设计 vs 业界)

### 3.1 5 条 DRY 原则(从我的内部合成 + 业界交叉验证)

1. **CLAUDE.md 写 lean root,不写 catalog** — 业界 Meta 模式:5-8K root + per-section drill
2. **index.md 写 catalog,不写 schema** — 单一职责
3. **AGENTS.md 写 memory 规则,不写 vault 协议** — 关注点分离
4. **每个新目录必须有 README.md** — 协议自描述
5. **README.md 不超过 3K** — 超过 = 该拆 sub-README

### 3.2 业界补充的 3 条新原则

6. **Progressive Disclosure**:Agent 启动只读 root,按 folder 加载 per-section CLAUDE.md (Meta 60K workers)
7. **Typed Schema 校验**:每类文件(agent / task / scratchpad)有 frontmatter schema 文档 + 自动 lint
8. **Blackboard Namespace**:scratchpad 按 `task-id/`、`agent-id/` 隔离,避免覆盖冲突 (fme.safe.com)

### 3.3 5 字段铁律(已写,验证 OK)

```yaml
# content page 必填 7 字段
title: ...
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity|concept|method|comparison|note|meta
tags: [...]
source: ...
confidence: high|medium|low
```

### 3.4 6 wikilink 规则(已写,验证 OK)

- 概念解释用反引号 `wikilink`
- skill 引用用反引号
- 跨页用 `[[path|alias]]`
- 每页 ≥2 出链 + ≥1 入链
- 不用大写+空格

### 3.5 **业界新增 1 条**(2026 新发现)

7. **Namespace 隔离**:scratchpad 文件用 `<task-id>/<N>.md` 而非扁平 `result-<N>.md`,避免多任务并发覆盖 (fme.safe.com / MongoDB Memory Engineering)

## 4. 7 个立刻要做的真改进(基于 12 来源交叉验证)

| # | 改进 | 来源 | 工作量 | 优先级 |
|---|---|---|---|---|
| 1 | **拆分 CLAUDE.md** — root 5-8K (5 层总览),详细 5 协议移 `protocols/wiki-protocol-detail-1..5.md` | Meta 60K / Eric Ma | 30 min | 🔴 P0 |
| 2 | **加 frontmatter schema 文档** — `protocols/frontmatter-schemas.md` 列 4 类必填字段 | OACP / fme.safe | 20 min | 🔴 P0 |
| 3 | **scratchpad 改 namespace** — `scratchpad/<task-id>/<N>.md` | fme.safe / MongoDB | 15 min | 🟡 P1 |
| 4 | **加 3rd 协议层** — `protocols/goal-alignment.md` (Agent 主动警告机制) | MyYearInData | 30 min | 🟡 P1 |
| 5 | **加 CODE 流程** — `methods/wiki-code-workflow.md` (Capture/Organize/Distill/Express) | Tiago Forte | 20 min | 🟡 P1 |
| 6 | **加 A2A 兼容段** — 在 `protocols/agent-coordination.md` 顶部加 "Compatible with Google A2A" | A2A / Gartner | 10 min | 🟢 P2 |
| 7 | **加 per-project CLAUDE.md 模板** — `protocols/project-claude-md-template.md` | Eric Ma / Meta | 15 min | 🟢 P2 |

## 5. 5 评估指标(已写 + 业界 2 个新)

我已有的 5 个:
- 协议可达性 / 内容可达性 / 协作可达性 / 索引更新率 / 死链率

业界新增 2 个:
- **Context 预算**:Agent 启动读的总 KB(目标:≤ 15K = 1 屏)
- **Schema 合规率**:frontmatter 字段齐备率(目标:100%)

## 6. 总结:Agent + Wiki 黄金组合(2026 版)

```
┌──────────────────────────────────────────────────────┐
│  Agent 启动 → 读 root CLAUDE.md(5-8K lean)         │
│           → 读 index.md → 找到相关页                  │
│           → 按需 drill 到 per-section CLAUDE.md       │
│           → 注册到 agents/                            │
│           → claim task(在 tasks/)                    │
│           → 写 scratchpad/<task-id>/<N>.md (namespace)│
│           → 完成后 archive,提炼到 concepts/methods    │
└──────────────────────────────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────────┐
│  Wiki: 4 + 2 目录结构                                │
│  agents/  (registry)        — Lean 3 字段(id/status/owner)│
│  scratchpad/  (per-task ns) — Namespace 隔离        │
│  tasks/  (state machine)    — 6 状态                  │
│  protocols/  (per-section)  — 拆 root CLAUDE.md 详细 │
│  concepts/entities/methods/comparisons/notes/refs/   │
│  raw/                                              │
└──────────────────────────────────────────────────────┘
```

## 7. 关键引用(20 来源 — markdown 链接形式)

> **规则**:外部 URL 用 markdown 链接 `[title](url)`,不用 wikilink(避免假死链)。

### 多 Agent 框架
- [Best Multi-Agent Frameworks in 2026 — GuruSup](https://gurusup.com/blog/best-multi-agent-frameworks-2026) — 跨 framework 互操作 + A2A 协议
- [Multi-Agent in Production in 2026: What Actually Survived — Medium](https://medium.com/@Micheal-Lanham/multi-agent-in-production-in-2026-what-actually-survived-f86de8bb1cd1) — 2026 production 共识:orchestrator + bounded
- [Multi-Agent Architecture Guide — Openlayer](https://openlayer.com/blog/post/multi-agent-system-architecture-guide) — 4 模式 + 失败模式
- [Best practices for building effective AI agents — Medium](https://medium.com/online-inference/best-practices-for-building-effective-ai-agents-and-multi-agent-systems-2c7fe11c9605) — tool surface + observability
- [Why Multi-Agent Systems Need Real-Time Context — Solace](https://solace.com/blog/analysts-say-mas-needs-real-time-context-eda) — EDA 实时上下文 + MCP/A2A 标准

### 第二大脑 / Obsidian
- [What Is the AI Second Brain — MindStudio](https://www.mindstudio.ai/blog/what-is-ai-second-brain) — AI Second Brain vs RAG 区别
- [Building a Second Brain with Obsidian and AI Agents — MyYearInData](https://www.myyearindata.com/posts/obsidian-second-brain-ai-agents) — 4 个 Agent 实践(goal alignment + RAG)
- [How We Built an AI Second Brain for 60K Knowledge Workers — Meta](https://medium.com/@AnalyticsAtMeta/how-we-built-an-ai-second-brain-for-60k-knowledge-workers-78c507dd795b) — progressive disclosure
- [Mastering Personal Knowledge Management with Obsidian and AI — Eric J Ma](https://ericmjl.github.io/blog/2026/3/6/mastering-personal-knowledge-management-with-obsidian-and-ai) — 30-40% → <10% overhead 真实案例
- [Obsidian AI Second Brain Complete Guide 2026 — NxCode](https://www.nxcode.io/resources/news/obsidian-ai-second-brain-complete-guide-2026) — 4 插件对比 + Claude Code MCP 集成
- [Obsidian Supercharged: The AI Revolution — Volodymyr Pavlyshyn](https://volodymyrpavlyshyn.substack.com/p/obsidian-supercharged-the-ai-revolution) — Obsidian CLI 100 命令

### 文件通信 / Blackboard
- [Show HN: Cross-agent messaging and shared memory over the local filesystem (OACP)](https://news.ycombinator.com/item?id=48283108) — per-agent inbox/outbox + 3-layer memory
- [AI Agent Memory Management — DEV Community](https://dev.to/imaginex/ai-agent-memory-management-when-markdown-files-are-all-you-need-5ekk) — 文件式 memory vs Vector DB
- [Understanding Shared Memory In Multi-Agent Systems — JumpCloud](https://jumpcloud.com/it-index/understanding-shared-memory-in-multi-agent-systems) — Blackboard architecture
- [Multi-Agent Systems Implementation Best Practices — FME](https://fme.safe.com/guides/ai-agent-architecture/multi-agent-systems) — JSON/YAML + namespace 隔离
- [Why Multi-Agent Systems Need Memory Engineering — MongoDB](https://medium.com/mongodb/why-multi-agent-systems-need-memory-engineering-153a81f8d5be) — RBC 框架 + collective intelligence

### PARA / CODE 方法
- [Building a Second Brain — Tiago Forte 官方](https://www.buildingasecondbrain.com) — Tiago Forte 官方
- [PARA Method — Workflowy](https://workflowy.com/help/para-method) — PARA 4 类别详解
- [Building a Second Brain Method — Evernote](https://evernote.com/learn/what-is-the-building-a-second-brain-method-a-practical-guide) — CODE 4 阶段 + Express

## 8. 关联

- 我的方法论:本文件即
- 协议:[[CLAUDE]]
- 注册:[[agents/README]]
- 任务:[[tasks/wiki-multi-agent-refactor]]
- 演示 scratchpad:[[scratchpad/wiki-multi-agent-refactor/result-01-final]]
- 总结日志:[[log]]
