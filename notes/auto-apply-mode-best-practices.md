---
title: Auto-Apply 模式最佳实践 (cron 8 步 + 5 guard rails)
created: 2026-06-05
updated: 2026-06-05
type: note
tags: [note, cron, auto-apply, hermes, memory-maintenance, best-practices, guard-rails]
source: |
  v1.6 "Re-enable guard rails" 修订 + 2026-06-05 00:50 main-claude 实战 + 用户硬偏好
confidence: high
---

# Auto-Apply 模式最佳实践

> 适用于**任何** LLM-agent-driven cron 任务的设计,不仅 memory maintenance。**核心思想**: 信任 agent 跑、留 backup 可回滚、5 guard rails 兜底、用户只看飞书最终结果。

## 1. 演化时间线

| 日期 | 模式 | 决策 | 后果 |
|---|---|---|---|
| 2026-06-02 | 无 | 0 cron | 干净 |
| 2026-06-03 | 1 cron (memory-staleness-monthly) | 第一次加 cron | 紧 token 预算 |
| 2026-06-04 morning | 3 cron (memory-staleness + memory-maintenance + hermes-full-maintain) | "minimax m3 订阅制量大管饱" | 任务数 = 3 |
| 2026-06-04 evening | **全部 teardown** | MEMORY 3500→5000 chars only-add bias | 0 cron 重新确立 |
| 2026-06-05 00:30 | 0 cron (但 memory limit 扩 40000/10000) | 用户硬偏好 | 0 cron |
| 2026-06-05 00:47 | 2 cron (memory-maintenance-morning + evening, **agent-driven**, staging review mode) | 用户硬偏好 + 5 guard rails | 2 cron,review 闸门 |
| **2026-06-05 00:50** | **2 cron (auto-apply mode, no review gate)** | **用户硬偏好 "全自动整理"** | **2 cron,auto-apply** |

## 2. 8 步标准流程(以 memory-maintenance 为例)

```
[T-1h]  Cron scheduler tick (Gateway PID)
[T+0]   触发 cron job
        ↓
[T+5s]  spawn fresh Hermes session (无 in-context)
        prompt + skill=memory-maintenance 注入
        ↓
[T+10s] Step 0 preflight: 扫 merge conflict + 查 stale architecture name
[T+15s] Step 1 Survey: 读 MEMORY/USER.md,数 entries/chars
[T+30s] Step 2 Categorize: 🟢 Durable / 🟡 Consolidate / 🔴 Stale
[T+1m]  Step 3 Plan: removals + consolidations
[T+2m]  Step 4 AUTO-BACKUP: `cp MEMORY.md MEMORY.md.bak.<ts>` (guard rail 1)
[T+2.5m] Step 5 APPLY: 直接改 live 用 file read/write (guard rail 2)
        - 检查 adds ≤ removes (guard rail 3)
        - 不写 self-referential (guard rail 4)
[T+3m]  Step 6 Survey again: 前/后 chars + entries
[T+3.5m] Step 7 Feishu message: 完整 report (guard rail 5 token monitor)
[T+4m]  Done. Rollback 命令附在飞书消息末尾
```

## 3. 5 Guard Rails(v1.6 修订 for auto-apply)

| # | 名称 | 怎么防 | 实操命令 |
|---|---|---|---|
| 1 | **AUTO-BACKUP** | 改 live 前必 backup,7 天保留 | `cp MEMORY.md MEMORY.md.bak.$(date +%s)` |
| 2 | **APPLY DIRECTLY** | 直接改 live,不用 `memory()` action (它有 limit 不显示 diff) | 用 `read_file` + `write_file` 工具,不是 `memory()` |
| 3 | **EQUAL REMOVALS** | adds ≤ removes,不平衡 skip + 报 | agent 内部计数:len(removes) ≥ len(adds) |
| 4 | **NO SELF-REFERENTIAL** | 不写 "from cron" / "this is from automated run" 元 entry | agent 自我审查 |
| 5 | **TOKEN MONITOR** | 报前/后总 chars | 飞书消息: "Before: 9464/40000 (24%), After: 7200/40000 (18%)" |

## 4. Auto-Apply 模式 vs Staging-Review 模式

| 维度 | Staging-Review (旧) | Auto-Apply (新) |
|---|---|---|
| 用户 review | ✅ 必 | ❌ 不需要 |
| Backup | ❌ | ✅ `.bak.<ts>` |
| 改 live | ❌ staging file | ✅ 直改 |
| 飞书消息 | "建议 diff,请 apply" | "已 apply,完整 diff" |
| 误改回滚难度 | 重跑(可能) | `cp <bak> <live>` 30 秒 |
| Token 风险 | 低(人眼) | 中(agent 误判) |
| 适用场景 | 极高风险改动 | 90% 自动化场景 |

## 5. 飞书消息模板(9 段)

