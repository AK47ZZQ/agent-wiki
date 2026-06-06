---
title: "Context Engineering — 把上下文窗口当作工程资源来管理"
created: 2026-06-05
updated: 2026-06-05
type: concept
tags: [concept, context-engineering, agent, prompt-design, progressive-disclosure]
sources:
  - anthropic.com/engineering/building-effective-agents (Dec 2024)
  - promptingguide.ai (Context Engineering section)
  - martinfowler.com/articles/harness-engineering.html § sidebar
confidence: medium
source: harness-engineering-2026
---

# Context Engineering — 把上下文窗口当作工程资源来管理

> **一句话**: Context Engineering 是 Harness Engineering 的**交付层**——设计了约束系统（Harness），需要通过精心设计的上下文（Context）将它注入 Agent。上下文窗口不是无限的——它是一个需要预算、优化、审计的工程资源。

---

## TL;DR

| 原则 | 一句话 |
|:-----|:------|
| **上下文是预算** | 每个 token 进上下文 = 占用推理能力。浪费 = 降低 Agent 质量 |
| **渐进式披露** | 不是一次性灌入所有信息，而是按需逐步展开 |
| **工具 = 上下文** | 工具描述不是免费的——每个参数描述都在争抢注意力 |
| **信息新鲜度 > 完整度** | 最新的 100 行 > 一个月前的 5000 行全文 |

---

## 1. 上下文作为稀缺资源

### 1.1 为什么上下文需要工程化

```
模型训练后不变的部分: 权重 (Weights)
每次调用都变的部分:   上下文 (Context)

工程可以控制的 = 上下文
工程不能控制的 = 权重
```

**上下文窗口是 Agent 唯一能"看见"的东西。** 放进去什么、按什么顺序放、什么时候放——这些决策直接决定了 Agent 能多好地完成任务。

### 1.2 上下文腐烂 (Context Rot)

随着对话继续，上下文窗口被填满，Agent 的推理能力**逐渐下降**:

```
Session 开始时:   ████████████░░░░░░░░ (50% 满, 推理质量 95%)
Session 中期:     ██████████████████░░ (70% 满, 推理质量 80%)
Session 末期:     █████████████████████ (95% 满, 推理质量 40%)
                                         ↑ 上下文腐烂
```

**对抗策略**:
| 策略 | 说明 | Hermes 中的实现 |
|:-----|:-----|:--------------|
| 压缩 (Compaction) | 将旧对话总结为摘要 | LCM compaction |
| 截断 (Offloading) | 大工具输出只保留头尾，完整内容写文件 | 工具输出 > 阈值 → 写 scratchpad |
| 渐进式披露 | 只加载当前需要的上下文 | Skills 的 frontmatter → body 模式 |
| 清空重建 (Ralph Loop) | 每次迭代完全清空上下文 | Ralph Loop |

---

## 2. 工具设计 = 上下文设计

### 2.1 工具描述不是免费的

Anthropic 的原则:
> "从模型的角度思考——这个工具的使用方式是否显而易见？"

每条工具描述、每个参数说明都在**消耗上下文预算**。10 个工具，每个 500 字的描述 = 5000 tokens 的固定开销，**每次调用都付一次**。

### 2.2 工具上下文的 4 条原则

| 原则 | 做法 | 反模式 |
|:-----|:-----|:------|
| **精简描述** | 参数名自解释 → 不加冗余说明 | `user_name` 还加 "The name of the user" |
| **示例优先** | 在 description 里给 1 个示例 | 只有抽象描述没有示例 |
| **渐进式加载** | 核心工具常驻，小众工具按需加载 (Skills 模式) | 100 个工具全部挤进系统提示词 |
| **错误消息即文档** | 工具返回的错误信息里嵌入修复指南 | 只返回 "Error: 400" |

---

## 3. 上下文分层的 4 层模型

