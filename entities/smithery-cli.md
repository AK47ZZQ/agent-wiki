---
title: Smithery CLI
type: entity
tags: [mcp, tool, cli, registry, smithery]
created: 2026-05-28
updated: 2026-05-28
source: GitHub (smithery-ai/cli) / WorkOS / Apigene / smithery.ai/docs
confidence: high (多源验证)
related:
  - concepts/mcp-ecosystem-2026.md
  - concepts/mcpb-bundle-format.md
---

# Smithery CLI

**Smithery CLI** 是 [Smithery.ai](https://smithery.ai) 的命令行接口，用于搜索、安装、管理 MCP 服务器和 Skills。

GitHub: [smithery-ai/cli](https://github.com/smithery-ai/cli) (★742, 607 commits, 49 branches, 89 forks)

## 核心功能

| 功能 | 命令 | 说明 |
|:----|:----|:------|
| 搜索 MCP 服务器 | `smithery mcp search [term]` | 搜索 Smithery Registry (~7,300 服务器) |
| 添加连接 | `smithery mcp add <url>` | 添加远程 MCP 连接 |
| 添加本地客户端 | `smithery mcp add <name> --client claude` | 添加到 Claude Desktop / Cursor |
| 列表连接 | `smithery mcp list` | 列出已连接的服务器 |
| 工具调用 | `smithery tool call <conn> <tool> [args]` | 直接调用 MCP 工具 |
| 搜索工具 | `smithery tool find [query]` | 按意图搜索工具（非传统搜索） |
| 发布服务器 | `smithery mcp publish <url> -n org/server` | 发布 URL 或 .mcpb 包 |
| 认证 | `smithery auth login / logout / whoami / token` | OAuth + 服务令牌 + 策略令牌 |
| 命名空间 | `smithery namespace list / use` | 多组织隔离 |
| Skills | `smithery skill search / add` | Skills 管理（用 `npx skills add` 安装） |

## 关键特性

1. **多客户端支持**：`--client claude`, `--client cursor` → 自动配置目标客户端
2. **MCP Bundle (.mcpb)**：支持发布 MCP Bundle 格式（ZIP + manifest.json + server + deps），跨客户端安装
3. **策略令牌**：`smithery auth token --policy '<json>'` 可签发资源受限令牌
4. **工具意图搜索**：`smithery tool find "create issue"` 不是关键词匹配，是按语义搜索
5. **Open 核心**：607 commits，最新 19 小时前，release-please 自动发布

## 架构

```
Smithery CLI (Node.js 20+, pnpm)
├── mcp/        # MCP 服务器管理
├── tool/       # 工具搜索和调用
├── skill/      # Skills 管理
├── auth/       # 认证 (OAuth + Token)
├── namespace/  # 组织隔离
└── publish/    # MCP Bundle 发布
```

**运行模式**：本地终端 CLI。远程服务器存在 Smithery 云端，工具调用通过远程连接转发。

## 适用场景

| 用户类型 | 适合 | 不适合 |
|:--------|:----|:-------|
| **独立开发者** | ✅ 快速发现+安装 MCP 服务器 | — |
| **原型验证** | ✅ 一键连接，即时测试工具 | — |
| **生产团队** | ⚡ 可入门，但缺认证管理/审计/灰度 | → 需要 MCP Gateway (如 Apigene) |
| **企业** | ❌ | 缺少 SSO、RBAC、SLA、输出压缩 |

## 对比

| 维度 | Smithery | PulseMCP |
|:----|:--------|:--------|
| 注册量 | ~7,300 | 15,930+ |
| 主要功能 | Registry + CLI 部署 | 目录 + 排名 |
| CLI | ✅ 完整 CLI | ❌ 仅网页 |
| 托管 | ✅ 本地+托管 | ❌ |
| 工具调用 | ✅ 直接调用 | ❌ |
| 发布 | ✅ .mcpb + URL | ❌ |

## 关联概念

- ⬅️ [[concepts/mcp-ecosystem-2026|MCP 生态全景 2026]] — Smithery 是 MCP Registry 生态的核心组件
- → [[concepts/mcpb-bundle-format|MCP Bundle (.mcpb)]] — Smithery 使用的发布格式
