---
title: "Multi-Agent Architecture Patterns — 6 种模式的对比与选型"
created: 2026-06-05
updated: 2026-06-05
type: comparison
tags: [comparison, multi-agent, architecture, orchestration, swarm, ralph-loop]
sources:
  - Anthropic "Building Effective Agents" (Dec 2024): Orchestrator-Workers
  - snarktank/ralph (19.9k★): Ralph Loop
  - OpenAI Swarm: github.com/openai/swarm
  - AutoGen (Microsoft): arxiv.org/abs/2308.08155
  - Generative Agents (Stanford/Google): arxiv.org/abs/2304.03442
confidence: high
---

# Multi-Agent Architecture Patterns — 6 种模式对比与选型

> **为什么需要看懂**: 单 Agent = 一个人的力量。多 Agent = 一支团队的力量。选择错误的架构 = 一个团队都在等人、传话、内耗。

---

## TL;DR — 选型速查

| 模式 | 适用场景 | 协调成本 | 典型项目 |
|:-----|:---------|:--------|:--------|
| **Ralph Loop** | 长时间自主执行单个任务 | 零（每次迭代清上下文） | Ralph (19.9k★) |
| **Orchestrator-Workers** | 动态子任务分解 | 中（中心调度） | Anthropic Canonical |
| **Swarm** | 大量相似并行任务 | 低（无状态 agent 池） | OpenAI Swarm |
| **Hierarchical** | 复杂项目、多层级决策 | 高（上下级协调） | Kanban 编排 |
| **Blackboard** | 无结构问题、多专家协作 | 低（共享状态空间） | 科学发现 Agent |
| **Conversational (AutoGen)** | 需要 Agent 间对话协商 | 中（消息传递） | AutoGen |

---

## 1. Ralph Loop — 单 Agent 循环执行

```
┌──────────────────────────────────────────┐
│ while not complete:                      │
│   fresh_context = load(AGENTS.md)        │
│   state = load(progress.txt, prd.json)   │
│   agent.execute(fresh_context, state)    │
│   if agent.exit_code == 0: break         │
│   save(progress.txt, prd.json)           │
│   git.commit()                           │
└──────────────────────────────────────────┘
```

**优势**:
- 每次迭代清空上下文 → 无上下文腐烂
- 文件系统是唯一状态 → 简单可靠
- 零协调开销

**劣势**:
- 单 Agent 能力上限
- 无法并行执行子任务

**Hermes 中**: [[methods/ralph-wiggum-loop]] = Ralph Loop + hermes-workflow

---

## 2. Orchestrator-Workers — 主从调度

```
┌─────────────────────────────────────┐
│         Orchestrator Agent           │
│    "先做 A → B → C"                 │
│          │        │        │         │
│    ┌─────┘   ┌────┘   └─────┐      │
│    ▼         ▼               ▼      │
│ Worker A   Worker B       Worker C  │
│ (做 A)     (做 B)         (做 C)    │
│    │         │               │      │
│    └─────────┴───────────────┘      │
│              ▼                      │
│         Orchestrator                │
│    "B 做完了，结果可以，继续 D"     │
└─────────────────────────────────────┘
```

**优势**:
- Orchestrator 动态分解任务（不需要预定义）
- Workers 可并行执行
- Orchestrator 可中途调整计划

**劣势**:
- Orchestrator 是单点瓶颈
- 复杂任务的分解质量依赖 Orchestrator 能力

**Hermes 中**: Kanban Orchestrator (`hermes-kanban-orchestrator`) + Workers (`hermes-kanban-worker`)

---

## 3. Swarm — 无状态 Agent 池

```
     ┌─────────────────────────────┐
     │        Task Queue           │
     │  [T1] [T2] [T3] [T4] ...   │
     └──────┬──────────┬───────────┘
            │          │
      ┌─────┘    ┌─────┘
      ▼          ▼
   ┌──────┐  ┌──────┐  ┌──────┐
   │Agent1│  │Agent2│  │Agent3│  ← 无状态，谁接谁做
   └──┬───┘  └──┬───┘  └──┬───┘
      │         │         │
      ▼         ▼         ▼
   结果      结果      结果
```

**优势**:
- 线性扩展：加 Agent = 加吞吐
- 无状态 = Agent 可随时替换
- 容错：一个 Agent 挂了不影响其他

**劣势**:
- 任务必须独立（无依赖）
- 无跨任务学习
- 不适合需要长上下文的任务

**Hermes 中**: `hermes kanban swarm` 模式

---

## 4. Hierarchical — 多层决策

