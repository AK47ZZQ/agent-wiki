---
title: AGENTS.md 严重 stale 检测报告 — 2026-06-04 18:35
created: 2026-06-04
updated: 2026-06-04
type: note
tags: [note, agents-md, stale, audit, drift-detection]
source: AGENTS.md (mtime 14:38) + 实际 daemon 状态 (18:25 自检) + 3rd 学习报告
confidence: high
---

# AGENTS.md 严重 stale 检测报告

> 本笔记**不改** AGENTS.md (CLAUDE.md § 2.1 写协议 + 跨 agent 资源需协商), **只报告 stale 事实**, 提议 main-claude 修正.

**触发**: 2026-06-04 18:25 Hermes 3rd 学习阶段, 对比 `AGENTS.md` (顶层 3.8K, mtime 14:38) 与实际系统状态 (18:25 self-check 输出)
**结论**: AGENTS.md **落后一天**, 9 个字段有偏差, 部分数字偏 154 倍. 建议 main-claude **下个 commit** 全面更新 AGENTS.md.

---

## 1. 偏差对照表 (9 项)

| 字段 | AGENTS.md 写 (14:38) | 实际 (18:25) | 偏差 | 严重度 |
|---|---|---|---|---|
| **Hermes 版本** | v0.15.2 | **v0.15.1** | -1 patch | 🟡 |
| **Hindsight 版本** | v0.6.1 | **v0.7.2** | -1 minor | 🟡 |
| **Hindsight 端口** | 8888 | **9177** | 端口错 | 🟡 |
| **Hindsight PID** | 6224 | **17300** | 进程 ID 错 | 🟢 (动态) |
| **Hindsight RSS** | 9.7 MB | **1505 MB** | **154 倍** | 🟡 |
| **MEMORY.md 容量** | 94% 满 (1375+825) | **26% 满 (4133/16000)** | 已修复但未同步 | 🟡 |
| **L1 状态** | LCM v0.15.0 在跑 | **本机没装 LCM** | 不一致 | 🟡 |
| **L2 facts** | 81 | **400+** | +5 倍 | 🟡 |
| **L0 messages** | 1247 | **941** (state.db 数字) | -304 | 🟢 (动态) |

---

## 2. 偏差来源分析

### 2.1 大部分偏差来自 6-4 14:25-15:13 的修复 (A.1)

`notes/hindsight-daemon-fix-2026-06-04.md` 详细记录:
- Hindsight v0.6.1 → **v0.7.2 升级** (修复过程中由 `pip install --upgrade` 完成)
- 端口 8888 → **9177** (v0.7.2 默认端口变更)
- PID 6224 → **17300** (新进程)
- RSS 9.7 MB → **1505 MB** (bge-m3 模型 + pg0 数据全部加载)
- L2 facts 81 → **400+** (v0.7.2 daemon 启动后持续 retain)

### 2.2 MEMORY.md 偏差来自 6-4 14:48 修复 (本报告作者 A 自检)

`notes/hermes-selfcheck-2026-06-04.md` 详细记录:
- MEMORY.md 从 7,548 字符 (94% 满) → **4,133 字符 (26% 满)** (合并 3 个 Hindsight troubleshooting entries)
- limit 从 8K → **16K** (config.yaml `memory_char_limit`)
- USER.md 从 5K → **10K** (config.yaml `user_char_limit`)

### 2.3 LCM 偏差来自更早的 6-3 笔记

`notes/lcm-upgrade-v0.12-to-v0.15.md` 记录 6-3 升级到 v0.15.0, 但**实际本机当前没装 LCM** (3rd 18:25 学习时验证 `plugins/context_engine/` 只有 `__init__.py`).
- **可能**: 升级笔记指的是 C:\Python314 隔离环境, 不是当前 `E:\hermes\hermes-agent` venv
- **或者**: 升级后又被卸载, 未记录
- **AGENTS.md 没反映**这个状态

---

## 3. 建议的 AGENTS.md 更新 (供 main-claude 参考)

### 3.1 顶层 4-Tier 架构表 (建议替换)

