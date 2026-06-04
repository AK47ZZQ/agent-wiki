---
title: AGENTS.md — Hermes Agent 工作环境与协作规约
created: 2026-06-04
updated: 2026-06-04
type: meta-protocol
tags: [agents, meta, protocol, multi-agent, hermes, v2]
sources: [hermes-self-check, wiki-keeper-v1.6, methods/using-knowledge-base]
---

# AGENTS.md — Hermes Agent 工作环境与协作规约 (v2)

> 写给**任何**要操作本环境的 Hermes Agent(主对话 / 3rd 笔记本 / 未来 agent)。v2 全面更新(2026-06-04 18:30+, Hermes 仓库删除 + wiki-keeper v1.6 协议后)。

## TL;DR

- **3 个角色** = main-claude(主对话) / hermes-3rd(笔记本) / future-agents
- **3 个仓库**: 1) hermes-all 本地 backup(已删远端) 2) agent-wiki 云端(主) 3) hermes 内部(hermes-all 本地)
- **5 步核验**: 永远走 `scripts/safe-commit-push.sh` v1.6,不裸 git
- **100% 公开 wiki**: https://github.com/AK47ZZQ/agent-wiki

## 1. 当前架构(4 层记忆 + 1 共享 KB)

### 1.1 4 层记忆

| Tier | 名称 | 实现 | 状态 |
|---|---|---|---|
| **L0** | Working Memory | Hermes 原生 messages | ✅ |
| **L1** | Short-term | LCM v0.15.0 | ✅ 7 压缩, 23.6:1 |
| **L2** | Long-term | Hindsight local v0.6.1 (auto-retain) | ✅ 81 facts |
| **L3** | Hard-coded | memory tool | ⚠️ 94% 满 |

### 1.2 1 共享 KB(多 Agent 第二大脑)

```
┌─────────────────────────────────────────────┐
│  agent-wiki (GitHub cloud)                  │
│  https://github.com/AK47ZZQ/agent-wiki      │
│  + PARA + Zettelkasten 融合                 │
│  + 73+ .md / 8 类目 / 100% frontmatter       │
│  + 0 死链 / 0 cron                          │
└─────────────────────────────────────────────┘
       ↑                                    ↑
       main-claude                        hermes-3rd
       (台式 Windows)                  (笔记本)
       commit + push                commit + push
       + wiki-keeper v1.6          + wiki-keeper v1.6
       + safe-commit-push         + safe-commit-push
```

### 1.3 0 自动化

- ✅ **0 cron**
- ✅ **0 自动 hook**
- ✅ **0 自动 retain**(除 Hindsight plugin 默认)
- ✅ **0 wiki 自动推送**(manual,5 步核验)

## 2. 3 节点角色(2026-06-04 18:30+)

| 节点 | 平台 | 状态 | 主任务 |
|---|---|---|---|
| **main-claude** | Windows 11(台式) | 🟢 活跃 | 每日 1-2 条 wiki + 协议维护 |
| **hermes-3rd** | Windows 11(笔记本) | 🟡 在线 | 每日 0-1 条 wiki + scratchpad 同步 |
| **future-agents** | 任意 | ⚪ 待入 | 拉 wiki + wiki-keeper + 5 步核验 |

### 2.1 main-claude 身份

