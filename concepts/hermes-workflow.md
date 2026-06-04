---
title: Hermes Workflow — Agent 执行层工作流
created: 2026-05-30
updated: 2026-05-30
type: concept
tags: [workflow, agent, harness-engineering, coding]
confidence: high
source: hermes-workflow skill
---

# Hermes Workflow

> Hermes Agent 的实际行为模式注入技能。P0-P4 AI 编码工作流 + Harness Engineering 深度融合。不是理论指导，而是从真实会话中提取的**实际工作方式**。

## 核心框架

| 层级 | 名称 | 说明 |
|:----|:----|:------|
| P4 Chat | 闲聊/头脑风暴 | 纯对话，无代码操作 |
| P3 Draft | 一次性代码生成 | 无后续维护 |
| P2 Edit | 人类审核+选择性采纳 | 审查 diff 后决策 |
| P1 Agent | 代理自动执行 | 定期检查 |
| P0 HARNESS | 约束系统设计 | Guides×Sensors 控制矩阵 |

## 与 Harness Engineering 的深度融合

- **Harnessability 决策** — 什么任务值得上 P0 约束
- **5 关键张力** — 工具决策映射（速度vs质量、自动化vs控制等）
- **CDLA 上下文分层** — Layer 1 常驻 / Layer 2 按需 / Layer 3 数据
- **Guides×Sensors 控制论矩阵** — Fowler 2×2 前馈/反馈
- **C1-C6 一致性检查** — Skill 自动校验

## 相关页面

- [[concepts/harness-engineering-deep-study]] — Harness Engineering 完整框架
- [[concepts/fowler-guides-sensors]] — Guides×Sensors 控制论
- [[methods/hermes-workflow-and-exploration]] — 双技能互补方法
- [[methods/ralph-wiggum-loop]] — 背压驱动执行模式
