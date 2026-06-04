---
title: MCP 生态全景 2026
type: concept
tags: [mcp, ai-protocol, agent, tool-calling, ecosystem]
created: 2026-05-28
updated: 2026-05-28
source: Digital Applied / MCP Official Blog / Zuplo / WorkOS / cnblogs
confidence: high (多源交叉验证)
related:
  - concepts/ai-coding-tools-comparison.md
  - concepts/harness-engineering-deep-study.md
  - concepts/ai-agent-ecosystem-2026.md
---

# MCP 生态全景 2026

## 定义

**MCP（Model Context Protocol）** 是 Anthropic 于 2024 年 11 月 25 日推出的开放标准，用于标准化 AI 系统（LLM）与外部工具、数据源之间的集成方式。2025-2026 年已发展为跨厂商的 AI 基础设施标准。

**本质定位**：MCP 是 **模型→工具/数据** 层的标准化协议，不是多智能体协作协议（那是 Google A2A 的领域）。

## 关键数据（2026 年 5 月）

| 指标 | 数据 | 来源 |
|:----|:----|:------|
| 官方 Registry 最新记录 | **9,652** | 官方 Registry API (2026-05-24) |
| Anthropic 引用的活跃公共服务器 | **10,000+** | Anthropic AAIF 公告 |
| GitHub mcp-server 主题仓库 | **15,926** | GitHub Search API (2026-05-24) |
| 月 SDK 下载量 | **9,700 万+** | Anthropic 引用 |
| modelcontextprotocol/servers 星标 | **86,148** | GitHub (2026-05-24) |
| Stacklok 企业生产采用率 | **41%**（29%有限+12%广泛） | Stacklok 2026 企业软件报告 |
| Zuplo 报告总服务器数 | **17,000+** | Zuplo MCP Report (2026) |
| PulseMCP | **15,930+** | Ecosystem Tracker |
| Smithery | **~7,300** | Ecosystem Tracker |
| 官方 Registry（验证过的） | **~2,000** | Ecosystem Tracker |

> ⚠️ 旧文章中"78% 企业团队采用 MCP"无可靠来源，已被 Stacklok 的 41% 取代。

## 协议演进时间线

```
2024-11-25  ──  Anthropic 发布 MCP（初始版本，stdio + HTTP+SSE）
2025-03-26  ──  v2 版本：扩展 MCP 超越本地场景
2025-11-25  ──  最大更新：async tasks、enhanced sampling、elicitation、
               server-side agent loops、Client ID Metadata、扩展系统、
               OAuth 2.1 正式化
2026-01-26  ──  MCP Apps (SEP-1865) 概念提出
2026-05-19  ──  Code with Claude London：MCP tunnels 研究预览、
               自托管 sandbox 公测
2026-05/06  ──  MCP 捐赠给 Linux Foundation 的 Agentic AI Foundation (AAIF)
2026-07-28  ──  **发布候选**（2024 年以来最大修订）：
               无状态协议、扩展一等公民、MCP Apps、JSON Schema 2020-12
```

## 2026-07-28 发布候选 — 核心变更

| 变更 | 说明 | 意义 |
|:----|:------|:------|
| **无状态协议** | 去掉 handshake 和 session id，任何请求可到任何服务器 | 水平扩展、负载均衡、Kubernetes 原生部署 |
| **扩展框架** | 新能力以 opt-in 扩展方式发布，稳定后再决定是否进规范 | 协议演进不再需要大版本更新 |
| **MCP Apps (SEP-1865)** | 服务器可提供交互式 HTML 界面，host 在沙箱 iframe 中渲染 | 从纯工具调用 → 富交互 UI |
| **JSON Schema 2020-12** | 工具参数支持完整 JSON Schema 2020-12 | 更精确的参数校验 |
| **功能生命周期策略 (SEP-2577)** | 明确的 deprecation 流程 | 协议治理成熟度提升 |
| **Tasks 毕业为扩展** | 长时间运行的工作从规范移到扩展层 | 规范瘦身 |

### 无状态协议对部署的影响

```
之前（有状态）：                   之后（无状态）：
Client ──→ Server A (session=1)    Client ──→ Server A
              ↕ 只能连同一实例                   ↕ 任意实例
           Server B (session=2)    Client ──→ Server B
```

这意味着 MCP 服务器可以：
- 放在 Kubernetes Deployment + Service 后面直接负载均衡
- 部署到 serverless 平台（不再需要粘性会话）
- 水平扩展无需共享 session store

## 传输协议格局

| 传输 | 2025 | 2026 |
|:----|:----|:------|
| **stdio** | 标准 | 继续支持，本地开发首选 |
| **Streamable HTTP** | 新引入 | **新标准** |
| **HTTP+SSE (旧)** | 标准 | **已废弃** |
| **MCP Tunnels** | — | 研究预览（Code with Claude London 2026-05） |

## 安全现状

### CVE 统计

| CVE | 漏洞 | CVSS | 影响 |
|:----|:----|:----|:------|
| CVE-2026-27826 | MCP Atlassian SSRF | 7.3 | 未认证攻击者可强制服务器向任意 URL 发出 HTTP 请求 |
| CVE-2026-33032 | nginx-ui MCP 认证缺失 | **9.8** | 未认证攻击者可通过 MCP 接管 Nginx 配置管理。已在野利用 |

