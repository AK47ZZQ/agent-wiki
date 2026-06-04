---
title: Hermes Codex Runtime
type: concept
tags: [hermes, codex, runtime, architecture, sandbox]
created: 2026-05-29
updated: 2026-05-29
source: Hermes Docs / GitHub Issues / AlphaSignal
confidence: high
related:
  - entities/codex.md
---

# Hermes Codex Runtime

Hermes Agent v0.15.0 "Velocity" 引入的 opt-in beta 功能。将 Hermes 的工具执行层委托给 **OpenAI Codex CLI App-Server**，保留 Hermes 的 Shell/编排层。

## 架构

```
用户输入
    │
    ▼
Hermes Agent (Shell Layer)
  会话DB / 斜杠命令 / Gateway / 记忆
  /goal Ralph 循环 / 技能审查 / Kanban
  22 平台 (Telegram, Discord, Slack...)
    │ JSON-RPC over stdio
    ▼
Codex CLI App-Server (Execution Engine)
  shell / apply_patch / 沙箱
  Codex 原生插件 / MCP 工具执行
```

**数据流：** Hermes 将 `openai/*` 和 `openai-codex/*` 模型轮的**工具执行**委托给 Codex CLI。推理仍由 Hermes 选择的模型完成。

## 配置

```yaml
# config.yaml
model:
  openai_runtime: codex_app_server
```

或交互式：`/codex-runtime codex_app_server`。切换回默认：`/codex-runtime auto`。

## 三源工具

启用后，Hermes 有三个独立的工具源：
1. **模型原生工具** — OpenAI 模型直接提供的工具
2. **Codex 插件** — Gmail/GitHub/Linear/Calendar/Canva/Outlook 等
3. **Hermes 工具 MCP** — Codex 通过 stdio MCP 生成 `hermes_tools_mcp_server`

## 对比

| 维度 | Hermes 原生 | Codex Runtime |
|:----|:-----------|:--------------|
| 沙箱 | 无内置 | 三级(read-only/workspace/no-sandbox) |
| 订阅 | API Key 按量 | ChatGPT $20/mo Pro |
| 模型 | 300+ 任意 | 仅 OpenAI |
| 插件 | MCP 插件 | OpenAI 原生插件 |
| 记忆 | 完整 | 有限(memory/session_search 未暴露) |

## 已知痛点(15+ issues)

- Gateway 上审批请求静默失败关闭
- Cloudflare 挑战阻止启动
- config.toml 生成无效配置
- 重复插件表
- 无 Hermes 级别沙箱配置
- 旧版 Hermes 不兼容

## 关联

- ⬅️ [[entities/codex|Codex]]
- ⬅️ [[concepts/hermes-kanban|Durable Kanban]]
