---
title: MCP Bundle (.mcpb)
type: concept
tags: [mcp, bundle, packaging, distribution, mcpb]
created: 2026-05-28
updated: 2026-05-28
source: MCP Official (David Soria Parra) / Smithery CLI
confidence: high (官方规范)
related:
  - concepts/mcp-ecosystem-2026.md
  - entities/smithery-cli.md
---

# MCP Bundle (.mcpb)

**MCP Bundle (.mcpb)** 是 MCP 项目的标准打包格式，用于将本地 MCP 服务器打包为可移植的 ZIP 存档，支持跨客户端安装。

提出者: David Soria Parra（MCP 联合创始人）和 Joan Xie。2025-11-21 加入 MCP 项目。

## 格式结构

```
bundle.mcpb (ZIP file)
├── manifest.json   # 必需：元数据 + 配置
├── server/         # 服务器实现代码
│   └── index.js
├── node_modules/   # 打包的依赖
└── icon.png        # 可选图标
```

**manifest.json** 包含：服务器名称、版本、描述、入口文件路径、环境变量要求、权限声明。

## 解决的问题

MCP Bundle 解决 MCP 服务器分发的三大痛点：

| 痛点 | 之前 | .mcpb 之后 |
|:----|:----|:----------|
| **手动配置** | 用户需手动配置 stdio 命令和 JSON 参数 | 解压即用，客户端自动读取 manifest.json |
| **依赖管理** | 依赖需用户自行安装 | 依赖捆绑在 ZIP 中 |
| **跨客户** | 每个客户端需不同配置方式 | 任何兼容客户端都支持 (Claude Desktop / Claude Code / MCP for Windows) |

## 工具链

| 工具 | 功能 |
|:----|:------|
| `mcpb` CLI | 创建 manifest.json + 打包为 .mcpb |
| Smithery CLI | `smithery mcp publish ./server.mcpb -n org/server` 发布到 Registry |

## 与 Regitries 的关系

```
开发者 ──mcpb CLI──→ .mcpb 包 ──smithery publish──→ Registry
                                                         │
用户 ──smithery mcp search──→ 发现 ──smithery mcp add──→ 客户端自动配置
```

**关键设计点**：.mcpb 是格式标准，Registry 是分发平台。格式标准由 MCP 项目维护，非商业实体所有。

## 关联概念

- ⬅️ [[concepts/mcp-ecosystem-2026|MCP 生态全景 2026]] — 生态背景
- ⬅️ [[entities/smithery-cli|Smithery CLI]] — .mcpb 发布工具之一
