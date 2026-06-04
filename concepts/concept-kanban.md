---
title: "Kanban — Hermes 内置并行任务调度系统"
created: 2026-05-29
updated: 2026-05-30
type: concept
tags: [tech, tool, workflow, hermes, multi-agent]
confidence: high
---

# Kanban — Hermes 内置并行任务调度系统

## 核心定义

Hermes 内置的 Kanban 看板系统，用于多代理协作和并行任务编排。调度器内嵌在 Gateway 进程中，30 秒轮询自动派发任务给 Worker。

## 架构

```
你 (Feishu)
  │
  └── 编排器 (deepseek-v4-flash) ← 规划 + 验收 (5%)
         │
         └── Kanban 调度器 (Gateway 内嵌, 30s 轮询)
                ├── minimax-worker1 ─ MiniMax M2.7
                ├── minimax-worker2 ─ MiniMax M2.7
                ├── minimax-worker3 ─ MiniMax M2.7
                ├── minimax-worker4 ─ MiniMax M2.7
                └── minimax-worker5 ─ MiniMax M2.7 (会员制, 无限token)
```

## Worker 配置

| 项 | 值 |
|:---|:---|
| 模型 | `minimax-cn/MiniMax-M2.7` (5 worker 完全相同) |
| Skill | `ai-harness-exploration` + `hermes-workflow` (精确加载) |
| 上下文 | LCM 上下文压缩引擎 ✅ |
| 记忆 | 只读（不污染编排器空间） |
| 分配 | Round-Robin 轮转 |
| SOUL.md | 通用型（搜/编/写/析/审全能） |

## 核心能力

### 并行执行
- 5 路同时并发，墙钟 ≈ 最慢 Worker 耗时
- 5 任务墙钟 ~3.5min（串行需 ~9min，加速比 ~2.6×）
- 每轮成本 ≈ ¥0.006（deepseek 编排）+ ¥0（MiniMax 会员）

### 依赖链 (`--parent`)
- 无 parent → 立即 ready，并行执行
- 有 parent(s) → 等父卡都 done 后自动 promoted → ready
- AND 条件（多个 parent 全部完成才触发）

### Swarm 模式 (内置扇出扇入)
```bash
hermes kanban swarm "主题" \
  --worker worker1:搜索A \
  --worker worker2:搜索B \
  --verifier worker4 \
  --synthesizer worker5
```
自动生成依赖链：workers(并行) → verifier(审查) → synthesizer(合稿)

### 持久 Workspace (`dir:`)
Scratch workspace 任务完成后 GC 清空。使用 `dir:` 持久路径跨 Worker 共享文件：
```bash
kanban create "任务" --workspace "dir:C:\workspace\kanban\project-x"
```

### 上下文治理
- Worker 启用 LCM stateless 模式（会话不持久化）
- sessions.auto_prune=true, retention=30 天
- 每日 02:00 Kanban GC（清理 workspace/日志）
- failure_limit=3，dispatch_stale_timeout=30 分钟

## 定时维护

| 时间 | 任务 |
|:----|:-----|
| 02:00 | Kanban GC（workspace + 事件 + 日志清理） |

## 关键陷阱

| 陷阱 | 方案 |
|:-----|:-----|
| Scratch GC 清空文件 | 使用 `dir:` 持久 workspace |
| Swarm 标题含冒号 → 被解析为 skill 分隔符 | 标题不用冒号 |
| auto_decompose:true 与 decompose CLI 冲突 | 关闭 auto_decompose，手动 decompose |
| Worker 401 认证失败 → 旧 API key | 重启 Gateway 重新加载 .env |

## 数据基线

| 指标 | 值 |
|:-----|:---|
| 5 路并发墙钟 | ~3.5min (最慢 Worker) |
| 串行 5 任务对比 | ~9min |
| 每轮成本 | ¥0.006 (deepseek) |
| db 大小 | ~25MB |
| cron 频率 | 30s 轮询 |
