---
id: researcher-1
created: 2026-06-04
updated: 2026-06-04
status: active
owner: agents/main-claude
type: agent-instance
template: hermes-kanban-worker
capabilities:
  - web-search-collect
  - read-existing-wiki
  - extract-key-facts
  - write-structured-result
interfaces:
  - input: scratchpad/2026-06-04-agent-stack-test/req-*.md
  - output: scratchpad/2026-06-04-agent-stack-test/result-*.md
last_active: 2026-06-04T14:25:00
---

# Agent Instance: researcher-1

> **实例化**(2026-06-04):从 `hermes-kanban-worker` 模板实例化,专用于本次测试任务的"研究"角色。
> **template**:[[agents/hermes-kanban-worker]]

## 角色

收集 + 整理信息,不写最终报告。
**输入**:orchestrator 的 request 文件
**输出**:结构化 result 文件(已读 wiki 哪些页、提取什么事实)

## 行为协议

1. 启动时读 `agents/hermes-kanban-worker` 模板 + 自己的 `interfaces` 字段
2. 检查 scratchpad/index 找 in-flight 任务
3. 接受 request → 写 `result-NN-research.md` → orchestrator claim done
4. 失败 → 写 `result-NN-failed.md` + 通知 orchestrator

## 失败兜底

- 失联 > 1h:orchestrator 重新分配
- Lock 过期(>600s):orchestrator 可 reassign
- 文件损坏:从 tasks/index 重建

## 测试状态

- **2026-06-04 14:25** — registered
- **2026-06-04 14:25** — 接受 ST-2 任务
