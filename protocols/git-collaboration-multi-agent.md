---
title: Git Collaboration Protocol — 多 Agent 共享 Wiki 同步协议
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [protocol, git, multi-agent, sync, github, conflict-resolution, hermes-3rd]
sources:
  - 本会话(2026-06-04 用户明确)
  - local
confidence: high
source: git-3rd-notebook-2026-06
---

# Git Collaboration Protocol — 多 Agent 共享 Wiki 同步协议

> **适用场景**:本 Hermes(部署在台式服务器)与 **Hermes 3rd**(部署在笔记本)共同维护同一个 GitHub wiki 仓库。
> 仓库: `https://github.com/AK47ZZQ/agent-wiki`(branch: main)
> 写入 wiki 内容:仍走 [[CLAUDE#§ 4.0|ai-harness-exploration § 4.0 申请协议]]

## 1. 协议核心原则

### 1.1 三条铁律
1. **永不复位远端** — 禁止 `git push --force` / `--force-with-lease`(除非显式协调)
2. **推送前必先拉取** — `git pull --rebase` 后无冲突才能 push
3. **冲突由人类裁决** — 自动合并失败时,停下,写 log,等用户决定

### 1.2 节点身份
| 节点 | 平台 | 角色 | 写入方式 |
|---|---|---|---|
| **本机 Hermes**(主对话) | Windows 11 台式服务器 | 主 Agent,跟用户直接对话 | Direct commit + push |
| **Hermes 3rd** | 用户笔记本 | 协作者,可能后台运行 | Direct commit + push |
| **用户** | 协调两边 | 最终决策者 | 通过本机 Hermes 写入 |
| **云端** | https://github.com/AK47ZZQ/agent-wiki | 共享镜像 | main branch |

## 2. 标准同步流程(每个 commit 前必跑)

### 2.1 写入前
```bash
# 1. 拿远端最新
git fetch origin main

# 2. 看是否有冲突风险
git log --oneline origin/main ^main | head -5
# 如果有 1+ commit = 3rd 推了东西,可能冲突

# 3. 拉取并 rebase
git pull --rebase origin main
# 冲突时停下,见 § 3
```

### 2.2 写入中
```bash
# 1. 改动文件(根据 § 4.0 申请)
# 2. 跑 check 脚本
python scripts/check-wiki-quality.py --strict
# 3. 确认 PASS
```

### 2.3 写入后
```bash
# 1. 本地 commit(明确作者信息)
git add -A
git commit -m "<conventional commit message>

Co-authored-by: <3rd if known>
"

# 2. 再 fetch(确认期间没新变更)
git fetch origin main

# 3. 如果 origin/main 落后,先 pull --rebase
git pull --rebase origin main

# 4. 推送
git push origin main
# 401/403 = PAT 失效,见 § 4
```

## 3. 冲突处理(3 类)

### 3.1 无冲突(理想情况)
3rd 没改同一文件 → 自动 rebase 成功 → push 成功。

### 3.2 文本冲突(同文件不同段落)
```bash
git pull --rebase origin main
# CONFLICT (...)
# 1. 打开冲突文件
# 2. 看 <<<<<<< / ======= / >>>>>>> 标记
# 3. 决策:留 3rd 版 / 留本机版 / 合并两版
# 4. 标记为已解决
git add <file>
git rebase --continue
# 5. 跑 check 脚本
python scripts/check-wiki-quality.py
# 6. push
git push origin main
```

### 3.3 逻辑冲突(同文件同段落)
**禁止自动决策**。停下,写 log 标记:
```bash
# 写 wiki/log.md
## 2026-MM-DD HH:MM — 冲突: <filename>
**本机版本**: <内容>
**3rd 版本**: <内容>
**决策**: 等待用户
```
然后通过本对话告诉用户冲突,让用户决定。

## 4. PAT 与鉴权

### 4.1 共享 PAT 风险(已踩坑)
- **2026-06-04 14:46**:GitHub 撤销了旧的 PAT(`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`)
- 推测:用户给 3rd 用新 PAT 时,旧 PAT 失效

### 4.2 推荐方案
| 方案 | 优点 | 缺点 |
|---|---|---|
| **A. 各自独立 PAT** | 一边失效不影响另一边 | 两边各自管 |
| **B. SSH key(per 机器)** | 永不失效 | 需配 SSH key 一次 |
| **C. GitHub Actions 自动 sync** | 0 PAT 过期 | 需配 workflow |

**当前未决**:等用户决定方案。

### 4.3 PAT 失效应急
```bash
# 1. 报错
fatal: User canceled device code authentication
# 或
error: failed to push, ... 401

# 2. 停下 — 不要再试 push(浪费重试)
# 3. 本地 commit 是安全的(没丢)
# 4. 通知用户提供新 PAT
# 5. 写 _netrc / 配置新 PAT
# 6. 重试 push
```

## 5. 双方可观察的状态

### 5.1 通过 git log 看见 3rd 的活动
```bash
git log --all --oneline -20
# 看哪些 commit 是 3rd 推的
# 通过 commit message 里的 "Co-authored-by" 或作者邮箱识别
```

### 5.2 通过 wiki 内的 agent registry 看见 3rd
- `agents/` 目录应该包含 3rd 的实例档案
- `agents/hermes-3rd.md`(若 3rd 写)或 `agents/hermes-3rd-instance.md`
- 若 3rd 创建,本机应通过 `git pull` 拉到

### 5.3 共享 scratchpad 用法(可选)
- `scratchpad/shared/<date>-<topic>/` 双方都可写
- 通过 pull 看到对方的中介状态

## 6. 边界(明确禁止)

❌ **本机 + 3rd 不应同时编辑同一文件**(避免冲突)
❌ **禁止 force push**(会丢失 3rd 的 commit)
❌ **禁止重置远端 history**(`git push origin :main` 删除 branch)
❌ **跳过 check 脚本**推损坏 wiki

## 7. 当前未解决(等用户)

- [ ] PAT 方案:共享 / 各自 / SSH / Actions
- [ ] 3rd 的 git 用户名 / 邮箱(用于 Co-authored-by)
- [ ] 冲突解决的 SLA(谁多久内必须响应冲突?)
- [ ] cron 频率:本机每周自动 push?每天?

## 8. 检查清单(每次 commit 前)

- [ ] `git fetch origin main` 拿最新
- [ ] `git pull --rebase` 无冲突
- [ ] `python scripts/check-wiki-quality.py --strict` PASS
- [ ] commit message 含 改动摘要
- [ ] Co-authored-by 标 3rd(若 3rd 也贡献)
- [ ] push 后 `git log origin/main` 看到新 commit

## 关联文档

- [[CLAUDE]] — wiki schema 与写入协议(§ 4.0 申请)
- [[protocols/agent-coordination]] — 6 原语 + A2A 兼容
- [[protocols/goal-alignment]] — 主动告警机制
- [[protocols/multi-agent-detail]] — frontmatter 9 字段 schema
- [[tasks/git-collaboration-rollout]] — 协议上线任务(待建,本会话创建)
- [[agents/hermes-3rd]] — 3rd 实例档案(待 3rd 笔记本首次启动时创建)
- 笔记本 Hermes(3rd)将创建 `agents/hermes-3rd.md` 声明身份
