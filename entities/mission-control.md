---
title: mission-control — Agent Fleet 编排仪表盘
created: 2026-06-05
updated: 2026-06-05
type: entity
tags: [tech, hermes, orchestration, dashboard, fleet-management]
source: https://github.com/builderz-labs/mission-control
confidence: high
---

# mission-control — Agent Fleet 编排仪表盘

> **仓库**: [builderz-labs/mission-control](https://github.com/builderz-labs/mission-control) (3.7k+ stars)
> **作者**: [builderz-labs](https://github.com/builderz-labs)
> **成熟度**: production — 稳定、持续维护

## 定位

面向 AI agent 编排的**开源仪表盘**。可管理 agent fleet、分发任务、跟踪成本并协调多 agent 工作流。自托管，基于 SQLite，无需外部数据库依赖。

与 [[entities/hermes-workspace]] (GUI 工作区) 形成互补——Workspace 偏重单 agent 交互体验，mission-control 偏重多 agent 编排与运维。

## 核心功能

| 功能 | 描述 |
|------|------|
| **Fleet 管理** | 管理多个 agent 实例，查看状态、健康度 |
| **任务分发** | 将任务路由到适合的 agent，支持队列和优先级 |
| **成本追踪** | 跟踪 API 调用成本，按 agent/任务/时间维度汇总 |
| **多 agent 协调** | 编排多 agent 工作流，支持依赖关系和并行执行 |
| **自托管** | 全部本地运行，数据存 SQLite，无外部依赖 |

## 在 Hermes 生态中的位置

在 Awesome 清单的三步路径中，mission-control 与 hermes-workspace 并列为 GUI 层选项，但定位不同：

| 维度 | hermes-workspace | mission-control |
|------|-----------------|-----------------|
| 侧重 | 单 agent 交互体验 | 多 agent 编排运维 |
| 受众 | 个人开发者 | 团队 / 生产环境 |
| 面板 | 聊天、终端、技能管理 | 监控、调度、成本 |
| Stars | 500+ | 3.7k+ |
| 部署 | WSL/Docker/Node | 自托管 SQLite |

进阶蓝图中"编排与运维"方案推荐 `mission-control + hindsight` 作为长期运行和团队场景的标准组合。

## 关联页面

- [[concepts/awesome-hermes-agent-ecosystem-2026]] — Awesome 清单全景
- [[entities/hermes-workspace]] — 互补的 GUI 工作区
- [[entities/hermes-workspace-deployment-guide]] — Workspace 部署指南（含 mission-control 对比）
- [[concepts/hermes-kanban]] — Hermes Kanban 编排（多 Worker 模式）
- [[concepts/hindsight-in-hermes-ecosystem-2026]] — 推荐搭配的记忆层
