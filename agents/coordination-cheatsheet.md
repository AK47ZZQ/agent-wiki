---
title: Agent Coordination Cheatsheet
created: 2026-06-04
updated: 2026-06-04
type: agents
tags: [wiki, multi-agent, coordination, cheatsheet]
sources: [protocols/multi-agent-detail, AGENTS]
---

# Agent 协调速查表

> 写给 Agent 看的 1 页速查 — 5 步协调 + 4 冲突解决 + 7 常用命令。

## TL;DR

- **3 必跑** = `git pull --rebase` / `bash safe-commit-push.sh` / `check-wiki-quality.py`
- **冲突解** = first-push + rebase
- **绝不** = `git push --force`

## 5 步协调流程

```bash
# 1. 拉最新
git fetch origin main
git pull --rebase

# 2. 改 wiki(走 § 4.0 申请)
# 写新内容前先看 ai-harness-exploration § 4.0

# 3. 自检
python scripts/check-wiki-quality.py

# 4. 5 步核验 commit + push
bash scripts/safe-commit-push.sh "msg"

# 5. log 追加
echo "## ..." >> indexes/log.md
```

## 4 冲突解决

1. **拉冲突** → `git pull --rebase` 会失败
2. **看冲突** → `git status` 列 conflict files
3. **手动解决** → 改 conflict marker → `git add -A`
4. **rebase continue** → `git rebase --continue` → 跑 step 4

## 7 常用命令

| 命令 | 用途 |
|---|---|
| `git fetch origin main` | 拉远端 ref |
| `git pull --rebase` | rebase 拉本地 |
| `git status --short` | 看未保存 |
| `git add -A` | 暂存所有 |
| `git commit -m "msg"` | 创建 commit |
| `git push origin main` | 推(走 5 步核验) |
| `python scripts/check-wiki-quality.py` | 自检 |

## 关联

- [[protocols/multi-agent-detail]]
- [[methods/safe-commit-push-protocol]]
- [[AGENTS]]
