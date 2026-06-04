---
title: Git Collaboration Rollout — 协议上线任务
created: 2026-06-04
updated: 2026-06-04
type: task
status: pending
owner: main-claude + hermes-3rd
tags: [task, git, multi-agent, rollout, coordination]
source: protocols/git-collaboration-multi-agent.md(2026-06-04 创建)
---

# Git Collaboration Rollout — 协议上线任务

> **任务**:将 [[protocols/git-collaboration-multi-agent|多 Agent Git 协作协议]] 上线,让本机 Hermes(主对话)与 Hermes 3rd(笔记本)能顺利同步云端 wiki。

## 阶段 1 — 本机(本会话)

- [x] 写 `protocols/git-collaboration-multi-agent.md`(2026-06-04)
- [x] 写 `tasks/git-collaboration-rollout.md`(本任务页,2026-06-04)
- [ ] 修 wiki 质量(0 死链 / 0 索引缺 / frontmatter PASS)— **进行中**
- [ ] 第一次 push(用户已给新 PAT)
- [ ] 创建本任务的 initial commit

## 阶段 2 — 笔记本 3rd(等 3rd 启动后)

- [x] 3rd 创建 `agents/hermes-3rd.md`(声明身份) — **2026-06-04 15:36 done, 5.4K, status: active**
- [x] 3rd clone 云端 wiki 到本地 — **done (tmp clone 验证)**
- [ ] 3rd 写第一份 scratchpad 同步测试 — **pending**
- [x] 3rd push,本机 pull 看到 — **2026-06-04 15:36 done, commit 22b386e**

## 阶段 3 — 联调

- [ ] 双方都 fetch + pull 看到对方 commit
- [ ] 跑一次冲突演练(模拟双方改同文件)
- [ ] check 脚本在两边都跑 PASS
- [ ] 确认 A2A 兼容映射有效

## 阶段 4 — 自动化(可选)

- [ ] 本机 cron 每周自动 `wiki-keeper` 同步
- [ ] 3rd cron 每天自动 sync
- [ ] GitHub Actions 自动校验

## 状态

- **本机**: 进行中(check 脚本还在调)
- **3rd**: 未启动
- **协作方式**: 手动协调(等 Phase 4 自动化)

## 关联

- [[protocols/git-collaboration-multi-agent]] — 协议本身
- [[CLAUDE]] — 写入协议
- [[agents/main-claude]] — 本机 orchestrator
- [[agents/hermes-3rd]] — 笔记本协作 Agent(待 3rd 创建)
