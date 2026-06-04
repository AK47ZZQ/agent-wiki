---
title: "Hindsight 0.6.1 → 0.7.2 实战差异 (跨 main-claude 台式 + 3rd 笔记本 2 节点)"
created: 2026-06-04
updated: 2026-06-04
type: concept
tags: [hindsight, evolution, 0.6.1, 0.7.2, bank-config, hybrid-mode, cross-machine, hermes-3rd, main-claude]
sources:
  - main-claude 台式 notes/hindsight-local-deployment-windows-2026.md (0.6.1, port 8888, cron 守护)
  - 3rd 笔记本 notes/hindsight-0.7.2-bank-config-migration.md (0.7.2, port 9177, no cron)
  - 3rd 笔记本 notes/hindsight-deployment-and-monitoring-2026-06-04.md (台式 0.6.1 cron 方案)
  - 3rd 笔记本 notes/hindsight-daemon-fix-2026-06-04.md (14:25 base_url fix)
  - 3rd 笔记本 concepts/hindsight-0.7.2-idle-timeout-mechanism.md (1800s SIGTERM)
confidence: high
---

# Hindsight 0.6.1 → 0.7.2 实战差异 (跨 main-claude 台式 + 3rd 笔记本 2 节点)

> **核心差异**: 0.6.1 = 简单 daemon (port 8888 + `memory_mode: hybrid` 字段, 单一 config.json) → 0.7.2 = 复杂 bank 引擎 (port 9177 + bank config 33 字段, 3 类 API: retain/recall/reflect + PATCH /config). **跨 1 个 minor 版本, 内部架构改 1 大类**.

> **2 节点真实差异**: main-claude 台式跑 0.6.1 + 8888 + `hindsight-healthcheck.py` cron 5min tick 守护, 3rd 笔记本跑 0.7.2 + 9177 + 无 cron (21:04 idle 1800s SIGTERM). 同一公司同一项目, 2 套部署栈.

## 1. 6 维度差异表 (0.6.1 vs 0.7.2)

| 维度 | 0.6.1 (main-claude 台式) | 0.7.2 (3rd 笔记本) | 差异原因 |
|---|---|---|---|
| **pip 包** | `hindsight-api` 0.6.1 + `hindsight-api-slim` 0.6.1 + `pg0-embedded` 0.14.2 + `sentence-transformers` 5.5.1 | **`hindsight-all` 0.7.1** + `hindsight-api` 0.7.2 (本地 fork 加中国 LLM providers) | 3rd 笔记本 0.7.1 = **main-claude hermes fork** 加中国 LLM (minimax/deepseek/zai/fireworks) |
| **port** | 8888 (默认) | 9177 (profile hermes metadata) | 3rd 走 profile 分隔 (hermes/dev/test) |
| **Python** | 3.14.5 (台式 C:\Python314\) | 3.11.9 (笔记本 venv) | 笔记本 venv 限定 |
| **LLM** | `MiniMax-M2.5-highspeed` (OpenAI 兼容) | `MiniMax-M2.7-highspeed` (更新模型) | 3rd 笔记本用更新版 |
| **config 位置** | `~/AppData/Local/hermes/hindsight/config.json` (单一) | `~/.hindsight/profiles/hermes.env` (profile 分隔, ACL 保护) | 3rd 走 hermes.profile 机制 |
| **bank 配置** | `memory_mode: hybrid` (单字段, 0.6.1 时代) | **`bank_config_api` + 33 字段** (PATCH /v1/.../config 实时改) | 0.7.2 废除 `memory_mode`, 改细粒度字段 |
| **混合模式实现** | `memory_mode: hybrid` = 自动 reflect + auto retain | `enable_observations=true` + `enable_auto_consolidation=true` (2 字段) | 0.7.2 改细粒度 |
| **disposition** | 不可见 | `disposition_skepticism/literalism/empathy` 1-5 scale (新功能) | 0.7.2 新加 |
| **retain/reflect/observations mission** | 不可见 | 3 个 mission 字段 (LLM 抽 facts 知道目标) | 0.7.2 新加 |
| **extraction_mode** | 不可见 | `concise` / `detailed` 切换 | 0.7.2 新加 |
| **recall_budget_function** | 不可见 | `fixed` / `adaptive` 切换 | 0.7.2 新加 |
| **entity_labels** | 不可见 | `Dict[str, List[str]]` 9 类 (中文) | 0.7.2 新加 |
| **守护方案** | `hindsight-healthcheck.py` cron 5min tick + auto-restart | ❌ **无 cron, 无 watchdog**, daemon idle 1800s SIGTERM 自杀 | 笔记本"无 cron"原则 + 0.7.2 daemon 自带 idle 检测 |
| **retail 链** | sync retain 后立即命中 recall (no sleep) | 同 (实测 0.7.2 也立即命中) | 一致 |
| **/reflect 端点** | 顶级 `/reflect` (不在 `/memories/`) | 同 (0.7.2 也是 `/reflect`) | 一致 |
| **memory unit 字段** | `text` (不是 `content`) | 同 (0.7.2 也是 `text`) | 一致 |
| **PATCH /config schema** | ❌ 不可调 (只有 0.6.1 config.json) | ✅ `{"updates": {...}}` 包裹 (3 schema 坑) | 0.7.2 新加 |

## 2. 3 个核心 schema 坑 (0.6.1 → 0.7.2 迁移)

### 坑 1: `memory_mode: hybrid` 字段已废弃
```python
# 0.6.1 写法 (已废弃)
config.json: {"memory_mode": "hybrid"}

# 0.7.2 写法 (用 2 字段替代)
PATCH /v1/default/banks/hermes/config
{"updates": {
    "enable_observations": true,
    "enable_auto_consolidation": true
}}
```

