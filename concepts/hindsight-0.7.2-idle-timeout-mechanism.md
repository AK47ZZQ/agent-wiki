---
title: "Hindsight 0.7.2 daemon idle timeout 机制 (1800s SIGTERM)"
created: 2026-06-04
updated: 2026-06-04
type: concept
tags: [hindsight, daemon, idle-timeout, sigterm, lifecycle, 0.7.2, minimax, hermes]
sources:
  - 本会话(2026-06-04)Hermes 3rd 笔记本实测
  - main-claude 台式 notes/hindsight-deployment-and-monitoring-2026-06-04.md
  - Hindsight 0.7.2 daemon 源码 grep (hindsight_api.daemon module)
confidence: high
---

# Hindsight 0.7.2 daemon idle timeout 机制 (1800s SIGTERM)

> **核心事实**:`HINDSIGHT_EMBED_DAEMON_IDLE_TIMEOUT=1800` (默认 1800 秒 = 30 分钟) 触发时, daemon 主进程 `hindsight_api.daemon` 检测到 worker pool 全部 idle 达到阈值, 调 SIGTERM 自杀, 退出码 15 (正常 shutdown signal, 不是 crash).

> **笔记本场景矛盾**: Hindsight v0.7.2 设计假设"有客户端持续调 retain/recall"防 idle, 但**笔记本飞书 gateway 走 Hermes CLI 主循环, 不直连 9177**, 0 流量 → 30 分钟 idle → daemon 自杀 → 笔记本 Hindsight 长期记忆链路断.

> **3rd 实战证据 (2026-06-04)**: 启 daemon 19:48 → 21:04 idle SIGTERM (75 分钟运行, 含 30 分钟 idle 检测 + 0 retain/recall 流量).

## 1. 触发条件 4 要素 (4 路独立证据)

| 要素 | 真实值 | 证据 |
|---|---|---|
| **env var 名** | `HINDSIGHT_EMBED_DAEMON_IDLE_TIMEOUT` | daemon 启动 env log + hindsight_api.daemon module grep |
| **默认值** | **1800** 秒 (30 分钟) | 跟 main-claude `notes/hindsight-deployment-and-monitoring-2026-06-04.md` § 3 一致 |
| **触发行为** | `hindsight_api.daemon: "Idle timeout reached (1800s), shutting down daemon"` → SIGTERM (exit 15) | 笔记本 21:04 daemon log 实际打印 |
| **worker pool 状态** | `pool: size=1 limits=5-100 idle=1 in_use=0` (缩到 1 worker, 全 idle, 0 active retain/recall/reflect) | 笔记本 21:02-21:04 持续 `[WORKER_STATS]` 日志 |

**关键细节**: **不是 retain 0 = idle**, **是 worker 全 idle + 0 active operation 达到 1800s 阈值**才触发. 笔记本实际跑了 30+ 分钟 (19:48 启, 21:04 退) 中间 30 分钟持续 0 active 才自杀.

## 2. 笔记本 vs 台式场景差异

| 维度 | 台式 main-claude (0.6.1, port 8888) | 笔记本 Hermes 3rd (0.7.2, port 9177) |
|---|---|---|
| **daemon 版本** | 0.6.1 | **0.7.2** (新) |
| **port** | 8888 | **9177** (profile hermes metadata) |
| **守护方案** | ✅ `hindsight-healthcheck.py` cron 5 min tick 自动重启 (`hermes cron list` 显示 4793e7a07e08) | ❌ **无 cron, 无 watchdog, 21:04 SIGTERM 死了就死** |
| **流量源** | Hermes CLI 主循环 + 飞书 gateway 持续调 retain/recall | 飞书 gateway 走 9090, **不直连 9177** = 0 流量 |
| **Idle 概率** | 低 (持续流量) | **高 (30 分钟内必 idle)** |
| **18+ 小时 broken 历史** | 6-3 14:46 → 6-4 18:08 (6+ 小时 broken) | **6-3 19:15 → 6-4 19:48 (18+ 小时 broken, 比台式长 3×)** |

## 3. 4 个"为什么 SIGTERM" 隐藏细节

| # | 隐藏细节 | 3rd 笔记本实测证据 |
|---|---|---|
| 1 | **不是 0 retain 触发, 是 0 active operation 持续 1800s 触发** | 19:48 启后 0 retain/recall/reflect, 但 pool 仍持续 30 分钟, 然后才 SIGTERM (不是 0 active 立刻) |
| 2 | **worker pool 会先缩到 1 worker (`pool: size=1`), 然后触发退出** | 21:02-21:04 持续 log 显示 `pool: size=1 limits=5-100 idle=1 in_use=0` |
| 3 | **exit code 15 (SIGTERM) ≠ crash (exit 1)** | 进程 proc_0caa14a7fecb 退出码 15 = 正常 shutdown signal, 不是 OOM 或异常 |
| 4 | **`--daemon` 模式才检测 idle, foreground 模式不检测** | `python -m hindsight_api.main --daemon --idle-timeout 1800` (检测) vs `python -m hindsight_api.main --port 9177` (不检测, foreground) |

## 4. 跟 4 周前 3rd onboard 笔记的差异

| 之前笔记说 | 真相 | 证据 |
|---|---|---|
| "Hindsight v0.7.2 默认有 keep-alive" | ❌ **错, 默认 1800s idle 自杀** | daemon log 直接打印 `Idle timeout reached (1800s)` |
| "笔记本跟台式 Hindsight 链路一致" | ❌ **错, 笔记本无 cron 守护** | `hermes cron list` 笔记本无 `hindsight-healthcheck` |
| "改 base_url 修了 Hindsight" | ⚠️ **只修了 LLM 链路, 守护问题没解决** | 19:48 base_url 修 → 21:04 仍 SIGTERM |
| "笔记本 Hindsight 完全恢复" | ❌ **错, 短暂恢复后还会死** | 19:48-21:04 跑 75 分钟 = 1.5 小时, 之后又死 |

## 5. 关联文档

- [[concepts/agent-4-tier-memory-architecture]] — 4 层记忆架构
- [[methods/hindsight-idle-timeout-watchdog]] — 笔记本无 cron 守护法
- [[notes/hindsight-deployment-and-monitoring-2026-06-04]] — main-claude 台式 0.6.1 + 8888 + cron 守护
- [[notes/hindsight-0.7.2-bank-config-migration]] — 3rd 笔记本 0.7.2 + 9177 修复
- [[notes/hindsight-daemon-fix-2026-06-04]] — 3rd 14:25 base_url 修复

## 6. 实战时间线 (3rd 笔记本 2026-06-04)

```
19:48  启 daemon PID 20520 (base_url 修后, 5 验证全 PASS)
19:48-20:34  daemon 健康, worker pool 持续 0 active
20:34-21:04  持续 0 active 30 分钟, pool 缩到 size=1
21:04:48  Idle timeout reached (1800s), shutting down daemon
21:04      SIGTERM (exit 15), PID 20520 死, port 9177 空
21:05+     /health HTTP 000, Hindsight 不可用
```