```
🧹 Memory Maintenance Report [morning/evening YYYY-MM-DD]

1. Before: 9464 / 40000 chars (24%), 13 entries
2. After:  7200 / 40000 chars (18%), 11 entries

Removed (2):
- 教程全集 — 一次性 session log
- MSYS curl 旧版 — 已被新版覆盖

Consolidated (1):
- LCM (3 lines → 1 line, 吸收 v2.x schema)

Added (0):
- (none)

Warnings: 无

Backup paths (rollback):
- C:\Users\...\MEMORY.md.bak.1762341600
- C:\Users\...\USER.md.bak.1762341600

Rollback: cp <backup-path> <live-path>

---
下次跑: 2026-06-05 18:00 (evening)
```

**或 0 changes**:
```
🧹 Memory Maintenance Report [morning 2026-06-05]
No changes needed. (last manual cleanup at 00:30)
```

**或 imbalance skip**:
```
🧹 Memory Maintenance Report [morning 2026-06-05]
Skipped: add/remove imbalance 3/1.
Reason: more additions than removals violates guard rail #3.
Next: agent will retry tomorrow.
```

## 6. cron 任务设计 checklist

设新 LLM-agent cron 时,自检 8 项:

- [ ] **schedule 用 cron syntax** (不是 "30m" / "every 2h"): `0 9 * * *` 比 "0 9 * * *" 通用
- [ ] **deliver = feishu** (你 home channel): `oc_56a22bfc2c7d92617d42ec50f62a5723`
- [ ] **skill = 任务专用 skill**: 不用 generic,让 LLM 拿到正确流程
- [ ] **prompt 自包含**: cron run 无 in-context,prompt 内含所有路径 + 约束
- [ ] **5 guard rails 写入 prompt**: 不依赖 skill 内部约定
- [ ] **no_agent = False** (默认): 除非真 trivial (healthcheck/alert),才用 `--no-agent`
- [ ] **bash/curl 注意**: MSYS 环境 curl POST JSON 必走 Python urllib
- [ ] **rollback 命令附报告**: 任何 apply 任务必给一键回滚命令

## 7. 已知风险与对策

| 风险 | 表现 | 对策 |
|---|---|---|
| **skill SKILL.md 内部建议用 `memory()` action** | agent 越过我 prompt 的 "用 file tools" 约束,直接改 live | 看第一次跑结果,如果越界,patch prompt 加 "Use file read/write tools only" |
| **staging file 残留** | `.staging` 文件留在 disk | auto-apply 模式**不**写 staging,无此问题 |
| **adds > removes 误判** | agent 偏好加新 entry,删少 | guard rail 3 强制 skip + 报 imbalance |
| **token 暴涨** | agent 误删 durable 条后补新条,反而涨 chars | guard rail 3 + 5 监测:前/后 chars |
| **3rd 端冲突** | cron 9:00 跑同时 3rd 端推 1 commit | cron 跑不动 live memory,3rd 推 git wiki,两不冲突 |
| **agent 死循环** | prompt 写 "if zero changes, silent" 但 agent 仍报飞书 | prompt 内加重: "EXIT SILENTLY if zero changes, do not even send feishu" |

## 8. 当前 3 cron 状态

| Job ID | Name | Schedule | 模式 | 触发什么 |
|---|---|---|---|---|
| `4793e7a07e08` | hindsight-healthcheck | every 5m | script (no_agent) | 5m 1 次 healthcheck 静默重启 |
| `75192f31bfd0` | memory-maintenance-morning | 0 9 * * * | **agent** (auto-apply) | 09:00 daily,改 MEMORY+USER,飞书报告 |
| `6284798cd28c` | memory-maintenance-evening | 0 18 * * * | **agent** (auto-apply) | 18:00 daily,同上 |

## 9. 未来扩展方向

- [ ] wiki 5 项自检 cron (替代手动)
- [ ] Hindsight healthcheck 升级到 LLM agent (从 5min 改 30min,带诊断)
- [ ] git push cheatsheet 自动演练 cron (5 步核验的 dry-run)
- [ ] 3rd 端 idle timeout 守护 cron

## 10. 关联文档

- [[AGENTS]] — v2 规约
- [[notes/lessons-learned-index]] — 经验索引
- [[methods/git-push-cheatsheet]] — 5 步核验
- [[methods/safe-commit-push-protocol]] — 协议
- `memory-maintenance` skill — v1.6 7 步流程
- `hermes-windows` skill — MSYS curl 坑
- `install-hindsight-as-hermes-memory` — Hindsight 部署

## 11. 元教训

> 自动化 ≠ 失控。Auto-apply 模式 + 5 guard rails + backup + 飞书 review = "用户信任 agent,但有兜底"。
> 反面:全静默 cron = 用户看不见 = 不可信。
> 反面:全 review 闸门 = 用户 review 疲劳 = 真问题被忽略。

## 12. D 报告验证(2026-06-05 00:58)

跑 `check-wiki-quality.py` 摸底后优化:

- 0 死链 / 0 缺索引 / 0 frontmatter 缺 / 0 secret
- 20+ orphan 全部为 `agents/ai-harness-exploration*` (已 SKIP_PREFIXES,预期)
- log.md 68K (历史累积) — 暂未裁剪
- 本 page 加入 lessons-learned-index § 7, 与其形成双向链

**结论**: auto-apply 模式可放心启用; 9:00 第一次跑观察 5 guard rails 是否被 agent 严格执行.
