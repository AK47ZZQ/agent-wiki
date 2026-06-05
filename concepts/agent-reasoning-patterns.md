---
title: "Agent Reasoning Patterns — CoT / ReAct / ToT / Reflexion"
created: 2026-06-05
updated: 2026-06-05
type: concept
tags: [concept, agent, reasoning, prompt-engineering, cot, react, tot, reflexion]
sources:
  - Chain-of-Thought: Wei et al. 2022, arxiv.org/abs/2201.11903
  - ReAct: Yao et al. 2022, arxiv.org/abs/2210.03629
  - Tree-of-Thought: Yao et al. 2023, arxiv.org/abs/2305.10601
  - Reflexion: Shinn et al. 2023, arxiv.org/abs/2303.11366
confidence: high
---

# Agent Reasoning Patterns — CoT / ReAct / ToT / Reflexion

> **为什么要懂**: 这些是 Agent「怎么想」的基础模式。不是 prompt trick，是改变推理架构的范式。理解它们 = 理解 Agent 为什么能做出好决策。

---

## TL;DR

| 模式 | 核心思想 | 何时用 | 典型提升 |
|:-----|:---------|:------|:--------|
| **CoT** | 一步一步想 | 数学/逻辑推理 | +20-40% 准确率 |
| **ReAct** | 想→做→看→想 (Reason + Act) | 需要工具的任务 | 比纯 CoT 好 20%+ |
| **ToT** | 分支探索 + 回溯 | 需要策略性规划 | Game of 24: 4%→74% |
| **Reflexion** | 从失败中学习 (口头强化学习) | 迭代改进型任务 | HumanEval: 80%→91% |

**递进关系**: CoT（基础推理）→ ReAct（加入行动）→ ToT（加入分支探索）→ Reflexion（加入从失败学习）

---

## 1. Chain-of-Thought (CoT)

> Wei et al., 2022. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"

### 核心思想

让模型在给出最终答案前生成**中间推理步骤**——像人类"一步一步想"。不是改模型，而是改 prompt。

### 示例

```
❌ 标准 prompt:
Q: Roger 有 5 个网球，又买了 2 罐每罐 3 个。他有多少个？
A: 11

✅ CoT prompt:
Q: Roger 有 5 个网球，又买了 2 罐每罐 3 个。他有多少个？
A: Roger 开始有 5 个球。2 罐每罐 3 个 = 6 个球。5 + 6 = 11。答案是 11。
```

### 关键发现

- 在 540B 参数以上的模型上效果显著（较小模型反而可能退化）
- 数学推理 (GSM8K): 从 ~18% 提升到 ~58%（PaLM 540B）
- **零样本 CoT** ("Let's think step by step") 同样有效
- 本质: **增加计算量换取推理质量**（test-time compute scaling）

### 局限

- 纯文本推理，不能调用工具
- 对简单任务反而浪费 token
- 可能在错误路径上越走越远（因为无回溯机制）

---

## 2. ReAct — Reasoning + Acting

> Yao et al., 2022. "ReAct: Synergizing Reasoning and Acting in Language Models"

### 核心思想

```
CoT 循环: Think → Think → Think → Answer
ReAct 循环: Think → Act → Observe → Think → Act → Observe → ... → Answer
```

Agent **交替进行**推理和行动，每次行动的结果（Observe）反馈到下一轮推理中。这是 Claude Code / Codex / Hermes 的底层执行模式。

### 示例（百科问答）

```
Thought: 我需要搜索 Apple Inc 的 CEO
Act: search("Apple Inc CEO")
Observe: Tim Cook is the CEO of Apple Inc since 2011

Thought: 需要验证 Tim Cook 的出生年份
Act: search("Tim Cook born")
Observe: Tim Cook was born November 1, 1960

Thought: 现在可以回答了
Answer: Tim Cook, born 1960, CEO of Apple since 2011
```

### 关键发现

- 在需要外部知识的任务上**大幅优于纯 CoT**（+20-30% 准确率）
- 减少幻觉: Observed 事实约束了推理空间
- **推理 + 行动交替** = 信息收集 + 推理的螺旋
- 这是所有现代 Agent 框架（LangChain、Claude Code、Codex）的内部循环

### Agent 的行动指南

```
你的 ReAct 循环应该:
1. Thought: 我现在知道什么？我需要什么信息？
2. Action: 选择正确的工具获取信息
3. Observation: 工具返回了什么？
4. 重复 1-3 直到有足够信息回答
```

---

## 3. Tree-of-Thought (ToT)

> Yao et al., 2023. "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"

### 核心思想

CoT 是**线性**的（一条推理链），ToT 是**分支**的——同时探索多条推理路径，回溯不好的分支，继续好的分支。

```
CoT: A → B → C → D → Answer
ToT: 
      A
     / \
    B   B'
   / \   \
  C   C'  C''
  |   |
  D   D' (回溯到这里)
  |
 Answer
```

