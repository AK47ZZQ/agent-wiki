---
id: writer-1
created: 2026-06-04
updated: 2026-06-04
status: active
owner: agents/main-claude
type: agent-instance
template: hermes-kanban-worker
capabilities:
  - read-research-output
  - write-structured-comparison
  - validate-frontmatter-schema
  - update-wiki-index
interfaces:
  - input: scratchpad/2026-06-04-agent-stack-test/result-01-research.md
  - output: scratchpad/2026-06-04-agent-stack-test/result-02-draft.md
last_active: 2026-06-04T14:25:00
---

# Agent Instance: writer-1

> **实例化**(2026-06-04):从 `hermes-kanban-worker` 模板实例化,专用于本次测试任务的"写作"角色。
> **template**:[[agents/hermes-kanban-worker]]

## 角色

消费 researcher 的研究输出,写结构化对比报告。
**输入**:researcher 的 result-01-research.md
**输出**:result-02-draft.md(带完整 frontmatter + 内部 wikilink)

## 行为协议

1. 启动时读 researcher 的研究输出
2. 验证 frontmatter 9 字段(否则报错)
3. 写 report(1-page overview + ≥ 2 wikilink + ≥ 1 可执行步骤)
4. 用 `lock: writer-1` + `lock_ttl: 600` 防止 orchestrator 误读部分写入
5. 完成 → release lock,通知 orchestrator

## 失败兜底

- 失联 > 1h:orchestrator 重新分配
- Lock 过期(>600s):orchestrator 可 reassign

## 测试状态

- **2026-06-04 14:25** — registered
- **2026-06-04 14:25** — 接受 ST-3 任务
