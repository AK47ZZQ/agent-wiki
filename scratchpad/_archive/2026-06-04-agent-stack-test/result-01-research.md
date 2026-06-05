---
title: Researcher Result — 3 Agent 工具对比研究
created: 2026-06-04T14:28:00
updated: 2026-06-04T14:28:00
type: research-result
tags: [agent, multi-agent, comparison, ai-coding, orchestration]
source: wiki/concepts/ai-coding-tools-comparison + wiki/concepts/hermes-kanban + wiki/concepts/symphony-spec-as-product
confidence: high
owner: agents/researcher-1
task_id: 2026-06-04-agent-stack-test
related_to: scratchpad/2026-06-04-agent-stack-test/req-01
---

# Researcher Result — 3 Agent 工具对比研究

> 读 [[scratchpad/2026-06-04-agent-stack-test/req-01|req-01]] 后产出。
> 3 工具 × 4 维度,无新 web 搜索(用 wiki 已有)。

## 3 工具 × 4 维度对比

| 工具 | 定位 | 适用场景 | 已知陷阱 |
|---|---|---|---|
| **AI Coding Tools**(Claude Code/Codex/Cline) | 独立 CLI / IDE 插件 / Agent 框架 | 开发者本地编码 | Harness 兼容性差异;多文件编辑可靠性 |
| **Hermes Durable Kanban** | SQLite 持久化多 Agent 任务板 | 长生命周期任务编排 | 任务分配冲突;worker 失联 |
| **Symphony Spec-as-Product** | Issue tracker 变控制面;Spec 变可交付 | 团队级规模化编码(+500% PR) | 需要团队文化适应;从交互转向目标设定 |

## 关键观察

1. **三者覆盖不同抽象层**:
   - AI Coding Tools = **工具层**(开发者直接用)
   - Hermes Kanban = **任务层**(多 Agent 协调)
   - Symphony = **流程层**(Issue/SPEC 控制整个交付)

2. **Harness Engineering 是公共主题**:
   - 3 个工具都涉及"约束如何嵌入 AI 行为"
   - 不同点:约束的载体(CLI flag vs SQLite row vs Spec)

3. **可组合性**:
   - Hermes Kanban 可调度 AI Coding Tools 作为 worker
   - Symphony Spec 可作为 Hermes Kanban 的任务模板

## 数据点(各源)

| 工具 | 关键数据 | 来源 |
|---|---|---|
| Hermes Kanban | v0.12.0 引入,SQLite 驱动 | [[concepts/hermes-kanban]] |
| Symphony | +500% PR 增量(前 3 周) | [[concepts/symphony-spec-as-product]] |
| AI Coding Tools | 3 工具 × 4 维度对比框架 | [[concepts/ai-coding-tools-comparison]] |

## 给 writer-1 的提示

- 报告聚焦"如何选用",不要全量展开
- 1-page overview(≤ 200 行)
- 至少 2 个 wikilink 出链
- 至少 1 个可执行步骤("如果你要做 X,用 Y")

## 状态

- **2026-06-04 14:28** — 完成,等待 writer-1 接管
- 通知目标:agents/writer-1
