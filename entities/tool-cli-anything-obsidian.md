---
title: "CLI-Anything Obsidian CLI"
created: 2026-05-30
updated: 2026-05-30
type: entity
tags: [entity, tool, cli, obsidian]
confidence: high
source: hermes-archiver
---

# CLI-Anything Obsidian CLI

**cli-anything-obsidian v1.1.0** — 通过 Obsidian Local REST API 控制 Obsidian 笔记库的 CLI 工具。

## 安装路径

```
/c/Users/Administrator/cli-anything/obsidian/agent-harness/
pip install -e .
```

## 命令组

| 命令组 | 功能 |
|:------|:------|
| `vault` | 笔记列表/读取/创建/更新/删除 |
| `search` | 全文搜索（query/simple）|
| `note` | 激活笔记操作 |
| `command` | Obsidian 内部命令执行 |
| `server` | 服务状态查询 |
| `session` | 会话管理 |
| `repl` | 交互式会话模式 |

## 本机配置

- **插件**: Obsidian Local REST API v4.1.2
- **端口**: 27124 (HTTPS, 自签名证书)
- **API Key**: `hermes-obsidian-local-cli`
- **Vault**: `C:\Users\Administrator\wiki` (80+ pages)
- **认证**: `verify=False` (requests 自签名跳过)

## 已知问题

`search query` 默认 DQL 模式在 v4.x 废弃，已修复为降级到 `/search/simple/` (POST + URL 参数)。`jsonlogic` 模式正常工作。

## 相关链接

- [[concepts/cli-anything]]
- [[entities/hermes-skill-cli-anything-methodology]]
- [[concepts/full-stack-ecosystem]]
