---
title: "Skill: kanban-orchestrator"
created: 2026-05-28
updated: 2026-05-30
type: entity
tags: [skill, hermes, tool, kanban, multi-agent]
confidence: high
source: Hermes skills/autonomous-ai-agents/kanban-codex-lane/SKILL.md
---

# kanban-orchestrator

Kanban 编排指挥技能 v5.2.0 — 负责任务分解、Round-Robin 分发、依赖链设计、DAG 动态重配置、错误检查与验收。

## 功能

- Round-Robin 分配 5 个 Worker
- 引入 `kanban_batch.py` 辅助批量创建
- DAG 重配置 (`kanban link/unlink`)
- 命名规范: `🔍 💻 📊 📝 👀`
- 上下文治理: 持久 workspace、Worker LCM stateless
- 断路器调优: failure_limit 场景建议

## Sessions Using This Skill
<!-- Sessions archived 2026-06-04, references removed -->

## Related Skills
- [[entities/hermes-skill-kanban-worker]] — Worker 端执行 skill (v3.1.0)
- [[entities/hermes-skill-ai-harness-exploration]] — Worker 默认加载的探勘 skill
- [[concepts/concept-kanban]] — Kanban 概念页