### 整体安全形势

| 指标 | 数据 | 来源 |
|:----|:----|:------|
| 无认证的 MCP 服务器 | **24%** | Zuplo MCP Report |
| 依赖 API Key | **40%** | Zuplo MCP Report |
| 存在命令注入风险的服务器 | **43%** | Network Intelligence |
| 协议层能强制执行安全 | **不能** | 官方确认 |

> **核心问题**：MCP 协议本身无法强制安全——安全完全取决于实现和运维控制。远程 MCP 服务器必须实现 OAuth 2.1 + PKCE。

## Registry 碎片化

2026 年有 **8+ 个并行 Registry/目录**：

| Registry | 规模 | 特点 |
|:--------|:----|:------|
| **PulseMCP** | 15,930+ | 最大，追踪每周下载和 GitHub 星标 |
| **Smithery** | ~7,300 | 支持一键安装 CLI，本地+托管部署 |
| **官方 Registry** | ~2,000 | 需 GitHub/DNS/OIDC 验证，质量最高 |
| **Raycast** | 中等 | 生产力工具导向 |
| **MCP.so** | 中等 | 简单目录 |
| **FluidMCP** | 小 | 新兴 |
| **TrueFoundry** | 企业 | VPC 内私有 Registry，RBAC+审计 |
| **GitHub MCP Registry** | 子注册表 | 发布一次，自动同步到 GitHub |

> 碎片化严重到开发者创建了 `mcp-submit` CLI 工具——一次提交推送 10+ 个目录。

## MCP vs A2A vs ACP vs Skills

| 协议 | 层次 | 作用 | 提出方 |
|:----|:----|:-----|:-------|
| **MCP** | 模型→工具/数据 | 标准化工具调用 | Anthropic |
| **A2A** | 智能体→智能体 | 多智能体协作 | Google |
| **ACP** | 智能体→智能体 | 智能体间通信协议 | — |
| **Skills** | 知识→行为 | 模块化的技能包 | 社区 |

**MCP 不是多智能体协议**。你的 MCP 服务器跑在 10 个实例后面做负载均衡，但你不需要用 MCP 让两个 AI Agent 互相交流——那是 A2A 的领域。

## 关键厂商支持

| 厂商 | 支持形式 |
|:----|:--------|
| **Anthropic** | Claude Desktop 原生 MCP 客户端 |
| **OpenAI** | ChatGPT MCP 支持 |
| **Google** | Gemini MCP 集成 |
| **Microsoft** | Copilot MCP 支持 |
| **GitHub** | GitHub MCP Registry |
| **Vercel** | MCP 服务器部署 |
| **VS Code** | MCP 扩展支持 |
| **Cursor** | MCP 原生支持 |

## 关键洞察

1. **基准数据不可信** — 旧文章的 78% 采用率无来源，已被 41%（Stacklok）取代。MCP 生态真实但被夸大。
2. **无状态化是大趋势** — 2026-07-28 RC 使 MCP 服务器可水平扩展，serverless 部署成为可能。
3. **安全是最大短板** — 24% 零认证 + 43% 命令注入风险 + 协议层无法强安全。有 CVE 在野利用。
4. **Registry 碎片化是主要痛点** — 8+ 个并行目录，开发者需要 `mcp-submit` 工具来一次发布多处。
5. **MCP Apps 是范式转变** — 从纯 text/tool 到 rich UI 交互，AI 工具生态从 CLI 进化到 GUI。
6. **MCP ≠ A2A** — MCP 管模型→工具，A2A 管智能体→智能体。两者互补，不是替代。

## MCP Bundle (.mcpb)

MCP Bundle 是 MCP 官方的标准化打包格式，用于分发和安装本地 MCP 服务器。

```
bundle.mcpb (ZIP file)
├── manifest.json   # 元数据 + 配置
├── server/         # 服务器实现
│   └── index.js
├── node_modules/   # 打包的依赖
└── icon.png        # 可选图标
```

**发布端：** `mcpb` CLI 创建 → 发布到 Registry（如 Smithery）
**安装端：** 客户端 CLI 解压并运行（跨客户端兼容）

**设计目标：** 解决 MCP 服务器分发碎片化——用户不再需要手动配置 stdio/json 路径。

## 工具链：Smithery CLI

Smithery CLI 是 MCP Registry 生态中最成熟的 CLI 工具（★742, GitHub smithery-ai/cli）：

| 类别 | 功能 | 命令 |
|:----|:----|:------|
| 发现 | 搜索 Registry | `smithery mcp search [term]` |
| 安装 | 添加到客户端 | `smithery mcp add <url> --client claude` |
| 调用 | 直接调工具 | `smithery tool call <conn> <tool> [args]` |
| 发布 | 发布 .mcpb/URL | `smithery mcp publish <url> -n org/server` |
| 认证 | OAuth + 策略令牌 | `smithery auth login / token --policy <json>` |
| Skills | 搜索安装 | `smithery skill search / add` |

**关键局限：** 适合独立开发者/原型验证，团队生产需要 MCP Gateway（认证管理+审计+灰度）。

## 关联概念

- ⬅️ [[concepts/ai-coding-tools-comparison|AI 编码工具对比]]
- ⬅️ [[concepts/harness-engineering-deep-study|Harness 工程深度研究]]