```markdown
| Tier | 名称 | 实现 | 状态 |
|---|---|---|---|
| **L0** | Working Memory | Hermes 原生 messages list (state.db) | ✅ 941 msgs (2026-06-04 18:25) |
| **L1** | Short-term | **未装 LCM** (本机) | ⚠️ 缺 (待评估 LCM v0.16.0) |
| **L2** | Long-term | Hindsight local **v0.7.2** (port 9177) | ✅ 400+ facts, 0 failed |
| **L3** | Hard-coded | memory tool (16000+10000 字符) | ✅ 26% 满 (已扩容) |
```

### 3.2 部署栈块 (建议替换)

```markdown
Hermes CLI v0.15.1
  + **未装 LCM** (本机; 台式 C:\Python314 有 v0.15.0)
  + Hindsight local v0.7.2 (memory provider)
    - Server: PID 17300, port 9177, RSS 1505 MB
    - Bank 'hermes': 400+ facts
    - Plugin auto-retain: ON (默认)
  + memory tool (built-in, 26% 满, 16K 软限)
  + session_search (FTS5)
  + wiki (Obsidian Graph + AK47ZZQ/agent-wiki 云端)
```

### 3.3 验证清单 (建议追加)

```markdown
- [x] Hindsight server 跑 (PID 17300, 1505 MB RSS)
- [x] **0 cron, 0 hook, 0 自动 retain** (除 plugin 默认)
- [x] memory tool **26% 满 (16K 软限)** — 6-4 14:48 扩容后
- [x] AGENTS.md **2026-06-04 18:35 检测到 stale** — 提议下个 commit 全面更新
```

---

## 4. 3rd 为何不自己改 AGENTS.md

按 CLAUDE.md § 2.1 + § 2.5 + § 5 (多 Agent 协作):

| 协议 | 要求 | 3rd 解读 |
|---|---|---|
| § 2.1 写协议 | 用户明确要求 | ❌ 用户没让 3rd 改 AGENTS.md |
| § 2.5 反模式 | 改写旧内容 (非追加) | AGENTS.md 是"实时记忆", 不是"积累型 wiki 页" |
| § 5 多 Agent | 跨 agent 资源需协商 | AGENTS.md 是 main-claude 主导, 3rd 写"提议" |
| 写入协议 (README) | 任何写入必须申请 (§ 4.0 申请协议) | 没 main-claude 在线, 申请对象缺失 |

**结论**: 3rd **写报告 + 提议 + 标置信度** (本笔记), 留 main-claude 决.

---

## 5. stale 检测方法论 (本报告沉淀)

### 5.1 检测维度 (5 维)

1. **版本号** (Hermes / Hindsight / LCM)
2. **端口** (daemon 监听)
3. **进程指标** (PID, RSS — 动态, 但基线值应稳定)
4. **资源使用** (MEMORY.md / USER.md 字符数 vs 软限)
5. **架构组件存在性** (LCM 装没装)

### 5.2 检测频率

- **手工**: 7 层自检时 (7 天 1 次) 必查
- **自动**: 暂无; 建议 future 写 `_diag/agents-md-stale-check.py` (跟 Hindsight provider matrix 一起)
- **触发**: wiki sync 完成后 (本批 A1+A2) 自动跑一次 stale-detect

### 5.3 偏差严重度分类

- 🟢 动态 (PID / 数字统计) — 不算 stale, 是 snapshot
- 🟡 配置 (版本 / 端口 / 路径 / 软限) — 真 stale
- 🟡 架构 (装没装 / 有没有) — 真 stale
- 🔴 矛盾 (有 vs 没有 / 写 vs 实) — 立即修

---

## 6. 关联文档

- 自检方法: [[notes/hermes-selfcheck-2026-06-04]] (7 层自检触发本报告)
- Hindsight 修复: [[notes/hindsight-daemon-fix-2026-06-04]] (本次 stale 偏差的主因)
- LCM 升级笔记: [[notes/lcm-upgrade-v0.12-to-v0.15]] (冲突的来源, 6-3 升 v0.15.0 但本机没装)
- Hermes 4-Tier 架构 (待更新): [[AGENTS]]
- 笔记本协作者: [[agents/hermes-3rd]] / [[entities/hermes-3rd]]
- 4-Tier 架构 (顶层 .md): [[agent-4-tier-memory-architecture]]
- 主动化方法论: [[hindsight-first-active-workflow]]
- 记忆模式: [[hindsight-first-memory-pattern]]
