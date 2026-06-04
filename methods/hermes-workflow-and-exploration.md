---
title: "Hermes Agent 自我编码工作流"
created: 2026-05-28
updated: 2026-05-29
type: method
tags: [method, workflow, convention, harness-engineering]
confidence: high
source: hermes-skill
---

# Hermes Agent 自我编码工作流

> 从八源融合（OpenAI Codex + Vibe Coding + Mitchell Hashimoto + Harness Engineering + Anthropic Agent 2026 + ghuntley Ralph Loop + Review Agent + Symphony Spec-as-Product）中提取的 Hermes Agent 实际行为模式，封装为可加载 skill。

## 概况

两个技能互补：**hermes-workflow** 是**执行层**，**ai-harness-exploration** 是**探勘层**。

| 技能 | 版本 | 核心价值 | 定位 |
|:----|:----|:--------|:----|
| [[concepts/hermes-workflow]] | **v4.4.0** | P0-P4 工作流 + Harness Engineering 深度融合 | **执行端** |
| [[entities/hermes-skill-ai-harness-exploration|ai-harness-exploration]] | **v6.0.0** | 6 步探勘法 + 四路并发搜索 + 知识形式化模板 | **发现端** |

## hermes-workflow v4.4.0

### 核心差异化

与市面上其他工作流指南不同，本技能**注入 Agent 的实际行为模式**：

| 板块 | 内容 |
|:----|:------|
| 🎯 **工具决策树** | 22 行工具选择速查表 + execute_code 三案例 |
| 🔬 **验证模式** | C1-C6 一致性检查矩阵 + 全栈自检（10 步）+ 3 监管维度映射 + 5 层质量门禁 |
| 📐 **工作流模式** | 13 个固定模式（Skill 迭代/创建、记忆整理、DSPy、Cron、并行搜索、Agentic MCP、OpenClaw 集成等） |
| 💬 **沟通模式** | 报告结构 + 格式规则 + 成本意识 + 跨引用验证 |
| 🪟 **实际陷阱** | 18 个陷阱（10 Windows + 3 配置 + 3 Skill 作者 + 2 新陷阱） |

### Harness Engineering 完整融合（v4.3+）

| Harness 概念 | 状态 |
|:------------|:-----|
| Harnessability 决策 + Ashby 定律 | ✅ C1-C6 一致性检查矩阵 |
| 5 张力 → 工具决策映射 | ✅ |
| CDLA 3 层上下文 | ✅ Layer 1/2/3 + Token 预算 |
| Spec-as-Product | ✅ 报告 3 步法（ORIENTATION→SPEC→P1/P2） |
| 3 监管维度 → 验证映射 | ✅ |
| Model-Harness 共演化 | ✅ 切换策略 |
| Ralph Loop Exit Code 2 | ✅ 代码级映射 |
| Builder-Validator 双代理 | ✅ 独立会话审查 |
| Agent 5 模式 → P0-P4 | ✅ |

### P0-P4 层级

| 层级 | 操作模式 | 输出 | 费力度 |
|:----|:--------|:----|:------|
| P4 Chat | 纯对话 | 想法/头脑风暴 | 0% |
| P3 Draft | 一次性代码生成 | 代码（无后续） | 30% |
| P2 Edit | 人类审核+选择性采纳 | Code Review | 60% |
| P1 Agent | 代理自动执行+定期检查 | 完整任务 | 80% |
| P0 Harness | 人类主导工程环境 | AGENTS.md+工作流 | 90% |

## ai-harness-exploration v6.0.0

### 6 步探勘法

| 步骤 | 内容 |
|:----|:------|
| Step 0 | 来源质量评估（5 维度） + 已有知识校验 + 来源多样性检查 |
| Step 1 | **Analyze** — 7 子步骤 + 4 轮递进搜索（R1-R4, 6-10 次） |
| Step 2 | **Extract** — Concept/Method/Workflow 三类产物 |
| Step 3 | **Formalize** — Skill/Method/Concept/AGENTS.md 四件套 |
| Step 4 | **Deliver** — 标准化报告 + 3 关键洞察 |
| Step 5 | **Verify** — 18 项检查 + Ralph 6 信条 |
| Step 6 | **Debrief** — 记忆 + 同步 + 兜底 + 凝练 |

### 四路并发搜索引擎

```
同一关键词 ──同时发往── DuckDuckGo (web_search)
                      ┌ tavily-search1 (1000次/月)
                      ├ tavily-search2 (1000次/月)
                      └ mcp_minimax_web_search (云备)
```

### 6 种入口模式

- 🚀 快速分析（了解下/简单说说）→ 3-5 分钟
- 🧠 全量探勘（学习一下/深入挖掘）→ 15-30 分钟
- 🔍 深度延续（继续/还有吗）→ 8-12 分钟
- 🔧 自我优化（优化skill/改进skill）→ 15-30 分钟
- 🧪 技能自测试 → 完整演练
- 🎯 默认 → 全量探勘

### 版本演进（v1.0 → v6.0.0）

| 版本 | 核心变更 |
|:----|:--------|
| v1.0 | 4 步探勘法 |
| v2.0 | +Agent 自省 + 产出模板四件套 |
| v3.0 | +跨源合成法 + 未知→已知过渡 + 验证清单 |
| v4.0 | +AGENTS.md 双通道 + Guides×Sensors + 4 学派 |
| v5.0 | +来源多样性 + 知识成熟度 + Debrief |
| v5.4 | +全引擎兜底 + 并行容错 + Meta 6 步法 |
| v5.6 | +并行搜索重构 + 3 策略表 + 上下文防护 + 配额感知 |
| **v6.0** | **回退链 → 四路并发**（major bump） |

## 使用方式

```bash
# 加载 hermes-workflow
/skill hermes-workflow
# 然后按 P0-P4 层级执行日常编码任务

# 加载 ai-harness-exploration
/skill ai-harness-exploration
# 然后按 6 步法分析新来源
```

## 与现有知识的关系

| 概念 | 关系 |
|:----|:----|
| [[concepts/harness-engineering-deep-study]] | Harness Engineering 完整框架 + Fowler 控制论 + Symphony Spec-as-Product |
| [[concepts/symphony-spec-as-product]] | Spec-as-Product：Issue 作控制面 +500% PR |
| [[concepts/fowler-guides-sensors]] | Guides×Sensors 控制论 2×2 矩阵 |
| [[concepts/ai-coding-tools-comparison]] | 工具选型决策直接嵌入工具决策树 |
