---
title: Harness Engineering 速览
created: 2026-05-30
updated: 2026-06-05
type: concept
tags: [harness-engineering, method, agent-patterns, control-theory]
confidence: high
sources:
  - openai.com/index/harness-engineering
  - martinfowler.com/articles/harness-engineering.html
  - github.com/deusyu/harness-engineering (3.5k★)
---

# Harness Engineering — 速览

> **Agent = Model + Harness**。完整手册见：[[concepts/harness-engineering-deep-study]]（v2.0，24KB，Agent 开箱即用）

## 一句话

传统工程：人类写代码 → 机器执行
Harness Engineering：人类设计约束 → Agent 写代码 → 机器执行

## 三大框架速览

| 框架 | 来源 | 核心 |
|:-----|:-----|:-----|
| **6 大核心概念** | OpenAI (2026-02) | 仓库即记录系统 / 地图非手册 / 机械化执行 / Agent 可读性 / 吞吐量合并 / 熵管理 |
| **Guides × Sensors** | Fowler/Böckeler (2026-04) | 前馈×反馈 × 计算性×推理性 = 2×2 矩阵 + 3 监管维度 |
| **7 层组件解剖** | LangChain (2026-03) | 系统提示词 → 工具 → 沙箱 → 编排 → 钩子 → 记忆 → 上下文管理 |

## 关键概念速查

| 概念 | 说明 |
|:----|:------|
| **Harnessability** | 代码库是否适合被 Agent 治理（强类型、清晰边界、成熟框架 = 高分） |
| **Ashby 定律** | 调节器多样性 ≥ 被调节系统多样性。紧约束 = 更多自主权 |
| **Guides × Sensors** | 前馈指导 + 反馈检测 → 两者缺一不可 |
| **Ralph Loop** | 每次迭代清空上下文，从文件系统读状态，背压门控驱动持续执行 |
| **Symphony** | Issue 作控制面，Agent 自动实现 → PR，人类只需审批 |
| **Builder-Validator** | 生成与审查必须分独立会话 |
| **模型-Harness 共演化** | 模型变强 → 约束放宽；模型变弱 → 约束收紧 |

## 3 个监管维度

| 维度 | 成熟度 | 现状 |
|:-----|:------|:-----|
| **可维护性** | ✅ 最成熟 | Linter / 类型检查 / Formatter 已完备 |
| **架构适配性** | 🟡 中等 | 适应度函数（Fitness Functions） |
| **行为正确性** | 🔴 最弱 | "房间里的大象"——AI 生成的测试不够可靠 |

## Agent 最小启动清单

- [ ] AGENTS.md ≤ 100 行（渐进式披露入口）
- [ ] Linter + Typecheck 作为提交通关门禁
- [ ] 结构测试检查模块边界
- [ ] CI 流水线分布快→慢反馈
- [ ] 漂移扫描 cron job

## 相关页面

- [[concepts/harness-engineering-deep-study]] — **完整手册 v2.0**（Agent 决策树 + 自检清单 + 模板 + 19 篇来源索引）
- [[concepts/fowler-guides-sensors]] — Guides × Sensors 控制论深入
- [[concepts/symphony-spec-as-product]] — Symphony 编排实现
- [[methods/ralph-wiggum-loop]] — Ralph Loop 实战方法
- [[concepts/hermes-workflow]] — Agent 端执行层实现
- [[concepts/mcp-ecosystem-2026]] — MCP 作为 Harness 第 2 层
