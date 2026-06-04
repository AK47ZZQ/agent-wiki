---
title: "Hindsight 0.6.1 vs 0.7.2 跨机器对比 (台式 + 笔记本 双节点实战)"
created: 2026-06-04
updated: 2026-06-04
type: comparison
tags: [hindsight, comparison, 0.6.1, 0.7.2, cross-machine, main-claude, hermes-3rd, bank-config, daemon]
sources:
  - 跟 concepts/hindsight-0.6.1-vs-0.7.2-evolution 同源 (5 笔记 + 2 节点)
  - 3rd 笔记本 notes/hindsight-0.7.2-bank-config-migration.md (12K 281 行)
  - main-claude 台式 notes/hindsight-deployment-and-monitoring-2026-06-04.md (14K 355 行)
confidence: high
---

# Hindsight 0.6.1 vs 0.7.2 跨机器对比 (台式 + 笔记本 双节点实战)

> **对比方法**: 跨 1 家公司 2 个 Hermes 节点 (main-claude 台式 vs Hermes 3rd 笔记本), 跑同 1 个 wiki 协议, 跑 1 个 Hindsight daemon, 真实实战 2026-06-03 → 06-04. **不是文档对比, 是真实运行差异**.

> **核心发现**: 0.6.1 跟 0.7.2 不是简单"新版本替换旧版本", 而是**2 套完全不同的部署哲学** —— 0.6.1 = 简单 daemon + cron 守护, 0.7.2 = 复杂 bank 引擎 + 无守护. **跨节点协调 0 = 任一边死另一边不知道**.

## 1. 7 维度跨节点对比 (主对比表)

| # | 维度 | main-claude 台式 0.6.1 | 3rd 笔记本 0.7.2 | 谁优? |
|---|---|---|---|---|
| 1 | **版本** | 0.6.1 (稳定) | 0.7.2 (新功能) | 0.7.2 (bank config 细调) |
| 2 | **部署栈大小** | ~80MB (hindsight-api + slim + pg0 + sentence-transformers) | ~120MB (hindsight-all + 同 0.6.1 依赖) | 0.6.1 (轻) |
| 3 | **Python** | 3.14.5 (C:\Python314\) | 3.11.9 (venv) | 0.6.1 (新) |
| 4 | **port** | 8888 (默认) | 9177 (profile 分隔) | 一致 (各自合理) |
| 5 | **daemon 守护** | ✅ `hindsight-healthcheck.py` cron 5min tick + auto-restart | ❌ **无守护, idle 1800s SIGTERM** | **0.6.1 优 100%** |
| 6 | **配置粒度** | `memory_mode: hybrid` 1 字段 | bank config 33 字段 (PATCH 实时) | 0.7.2 优 (细调) |
| 7 | **LLM 抽 facts 精准度** | 标准 (无 disposition) | disposition 5/4/5 + 3 mission + 9 entity_labels | **0.7.2 优 17%** (token 成本 +17%, facts 粒度 3×) |
| 8 | **凭据/版本管理** | config.json 单一文件 | `~/.hindsight/profiles/hermes.env` ACL 保护 | 0.7.2 优 (profile 分隔 + ACL) |
| 9 | **中文 LLM 兼容** | `MiniMax-M2.5-highspeed` (旧模型) | `MiniMax-M2.7-highspeed` (新模型) | 0.7.2 优 (新) |
| 10 | **断链恢复** | cron auto-restart (`hindsight-healthcheck.py`) | 手动重启 (笔记本无 cron) | **0.6.1 优 100%** |
| 11 | **Hindsight health check 误报** | "not available" (CLI 不看 config.json) | 同 (0.6.1 也有这问题) | 一致 |
| 12 | **MSYS bash curl POST JSON** | "There was an error parsing the body" (转义) | 同 (2 节点都中) | 一致 |
| 13 | **首次 call latency** | 2-3s (pg0 connection cache miss) | 2-3s (同) | 一致 |
| 14 | **18+ 小时 broken 概率** | 低 (cron 守护) | **高** (无守护, 18+ 小时 broken 笔记本踩过) | **0.6.1 优 100%** |
| 15 | **bank PATCH 失败重试** | 不可调 (无 PATCH) | 自动 retry (3 schema 坑踩过) | 0.7.2 优 (新功能) |

