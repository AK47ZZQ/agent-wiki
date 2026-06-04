---
title: Fowler Guides × Sensors 控制论框架
created: 2026-06-02
updated: 2026-06-02
type: concept
tags: [fowler, control-theory, guides-sensors, harness-engineering]
confidence: high
source: works/fowler-harness-engineering-full-translation.md
---

# Fowler Guides × Sensors 控制论框架

> Birgitta Böckeler 和 Martin Fowler 于 2026-04-02 发表的正式文章，将 Harness Engineering 从临时实践提升为**有原则的控制论系统**。

## 2×2 矩阵

| | **计算性**（确定性，CPU） | **推理性**（语义，LLM） |
|---|---|---|
| **前馈/Guides**（行动前） | bootstrap 脚本、OpenRewrite、LSP | AGENTS.md、Skills、ARCHITECTURE.md |
| **反馈/Sensors**（行动后） | linter、ArchUnit、类型检查、覆盖率 | AI code review、LLM-as-judge |

### 前馈（Feedforward）
在 Agent 行动之前指导它 → 提高首次尝试成功率

### 反馈（Feedback）
在 Agent 行动之后观察它 → 实现自我纠正机制

**关键：** 两个维度单独使用都不够。只有反馈 = 同样的错误重复犯；只有前馈 = 无法知道规则是否生效。

## 三个监管维度

| 维度 | 成熟度 | 说明 |
|:----|:------|:------|
| **可维护性 Harness** | ✅ 最成熟 | 内部代码质量，现有工具丰富（linter/type checker/formatter） |
| **架构适配性 Harness** | 🟡 中等 | 适应度函数（Fitness Functions） |
| **行为正确性 Harness** | 🚩 最弱 | 功能正确性验证——**房间里的大象** |

## Ashby 必要多样性定律

**调节器必须至少拥有与被调节系统同等的多样性。**

LLM 可以生成几乎任何东西（高多样性）→ 选定的拓扑结构*减少*多样性 → 综合 Harness 变得可行。这就是"更紧的约束 = 更多自主权"的控制论基础。

## Harnessability（可 Harness 性）

不是所有代码库都同样适合被 harness：强类型、清晰的模块边界、成熟框架、"环境便利设施"（ambient affordances）都重要。

**推论：** Fowler 的技术栈收敛假说可能最终走向 Java，而非 TypeScript/Python。

## 与 [[concepts/hermes-workflow]] 的关系

| Hermes 组件 | Fowler 矩阵位置 |
|:-----------|:---------------|
| `hermes-workflow` skill | 推理前馈（Agent 知道怎么工作） |
| 10 步自检 | 计算性反馈（确定性健康检查） |
| 重启验证 | 计算性反馈 |
| 记忆整理 cron | 计算性反馈 |
| wiki-lint | 计算性反馈（C1-C7 检查的等价物） |
| Dojo improve | 推理反馈（自我改进循环） |