### 机制

1. **生成**: 从当前节点生成多个候选下一步（"分叉"）
2. **评估**: 对每个候选打分（"哪些值得继续"）
3. **搜索**: BFS（广度优先）或 DFS（深度优先）遍历树
4. **回溯**: 死路时回到上一步，尝试其他分支

### 关键发现

- Game of 24: 从 CoT 的 4% → ToT 的 74%（18 倍提升）
- 创造性写作: ToT 生成的文章人类评分更高
- 代价: token 消耗是 CoT 的 5-10 倍

### 何时用 vs 何时不用

| ✅ 用 ToT | ❌ 不用 ToT |
|:---------|:----------|
| 需要策略性规划（下棋、解谜） | 事实性问答 |
| 多步骤路径，需要回溯 | 线性可解的推理 |
| 有明确的评估标准 | Token 预算紧张 |

---

## 4. Reflexion — 从失败中学习

> Shinn et al., 2023. "Reflexion: Language Agents with Verbal Reinforcement Learning"

### 核心思想

**口头强化学习**: Agent 执行任务 → 失败 → 反思为什么失败 → 将反思存为经验 → 下次尝试时读取经验 → 改进。

```
Iteration 1: 执行 → 失败 → "我应该先检查 api 版本"
Iteration 2: 读取上次教训 → 改进了 → 仍然失败 → "还需要处理 pagination"
Iteration 3: 读取两条教训 → 成功！
```

### 机制

```
┌──────────────────────────────────────────┐
│         Reflexion Loop                   │
│                                          │
│  1. Actor: 根据记忆执行任务             │
│  2. Evaluator: 检查结果，发现失败       │
│  3. Self-Reflection: 生成反思文字        │
│     "我失败是因为 X，下次应该 Y"        │
│  4. Memory: 将反思存入 episodic memory   │
│  5. 重复 1-4 直到成功或达到最大迭代     │
└──────────────────────────────────────────┘
```

### 关键发现

- HumanEval 代码生成: GPT-4 基础 80% → Reflexion 达到 91%
- AlfWorld 决策任务: 失败率从 30% → 3%
- 反思文本**不需要人工标注**——LLM 自己生成
- 反思可以跨任务泛化

### 与 Hindsight / Memory 的关系

Reflexion 的 episodic memory **类似 Hindsight 的 L2 记忆**——都是从失败中提取教训，注入未来上下文。区别：
- Reflexion: 反思由 LLM 自己生成，面向短期任务内改进
- Hindsight: 由记忆系统整理，面向跨 session 持久化

---

## 5. 四种模式的组合决策树

```
任务类型？
│
├─ 纯推理（数学、逻辑）
│   └─ → CoT (加 "Let's think step by step")
│
├─ 需要外部信息 / 工具
│   └─ → ReAct (Think → Act → Observe 循环)
│
├─ 需要策略规划 + 多路径探索
│   └─ → ToT (候选生成 + BFS/DFS)
│       └─ 但如果 token 预算紧 → 退回到 ReAct
│
├─ 需要从失败中迭代改进
│   └─ → Reflexion (执行 → 失败 → 反思 → 重试)
│       └─ 可以叠在任何其他模式上（Reflexion + ReAct）
│
└─ 长时间自主执行
    └─ → ReAct + Reflexion + Ralph Loop
```

---

## 6. 现代 Agent 中的实际应用

| Agent/框架 | 内置模式 | 说明 |
|:-----------|:--------|:-----|
| **Claude Code** | ReAct + Reflexion | 底层 think → tool → observe 循环；用户反馈触发反思 |
| **Codex CLI** | ReAct | Reasoning → Bash → Observe 交替 |
| **Hermes** | ReAct + Ralph Loop | hermes-workflow 是 ReAct 的实现；Ralph Loop 是长时间执行层 |
| **LangChain/LangGraph** | ReAct + Reflexion | `create_react_agent()` + `Reflexion` 模块 |

---

## 7. 关联 Wiki 页面

- [[concepts/harness-engineering-deep-study]] — Harness 中嵌入这些推理模式
- [[methods/ralph-wiggum-loop]] — Ralph Loop 叠在 ReAct 上的长时间执行
- [[concepts/hermes-workflow]] — P0-P4 工作流 = ReAct 的具体实现
- [[concepts/agent-memory-state-2026]] — Reflexion ↔ Hindsight 记忆系统
- [[concepts/agent-4-tier-memory-architecture]] — Reflexion 的 episodic memory 对应 L2

---

## 8. 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-06-05 | 初始版：CoT / ReAct / ToT / Reflexion 四种模式 + 决策树 + 现代应用 |

---

> **核心领悟**: Agent 的智能不只来自模型权重，更来自**推理架构**——CoT 给推理深度，ReAct 给外部感知，ToT 给策略选择，Reflexion 给学习能力。最好的 Agent 不是最强的模型，而是最聪明地组合这些模式的 Agent。
