---
title: LCM 升级记录 (v0.12.0 → v0.15.0)
created: 2026-06-03
updated: 2026-06-03
type: note
tags: [tech, lcm, upgrade, maintenance]
sources:
  - https://github.com/stephenschoettler/hermes-lcm/releases/tag/v0.15.0
  - local: ~/hermes-all/hermes/lcm.db
confidence: high
source: lcm-3rd-notebook-2026-06
---

# LCM 升级记录 (v0.12.0 → v0.15.0)

**日期**: 2026-06-03
**操作**: 升级 hermes-lcm plugin
**前置版本**: v0.12.0
**目标版本**: v0.15.0
**方式**: 直接下载 GitHub tarball + 覆盖 plugin 目录

## 升级前发现

之前一直以为最新是 v0.14.0（基于 README 显示）。**实际最新是 v0.15.0**，2026-06-03 发布（升级当天！）—— 跳过了 2 个中间版本。

## 升级步骤

| 步骤 | 操作 | 结果 |
|---|---|---|
| 1 | 备份 plugin 目录到 `lcm.bak-0.12.0` | ✅ |
| 2 | 备份 lcm.db 到 `lcm.db.bak-pre-v0.14.0` | ✅ |
| 3 | 删 `__pycache__/*.pyc` 防止旧字节码 | ✅ |
| 4 | `curl -sL https://api.github.com/repos/stephenschoettler/hermes-lcm/tarball/v0.15.0` | ✅ 4.9MB |
| 5 | `tar -xzf` 解包到 `/tmp/stephenschoettler-hermes-lcm-*` | ✅ |
| 6 | `cp -r` 覆盖到 `site-packages/plugins/context_engine/lcm/` | ✅ |
| 7 | 验证 `plugin.yaml` 显示 v0.15.0 | ✅ |
| 8 | `lcm_status` → 报 `plugin_version: 0.15.0` | ✅ |
| 9 | `lcm_doctor` → 12 项检查全过（无 regression） | ✅ |

## 关键发现

### v0.15.0 新功能
- `codex_spark_context` preset（GPT-5.3 Codex Spark 128k 路线）
- `/lcm preset suggest` 增强（区分 128k Spark vs 272k long-context）
- 改进的 benchmark provenance
- **runtime config 仍 inspect-only**（无 auto-apply）— 安全设计

### 升级无破坏性原因
1. **DB schema 自动迁移**：`db_bootstrap.py` 包含 `ALTER TABLE ... ADD COLUMN` 自动跑
2. **JSON 元数据兼容**：旧 lifecycle 数据自动 normalization
3. **工具签名兼容**：7 个 lcm_* 工具 API 未变

## 升级后状态

| 指标 | 数值 |
|---|---|
| `plugin_version` | **0.15.0** |
| `store.messages` | 739 |
| `database_size` | 28.7 MB (+5MB vs 0.12.0) |
| `lifecycle_fragmentation` | warn (历史碎片，不变) |
| `context_pressure` | 47.1% |

## 备份位置

| 备份 | 路径 | 大小 |
|---|---|---|
| 旧 plugin 源码 | `C:\Python314\Lib\site-packages\plugins\context_engine\lcm.bak-0.12.0` | ~1MB |
| 旧 lcm.db | `C:\Users\Administrator\AppData\Local\hermes\lcm.db.bak-pre-v0.14.0` | ~25MB |

## 关键教训

1. **README 显示 0.12.0 不代表最新** — 检查 GitHub releases API
2. **覆盖式升级比 pip 可靠** — 这是 LCM 推荐方式（不是 pip 包）
3. **删 `__pycache__` 是必须的** — 防止旧 .pyc 与新源码混用
4. **lcm.db schema 迁移是自动的** — `db_bootstrap.py` 内置 ALTER TABLE

## 关联文档

- [[comparisons/hermes-memory-systems-comparison-2026]] — LCM 在 Hermes 生态的定位
- [stephenschoettler/hermes-lcm 原仓库 README](https://github.com/stephenschoettler/hermes-lcm)
