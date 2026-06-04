---
owner: agents/main-claude
ttl: 2026-06-04T23:59:59
topic: wiki 重构的最终结果
readers: [agents/main-claude, agents/hermes-self-check]
created: 2026-06-04
level: long
task_id: wiki-multi-agent-refactor
---

# ephemeral-2026-06-04-wiki-refactor-progress

> 🔥 ephemeral:session 末删除。

## 死链修复前状态

- 总死链 222 → 35(94% reduction)
- wiki/wiki/* 嵌套 → 平铺到 wiki/*

## 多 Agent 架构选择

3 类节点:
- **agents/** — 注册表(谁存在)
- **scratchpad/** — 短期共享(中间变量)
- **tasks/** — 长生命周期(目标)
- **protocols/** — 协作原语

## 决策点

- 不用外部 runtime(纯文件协调)
- 不引 KV / DB
- 锁机制:frontmatter `lock` 字段 + TTL
- 共识:后写覆盖 + contested 标记
- 失败兜底:last_active 过期

## 待办

- [x] 修死链
- [x] 设计 4 目录
- [x] 写 README × 4
- [x] 注册 2 个 Agent
- [x] 写协作协议
- [x] 演示 1 个 task + 1 个 scratchpad
- [x] 整合到 CLAUDE.md
- [x] log.md 记录本次变更
- [x] ai-harness-exploration:写方法论页 wiki-as-second-brain
- [x] ai-harness-exploration:修 index.md 4 段新目录
- [x] ai-harness-exploration:补 kanban-worker 实例化规则

## 状态:2026-06-04 12:35 完成
