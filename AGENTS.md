# AGENTS.md — Hermes 记忆系统（精简版）

> 2026-06-03 接受 Hindsight plugin 默认 auto-retain, 精简到最小可用集.

## 当前架构 (4 层)

| Tier | 名称 | 实现 | 状态 |
|---|---|---|---|
| **L0** | Working Memory | Hermes 原生 messages list | ✅ 1247 msgs, 905k tokens |
| **L1** | Short-term | LCM v0.15.0 (context.engine: lcm) | ✅ 7 压缩, 23.6:1 ratio |
| **L2** | Long-term | Hindsight local v0.6.1 (plugin auto-retain) | ✅ 81 facts, **plugin 默认行为** |
| **L3** | Hard-coded | memory tool (1375+825 字符) | ⚠️ 94% 满 |

## 接受的关键事实

- **Hindsight plugin 默认 `_auto_retain=True`** — 每 turn 静默 retain
- **你接受这个默认行为** (不与 plugin 竞争)
- **handoff v1.2 是 manual API** — 0 自动调用
- **L2 token 成本 ~10k/天** (plugin 控制, 你不能直接停)

## 部署栈 (现状)

```
Hermes CLI v0.15.2
  + LCM v0.15.0 (context engine)
  + Hindsight local v0.6.1 (memory provider)
    - Server: PID 6224, port 8888
    - Bank 'hermes': 81 facts
    - Plugin auto-retain: ON (默认)
  + memory tool (built-in, 94% full)
  + session_search (FTS5)
  + wiki (Obsidian Graph)
```

## 0 自动化

- ✅ **0 cron 任务**
- ✅ **0 自动 hook**
- ✅ **0 自动 retain** (handoff 是 manual)
- ⚠️ **Plugin 默认 auto-retain ON** (你接受)

## 3 件工具 (manual API)

| 工具 | 用途 | 何时用 |
|---|---|---|
| `hindsight_handoff.py` | 5 重防死循环 + 3 API | 想手动 retain 关键事实 (避开 plugin) |
| `hindsight_watchdog.py` | 内存监控 | 怀疑 Hindsight 跑久了内存涨 |
| `hindsight memory {retain,recall,reflect}` CLI | 官方 CLI | 单次手动操作 |

## 关键文件

| 路径 | 用途 |
|---|---|
| `~/.hermes/hindsight/config.json` | Hermes provider 配置 |
| `~/.hermes/hindsight/handoff_state.json` | handoff 限频/去重状态 |
| `~/hermes-all/hermes/scripts/` | (无 hook 了, 已精简) |
| `C:\Python314\hindsight_handoff.py` | handoff v1.2 主程序 |
| `C:\Python314\hindsight_watchdog.py` | watchdog 主程序 |
| `C:\Python314\start_hindsight_local.py` | server 启动 |

## 决策记录 (2026-06-03)

- **接受 L2 plugin auto-retain** (不改 Hermes 内部)
- **0 cron** (你否决过, 保持)
- **0 自动 hook** (BC 混合失败, 已卸)
- **MAX_RETAINS_PER_SESSION=5** (适配多 candidates, 但实际 0 uses)
- **Hindsight Cloud 暂不切换** (local 跑得稳)

## 精简掉的

- ❌ `on_session_end hook` (per-turn, 0 candidates, 1.25s/turn 浪费)
- ❌ `hindsight-session-end-hook-implementation.md` (BC 混合失败记录)
- ❌ `hindsight-trigger-protocol-v1.md` (从未使用)
- ❌ `hindsight-exploration-2026-06-03.md` (临时日志)
- ❌ `hindsight-handoff-v1-anti-deadlock.md` (合并到 skill)
- ❌ 4 个 .bak 文件 (上次卸载备份)

## 关联文档 (精简后剩 10 个)

- [[concepts/hindsight-in-hermes-ecosystem-2026]] — 真实定位
- [[methods/install-hindsight-native-hermes-method]] — 安装方法
- [[methods/hindsight-4d-retrieval-complete]] — 4 维检索完整
- [[notes/hindsight-local-deployment-windows-2026]] — 本地部署记录
- [[notes/hindsight-risks-and-optimizations-2026]] — 风险与优化
- [[comparisons/hindsight-automation-patterns-2026]] — 4 模式对比
- [[comparisons/hermes-memory-systems-comparison-2026]] — 8 provider 对比
- `install-hindsight-as-hermes-memory` skill (安装)
- `hindsight-watchdog` skill (监控)
- `hindsight-handoff` skill (manual API)

## 验证清单

- [x] Hindsight server 跑 (PID 6224, 9.7 MB RSS)
- [x] LCM v0.15.0 在跑 (cache hit 99.74%)
- [x] 0 cron, 0 hook, 0 自动 retain (除 plugin 默认)
- [x] memory tool 94% 满 (待清理, 但能用)
- [x] 10 个 wiki 文档齐全
- [x] 3 个 skill 部署 (install/watchdog/handoff)
