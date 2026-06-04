---
title: Wiki 操作日志
created: 2026-06-02
updated: 2026-06-04
type: meta
tags: [log, wiki, history]
source: wiki/indexes/log.md
confidence: high
---

## 2026-06-02 — Hindsight 主动化 + 4-Tier 记忆架构

**操作**：创建 4 个新页面（1 概念 + 1 方法 + 1 工作流 + 1 AGENTS），2 个执行脚本

**触发**：用户要求"Hindsight 为主，LCM 辅助"全面拥抱 Hindsight。担心"如果 LCM 关闭主动压缩，对话上下文怎么控制"。

**产出**：
| 类型 | 路径 | 用途 |
|---|---|---|
| 概念 | `wiki/concepts/agent-4-tier-memory-architecture.md` | 4-Tier 记忆架构理论基础 |
| 方法 | `wiki/methods/hindsight-first-memory-pattern.md` | Hindsight 主动化方法论 |
| 工作流 | `wiki/workflows/hindsight-first-active-workflow.md` | 端到端执行手册 |
| AGENTS | `wiki/AGENTS.md` | 系统级应用规则 |
| 脚本 | `~/hermes-all/hermes/scripts/hindsight-nightly-retain.py` | 每日 23:00 cron 批量 retain |
| 脚本 | `~/hermes-all/hermes/scripts/hindsight-morning-reflect.py` | 每日 08:00 cron 拉早晨摘要 |

**关键决策**：
- **不删 LCM**，只重新定位（被动日志）
- **不改** `context.engine: lcm`（Kanban workers 需要）
- **不改** `memory.provider: hindsight`（已就位）
- **新加** cron 任务 2 个（23:00 + 08:00）
- **新加** Agent 行为守则（turn 内 self-check）

**验证**：
- ✅ morning-reflect.py 实测成功，3 段查询全返回高质量中文
- ✅ Hindsight retain/recall/reflect 链路工作正常
- ✅ M3 LLM + 中文嵌入 + 中文 reranker 全栈就位

**外部来源**（已记录到 frontmatter sources）：
1. cloudidr.com - 4-Tier 记忆架构权威文章
2. hindsight.vectorize.io - Hindsight 官方短/长期记忆指南
3. mem0.ai - 短/长期记忆工程师指南
4. devgenius.io - 2026 Agent 记忆系统综述
5. cnblogs/deephub - 中文综合

**下一步**：
- 用户明早检查，回复"go"则注册 cron

## 2026-06-03 — 精简 + 5 文档导出

**操作**:
- 接受 L2 plugin auto-retain (10k tokens/天)
- 精简 4 .bak + 4 个失败 wiki (session-end-hook / trigger-protocol / exploration-log / handoff-v1-anti-deadlock)
- 卸 on_session_end hook (per-turn 0 candidates)
- 改 MAX 3→5 (handoff 限频)
- 写 5 文档导出到 `~/hermes-all/exports/hindsight-agent-brief/` (7 文件, 1719 行, 61 KB)
- 写新概念页 [[concepts/hindsight-agent-brief-export-2026]]
- 更新 [[AGENTS]] (精简版, 3.8 KB)
- 更新 [[index]] (新表, 5 文档导出)

**关键决策**:
- **接受** plugin auto-retain (不改 Hermes 内部)
- **0 cron** (你否决过, 保持)
- **0 自动 hook** (BC 混合失败, 已卸)
- **handoff v1.2 0 主动调用** (manual API 备用)
- **飞书同步**: 09:00 cron 独立维护, 不手动推

**下一步**:
- 09:00 cron 自动同步 5 文档到飞书
- 用户 review 5 文档是否完整
- 评估 L3 memory tool 清理 (94% 满)

## 2026-06-04 — Memory Maintenance + Skill + Cron

**操作**:
- 扩 memory 容量 2200/1375 → **8000/5000** (3.6×)
- 解决 USER.md 未解决 git merge 冲突 (`<<<<<<<` / `=======` / `>>>>>>>`)
- 删重复段 (Services 写了两遍)
- 修过时数字: Wiki 92页 → **117页** (今加 5 文档 + 索引)
- 修过时架构: Kanban minimax-worker1~7 → **Swarm v2 10 semantic workers** (orchestrator/builder/...)
- 删过时: "L3 94% 满" 误述 → 改"L3 健康 (MEMORY 40% + USER 30%)"
- 写新 skill: `memory-staleness-detection` (9.5 KB SKILL.md + 5.5 KB check.py, 7 维检查)
- 写新 wiki: `agent-memory-state-2026.md` (6.1 KB, MEMORY/USER 镜像)
- 创建**唯一 cron**: `memory-staleness-monthly` (job 5c77e117e673, 月 1 09:00, **no_agent 模式**)

**关键发现**:
- Swarm **过渡期**: swarm.yaml (v2) 已切, profiles 目录仍 7 个老 minimax-worker1~7 (v1, 未迁移)
- Hindsight script 误用 `tasklist` 找不到 Python child process → 改用 `curl /health` 验证
- Hermes .bak 保留策略: 至少 7 天 (one full cron cycle), 跑稳后删
- 之前"0 cron"原则 vs 新 cron: **no_agent 模式例外** (纯脚本, 0 LLM token, 1 月 1 次, 飞书通知)

**验证**:
- ✅ memory-staleness-detection 跑通: 13 项检查, 🟢 11 + 🟡 2 + 🔴 0
- ✅ MEMORY 40% (3248/8000) + USER 30% (1512/5000) = 健康
- ✅ Git merge 冲突已解决
- ✅ Swarm 状态准确反映 (过渡期)

**下一步**:
- 2026-06-10: 检查 .bak.1780502939 7 天保留期到, 决定删/留
- 2026-07-01 09:00: 首次 cron 跑 memory-staleness-detection
- Swarm v1→v2 profiles 迁移 (待你决定)

- 2026-06-04 19:33: ABC 完成: 4 死链修复 (5 stub + 3 rename + index + AGENTS.md v2 + safe-commit-push.sh v1.6); 0 死链 / 102 索引 / check PASS
