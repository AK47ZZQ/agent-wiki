---
title: "Harness Engineering 完整框架"
created: 2026-05-29
updated: 2026-05-29
type: concept
tags: [concept, harness-engineering, architecture, method]
confidence: high
source: deusyu/harness-engineering
---

# Harness Engineering

> 从 deusyu/harness-engineering（3.2k★）仓库提取的完整 Harness 工程框架。已深度融合到 [[concepts/hermes-workflow]] 和 [[entities/hermes-skill-ai-harness-exploration|ai-harness-exploration]] 两个核心技能中。

## 核心概念

| 概念 | 说明 | 在 Hermes 中的位置 |
|:----|:----|:-----------------|
| **Harnessability** | 什么值得自动化 — 4 门槛（频率/代价/模式/来源）+ Ashby 定律 | hermes-workflow 核心哲学 |
| **5 关键张力** | 速度 vs 质量 / 自动化 vs 控制 / 通用 vs 特化 / 短期 vs 长期 / 探索 vs 利用 | hermes-workflow 工具决策映射 |
| **CDLA** | 上下文分层架构 — Layer 1 常驻 / Layer 2 按需 / Layer 3 数据引用 | hermes-workflow CDLA 分层 |
| **Spec-as-Product** | Issue 作控制面，先写规格再编码 | hermes-workflow 报告模式 |
| **3 监管维度** | 可维护性 / 架构适配 / 行为正确性 | hermes-workflow 验证映射 |
| **C1-C6 一致性检查** | 计数→交叉验证→结构→链接→声明→追踪 | hermes-workflow Verify 矩阵 |
| **Ralph Loop Exit Code 2** | 用退出码驱动循环：Exit 0=完成 / Exit 2=钩子触发 | hermes-workflow Ralph Loop |
| **Builder-Validator** | 生成与审查必须分独立会话 | hermes-workflow 双代理模式 |
| **Model-Harness 共演化** | 模型更强=工具约束放宽，更弱=约束收紧 | hermes-workflow 模型切换策略 |
| **Guides×Sensors** | Fowler 控制论 2×2 矩阵：前馈 vs 反馈 x 简单 vs 复杂 | ai-harness-exploration Analyze |
| **4 学派** | 约束/架构/控制论/怀疑学派 | ai-harness-exploration 跨源定位 |

## 外部来源

| 来源 | 贡献 |
|:----|:------|
| [[concepts/symphony-spec-as-product]] | Spec-as-Product：Issue 作控制面 +500% PR |
| [[concepts/fowler-guides-sensors]] | Guides×Sensors 控制论 2×2 矩阵 |
| ghuntley/ralph-orchestrator | Ralph Loop Exit Code 2 |
| Anthropic Agent 2026 | Agent 5 核心模式 |
| Review Agent 2026 | Generator≠Reviewer / 5 层质量门禁 |
