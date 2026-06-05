---
title: Writer Draft — 3 Agent 工具对比报告
created: 2026-06-04T14:32:00
updated: 2026-06-04T14:32:00
type: comparison-draft
tags: [agent, multi-agent, comparison, selection-guide]
source: scratchpad/2026-06-04-agent-stack-test/result-01-research
confidence: high
owner: agents/writer-1
task_id: 2026-06-04-agent-stack-test
related_to: scratchpad/2026-06-04-agent-stack-test/result-01-research
# Lock 机制测试: writer-1 正在写,其他人勿动
lock: writer-1
locked_at: 2026-06-04T14:32:00
lock_ttl: 600
status: done  # 2026-06-04 14:35 writer-1 完成,release lock
---

# 3 Agent 工具选型对比(草稿)

> 来自 [[scratchpad/2026-06-04-agent-stack-test/result-01-research|researcher-1 的研究]]。
> 本文件正在被 writer-1 编辑(lock 生效中)。

## 1-page 摘要

3 个工具不是竞品 — **它们覆盖不同抽象层**:
- **AI Coding Tools**(Claude Code/Codex/Cline)= **工具层**(开发者直接用,每次任务)
- **Hermes Durable Kanban** = **任务层**(多 Agent 协调,跨任务)
- **Symphony Spec-as-Product** = **流程层**(Issue/SPEC 控制整个团队交付)

**选型决策**:看你的痛点在**哪一层**。

## 决策树(可执行步骤)

```
你现在的痛点是什么?
  │
  ├─ "我写代码慢/代码质量差" → AI Coding Tools
  │   选 Claude Code(质量) / Codex(速度) / Cline(IDE 集成)
  │
  ├─ "我有多个长任务要并行,Agent 互不干扰" → Hermes Kanban
  │   装 hermes-kanban,SQLite 任务板,worker pool
  │
  └─ "团队 5+ 人协作 AI 代码交付" → Symphony
      写 SPEC.md + WORKFLOW.md,Issue tracker 变控制面
      预期 +500% PR 增量(前 3 周)
```

## 何时**不**用

- ❌ AI Coding Tools 不能解决"团队流程"
- ❌ Hermes Kanban 不能解决"开发者手感"
- ❌ Symphony 不能解决"个人效率"

## 可组合

- **Hermes Kanban 调 AI Coding Tools 作为 worker**(任务层调用工具层)
- **Symphony Spec 作为 Hermes Kanban 的任务模板**(流程层驱动任务层)

## 数据点

- Hermes Kanban: v0.12.0 引入,SQLite 持久化
- Symphony: 团队 +500% PR 增量(前 3 周实测)
- AI Coding Tools: 3 主流 × 4 维度对比

## 出链

- [[concepts/ai-coding-tools-comparison]]
- [[concepts/hermes-kanban]]
- [[concepts/symphony-spec-as-product]]
- [[protocols/agent-coordination]] — 多 Agent 协议原语
- [[scratchpad/2026-06-04-agent-stack-test/result-01-research]] — 原始研究

## 状态

- **2026-06-04 14:32** — writer-1 写入,lock 生效
- 下一阶段: main-claude 验证
