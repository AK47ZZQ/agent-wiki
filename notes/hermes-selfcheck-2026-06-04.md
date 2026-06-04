---
title: Hermes 7 层系统自检报告 — 2026-06-04 14:48
created: 2026-06-04
updated: 2026-06-04
type: note
tags: [note, self-check, hermes, daemon, 7-layer, health]
source: hermes 飞书 history (2026-06-04 14:48 完整 7 层报告) + 本会话自检脚本输出
confidence: high
---

# Hermes 7 层系统自检报告

> 2026-06-04 14:48 笔记本侧 Hermes 系统完整 7 层自检. 报告基于 `hermes-self-audit` skill 7 层结构, 输出结构化表格 + 真实命令证据.

**触发**: Hindsight daemon 修复完成后, 全面验证系统健康
**耗时**: ~12 分钟 (查 7 层 + 跑 4 验证 + 写报告)
**结论**: ✅ 核心工作正常; ⚠️ 2 个中风险 (MEMORY.md 容量 + daemon RSS)

---

## 1. 检查方法 (7 层 + 2 修正)

| 层 | 检查项 | 工具 |
|---|---|---|
| L1 | daemon 进程 / 端口 | tasklist, netstat |
| L2 | LLM 路径 (provider/model/base_url) | hermes.env + daemon metrics |
| L3 | 配置 + env 一致性 | cat + diff |
| L4 | endpoints 状态 | curl /health /version /stats |
| L5 | operations 队列 (failed/pending/processing) | curl /operations |
| L6 | 存储层 (pg0 + .md) | du + sqlite3 + MemoryStore |
| L7 | 知识库 / MEMORY.md 一致性 | check-wiki-quality.py + python read |

**关键修正** (本报告方法论沉淀):
- 字节数 ≠ 字符数 (中文 UTF-8 一字 3 字节) — 之前混淆
- `MemoryStore.add` 不静默拒, 返 `{success: False, error: ...}`
- `_sync_turn_observations` / `agent_loop.py:440 fire-and-forget` 实际代码里**不存在** (之前 Plan B 描述未真正落地)

---

## 2. 检查结果 (5 PASS + 2 中风险)

### 2.1 进程 + 端口 + 资源

| 角色 | PID | RSS | 状态 |
|---|---|---|---|
| gateway parent (venv) | 2964 | 1.1 MB | idle wrapper |
| **gateway main (py311)** | 8856 | **82.8 MB** | 正常服务 |
| hindsight-daemon parent (venv) | 12448 | 1.1 MB | idle wrapper |
| **hindsight-daemon main (py311)** | 17300 | **1505.3 MB** | bge-m3 + pg0 全加载 |

**Total pythonw: 8, Total RSS: 1621 MB**

### 2.2 Hindsight daemon

| 端点 | 状态 | 关键数据 |
|---|---|---|
| `/health` | ✅ 200 | `database: connected` |
| `/version` | ✅ 200 | **v0.7.2**, 5 features |
| `/stats` | ✅ 200 | nodes=400, links=8853, docs=16, obs=112 |
| ops_by_status | ✅ | `{'completed': 57}` — pending=0, failed=0, processing=0 |

### 2.3 配置 + env

| 项 | 值 | 状态 |
|---|---|---|
| `HINDSIGHT_API_LLM_PROVIDER=minimax` | ✅ | hermes.env line 1 |
| `HINDSIGHT_API_LLM_BASE_URL=https://api.minimaxi.com/v1` | ✅ | line 4 (带 i 真域名) |
| `HINDSIGHT_API_LLM_MODEL=MiniMax-M2.7-highspeed` | ✅ | line 3 |
| daemon 实际用 | ✅ 匹配 | metrics 暴露 minimax + M2.7-highspeed |
| NTFS junction `~/.hermes` ↔ `E:\hermes\hermes` | ✅ | inode 相同, env 文件 mtime 一致 |

### 2.4 pg0 + bank 持久化

| 项 | 状态 |
|---|---|
| pg0 data size | **75.7 MB** |
| 独立 Python 进程 recall | ✅ 5 results / 14 entities (命中 4 条今天 retain) |

**数据真在 pg0 磁盘**, daemon 重启仍可查.

### 2.5 Hermes gateway + MEMORY.md

| 项 | 值 | 状态 |
|---|---|---|
| `E:/hermes/hermes/memories/MEMORY.md` | 7,548 字符 / 8,000 软限 | ⚠️ **94% 满** |
| `E:/hermes/hermes/memories/USER.md` | 2,459 字符 / 5,000 软限 | ⚠️ 49% |
| `memory_store.db` (SQLite) | 0 facts / 0 entities | ⚠️ 完全未使用 (legacy 路径) |
| gateway 在 9090 端口 | 飞书长连 (不暴露 HTTP) | 设计如此 |

### 2.6 Skills / Tools / MCP

| 域 | 状态 |
|---|---|
| Tools enabled (CLI) | **20/27** |
| Skills | 169 enabled |
| MCP servers | 4 (tavily × 3 + feishu) |
| Cron jobs | 0 (符合"无 cron"原则) |
| config.yaml | v26, 17,175 字节, mtime 2026-06-04 14:07 |