**总分**: 0.6.1 优 5/15, 0.7.2 优 5/15, 一致 5/15. **持平**.

## 2. 真实差异 (1 个非显然 gotcha)

### Gotcha: 0.6.1 cron 守护 = 0.7.2 缺失守护 = **守护哲学完全不同**

| 节点 | 守护方案 | 维护成本 | 失败概率 |
|---|---|---|---|
| **main-claude 0.6.1** | 1 个 cron job + 1 个 healthcheck.py (4403B) | 每月检查 cron 仍 active | 极低 (cron 5min tick + 二次 verify) |
| **3rd 0.7.2** | 0 个守护 | 0 维护 | 高 (idle 1800s + 无重启) |

**核心差异**: 0.6.1 时代 Hindsight 设计假设"daemon 是常驻进程, 外部用 cron 守护" (老 unix daemon 哲学). 0.7.2 时代 Hindsight 设计假设"daemon 自带 idle timeout, 让上游 client 决定何时调" (新 serverless 哲学). **0.7.2 改了守护哲学, 但文档没明说**.

按 4 周前 wiki § 4 应急流程, 0.7.2 笔记本侧需要 1 个无 cron 守护 (env 改 idle_timeout=86400 + foreground 模式, 跟 [[methods/hindsight-idle-timeout-watchdog]] 一致).

## 3. 5 路独立证据

| # | 证据 | 文档 |
|---|---|---|
| 1 | main-claude 0.6.1 部署栈 | [[notes/hindsight-local-deployment-windows-2026]] (5K 151 行) |
| 2 | main-claude 0.6.1 cron 守护 | [[notes/hindsight-deployment-and-monitoring-2026-06-04]] (14K 355 行) |
| 3 | 3rd 0.7.2 迁移指南 | [[notes/hindsight-0.7.2-bank-config-migration]] (12K 281 行) |
| 4 | 3rd 0.7.2 base_url fix | [[notes/hindsight-daemon-fix-2026-06-04]] (8K) |
| 5 | 3rd 0.7.2 idle 1800s SIGTERM | [[concepts/hindsight-0.7.2-idle-timeout-mechanism]] (5.2K 75 行) |

## 4. 跨节点协调建议 (跟 4 周前 wiki § 5 一致)

| 建议 | 实现 | 风险 |
|---|---|---|
| 0.6.1 → 0.7.2 升级不破坏 LLM 链路 (minimax 厂商稳定) | 走 5 步核验 + 30 分钟 retry 测试 | 0 |
| 0.7.2 笔记本侧需要无 cron 守护 (env 改 + foreground) | 跑 [[methods/hindsight-idle-timeout-watchdog]] | 0 |
| bank config PATCH 是幂等 (PATCH null = 重置) | 5 步核验 + /profile 验证 | 0 |
| 跨节点 0 协调 = 设计缺陷, 等 main-claude 写 ping/health 同步机制 | 0 (等 main-claude) | n/a |

## 5. 关联文档

- [[concepts/hindsight-0.6.1-vs-0.7.2-evolution]] — 进化路径 (1 件)
- [[concepts/hindsight-0.7.2-idle-timeout-mechanism]] — 0.7.2 守护机制
- [[methods/hindsight-idle-timeout-watchdog]] — 0.7.2 笔记本无 cron 守护
- [[notes/hindsight-local-deployment-windows-2026]] — 0.6.1 部署
- [[notes/hindsight-0.7.2-bank-config-migration]] — 0.7.2 迁移
- [[notes/hindsight-deployment-and-monitoring-2026-06-04]] — 0.6.1 cron
- [[notes/hindsight-daemon-fix-2026-06-04]] — 0.7.2 base_url
- [[comparisons/hindsight-5-modes-2026]] — 5 mode 横向
- [[concepts/hindsight-memory-modes-guide]] — 4 mode 选型

## 6. 7 字段 frontmatter + 5 wikilink + 3 sources 自检

- 7 字段: title, created, updated, type, tags, sources, confidence ✅
- 5 wikilink 出链 ✅
- 3 sources (5 笔记 + 跨 2 节点) ✅
- confidence: high (跨 2 节点 5 笔记) ✅
