---
title: "Codex CLI 深度解析 — 原语、架构与 Hermes 的协作"
created: 2026-06-05
updated: 2026-06-05
type: entity
tags: [entity, codex, openai, cli, agent, architecture]
sources:
  - github.com/openai/codex (88.8k★)
  - github.com/openai/symphony (25k★)
  - concepts/hermes-codex-runtime.md
confidence: high
---

# Codex CLI 深度解析

> **定位**: Codex 是 OpenAI 的旗舰 coding agent CLI——Rust 实现、沙箱架构、AGENTS.md 驱动。Hermes 可以将其作为底层执行引擎。本文聚焦 Codex 自身的原语设计，不与 Hermes 特化内容重复。

---

## TL;DR

| 维度 | Codex 的做法 |
|:-----|:-----------|
| **语言** | Rust (Apache 2.0) |
| **入口** | `codex` CLI + `codex app` 桌面版 |
| **核心原语** | 沙箱 (3 级) / AGENTS.md / MCP / Symphony |
| **与 Claude Code 对比** | Codex 默认无审批弹窗、更激进的自主执行 |
| **与 Hermes 的关系** | Hermes 可将其作为执行层引擎 |

---

## 1. 沙箱架构 — Codex 最核心的设计

Codex 的沙箱设计是它区别于其他 coding agent 的最大特点。

### 1.1 三级沙箱

| 级别 | CLI flag | 文件系统 | 网络 | 适用场景 |
|:-----|:---------|:--------|:-----|:--------|
| **read-only** | `--sandbox read-only` | 只读 | ❌ 禁止 | 代码审查、分析 |
| **workspace** | `--sandbox workspace` (默认) | 读写当前目录 | ✅ 允许出站 | 日常编码 |
| **no-sandbox** | `--no-sandbox` | 完全访问 | ✅ 完全 | 信任环境 / 调试 |

### 1.2 设计哲学

Codex 的沙箱**不是** Docker 容器——它是在文件系统调用级别的拦截：
- 拦截所有文件 I/O → 检查是否在允许路径内
- 拦截网络请求 → 检查是否允许出站
- 拦截进程创建 → 检查是否在白名单中

**优势**: 零启动延迟（不需要起容器）、跨平台一致、性能开销可忽略。

---

## 2. AGENTS.md — Codex 的项目级指令

Codex 在**每次启动时**自动读取项目根目录的 `AGENTS.md`，注入到系统提示词。

### 2.1 Codex 的 AGENTS.md 约定

```markdown
# AGENTS.md

## Project Overview
[一段话描述项目]

## Tech Stack
- Python 3.12, FastAPI, PostgreSQL

## Code Conventions
- 所有 API 返回 {"status": "ok", "data": ...}
- 使用 TypeGuard 而非 isinstance 做类型收窄

## Testing
- pytest, 覆盖率 > 80%
- 每个 API 端点至少 1 个集成测试

## Git
- 分支命名: feat/xxx, fix/xxx, refactor/xxx
- Commit: Conventional Commits (feat:, fix:, refactor:)
```

### 2.2 Codex vs Claude Code 的 AGENTS.md 差异

| 方面 | Codex | Claude Code |
|:-----|:------|:-----------|
| 加载时机 | 每次 CLI 启动 | 每次 session 开始 |
| 格式 | 自由格式 Markdown | 自由格式 Markdown (推荐 ≤100 行) |
| 多文件 | 不支持渐进式披露 | 支持 (AGENTS.md → 深层文档) |
| 子目录 | 会读取子目录的 AGENTS.md | 不会 |

---

## 3. Codex App — 桌面版 vs CLI 版

| 特性 | `codex` CLI | `codex app` |
|:-----|:----------|:-----------|
| 界面 | 终端 | 独立窗口 / IDE 嵌入式 |
| 沙箱 | 终端级 | 应用级 (更强隔离) |
| 多项目 | 一次一个 | 多 tab / 多窗口 |
| IDE 集成 | 无 | VS Code / JetBrains 插件 |

---

## 4. MCP 支持

Codex 原生支持 MCP (Model Context Protocol)，方式类似 Claude Code：

```json
// .codex/mcp.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    },
    "postgres": {
      "command": "npx", 
      "args": ["-y", "@modelcontextprotocol/server-postgres"]
    }
  }
}
```

### Codex MCP vs Claude Code MCP

| 方面 | Codex | Claude Code |
|:-----|:------|:-----------|
| 配置文件 | `.codex/mcp.json` | `.claude/mcp.json` |
| 传输方式 | stdio + SSE | stdio + SSE |
| 工具发现 | 自动 | 自动 |
| 动态注册 | ❌ | ❌ (都需要重启) |

---

## 5. Symphony 集成

Codex CLI 可以直接作为 Symphony 的底层执行器：

```
Linear Issue → Symphony → Codex CLI → 写代码 → PR
```

Codex 的沙箱 + Symphony 的编排 = **全自动 coding pipeline**：
1. Symphony 监控 Issue board
2. 发现新 Issue → 启动 Codex 在 workspace 沙箱中实现
3. Codex 写代码 + 运行测试 + 提交 PR
4. Symphony 收集验证结果，通知人类审批

---

## 6. Codex 的退出与继续机制

Codex 对长时间任务的优雅处理：

```
exit_code 0  → 任务完成
exit_code 2  → 部分完成，需要继续（Ralph Loop 触发）
exit_code 1  → 错误
```

Exit code 2 是关键：Agent 说"我做了一半，上下文满了，需要新 context 继续"。这直接对应 Ralph Loop 的循环模式。

---

## 7. 与 Hermes 的协作模式

```
┌────────────────────────────────────────────┐
│              Hermes (编排层)                │
│  - 任务分解 (P0-P4 workflow)               │
│  - 多 Agent 协作 (Kanban)                  │
│  - 记忆管理 (LCM + Hindsight)              │
│  - Harness Engineering 哲学                │
└────────────────┬───────────────────────────┘
                 │ 委托执行
                 ▼
┌────────────────────────────────────────────┐
│            Codex CLI (执行层)               │
│  - 沙箱隔离                                │
│  - 代码生成 + 测试                         │
│  - AGENTS.md 读取                          │
│  - MCP 工具扩展                            │
└────────────────────────────────────────────┘
```

**Hermes 管理"做什么" + "怎么做对"** — 任务分解、记忆、约束。
**Codex 管理"怎么执行"** — 沙箱安全、代码生成、测试运行。

---

## 8. 关联 Wiki 页面

- [[concepts/hermes-codex-runtime]] — Hermes↔Codex 桥接架构
- [[concepts/symphony-spec-as-product]] — Symphony: Issue→PR 编排
- [[concepts/harness-engineering-deep-study]] — Codex 是 Harness Engineering 的第一个实践案例
- [[concepts/agent-safety]] (新建) — 沙箱 = 安全模型的核心
- [[comparisons/multi-agent-architecture-patterns]] — Codex 在 Swarm / Orchestrator-Workers 中的角色

### 外部链接
- https://github.com/openai/codex (88.8k★)
- https://github.com/openai/symphony (25k★)
- https://github.com/snarktank/ralph (19.9k★)

---

## 9. 版本历史

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-06-05 | 初始版：沙箱 / AGENTS.md / App / MCP / Symphony / Hermes 协作 |

---

> **核心定位**: Codex 不是 Hermes 的竞争对手，而是 Hermes 的一道执行层。就像 Linux 的 `exec()` 系统调用——Hermes 负责调度，Codex 负责在沙箱中安全地执行。
