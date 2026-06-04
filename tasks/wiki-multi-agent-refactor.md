---
id: wiki-multi-agent-refactor
created: 2026-06-04
updated: 2026-06-04
status: done
owner: agents/main-claude
assignees: [agents/main-claude]
depends_on: []
priority: high
tags: [refactor, wiki, multi-agent, second-brain]
title: Wiki Multi-Agent Refactor
type: task
source: 2026-06-04 Wiki 升级为多 Agent 第二大脑的重构任务
---

# wiki-multi-agent-refactor

## 目标

把 wiki 从"单人知识库"重构为"多 Agent 共享第二大脑"。

## 范围

**包含**:
- 修 21 个死链(已完成)
- 新建 4 个目录:`agents/` `scratchpad/` `protocols/` `tasks/`
- 写 4 个 README / 模板
- 注册首批 Agent
- 写协作协议

**不包含**:
- 不动 hermes/ 运行时
- 不改 git 仓库(用户要求忽略)
- 不部署真正的多 Agent runtime

## 验收标准

- [x] 死链 < 5 个(实际 0,只有 plain text 误报)
- [x] 新建 4 个目录 + 4 个 README
- [x] 至少 2 个 Agent 注册完成
- [x] 1 个 task 演示完整流程
- [x] 1 个 scratchpad 演示短期使用
- [x] CLAUDE.md 整合第 4 层(多 Agent 协作)
- [x] log.md 记录本次变更

## 第二轮(13:00-13:20)— 4 个 P1/P2 改进完成
- 2026-06-04 13:00 — Goal Alignment 协议
- 2026-06-04 13:10 — CODE 工作流
- 2026-06-04 13:15 — A2A 兼容段
- 2026-06-04 13:20 — Per-project CLAUDE.md 模板
- 7 个真改进点全完成

## 第三轮(14:00-14:10)— search fallback 实测修正 + v6.13.0
- 2026-06-04 14:00 — 实测 11 个搜索通道,修正文档
- 2026-06-04 14:05 — 加 § 9.0 完整 fallback 矩阵
- 2026-06-04 14:10 — v6.12.0 → v6.13.0

## 进度日志

- 2026-06-04 11:30 — created
- 2026-06-04 11:35 — 修 21 个死链 → 0
- 2026-06-04 11:50 — 设计 4 目录架构
- 2026-06-04 11:55 — agents/README + main-claude + hermes-self-check 注册
- 2026-06-04 12:00 — scratchpad/README + tasks/README
- 2026-06-04 12:05 — protocols/agent-coordination + 演示 scratchpad

## 关联

- 协议:[[protocols/agent-coordination]]
- 写入规则:[[CLAUDE]]
- 关联任务:[[tasks/cleanup-worker-debris]]