```
            ┌──────────┐
            │  CEO     │  ← 最高决策，"做什么"
            └────┬─────┘
        ┌────────┼────────┐
        ▼        ▼        ▼
   ┌────────┐┌────────┐┌────────┐
   │ PM A   ││ PM B   ││ PM C   │  ← 中层规划，"怎么做"
   └───┬────┘└───┬────┘└───┬────┘
   ┌───┼───┐  ┌──┼──┐  ┌──┼───┐
   ▼   ▼   ▼  ▼  ▼  ▼  ▼  ▼   ▼
  W1  W2  W3  ...           ← 执行层，"做"
```

**优势**:
- 适合大型复杂系统
- 决策和信息在不同层级间分离（降低每层复杂度）
- CEO 只看摘要，Worker 只看细节

**劣势**:
- 信息传递损失（每层 summary 丢失细节）
- 协调成本最高
- 决策延迟长（多层审批）

---

## 5. Blackboard — 共享知识空间

```
       ┌───────────────────────────┐
       │      Blackboard           │
       │  (共享状态 / 知识空间)    │
       │                          │
       │  facts: {...}            │
       │  hypotheses: [...]      │
       │  partial_results: [...] │
       └───┬───┬───┬───┬─────────┘
           │   │   │   │
      ┌────┘   │   │   └────┐
      ▼        ▼   ▼        ▼
   Expert A  Expert B  Expert C
   "我来读"  "我来写"  "我来验证"
```

**优势**:
- 专家 Agent 松耦合
- 天然适合无结构探索型问题
- 新专家可以随时加入/离开

**劣势**:
- Blackboard 可能成为瓶颈（读写竞争）
- 需要专业知识表示格式
- 不适合有明确流程的任务

---

## 6. Conversational (AutoGen) — Agent 间对话

```
Agent A: "我需要 B 提供 X 数据"
Agent B: "X 数据需要 C 先验证格式"
Agent A: "那 B 和 C 先协调，我等着"
Agent B: → → → 找 C
Agent C: "格式 OK，数据发给 B"
Agent B: → → → 回 A
Agent A: "收到，继续"
```

**优势**:
- Agent 间自然协商
- 协议灵活，不需要预定义接口
- 适合需要协商的开放任务

**劣势**:
- 对话可能循环（A 问 B，B 问 C，C 问 A）
- Token 消耗大（每次对话都进上下文）
- 缺少中央协调者时可能发散

---

## 7. 选型决策矩阵

| 问自己 | → 答案 | → 推荐模式 |
|:-------|:------|:----------|
| 任务是单个还是多个？ | 单个 | Ralph Loop |
| | 多个 | ↓ |
| 子任务可以预定义吗？ | 可以 | Swarm（并行）或 Orchestrator-Workers（有依赖） |
| | 不能，需要动态分解 | Orchestrator-Workers |
| 任务之间有依赖吗？ | 有依赖 | Orchestrator-Workers 或 Hierarchical |
| | 无依赖 | Swarm |
| 需要 Agent 之间协商吗？ | 需要 | Conversational (AutoGen) |
| 问题是探索性的（无明确流程）吗？ | 是 | Blackboard |
| 系统非常大（多团队/多层级）吗？ | 是 | Hierarchical |

---

## 8. Hermes 中的模式映射

| Hermes 组件 | 对应模式 | 说明 |
|:-----------|:--------|:-----|
| `hermes-workflow` | ReAct + Ralph | 单 Agent 执行层 |
| `kanban-orchestrator` | Orchestrator-Workers | 中心调度 + 多 worker |
| `kanban swarm` | Swarm | 无状态并行任务池 |
| `hermes-kanban-worker` × 7 | Workers | 轮转执行的 worker 实例 |
| `multi-agent-communication.md` | Conversational | 4 频道协议 |
| `scratchpad/` | Blackboard | 短期共享状态空间 |

---

## 9. 关联 Wiki 页面

- [[methods/ralph-wiggum-loop]] — Ralph Loop 详细实现
- [[concepts/hermes-kanban]] — Hermes Kanban 编排
- [[protocols/agent-coordination]] — 6 通信原语
- [[multi-agent-communication]] — 4 频道通信协议
- [[concepts/agent-reasoning-patterns]] — ReAct / Reflexion (底层推理模式)
- [[concepts/harness-engineering-deep-study]] — Harness 如何支撑多 Agent 架构

---

## 10. 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-06-05 | 初始版：6 种模式 + 决策矩阵 + Hermes 映射 |

---

> **选型第一原则**: 能用简单的就不要复杂的。Ralph Loop 能搞定的不用 Swarm，Swarm 能搞定的不用 Hierarchical。每加一层协调 = 加一类新的失败模式。
