---
title: "Method: Feishu 命令文档 → Wiki 手动同步"
created: 2026-05-29
updated: 2026-06-04
type: method
tags: [method, workflow, feishu, wiki, sync]
confidence: high
source: hermes-session
---

# Method: Feishu 命令文档 → Wiki 手动同步

> 2026-06-04 精简：原"07:30 cron 全自动流水线"已废弃，改为手动按需同步。

## 现状（2026-06-04 起）

- **轻量同步脚本** `sync-feishu-commands.py`（替换 5/31 删除的 `wiki-feishu-pipeline.py`）
- 目标文档：`FHF3dWeXRoTRU9xKeb5cSRC1nMI`（Hermes命令大全V2）
- 单向同步：飞书 → `wiki/references/hermes-commands-full.md`（自动 commit）
- **手动触发**，**无 cron**（遵循 2026-06-03 "0 cron" 决策）
- 版本记录：`wiki/.feishu-pipeline-stamp.json`（revision_id + sha256）

## 架构（精简后）

```
飞书文档 (FHF3dWeXRoTRU9xKeb5cSRC1nMI)
  → lark-cli docs +fetch (v2 API)
    → 写入 wiki/references/hermes-commands-full.md
      → git commit + 更新 stamp
```

## 使用方式

```bash
# 手动同步 (按需)
python "C:\Users\Administrator\AppData\Local\hermes\scripts\sync-feishu-commands.py"

# 静默模式（无变更不输出）
# 脚本内置: --silent 标志自动启用，仅在 revision 变化时输出
```

## 已知陷阱

- 飞书文档用 `--doc <token>`（不是 `--document-id`）
- lark-cli 需用完整路径 `AppData/Roaming/npm/lark-cli.cmd` 调用（subprocess PATH 问题）
- 飞书 API v2 与 v1 字段差异：`document.revision_id`（v2）vs `data.revision_id`（v1）
- 6 天以上不冷启动 → lark-cli token 可能过期，需先 `lark-cli auth login`

## 何时同步

- 飞书命令文档发布新版本
- 发现本地 `hermes-commands-full.md` 落后于飞书
- memory-maintenance 提示有命令相关 drift

## 历史

- **2026-05-29** 创建：基于 `wiki-feishu-pipeline.py` + 07:30 cron 的"全自动流水线"愿景
- **2026-05-31 23:24** 夜间维护误删 `wiki-feishu-pipeline.py`（git `9090251c7`）
- **2026-06-01** 新建 `sync-feishu-commands.py`（轻量替代，仅同步命令文档）
- **2026-06-03** AGENTS.md 精简：0 cron 原则，删除飞书同步 cron
- **2026-06-04** 本文档更新：明确"手动同步"为新约定，dry-run 验证 rev 34→38 链路正常

## 相关

- [[concepts/hindsight-in-hermes-ecosystem-2026]] — Hermes 记忆生态
- [[hermes-skill-wiki-ingest]] — 知识摄入管道（更通用的版本）
- [[hermes-skill-wiki-archive]] — 会话归档
- [[methods/hermes-workflow-and-exploration]] — Hermes 工作流整体概述
