---
title: "CLI-Anything"
created: 2026-05-30
updated: 2026-05-30
type: concept
tags: [concept, cli, tool, opensource]
confidence: high
source: HKUDS/CLI-Anything
---

# CLI-Anything

**CLI-Anything** (HKUDS, 40.6K ⭐) — 将任意 GUI 桌面软件转换为 Agent-native CLI 的 SOP（标准操作流程）和工具集。

## 核心洞察

> **"无引擎，纯提示词"** — 整个项目的本质是一个 747 行的 HARNESS.md 提示词，AI Agent 读取后自动执行 8 阶段：分析→架构→实现→测试→文档→技能生成→发布。

## 生态数据

| 指标 | 值 |
|:----|:---:|
| GitHub Stars | 40.6K ⭐ |
| 社区 CLI 工具 | 700+ |
| 测试用例 | 2,269 |
| 最新版本 | v0.3.0 |
| 首次发布 | 2026-03-11 |

## 架构模式

- **模式 1**: 脚本 API 包装（Blender/GIMP — bpy 脚本生成）
- **模式 2**: REST API 包装（Obsidian/Novita — HTTP 封装）
- **模式 3**: 直接文件操作（Drawio/LibreOffice — XML/ODF 操作）
- **模式 4**: MCP 后端（Browser/DOMShell — stdio 传输）

## 命名空间包

PEP 420 命名空间包：所有 CLI 共享 `cli_anything` 命名空间，每个都是独立 PyPI 包（`cli-anything-*`），可共存。

## 相关链接

- GitHub: https://github.com/HKUDS/CLI-Anything
- CLI-Hub: https://hkuds.github.io/CLI-Anything/
- 本地克隆: `/c/Users/Administrator/cli-anything/`
- [[entities/hermes-skill-cli-anything-methodology]]
- [[concepts/harness-engineering]]
