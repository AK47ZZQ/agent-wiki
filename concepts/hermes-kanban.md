---
title: Hermes Durable Kanban
type: concept
tags: [hermes, kanban, workflow, agent, orchestration]
created: 2026-05-29
updated: 2026-05-29
source: Hermes Docs / GitHub Issues / Community
confidence: high
related:
  - concepts/hermes-codex-runtime.md
---

# Hermes Durable Kanban

Hermes Agent 从 v0.12.0 引入的持久化多 Agent 任务编排系统。SQLite 驱动的任务板，跨所有 Profile 共享。

## 核心定位

`delegate_task` 是函数调用（内存/上下文），Kanban 是持久化工作队列（SQLite 行）。

## 架构

```
┌─────────────────────────────────────┐
│  Dispatcher Daemon (gateway/run.py) │
│  每 tick 扫描板, 分配任务, 生成 worker │
└──────────┬──────────────────────────┘
           │ spawn: hermes -p <profile> chat
           ▼
┌─────────────────────────────────────┐
│  Worker A (profile: researcher)     │
│  Worker B (profile: script-writer)  │
│  Worker C (profile: optimizer)      │
│  每个 worker 是独立操作系统进程       │
└─────────────────────────────────────┘
           │ kanban_* tools
           ▼
┌─────────────────────────────────────┐
│  SQLite Board (~/.hermes/kanban.db) │
│  tasks / task_runs / task_events    │
│  所有 profile 共享同一数据库          │
└─────────────────────────────────────┘
```

## 三种访问面

1. **Web Dashboard** — Hermes 网页面板中的 Kanban 视图
2. **CLI** — `hermes kanban` 命令族
3. **Worker Tools** — 7+ 个 `kanban_*` 工具

## 任务生命周期

```
created → dispatched → claimed → running → completed
                                     ↓ (失败)
                                  blocked → (重试) → running
```

## Worker 工具

| 工具 | 功能 |
|:----|:------|
| `kanban_show` | 获取任务细节 |
| `kanban_complete` | 完成任务+交接(含摘要/元数据) |
| `kanban_heartbeat` | 更新活性+声明TTL |
| `kanban_block` | 阻塞在依赖上 |
| `decompose` / `specify` | 拆分子任务 |

## Checkpoints v2 + /rollback

- 影子 Git 仓库 (`~/.hermes/checkpoints/store/`)
- 内容可寻址，跨项目去重
- 真正裁剪 + 磁盘防护
- 回滚范围：文件系统 + Kanban 卡片 + 运行中目标 + 内存指针
- 默认关闭，`--checkpoints` 按会话启用

| 命令 | 功能 |
|:----|:------|
| `/rollback <N>` | 恢复到检查点 N |
| `/rollback diff <N>` | 预览差异 |
| `/rollback <N> <file>` | 恢复单文件 |

## 心跳机制

- **双重心跳**: `kanban_heartbeat` 工具调用 + 自动桥接
- **声明 TTL**: 15 分钟
- **看门狗**: 调度程序读取心跳字段，超时标记为 zombie

## 生产案例

1. **4-Agent 内容流水线** — 研究→脚本→X优化→Supabase，每周 cron
2. **SEO 网站生成** — 50 页并行 Worker
3. **Fleet Farming** — 同质 Worker 并行处理独立任务

## 已知痛点

- SQLite 并发限制（PostgreSQL 适配器已提议）
- Profile 作用域 DB 隔离问题
- 心跳不延长 claim_expires 导致 Worker 被误回收
- 无全局 `max_active_tasks` 配置

## 关联

- → [[concepts/hermes-codex-runtime|Codex Runtime]]
