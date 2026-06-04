---
title: Scratchpad — 共享短期工作记忆
created: 2026-06-04
updated: 2026-06-04
type: meta
tags: [scratchpad, ephemeral, multi-agent, coordination]
source: local
confidence: high
---

# Scratchpad — 共享短期工作记忆

> Agent 之间的"走廊对话":用完即弃,只保留必要的中间状态。

## 三种 TTL 等级

| 等级 | 命名 | TTL | 用途 | 清理方式 |
|---|---|---|---|---|
| **🔥 ephemeral** | `scratchpad/{task-id}/ephemeral-<date>-<topic>.md` | session 结束 | 一次对话内的中间变量 | session 末由 owner Agent 删除 |
| **⏱ short** | `scratchpad/{task-id}/short-<date>-<topic>.md` | 7 天 | 跨 session 但不需要永久保留 | 由 [[agents/hermes-kanban-worker]] 每周清 |
| **📌 long** | `scratchpad/{task-id}/long-<date>-<topic>.md` | 永久 | 重要的中间状态(进度报告、协议状态) | 不自动清,手动归档 |

## Namespace 隔离(2026-06-04 改进)

**所有 task 必须在 `<task-id>/` 子目录下**,避免多任务并发覆盖:

```
scratchpad/
├── README.md                    # 本文件
├── index.md                     # 活跃任务清单
├── _archive/                    # 已完成任务
│   └── <task-id-archived>/
└── {task-id}/                   # 每任务独立 namespace
    ├── index.md                 # 任务 workspace 入口
    ├── result-01.md             # 输出
    ├── intermediate-01.md       # 中间状态
    └── final.md                 # 终态
```

**好处**:
- 多任务并发不会覆盖彼此文件
- 任务结束 = `mv scratchpad/{task-id}/ scratchpad/_archive/`
- 其他 Agent 读 `<task-id>/index.md` 知道这任务的所有状态文件

**当前活跃任务 namespace**:
- `scratchpad/wiki-multi-agent-refactor/` — wiki 改造为多 Agent 第二大脑(2026-06-04)

## 协议

### 读
- 任何 Agent 在动手前**必须**先 grep scratchpad,看是否有相关进行中任务
- 找到相关 → 先读再决定

### 写
- 命名:`<level>-YYYYMMDD-<short-topic>.md`
- 文件头必须有 YAML frontmatter,声明:
  - `owner` (哪个 Agent 写的)
  - `ttl` (到期日)
  - `topic` (一句话)
  - `readers` (哪些 Agent 需要读)
- 写完必须在 `index.md` 加一条目

### 删
- TTL 到期由 [[agents/hermes-kanban-worker]] 清理
- ephemeral 在 owner session 末尾由 owner 删除

## 锁机制(可选)

如果需要"独占写",在文件 frontmatter 加:
```yaml
lock: <agent-id>
locked_at: <ISO timestamp>
lock_ttl: 600  # 秒
```

其他 Agent 检测到 lock 存在 + 未过期 → 不写,**只读**。

## 当前 scratchpad 状态

<!-- 每次访问时由 Agent 扫描生成 -->

参见 [[scratchpad/index]]

## 关联

- 协议:[[protocols/agent-coordination]]
- 注册:[[agents/README]]
- 任务:[[tasks/README]]
- 写入规则:[[CLAUDE]]
