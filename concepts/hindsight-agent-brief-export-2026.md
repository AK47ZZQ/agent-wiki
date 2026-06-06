---
title: Hindsight Agent Brief (5 文档导出)
created: 2026-06-03
updated: 2026-06-03
type: concept
tags: [meta, export, hindsight, brief, agent-feeding]
sources:
  - ~/hermes-all/exports/hindsight-agent-brief/ (7 文件, 61 KB)
confidence: high
source: hindsight-deployment-2026-06
---

# Hindsight Agent Brief (5 文档导出)

> **目标**: 把 Hindsight 全部经验转化为可喂给其他 Agent 的 5 文档 + Wiki 同步.

## 7 文件清单 (1719 行, 61 KB)

| # | 文件 | 行 | 受众 |
|---|---|---|---|
| 00 | [00-README.md](~/hermes-all/exports/hindsight-agent-brief/00-README.md) | 134 | 入口 + 决策树 |
| 01 | [01-deploy-guide.md](~/hermes-all/exports/hindsight-agent-brief/01-deploy-guide.md) | 351 | 装 Hindsight |
| 02 | [02-handoff-api.md](~/hermes-all/exports/hindsight-agent-brief/02-handoff-api.md) | 249 | 调 retain/recall |
| 03 | [03-case-study-5-stages.md](~/hermes-all/exports/hindsight-agent-brief/03-case-study-5-stages.md) | 315 | 5 阶段案例 |
| 04 | [04-4-tier-architecture.md](~/hermes-all/exports/hindsight-agent-brief/04-4-tier-architecture.md) | 239 | 4 层架构 |
| 05 | [05-decision-matrix.md](~/hermes-all/exports/hindsight-agent-brief/05-decision-matrix.md) | 300 | 装不装决策 |
| 99 | [99-references.md](~/hermes-all/exports/hindsight-agent-brief/99-references.md) | 131 | 来源汇总 |

**路径**: `~/hermes-all/exports/hindsight-agent-brief/`

## 5 文档使用场景

| 场景 | 读哪些 |
|---|---|
| 装 Hindsight | 00 + 01 + 02 |
| 调 retain/recall | 02 |
| 避坑 | 03 |
| 理解架构 | 04 |
| 评估装不装 | 00 + 05 + 04 |
| 引用来源 | 99 |

## 飞书同步状态

- **本次不手动同步飞书** (按你之前定的规矩: 09:00 cron 独立维护)
- 09:00 cron 会自动读 `~/hermes-all/exports/hindsight-agent-brief/` 同步到飞书文档
- 期间飞书文档保持原状

## Wiki 同步状态

- ✅ `wiki/AGENTS.md` 已精简 (3.8 KB, 反映 plugin 默认接受)
- ✅ `wiki/concepts/hindsight-in-hermes-ecosystem-2026.md` (7.4 KB, 真实定位)
- ✅ `wiki/methods/install-hindsight-native-hermes-method.md` (7.2 KB)
- ✅ `wiki/methods/hindsight-4d-retrieval-complete.md` (6.1 KB)
- ✅ `wiki/notes/hindsight-local-deployment-windows-2026.md` (4.9 KB)
- ✅ `wiki/notes/hindsight-risks-and-optimizations-2026.md` (6.6 KB)
- ✅ `wiki/comparisons/hindsight-automation-patterns-2026.md` (5.6 KB)
- ✅ `wiki/comparisons/hermes-memory-systems-comparison-2026.md` (8 provider 对比)
- ✅ `wiki/AGENTS.md` (本文件, 精简版架构)

## 关键决策 (2026-06-03 接受)

- **接受 L2 plugin auto-retain** (不与 plugin 竞争)
- **0 cron 任务** (主动化最易反弹)
- **0 自动 hook** (BC 混合失败, 已卸)
- **MAX_RETAINS_PER_SESSION=5** (handoff 限频)
- **Hindsight Cloud 暂不切换** (local 跑得稳)

## 验证 (装好后跑这些)

```bash
# 1. Server 跑
curl http://localhost:8888/health  # 期望: {"status":"healthy"}

# 2. Hermes 接入
hermes memory status  # 期望: Provider: hindsight

# 3. 端到端
hindsight memory retain hermes "test fact"
sleep 3
hindsight memory recall hermes "test"  # 期望: 命中

# 4. 内存监控
python C:\Python314\hindsight_watchdog.py  # 期望: status=healthy, rss_mb<1024
```

## 下次 review 触发条件

- 装 Hindsight 0.7+ 时
- Hermes 升级到 0.16+ 时
- plugin 默认行为变更时
- 你说"重新审视"时

## 关联文档

- [[concepts/hindsight-in-hermes-ecosystem-2026]] — 真实定位
- [[methods/install-hindsight-native-hermes-method]] — 安装方法
- [[methods/hindsight-4d-retrieval-complete]] — 4 维检索
- [[notes/hindsight-local-deployment-windows-2026]] — 部署
- [[notes/hindsight-risks-and-optimizations-2026]] — 风险
- [[comparisons/hindsight-automation-patterns-2026]] — 4 模式
- [[comparisons/hermes-memory-systems-comparison-2026]] — 8 provider
- `install-hindsight-as-hermes-memory` skill
- `hindsight-watchdog` skill
- `hindsight-handoff` skill