```
┌───────────────────────────────────────────┐
│ Layer 1: 不可变核心 (常驻, ~20% 预算)      │
│ system prompt + AGENTS.md + 关键约定       │
├───────────────────────────────────────────┤
│ Layer 2: 按需注入 (首次使用才加载, ~10%)   │
│ Skills 正文 / 架构文档 / 规范              │
├───────────────────────────────────────────┤
│ Layer 3: 即时检索 (运行时搜索, ~20%)       │
│ web_search / MCP query / 代码库搜索        │
├───────────────────────────────────────────┤
│ Layer 4: 会话动态 (最不稳定, ~50%)         │
│ 对话历史 / 工具调用结果 / 中间输出         │
└───────────────────────────────────────────┘
```

### 每层的管理策略

| 层 | 何时加载 | 何时卸载 | 成本 |
|:---|:---------|:---------|:-----|
| L1 核心 | Agent 启动 | 永不（短到极限） | 一次性 |
| L2 按需 | 用户触发 / Agent 判断需要 | 任务完成后压缩 | 按任务 |
| L3 检索 | 每次查询时 | 查询结束即丢 | 每次查询 |
| L4 动态 | 持续累积 | 压缩/截断/清空 | 持续增长 |

---

## 4. AGENTS.md 设计 — Context Engineering 的旗舰案例

AGENTS.md 是上下文工程的核心产物。设计得好的 AGENTS.md:

### 4.1 好设计

```markdown
# AGENTS.md — project-x (12 行)

## TL;DR
Python 后端 + React 前端。用 `make dev` 启动。

## 关键规则
- 所有 API 返回 JSON:API 格式
- 禁止直接用 `os.system()` — 用 `subprocess.run()`
- 数据库 migration 用 Alembic

## 更多信息
- 架构: [[docs/ARCHITECTURE.md]]
- API 约定: [[docs/API-CONVENTIONS.md]]
- 部署: [[docs/DEPLOY.md]]

## 质量门禁
make lint && make typecheck && make test
```

**为什么好**: 12 行，核心信息全在，深层次内容通过链接渐进式披露。Agent 读完知道"规则是什么 + 去哪里找更多"。

### 4.2 坏设计

```markdown
# AGENTS.md — project-x (287 行)

## 项目背景（30 行）
本项目始于 2023 年，最初是一个...（历史）

## 架构（80 行）
系统采用微服务架构，包括服务 A、服务 B...（全架构文档）

## API 规范（100 行）
所有 API 必须...（完整规范）

## 常见问题（77 行）
Q: 为什么选 React 而不是 Vue？
A: ...
```

**为什么坏**: 287 行 = 每次 Agent 启动浪费 ~3000 tokens 在可能用不到的信息上。这是 Harness Engineering 的反模式 "Map, Not Manual" 所反对的。

---

## 5. Context Engineering 与 Harness Engineering 的关系

```
Harness Engineering        Context Engineering
(设计约束系统)              (把约束注入 Agent)
        │                        │
        │  "要检查 linter"        │  "把 lint 规则写进上下文"
        │  "要跟 AGENTS.md"       │  "设计 AGENTS.md 的层级"
        │  "要用 Skills"          │  "Skills 什么时候加载"
        │                        │
        └────────┬───────────────┘
                 │
          两者协同 = 好的 Agent 体验
```

Fowler 的原话:
> "Context engineering provides us with the means to make guides and sensors available to the agent. Engineering a user harness for a coding agent is a specific form of context engineering."

---

## 6. 关联 Wiki 页面

- [[concepts/harness-engineering-deep-study]] — Harness 的 Guides × Sensors 依赖 Context Engineering 作为交付层
- [[methods/agent-writing-standard]] — 写 AGENTS.md 时如何避免上下文污染
- [[concepts/agent-memory-state-2026]] — 记忆系统是 Context Engineering 的信息来源
- [[concepts/agent-4-tier-memory-architecture]] — L1/L2/L3 记忆分别注入哪层上下文
- [[methods/ralph-wiggum-loop]] — Ralph Loop = 终极上下文清空策略

---

## 7. 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-06-05 | 初始版：上下文预算 / 工具设计 / 4 层模型 / AGENTS.md 设计 |

---

> **核心领悟**: 给 Agent 最好的信息不是最多的信息，而是**刚好够用且刚好在需要时出现**的信息。Context Engineering 就是把"刚好"变成可工程化的实践。
