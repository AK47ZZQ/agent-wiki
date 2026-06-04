---
title: Hermes Workspace 架构深度分析
created: 2026-05-31
updated: 2026-05-31
type: entity
tags: [hermes-workspace, architecture, analysis]
source: https://github.com/outsourc-e/hermes-workspace
confidence: medium
---

# Hermes Workspace (outsourc-e/hermes-workspace) — 架构深度分析

> 分析日期: 2026-05-31  
> 版本: v2.3.0 | Stars: 5,110 | 许可证: MIT | 零 Fork 设计

---

## 目录## 目录

1. [总体架构概述](#1-总体架构概述)
2. [与 Hermes Agent Gateway 的交互（API 协议细节）](#2-与-hermes-agent-gateway-的交互api-协议细节)
3. [Conductor 任务的分解和执行流程](#3-conductor-任务的分解和执行流程)
4. [Swarm Mode 的多 Agent 编排机制](#4-swarm-mode-的多-agent-编排机制)
5. [前端技术栈（React/Three.js）和关键依赖](#5-前端技术栈reactthreejs和关键依赖)

---

## 1. 总体架构概述

### 1.1 三层架构

```
┌──────────────────────────────────────────────────┐
│              Hermes Workspace (:3000)             │
│     React + Vite SPA (PWA 可安装)                 │
│     Chat · Dashboard · Kanban · MCP · Swarm      │
│     Conductor · 内置 PTY 终端 · 文件浏览器         │
└────────────┬──────────┬──────────────────────────┘
             │          │
     REST/SSE│          │REST API (Dashboard API)
             ▼          ▼
┌────────────────────┐ ┌─────────────────────────────┐
│ Hermes Gateway     │ │ Hermes Dashboard API        │
│ (:8642)            │ │ (:9119)                      │
│ OpenAI-compatible  │ │ FastAPI + Uvicorn            │
│ Chat Completions   │ │ Sessions / Skills / Jobs     │
│ SSE 流式响应       │ │ Config / Cron / Analytics    │
│ Agent 会话管理     │ │ Kanban / MCP / Profiles      │
└─────────┬──────────┘ └─────────────────────────────┘
          │
          ▼
┌──────────────────────┐
│ Hermes Agent Core    │
│ LLM Provider Router  │
│ Kanban Dispatcher    │
│ MCP Tool Executor    │
│ LCM Context Engine   │
│ 22 个消息平台适配器  │
└──────────────────────┘
```

### 1.2 核心设计理念：Zero-Fork

- **不 Fork hermes-agent** — Workspace 直接对接上游标准 API
- Gateway 暴露 OpenAI-compatible API（`:8642`）— 任何 OpenAI SDK 兼容客户端都能连接
- Dashboard API（`:9119`）— 提供管理面（sessions, config, cron, skills）
- Workspace 同时连接这两个接口，各自独立认证

---

## 2. 与 Hermes Agent Gateway 的交互（API 协议细节）

### 2.1 双 API 接口架构

| 接口 | 端口 | 协议 | 用途 | 认证方式 |
|------|------|------|------|---------|
| **Gateway API** | `:8642` | OpenAI Chat Completions API (REST + SSE) | 聊天、Agent 交互 | `API_SERVER_KEY` (Bearer Token) |
| **Dashboard API** | `:9119` | FastAPI (REST) | 配置、会话、技能、Kanban、MCP 管理 | `X-Hermes-Session-Token` (per-session) |

### 2.2 Gateway API (:8642) — OpenAI 兼容协议

Hermes Gateway 暴露的是**兼容 OpenAI Chat Completions API 的 HTTP 接口**，使 Workspace 可以用标准 OpenAI SDK 或 fetch API 连接。

**关键环境变量：**
```bash
API_SERVER_ENABLED=true          # 启用 API 服务器
API_SERVER_HOST=0.0.0.0          # 监听地址 (默认 127.0.0.1)
API_SERVER_PORT=8642              # 监听端口
API_SERVER_KEY=<token>            # 认证令牌 (必需, 即使 loopback)
```

**核心 API 端点：**

| 端点 | 方法 | 说明 |
|------|------|------|
| `/v1/chat/completions` | POST | 聊天补全 (SSE 流式) |
| `/v1/models` | GET | 获取可用模型列表 |

**请求格式 (POST `/v1/chat/completions`)：**
```json
{
  "model": "deepseek-v4-flash",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "你好"}
  ],
  "stream": true,
  "max_tokens": 4096,
  "temperature": 0.7
}
```

**请求头：**
```
Authorization: Bearer <API_SERVER_KEY>
Content-Type: application/json
```

**响应 (SSE 流式, `stream=true`)：**
```
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"delta":{"content":"你好"},"index":0}]}
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","choices":[{"delta":{"content":"！"},"index":0}]}
data: [DONE]
```

**非流式响应 (`stream=false`)：**
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "choices": [{"message": {"role": "assistant", "content": "你好！"}, "index": 0}],
  "usage": {"prompt_tokens": 50, "completion_tokens": 10, "total_tokens": 60}
}
```

**Workspace 连接方式：**
```javascript
// 在 .env 中配置
HERMES_API_URL=http://localhost:8642
HERMES_API_TOKEN=<API_SERVER_KEY>
```

### 2.3 Dashboard API (:9119) — 管理面接口

Hermes Dashboard 是用 FastAPI 构建的内置管理服务器。所有非公开端点通过 `X-Hermes-Session-Token`（per-session token, 每次启动随机生成）保护。

**关键 API 端点分类：**

| 分类 | 端点 | 说明 |
|------|------|------|
| **状态** | `GET /api/status` | Dashboard 和服务状态 |
| **会话管理** | `GET /api/sessions` | 列出所有会话 |
| | `GET /api/sessions/search` | 搜索会话 |
| | `GET /api/sessions/{id}/messages` | 获取会话消息 |
| | `DELETE /api/sessions/{id}` | 删除会话 |
| **配置** | `GET /api/config` | 读取配置 |
| | `PUT /api/config` | 修改配置 |
| | `GET /api/config/raw` | 原始 YAML 配置 |
| | `PUT /api/config/raw` | 写入原始 YAML |
| | `GET /api/env` / `PUT /api/env` / `DELETE /api/env` | 环境变量管理 |
| **模型** | `GET /api/model/info` | 当前模型信息 |
| | `GET /api/model/options` | 可用模型选项 |
| | `POST /api/model/set` | 切换模型 |
| **技能** | `GET /api/skills` | 列出所有技能 |
| | `PUT /api/skills/toggle` | 启用/禁用技能 |
| **Cron** | `GET /api/cron/jobs` | 列出 Cron 任务 |
| | `POST /api/cron/jobs` | 创建 Cron 任务 |
| | `PUT /api/cron/jobs/{id}` | 更新 Cron 任务 |
| | `DELETE /api/cron/jobs/{id}` | 删除 Cron 任务 |
| **Profiles** | `GET /api/profiles` | 列出 Profile |
| | `POST /api/profiles` | 创建 Profile |
| | `POST /api/profiles/{name}/open-terminal` | 打开 Profile 终端 |
| **日志** | `GET /api/logs` | 读取日志 |
| **分析** | `GET /api/analytics/usage` | 使用量统计 |
| | `GET /api/analytics/models` | 模型使用统计 |
| **MCP (通过命令行)** | 依赖 `hermes mcp` CLI 命令 | MCP 服务器管理 |

**认证机制：**
```javascript
// Dashboard 的 session token 每次服务器重启时生成
// 通过 HTML 注入给 SPA，Workspace 需要在首次加载时获取
headers: {
  'X-Hermes-Session-Token': '<ephemeral_token>'
}
```

### 2.4 MCP 管理 API

Workspace 的 `/mcp` 页面管理 MCP 服务器。MCP 服务器的 CRUD 操作通过调用 `hermes mcp` CLI 命令实现（非 REST 端点），Workspace 通过 PTY 终端或子进程执行：

```bash
# 内部使用的命令
hermes mcp list                           # 列出 MCP 服务器
hermes mcp add <name> --command <cmd>     # 添加 MCP 服务器
hermes mcp remove <name>                  # 删除 MCP 服务器
hermes mcp market                         # 浏览 MCP 市场
```

---

## 3. Conductor 任务的分解和执行流程

### 3.1 架构定位

Conductor 是 Hermes Workspace 的高级任务编排层，**依赖 Hermes Dashboard API**（`:9119`）。如果 Dashboard API 不可用，自动降级为 `native-swarm` 模式。

### 3.2 核心工作流

```
用户输入复杂任务
     │
     ▼
┌─────────────────────────────────────────┐
│  Conductor (在 Workspace 前端)           │
│  1. 任务分析 → LLM 驱动的意图理解        │
│  2. 任务分解 → DAG 子任务图              │
│  3. 依赖分析 → 识别并行/串行依赖         │
│  4. 资源分配 → 指派 Agent/Worker         │
│  5. 任务触发 → Dashboard API 调用        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Dashboard API (:9119)                  │
│  → 创建 Kanban 任务                      │
│  → 设置依赖链 (parent links)             │
│  → 设置 Worker 分配                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Gateway Kanban Dispatcher              │
│  (内嵌在 Gateway 进程中, 30s 轮询)       │
│  → 扫描 ready 任务                      │
│  → Spawn Worker 子进程                   │
│  → 心跳监控 (15min TTL)                 │
│  → 失败重试 (failure_limit=3)           │
│  → 依赖链 promote (AND 条件)            │
└─────────────────────────────────────────┘
```

### 3.3 任务生命周期

```
created ──→ dispatched ──→ claimed ──→ running ──→ completed
                │                              │ (失败)
                ▼                              ▼
            (有 parent)                    blocked ──→ (重试) ──→ running
                │
            waiting_for_deps ──→ (deps done) ──→ ready ──→ dispatched
```

**状态机细节：**
- **created**: 任务被创建，尚未调度
- **dispatched**: Dispatcher 选定了 Worker
- **claimed**: Worker 进程已启动并声明了任务
- **running**: Worker 正在执行
- **completed**: Worker 调用 `kanban_complete` 完成任务
- **blocked**: 执行失败，等待重试或人工干预

### 3.4 Kanban 任务工具

Worker 通过以下工具与看板交互：

| 工具 | 功能 |
|------|------|
| `kanban_show` | 获取任务详情（描述、依赖、workspace 路径） |
| `kanban_complete` | 完成任务 + 传递摘要/元数据给下游 |
| `kanban_heartbeat` | 更新活性信号 + 延长声明 TTL |
| `kanban_block` | 阻塞在未完成的依赖上 |
| `decompose` | 将任务拆分为子任务（子 DAG） |
| `specify` | 细化任务规格说明 |

### 3.5 依赖链机制 (DAG)

- **无 parent**: 立即变成 `ready`，并行执行
- **有 parent(s)**: 等待所有父任务 `completed` 后自动 `promote` 为 `ready`
- **AND 条件**: 多个 parent 全部完成才触发（不是 OR）
- **DAG 重配**: 支持 `kanban link/unlink` 运行时修改依赖

### 3.6 数据后端

- **SQLite 数据库**: `~/.hermes/kanban.db`
  - 表: `tasks`, `task_runs`, `task_events`
  - 所有 Profile 共享同一数据库
  - 跨会话持久化（Gateway 重启后任务不丢失）

---

## 4. Swarm Mode 的多 Agent 编排机制

### 4.1 架构概览

Swarm Mode 是 Hermes Workspace 的**持久化多 Agent 编排模式**，基于 tmux 会话管理 Worker 进程池。

```
┌──────────────────────────────────────────────────┐
│  Hermes Workspace Swarm 面板                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ Worker 1  │ │ Worker 2 │ │ Worker 3 │  ...     │
│  │ tmux pane │ │ tmux pane│ │ tmux pane│          │
│  │ PID: 1234 │ │PID: 1235 │ │PID: 1236 │          │
│  └──────────┘ └──────────┘ └──────────┘          │
└──────────────────┬───────────────────────────────┘
                   │ tmux session management
                   ▼
┌──────────────────────────────────────────────────┐
│  tmux session: hermes-workspace                   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │ pane 0:     │ │ pane 1:     │ │ pane 2:     │ │
│  │ Worker A    │ │ Worker B    │ │ Worker C    │ │
│  │ hermes chat │ │ hermes chat │ │ hermes chat │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ │
└──────────────────────────────────────────────────┘
```

### 4.2 Swarm CLI 命令

```bash
# 基本 Swarm 命令
hermes kanban swarm "主题" \
  --worker worker1:搜索A \
  --worker worker2:搜索B \
  --verifier worker4 \
  --synthesizer worker5
```

**自动生成的依赖链：**
```
workers(并行: 搜索A, 搜索B) → verifier(审查) → synthesizer(合稿)
```

### 4.3 Worker 池管理

**Worker 类型：**
| 类型 | 说明 | 配置方式 |
|------|------|---------|
| Kanban Worker | Gateway Dispatcher 自动 spawn | `kanban` CLI + Profile 配置 |
| Swarm Worker | Workspace 前端 tmux 管理 | Swarm 面板 (.env/preferences) |
| Native Worker | 无 Dashboard 时的降级方案 | Workspace 内置回退模式 |

**Worker 参数：**
| 参数 | 默认值 | 说明 |
|------|--------|------|
| 模型 | Profile 默认 | MiniMax M2.7 / DeepSeek 等 |
| Skill | `kanban-orchestrator` + `hermes-workflow` | 精确加载 |
| 上下文 | LCM stateless | 会话不持久化，降低内存 |
| 记忆 | 只读 | 不污染编排器记忆空间 |
| 分配 | Round-Robin | 轮转分配任务 |
| Heartbeat TTL | 15 分钟 | 超时标记为 zombie |
| Failure Limit | 3 | 超过后 blocked |
| Dispatch Interval | 30 秒 | Dispatcher 轮询间隔 |

### 4.4 Swarm 模式 vs Conductor 模式

| 维度 | Swarm Mode | Conductor Mode |
|------|-----------|----------------|
| 架构 | tmux-based Worker 池 | Dashboard API 驱动的任务图 |
| 持久化 | 进程级（tmux session） | SQLite 持久化（跨重启） |
| 依赖 Dashboard | **不需要** | **需要** (:9119) |
| DAG 支持 | 基本（CLI --parent） | 完整 DAG（link/unlink） |
| 降级方案 | 无（基础模式） | `native-swarm` 回退（Issue #262） |
| 最佳场景 | 持久化 Worker 常驻 | 复杂多步工作流编排 |
| 前端支持 | 实时 tmux pane 面板 | 可视化 DAG 面板 |

### 4.5 持久 Workspace (`dir:`)

- **Scratch workspace**: 任务完成后 GC 自动清理
- **持久 workspace**: 使用 `dir:` 前缀保留跨 Worker 共享文件
  ```bash
  kanban create "任务" --workspace "dir:C:\workspace\kanban\project-x"
  ```

---

## 5. 前端技术栈（React/Three.js）和关键依赖

### 5.1 核心技术栈

| 层级 | 技术 | 版本/说明 |
|------|------|----------|
| **构建工具** | Vite | 现代 JS 构建器, HMR |
| **UI 框架** | React 18+ | SPA 前端 |
| **路由** | React Router v6 | 客户端路由 |
| **状态管理** | React Context + Hooks | 无 Redux，轻量 |
| **HTTP 客户端** | Fetch API / Axios | REST + SSE |
| **SSE 流式** | EventSource / ReadableStream | Chat 流式响应 |
| **终端** | xterm.js + node-pty | 内置 PTY 终端 |
| **3D 可视化** | Three.js (通过 react-three-fiber) | 3D Agent 拓扑可视化 |
| **代码编辑器** | Monaco Editor (VS Code 内核) | 文件/代码编辑 |
| **样式** | CSS Modules + CSS Variables | 5 种主题 |
| **PWA** | Service Worker + Manifest | 离线安装 |

### 5.2 关键 npm 依赖分析（推测）

根据项目技术栈和社区知识库推断：

```json
{
  "dependencies": {
    "react": "^18.x",
    "react-dom": "^18.x",
    "react-router-dom": "^6.x",
    "react-three-fiber": "^8.x",          // Three.js React 桥接
    "@react-three/drei": "^9.x",           // Three.js 辅助工具
    "three": "^0.160.x",                   // 3D 引擎
    "xterm": "^5.x",                       // 终端模拟器
    "@xterm/xterm": "^5.x",
    "node-pty": "^1.x",                    // 伪终端 (PTY)
    "monaco-editor": "^0.45.x",           // 代码编辑器
    "axios": "^1.x",                       // HTTP 客户端
    "react-markdown": "^9.x",              // Markdown 渲染
    "rehype-highlight": "^7.x",            // 代码高亮
    "zustand": "^4.x"                      // 轻量状态管理 (可能采用)
  },
  "devDependencies": {
    "vite": "^5.x",                        // 构建工具
    "@vitejs/plugin-react": "^4.x",        // React 插件
    "typescript": "^5.x",                  // (可选) TS 支持
    "vitest": "^1.x"                       // 测试框架
  }
}
```

### 5.3 Three.js 在 Workspace 中的应用

Three.js 通过 `react-three-fiber` (R3F) 集成，用于：

1. **Agent 拓扑可视化** — 实时 3D 展示 Agent/Worker 拓扑结构
2. **任务依赖图** — 3D DAG 可视化（Conductor 模式）
3. **Swarm 面板** — 3D Worker 状态展示
4. **Dashboard 看板** — 3D 数据可视化（Agent 活动/性能指标）

### 5.4 内置 PTY 终端架构

```
┌──────────────────────────────────────────────────┐
│  Workspace Browser                               │
│  ┌──────────────────┐                            │
│  │ xterm.js Terminal │  ← 前端终端渲染器          │
│  └────────┬─────────┘                            │
└───────────┼──────────────────────────────────────┘
            │ WebSocket
            ▼
┌──────────────────────────────────────────────────┐
│  Gateway / Web Server                            │
│  ┌──────────────────────┐                        │
│  │ WebSocket Handler    │  /api/pty 端点          │
│  │ node-pty / pywinpty  │  跨平台 PTY 后端        │
│  │ Shell Process        │  bash/zsh/cmd          │
│  └──────────────────────┘                        │
└──────────────────────────────────────────────────┘
```

### 5.5 PWA 支持

- **Service Worker**: 缓存核心资源，离线基本可用
- **Web Manifest**: 可添加至主屏幕（类原生体验）
- **Electron WIP**: 原生桌面应用开发中（未来替代 PWA）

### 5.6 5 种主题系统

| 主题 | 模式 | 特点 |
|------|------|------|
| Hermes | 亮/暗 | 默认主题 |
| Nous | 亮/暗 | Dark 风格 |
| Bronze | 亮/暗 | 青铜色系 |
| Slate | 亮/暗 | 板岩灰 |
| Mono | 亮/暗 | 单色极简 |

通过 CSS Variables 实现运行时切换，无需重新编译。

---

## 附录 A：Workspace 的环境变量

```bash
# === Gateway API (必需) ===
HERMES_API_URL=http://localhost:8642          # Gateway API 地址
HERMES_API_TOKEN=<API_SERVER_KEY>             # Gateway 认证令牌

# === Dashboard API (必需) ===
HERMES_DASHBOARD_URL=http://localhost:9119    # Dashboard API 地址

# === 部署配置 ===
PORT=3000                                      # Workspace 前端端口
COOKIE_SECURE=0                                # HTTP 环境 (非 HTTPS)
HERMES_PASSWORD=<password>                     # 登录密码

# === 性能 ===
NODE_OPTIONS="--max-old-space-size=2048"       # Node 内存限制
```

## 附录 B：端口占用表

| 端口 | 服务 | 协议 |
|------|------|------|
| `:3000` | Hermes Workspace (Vite Dev Server) | HTTP / WebSocket |
| `:8642` | Hermes Gateway API | HTTP (OpenAI 兼容) |
| `:9119` | Hermes Dashboard API | HTTP (FastAPI) |

## 附录 C：部署方式

| 方式 | 复杂度 | 推荐场景 |
|------|--------|---------|
| Docker Compose | ⭐⭐ | 最简单，最干净 |
| pnpm dev (已有 Agent) | ⭐⭐⭐ | 已有本地 hermes-agent |
| WSL + PowerShell | ⭐⭐⭐⭐ | Windows 深度集成 |

---

*Related: [[entities/hermes-workspace]] — Hermes Workspace 实体页*