- **位置**: `C:\Users\Administrator\hermes-all\`
- **git 用户**: `Hermes <hermes@hermes.local>`
- **写入权限**: 全部 wiki 类目
- **任务调度**: 用户指令驱动(0 cron)

### 2.2 hermes-3rd 身份

- **位置**: 笔记本端(待确认精确路径)
- **git 用户**: `Hermes 3rd` (per AGENTS v1.4 规约)
- **写入权限**: 全部 wiki 类目(per 协议)
- **任务调度**: 自身 + 用户协作

## 3. 5 步核验协议(wiki-keeper v1.6)

### 3.1 为什么需要

- **不依赖单一信号**:`git commit` 输出"成功" 不等于真成功
- **防假成功**:`git push` 输出"Everything up-to-date" 不等于真推
- **必须**:`commit 对象存在(cat-file 验证)` + `远端 hash = 本地 hash`

### 3.2 协议命令(永远用)

```bash
bash scripts/safe-commit-push.sh "commit message"
```

**禁止**:
- ❌ 裸 `git add -A && git commit && git push`
- ❌ `git push` 看到"success" 就信
- ❌ 跳过任何 1 步

### 3.3 v1.6 vs v1.5 升级

| 升级 | v1.5 | v1.6 |
|---|---|---|
| 排除 `.canvas` / `.bak` / `.obsidian/*` 等 | ❌ | ✅ |
| Step 1.5 排除 Obsidian 本地 | ❌ | ✅ |
| 自动写 `.gitignore` 防御 | ❌ | ✅ |
| 6 步核验(原 5 步 + Step 1.5) | 5 步 | 6 步 |

**3rd 反馈驱动**: `c030a77` commit 报 `未命名.canvas` 被 v1.5 误 add,v1.6 修复。

## 4. 写作规约(wiki 第二大脑)

### 4.1 5 问检查(开写之前)

1. 能复用吗?(grep 找)
2. 能链接吗?(至少 1 个 wikilink)
3. 有源吗?(sources 字段)
4. 位置对吗?(concepts/methods/notes/entities/tasks)
5. frontmatter 齐吗?(6 字段)

### 4.2 § 4.0 申请(本 skill)

- 写新 wiki 内容 = 必申请(ai-harness-exploration § 4.0)
- 维护(死链/索引/frontmatter 修复) = 不需申请
- 9 字段 frontmatter(title/created/updated/type/tags/sources)

### 4.3 5 反模式

- ❌ 复制 LCM 摘要
- ❌ 写百科条目
- ❌ 改 frontmatter schema
- ❌ 用 `\u2014` 等 unicode escape
- ❌ 跳过 `check-wiki-quality.py`

## 5. 协作规约(多 Agent)

### 5.1 通信 4 频道

| 频道 | 介质 | 何时用 |
|---|---|---|
| **Git remote** | GitHub `agent-wiki` | 长效内容(wiki) |
| **scratchpad/** | 本地文件 | 短期协调(任务上下文) |
| **LCM 摘要** | L1 内存 | 跨 session 上下文 |
| **send_message** | 飞书/IM | 用户通知 |

### 5.2 git 协作 3 步

1. `git fetch origin main` 拉最新
2. `git pull --rebase`(不 merge,避免分叉)
3. `bash safe-commit-push.sh "msg"` 推

### 5.3 冲突解决

- 3rd 看到冲突 → 报告 main-claude → **不擅自修**
- main-claude 看到冲突 → pull --rebase + 修
- **绝不 force-push**(协议 v1.1 § 2.2)

## 6. 工具栈

| 工具 | 用途 | 位置 |
|---|---|---|
| **Hermes CLI v0.15.2** | 主 agent | 全局 |
| **LCM v0.15.0** | 上下文压缩 | Hermes 内置 |
| **Hindsight local v0.6.1** | 长期记忆 | PID 6224:8888 |
| **memory tool** | 硬编码事实 | Hermes 内置 |
| **session_search** | 历史检索 | FTS5 |
| **wiki-keeper skill v1.6** | wiki 维护 | `hermes/skills/...` |
| **safe-commit-push.sh v1.6** | 5 步核验 | `wiki/scripts/` |
| **check-wiki-quality.py** | 死链/索引/frontmatter 验证 | `wiki/scripts/` |

## 7. 仓库清单(2026-06-04 18:30+)

| 仓库 | 远端 | 状态 |
|---|---|---|
| **agent-wiki** | `https://github.com/AK47ZZQ/agent-wiki` | 🟢 主推 |
| **hermes-all(本地)** | ❌ 远端已删(2026-06-04 18:00) | 🟡 local backup only |
| **hermes(上游)** | `NousResearch/hermes-agent` | 🔵 upstream(无写权限) |

**变更记录**:
- 2026-06-04 18:00 用户**删除** GitHub `AK47ZZQ/hermes` 仓库
- `hermes-all` 本地目录仍在,`1c2ef6324` commit(wiki-keeper v1.5)保留
- **所有新写入**走 `agent-wiki` 仓库

## 8. 决策记录

- ✅ **接受 Hindsight plugin auto-retain**(不与 plugin 竞争)
- ✅ **0 cron**(2026-06-03 精简)
- ✅ **PARA + Zettelkasten 融合**(2026-06-04 改版)
- ✅ **agent-wiki 是唯一远端 wiki 仓库**(2026-06-04 18:30)
- ✅ **5 步核验 = wiki-keeper v1.6 协议**(2026-06-04 18:30)
- ✅ **hermes user.name = "Hermes"**(2026-06-04 17:00)
- ✅ **hermes-all 仓库本地保留,远端删**(2026-06-04 18:00)

## 9. 关联文档

- `wiki-keeper` skill (本地, 在 hermes-all 仓库的 hermes/skills/) — v1.5/v1.6 skill 详细
- [[methods/safe-commit-push-protocol]] — 5 步核验详细
- [[methods/using-knowledge-base]] — wiki 整体入口
- [[protocols/git-collaboration-multi-agent]] — 协作协议
- `agents/main-claude.md` (本地) — 主对话身份
- [[agents/hermes-3rd]] — 笔记本身份
- [[concepts/agent-4-tier-memory-architecture]] — 4 层记忆设计
- `indexes/knowledge-map.md` (本地) — wiki 知识地图

## 10. v1 → v2 变更日志

- v1(2026-06-03 精简版):4 层记忆 + 0 cron + 3 件工具
- v2(2026-06-04 18:30+): 加入 5 步核验 + 多 Agent 第二大脑 + 仓库清单 + 协作规约
- 旧内容(L2 token 成本 / handoff v1.2 / 卸载清单) — 保留在 v1,详见 git history
