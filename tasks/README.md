---
title: Task Board — 跨 Agent 任务板
created: 2026-06-04
updated: 2026-06-04
type: meta
tags: [task, multi-agent, kanban, coordination]
source: local
confidence: high
---

# Task Board — 跨 Agent 任务板

> 比 scratchpad 寿命长、比 concepts 灵活。**任务**(goal)有明确起止;**概念**没有。

## 状态机

```
pending → claimed → in_progress → review → done
                     ↓
                   blocked → (等依赖)
```

## 命名

`<task-id>.md` — 短描述性 id,全小写连字符。

例: `wiki-multi-agent-refactor.md`、`hindsight-modes-research.md`

## Frontmatter 必填

```yaml
---
id: <task-id>
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: pending|claimed|in_progress|review|done|blocked
owner: <agent-id>          # 谁负责
assignees: [<agent-id>]   # 谁参与
depends_on: [<task-id>]   # 前置依赖
priority: high|medium|low
tags: [scope-tag, ...]
---

# <task-id>

## 目标
(一句话)

## 范围
- 包含:...
- 不包含:...

## 验收标准
- [ ] ...
- [ ] ...

## 进度日志
- 2026-06-04 11:00 — created
- 2026-06-04 11:30 — claimed by <agent-id>
- ...
```

## 任务分配规则

1. **明确 owner** — 不能悬空(否则谁都没责任)
2. **明确 assignees** — 列出实际干活的人
3. **依赖图清晰** — `depends_on` 必须可追溯到现有任务
4. **任务结束** — 必须移到 `tasks/_archive/` 并在 README 更新索引

## 当前活跃任务

<!-- 由 Agent 扫描生成 -->

参见 [[tasks/index]]

## 关联

- 协议:[[protocols/agent-coordination]]
- 注册:[[agents/README]]
- 写入规则:[[CLAUDE]]