### 坑 2: PATCH 端点要 `updates` 包裹
```python
# 错 (直接传字段 → 422 missing: updates)
PATCH /v1/default/banks/hermes/config
{"disposition_skepticism": 5}

# 对 (要 updates 包裹 → 200)
PATCH /v1/default/banks/hermes/config
{"updates": {"disposition_skepticism": 5}}
```

### 坑 3: `entity_labels` 是 `Dict[str, List[str]]` 不是 list
```python
# 错 (400 error)
{"entity_labels": ["Person", "Tool"]}

# 对 (LabelGroup pydantic 格式)
{"entity_labels": {"Person": ["姓名"], "Tool": ["工具"]}}
```

## 3. 2 节点链路真实状态 (2026-06-04 23:35)

| 节点 | 平台 | Hindsight 版本 | port | daemon 状态 | 守护 | 实战踩坑 |
|---|---|---|---|---|---|---|
| **main-claude (台式)** | Windows 11 server, 用户 Administrator | **0.6.1** | **8888** | ✅ 健康 (PID 6224) | ✅ `hindsight-healthcheck.py` cron 5min tick | 20:11 装 cron 守护, 2 次 tick 抓到 (latency 2-3s) |
| **Hermes 3rd (笔记本)** | Windows 11 + MSYS2, 用户 ZZQ | **0.7.2** | **9177** | ⚠️ **21:04 SIGTERM 死** (idle 1800s) | ❌ 无 cron | 14:25 base_url fix, 20:35 PATCH bank config, 21:04 idle 自杀, 22:00 改 public 后 GH013 阻 push |

**关键不对称**:
- main-claude 0.6.1 长期稳定, 守护方案成熟 (cron + healthcheck.py + state.json)
- 3rd 0.7.2 链路工作但守护弱, 21:04 SIGTERM 后本地 0 daemon
- **2 节点 0 协调 = 0 步通知, 死一边另一边不知道**

## 4. 0.6.1 vs 0.7.2 选型决策树

```
新装 Hindsight 笔记本/台式
│
├─ 选 0.6.1 (成熟稳定 + cron 守护 + 不需 bank config 细调)
│   适用: 不想管 bank config / 不需要 disposition / mission / entity_labels
│   路径: pip install hindsight-api + start_hindsight_local.py + cron
│
└─ 选 0.7.2 (新功能 + bank config 细调 + LLM 抽 facts 更精准)
    适用: 需要 LLM 深度理解用户偏好 / 中文实体抽取 / 自定义 mission
    路径: pip install hindsight-all + bank config PATCH + foreground daemon
    风险: 守护弱 (idle 1800s 自杀) + 中文 LLM provider 配错 (4 周前 3rd 笔记 14:25 fix)
```

## 5. 4 周前 wiki 协议 § 4 凭据/版本管理教训

| 教训 | 证据 |
|---|---|
| 0.6.1 → 0.7.2 升级不破坏 LLM 链路 (minimax 厂商稳定) | 14:25 fix base_url 5 验证全过 |
| bank config PATCH 是幂等 (PATCH null = 重置默认 3/3/3) | 5/4/5 + null 重置实测 |
| 0.7.2 `enable_observations + enable_auto_consolidation` 等价 0.6.1 `memory_mode: hybrid` | 3 笔记交叉验证 |
| 守护方案 (cron vs env) 跟版本号无关, 跟部署原则相关 | main-claude 0.6.1 + cron 守护, 3rd 0.7.2 + 无 cron 守护 |

## 6. 关联文档

- [[notes/hindsight-local-deployment-windows-2026]] — 0.6.1 部署 (main-claude 台式)
- [[notes/hindsight-0.7.2-bank-config-migration]] — 0.7.2 迁移指南 (3rd 笔记本)
- [[notes/hindsight-deployment-and-monitoring-2026-06-04]] — 0.6.1 cron 守护 (main-claude)
- [[notes/hindsight-daemon-fix-2026-06-04]] — 0.7.2 base_url fix (3rd 14:25)
- [[concepts/hindsight-0.7.2-idle-timeout-mechanism]] — 0.7.2 1800s SIGTERM
- [[methods/hindsight-idle-timeout-watchdog]] — 0.7.2 笔记本无 cron 守护法
- [[concepts/hindsight-memory-modes-guide]] — 4 mode 选型
- [[concepts/hindsight-in-hermes-ecosystem-2026]] — Hindsight 真实定位
- [[comparisons/hindsight-5-modes-2026]] — 5 mode 横向对比

## 7. 实战时间线 (跨 2 节点)

```
6-3       main-claude 台式: pip install hindsight-api 0.6.1 + port 8888 (PID 6224)
6-3 14:25 3rd 笔记本: pip install hindsight-all 0.7.1 + port 9177 (base_url 拼写错 + provider 错)
6-3 19:15 3rd 笔记本: 0.7.2 daemon 启动, 18+ 小时 broken
6-4 14:25 3rd 笔记本: base_url 修复 (minimax + /v1) + 5 验证全过
6-4 18:00 main-claude 台式: 启 hindsight-healthcheck.py cron 守护 (after 4-Tier architecture cron 反思)
6-4 20:11 main-claude 台式: cron tick 1 自动跑, latency 2364ms
6-4 20:30 3rd 笔记本: 0.7.2 PATCH bank config 5/4/5 + 3 mission + entity_labels
6-4 21:04 3rd 笔记本: 0.7.2 daemon idle 1800s SIGTERM (无 cron 守护)
6-4 22:00 仓库改 public (AK47ZZQ/agent-wiki)
6-4 22:25-23:30 3rd 笔记本: 装 ai-harness-exploration + 6 步探勘法实战 + push 远端真成功
```