### 2.7 模型 + 缓存 + cost

| 项 | 值 |
|---|---|
| Hermes 版本 | v0.15.1 (2026.5.29) |
| **主模型** | **MiniMax-M3** (provider=minimax) |
| **Context length** | **512,000 tokens** |
| **兜底链** | M2.7-highspeed → V4 Flash → V4 Pro |
| **daemon LLM 调用累计** (since 21:13) | **71 calls** (33 retain_extract + 28 consolidation + 9 reflect + 1 verification) |
| **0 失败** | ✅ 所有调用 success=true |

---

## 3. 风险清单 (2 中 + 6 低)

| 风险 | 等级 | 描述 | 建议 |
|---|---|---|---|
| **MEMORY.md 7,548/8,000 (94%)** | 🟡 中 | MemoryStore 写时硬拒, 新 turn 写入可能**静默丢** | 跑 `hermes memory` 压缩或调高 limit |
| **USER.md 2,459/5,000 (49%)** | 🟡 中 | 接近 5K 软限, 75% 压缩阈值已过 | 同上 |
| **daemon 1.5 GB RSS** | 🟢 符合 | bge-m3 1GB + pg0 1GB | idle_timeout=1800 已设 |
| **memory_store.db 0 facts** | 🟢 低 | legacy SQLite 路径, Hindsight v0.7.2 已切 pg0 | 不需处理 |
| **`~/.hermes` ↔ `E:\hermes\hermes` NTFS junction** | 🟢 已消解 | 同 inode, 无配置漂移 | 无需 |
| **MEMORY.md 容量问题** | 🟡 中 | 当前 94% 软限, 写入可能静默 | 1) 跑压缩 2) 放宽 limit (8K → 16K) |
| **0 cron jobs** | 🟢 合规 | 符合"无 cron"原则 | 无需 |
| **20/27 tools enabled** | 🟢 健康 | 关键工具全开 | 按需开 |

---

## 4. 结论 + 后续动作

### 4.1 系统核心工作正常 ✅

- Hindsight daemon 全栈 OK, LLM 调用 0 失败
- Hermes gateway 健在 (飞书 9090 长连)
- 持久化 pg0 持续增长 (248 → 400 nodes / 半小时)
- 兜底链、嵌入、provider 配置全部对齐

### 4.2 2 项中风险已修复 (后续动作)

| 风险 | 修复 |
|---|---|
| MEMORY.md 7,548 → 4,133 字符 (-45.2%) | 合并 3 个 Hindsight troubleshooting entries 为 1 |
| MEMORY.md 8K → 16K, USER.md 5K → 10K | 改 `config.yaml` `memory_char_limit` |

**修复后**: 5 端点 verify 全 200, MemoryStore reload 6 entries, test add 成功.

### 4.3 矛盾识别 (写报告方法论)

| 自检时报告 | 真实 | 修正 |
|---|---|---|
| MEMORY.md 10,407 字节 = 130% 软限 | 7,548 字符 = 94% 软限 | 字节数 ≠ 字符数 (中文 UTF-8) |
| `MemoryStore.add` 静默拒 | 返 `{success: False, error: ...}` 不静默 | 之前 memory 描述错 |
| `_sync_turn_observations` 已部署 | 实际代码 grep 不到 | Plan B 描述未真正落地 |

---

## 5. 自检方法论沉淀 (给未来 agent 复用)

### 5.1 7 层结构 (本报告骨架)

```
L1 进程/端口/资源
L2 LLM 路径
L3 配置/env
L4 endpoints
L5 operations 队列
L6 存储层
L7 知识库一致性
```

### 5.2 5 个常见陷阱 (本报告踩过)

1. **字节数 ≠ 字符数** (中文 UTF-8)
2. **静默拒 vs error 返** (看 `MemoryStore.add` 实现, 不假设)
3. **历史 memory 描述** 可能过期 (本报告自查 `_sync_turn_observations` 描述)
4. **daemon metrics 是真值** (不是 hermes 自己的 claim)
5. **legacy 路径** (如 `memory_store.db`) 可能完全未用, 报告要标 "dead code"

### 5.3 验证清单 (4 步)

- [ ] 7 层每层跑实际命令 (tasklist / curl / sqlite3 / cat)
- [ ] 数字 + 单位 (字节 vs 字符 vs tokens)
- [ ] 矛盾自检 (拿"已知事实" vs "实际命令输出" 对照)
- [ ] 风险等级 (🔴 高 / 🟡 中 / 🟢 低) + 修复建议

---

## 6. 关联文档

- 触发场景: [[notes/hindsight-daemon-fix-2026-06-04]] (14:25 修复后立刻自检)
- 自检方法: [[agents/hermes-self-check]] (模板)
- Hermes 4-Tier 记忆: [[AGENTS]]
- L0 (Working Memory): Hermes 原生 messages list (state.db)
- L2 (Long-term): Hindsight local v0.7.2
- L3 (Hard-coded): memory tool (1375+825 字符默认, 已调高到 16K+10K)
- 笔记本协作者: [[agents/hermes-3rd]] (本报告作者) / [[entities/hermes-3rd]]
- Hindsight 修复: [[notes/hindsight-daemon-fix-2026-06-04]]
