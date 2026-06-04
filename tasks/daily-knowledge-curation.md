---
title: Daily Knowledge Curation
created: 2026-06-04
updated: 2026-06-04
type: task
status: active
owner: main-claude + hermes-3rd
tags: [wiki, daily, cron, knowledge-management]
sources: [methods/wiki-curation-guide, protocols/git-collaboration-multi-agent]
---

# Daily Knowledge Curation

> 每天往 wiki 塞新知识的任务定义:谁来塞、塞什么、怎么同步。

## TL;DR

- **2 个智能体**轮流:**main-claude(台式)** + **hermes-3rd(笔记本)**
- **每天 1-3 条新知识**,topic 由每日 brief 决定
- **时间**:任意时刻,不必同时间
- **写前必须读** `methods/wiki-curation-guide.md`(5 问 4 步)
- **写后必走 8 步流程**(策划 → 申请 → 写 → 链接 → check → commit → push)
- **冲突按** `methods/wiki-curation-guide.md` § 5 **解决**

## 1. 任务范围

### 1.1 什么算"新知识"

- **新概念**:之前 wiki 没有的 AI/技术/方法概念
- **新方法**:可复用的操作流程(教程级)
- **新实体**:具体的工具/库/服务/产品
- **新比较**:横评(2+ 个相关工具对比)
- **新协议**:多 agent 协作新规则

### 1.2 什么不算

- **个人日记 / 心情** → LCM/memory,不进 wiki
- **一次性 bug 报告** → scratchpad,1 周后归档
- **复制粘贴的官方文档** → 不进 wiki(只写"我们用得怎么样")
- **会话摘要原文** → LCM 已压缩,直接复制 = 二次损失(见 curation § 7.2)

## 2. 角色分配

| 角色 | 节点 | 频率 | 负责类型 |
|---|---|---|---|
| **主塞者** | main-claude(我,台式) | **每天 1-2 条** | 方法 / 协议 / 中文场景 |
| **副塞者** | hermes-3rd(笔记本) | **每天 0-1 条** | 英文场景 / 3rd 视角 / 端到端测试反馈 |
| **质量检查** | 任何一端(write 前必须) | 每次 | 跑 `check-wiki-quality.py` |

**3rd 副塞**允许 0 条(笔记本不在,无需补)。

## 3. 单条新知识的标准流程

按 `methods/wiki-curation-guide.md` § 4 的 8 步。**简版**:

```
[1] 5 问检查(5 min)
   ↓ pass
[2] § 4.0 申请用户授权(在对话中列候选清单)
   ↓ 批准
[3] 选目录(concepts/ / methods/ / entities/ / notes/ / protocols/)
   ↓
[4] 写 frontmatter(6 字段:title/created/updated/type/tags/sources)
   ↓
[5] 写正文(分段,4-7 段,每段 1 主题)
   ↓
[6] 加 ≥2 wikilink(交叉引用现有页面)
   ↓
[7] 跑 check 脚本(0 死链 / 0 缺 frontmatter)
   ↓
[8] commit + push(协议 v1.1,先 fetch 再 rebase 再 push)
```

**预计时间**:15-30 min / 条。

## 4. 每日 Brief 模板

每天开始塞新知识前,在对话中(或 scratchpad 临时文件)列 1-3 条候选:

```markdown
## 2026-06-05 候选新知识

1. **[[concepts/<name>]]**(新) — 一句话说明 + 源 URL
2. **[[methods/<name>]]**(新) — 一句话说明 + 源 URL
3. **[[notes/<name>]]**(新) — 一句话说明 + 源 URL

每条都过了 5 问吗? [ ]
- [ ] 能复用
- [ ] 能交叉链接
- [ ] 有源
- [ ] 位置明确
- [ ] frontmatter 6 字段已想好
```

## 5. 同步与冲突

- 写完 commit 但**不立刻 push**(等所有今日新知识一起)
- **每天 23:00 统一 push**(按 `protocols/git-collaboration-multi-agent.md` § 3)
- 冲突时按 `methods/wiki-curation-guide.md` § 5 解决
- 第二天 main-claude 主动 fetch + rebase,把 3rd 的内容拉下来

## 6. 验收标准

每周日 23:30 main-claude 跑一次 `tasks/_archive/daily-curation-weekly-review.md`:

| 指标 | 周目标 |
|---|---|
| 新增 .md 页面 | 7-21(每天 1-3) |
| 死链 | <5(每条新页面应加 ≥2 wikilink) |
| 缺 frontmatter | <3(写时补) |
| 冲突解决次数 | <2(说明 3rd 也活跃了) |
| 3rd 推送 | ≥3 次(说明协作) |

## 7. 异常处理

| 异常 | 处理 |
|---|---|
| **今天 0 条** | OK,不强求(质量 > 数量) |
| **3rd 沉默 >3 天** | 发 `scratchpad/inbox-3rd.md` 询问 |
| **check 失败 > 10** | 暂停塞新,先修旧(污染 = -1 价值) |
| **3rd 推 force-push** | 违反协议 v1.1,提醒 + 拒收 |
| **用户打断塞新流程** | 立即停,回到用户任务 |

## 8. 相关资源

- `methods/wiki-curation-guide.md` — 完整策展指南(必读)
- `protocols/git-collaboration-multi-agent.md` — push 协议 v1.1
- `methods/wiki-as-second-brain.md` — 设计依据
- `scripts/check-wiki-quality.py` — 自检脚本
- `scripts/sync-daily.sh` — 每日 23:00 自动 sync(可参考)

## 9. 任务状态

- [x] 创建任务定义
- [ ] 第一天执行(2026-06-05 起)
- [ ] 第一周复盘(2026-06-11)
- [ ] 第一个月复盘(2026-07-04)

## 10. 变更日志

- 2026-06-04:创建
