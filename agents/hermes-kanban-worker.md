---
id: hermes-kanban-worker
created: 2026-06-04
updated: 2026-06-04
owner: system
status: template
capabilities: [read, write, terminal, code-exec, web-search]
interfaces: [mcp:terminal, mcp:execute_code, mcp:web_search]
tags: [agent, role:worker, multi-agent, template]
---

# hermes-kanban-worker (Worker Agent — 模板)

> 跟 orchestrator 一样,这是模板。实例化后才有独立 id。

## 角色

单一任务的执行者。被 orchestrator 分配一个子任务,完成后回报。

## 能力清单

- 执行:跑 terminal / code / search
- 写:把结果写到 `wiki/scratchpad/result-<task-id>.md`
- 清理:按 orchestrator 指令清理过期 scratchpad

## 接口

- 上游:[[agents/hermes-kanban-orchestrator]]
- 同级:其他 worker(通过 scratchpad 通信)
- 通信:读 `wiki/tasks/<id>.md` 看自己的子任务,完成后写 scratchpad

## 当前状态

- last_active: N/A (template)
- in_flight: 0
- pending: 无

## 实例化规则

1. orchestrator 写 `wiki/tasks/<parent>.md`,assignees 含本 worker 实例
2. worker 启动 → 改 `wiki/tasks/<parent>.md` 的 `status: claimed`
3. worker 开始执行 → `status: in_progress`,追加进度日志
4. worker 完成 → 写 `wiki/scratchpad/result-<N>.md`,改 `status: done`
5. orchestrator 看到 `status: done`,合并结果

**实例化命名规则**(2026-06-04 制定):
- 实例 id: `kanban-worker-<N>`(N=01, 02, ...)
- 实例页: 复制本模板 → 改 `id` 字段
- 同时在 `agents/` 目录创建实例页
- 完成后状态: `status: completed`,保留在 `agents/`(不删,作为历史)

**实例化与模板的关系**:
- 模板:不可变,只读
- 实例:可改 frontmatter,记录 in-flight 状态
- 一个 orchestrator 可同时管理多个 worker 实例

## 失败兜底

- worker 失联 > 1h:orchestrator 重新分配给其他 worker
- worker 写的 scratchpad 文件名冲突:在文件名加 N 后缀
- worker 写的 wiki 页 > 200 行:必须拆分

## 关联

- 上游:[[agents/hermes-kanban-orchestrator]]
- 同级:其他 worker 实例
- 协议:[[protocols/agent-coordination]]
- 任务示例:[[tasks/wiki-multi-agent-refactor]]
