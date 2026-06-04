---
title: Hermes Workspace (outsourc-e)
created: 2026-05-31
updated: 2026-06-05
type: entity
tags: [tool, ui, web, automation, orchestration]
confidence: high
sources: [outsourc-e/hermes-workspace GitHub, NousResearch/hermes-agent, wiki-ingest]
---

# Hermes Workspace (outsourc-e)

> 源分析: [[entities/hermes-workspace-architecture]] | 部署指南: [[entities/hermes-workspace-deployment-guide]]

## 核心定义

Hermes Agent 的**全功能 Web 工作空间**——不仅是聊天界面，而是集 ChatGPT、Dashboard、MCP 管理器、Kanban 看板、Swarm 编排于一体的 Agent 运营中心。零 Fork 设计，直接对接上游 NousResearch/hermes-agent。

## 基本信息

- **GitHub**: [outsourc-e/hermes-workspace](https://github.com/outsourc-e/hermes-workspace) (⭐ 5,110)
- **版本**: v2.3.0 | **许可证**: MIT | **语言**: JavaScript (React + Vite)
- **发布时间**: 2026-03-16 | **活跃迭代中**

## 架构原理

### 三层架构

```
Workspace (:3000) — React SPA (PWA 可安装)
  │
  ├── Gateway API (:8642) — OpenAI Chat Completions + SSE 流式
  │    作用: 聊天、Agent 交互、会话管理
  │
  └── Dashboard API (:9119) — FastAPI (REST)
       作用: 配置/会话/Skills/Kanban/MCP/Cron/Profiles 管理面
```

### Zero-Fork 设计

不 Fork Hermes Agent 代码库——Workspace 直接对接上游标准 API。Gateway 暴露 OpenAI 兼容接口，Dashboard API 提供管理面，Workspace 同时连接两个接口。

### Conductor 任务编排

Dashboard API 驱动的 DAG 编排引擎：LLM 任务分解 → Kanban 创建（含依赖链） → Dispatcher 轮询 spawn Worker → Worker 执行 → 汇总。SQLite 持久化，跨重启不丢。

### Swarm Mode (多 Agent 编排)

tmux-based 持久 Worker 池管理。Workspace 前端通过 tmux panes 实时展示 Worker 状态。支持 `hermes kanban swarm` CLI 一键扇出扇入。与 [[entities/hermes-skill-kanban-orchestrator|kanban-orchestrator]] 的 Kanban Worker 配置完全匹配。

## 关键功能

| 功能 | 支持度 | 说明 |
|:-----|:------:|:-----|
| ChatGPT (SSE 流式) | ✅ | 完整聊天体验 |
| 多会话管理 | ✅ | |
| Memory 实时编辑 | ✅ | 浏览 + 搜索 + 编辑 |
| Skills 市场 (2,000+) | ✅ | 来源标签 + 过滤 + 源路径 |
| **MCP 完整管理** | ✅ | 唯一支持可视化 MCP 管理的 UI |
| 文件浏览器 (Monaco) | ✅ | 内嵌代码编辑器 |
| **内置 PTY 终端** | ✅ | 跨平台 |
| **Swarm 多 Agent** | ✅ | tmux Worker 池 |
| **Conductor 编排** | ✅ | 任务分解 + 依赖链 |
| **Kanban 集成** | ✅ | 直接对接 7 Worker |
| Agent 实时面板 | ✅ | 状态/队列/用量 |
| Dashboard 总览 | ✅ | 会话/模型/成本/注意卡 |
| PWA 安装 | ✅ | 可装成桌面应用 |
| Tailscale 远程 | ✅ | 内置远程访问方案 |
| 5 种主题 | ✅ | Hermes/Nous/Bronze/Slate/Mono |
| 密码保护 | ✅ | |

## 与当前环境的匹配度

我们的配置：**7 Kanban Worker + MiniMax MCP + Tavily MCP 搜索链 + Gateway :8642 运行中 + Node 24/pnpm 11.3**

| 需求 | 匹配度 | 说明 |
|:-----|:-----:|:-----|
| Kanban Worker 可视化 | ⭐⭐⭐⭐⭐ | 原生 Kanban 面板 |
| MCP 管理 | ⭐⭐⭐⭐⭐ | 唯一支持 /mcp 页面的 UI |
| Swarm 编排 | ⭐⭐⭐⭐⭐ | tmux Worker 池管理 |
| Conductor 分解 | ⭐⭐⭐⭐⭐ | Dashboard 驱动 |
| MiniMax + Tavily MCP | ⭐⭐⭐⭐ | 通过 Agent MCP API 暴露 |
| Windows 部署 | ⭐⭐⭐ | 推荐 Docker 或 clone+pnpm dev |
| 远程访问 | ⭐⭐⭐⭐⭐ | PWA + Tailscale |

## 部署方式

### 方式 1: 指向现有 Hermes Agent（推荐，3 分钟）

```bash
git clone https://github.com/outsourc-e/hermes-workspace.git ~/hermes-all/projects/hermes-workspace
cd ~/hermes-all/projects/hermes-workspace
pnpm install
cp .env.example .env
# 编辑 .env:
# HERMES_API_URL=http://localhost:8642
# HERMES_DASHBOARD_URL=http://localhost:9119
pnpm dev   # → http://localhost:3000
```

### 方式 2: Docker Compose

```bash
git clone → cd → docker compose up -d → localhost:3000
```

### 前置条件

- ✅ Node.js 22+（当前 **24.15.0** ✅）
- ✅ pnpm（当前 **11.3.0** ✅）
- ✅ Gateway :8642 运行中（已确认 ✅）
- ❌ Dashboard :9119 未运行（需 `hermes dashboard` 启动）

## 与同类 UI 对比

| 维度 | 官方 Dashboard | hermes-webui (9.5k⭐) | hermes-desktop (8.8k⭐) | **hermes-workspace (5.1k⭐)** |
|:-----|:-------------:|:--------------------:|:---------------------:|:--------------------------:|
| 聊天 | ❌ (仅 TUI) | ✅ | ✅ | ✅ |
| MCP 管理 | ❌ | ❌ | ❌ | **✅** |
| Swarm 编排 | ❌ | ❌ | ❌ | **✅** |
| Kanban 面板 | ❌ | ❌ | ❌ | **✅** |
| PTY 终端 | ❌ | ❌ | ❌ | **✅** |
| Memory 编辑 | ❌ | ❌ | | **✅** |
| Win 原生 | ✅ | ❌ (仅 WSL) | **✅ (exe)** | ⚠️ (Docker/Node) |
| PWA 远程 | ❌ | ❌ | ❌ | **✅** |
| 部署复杂度 | 内置 | 低 | 中 | 中 |

## 已知坑

1. Dashboard API 必需 — 缺少则降级为 portable 模式（失技能/MCP/Kanban）
2. Swarm 依赖 tmux — Windows 上需 WSL 或 Docker
3. Issue #560: Docker 部署时 MCP 标签页可能不可用
4. Auth 令牌匹配问题 — `HERMES_API_TOKEN` 必须与 gateway 的 `API_SERVER_KEY` 一致
5. 56 个 open issues，部分功能 WIP

## 关联页面

- [[entities/hermes-skill-kanban-orchestrator|kanban-orchestrator]] — Kanban Worker 编排
- [[entities/hermes-skill-ai-harness-exploration|ai-harness-exploration]] — 搜索方法论
- [[concepts/hermes-workflow]] — 工作流模式
- [[entities/hermes-workspace-architecture]] — 架构深度分析
- [[entities/hermes-workspace-deployment-guide]] — 部署详细步骤
- [[entities/mission-control]] — 互补的 Agent Fleet 编排仪表盘
- [[concepts/awesome-hermes-agent-ecosystem-2026]] — Awesome 清单（Workspace 在其中为 production 级 GUI）
