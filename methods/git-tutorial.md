---
title: Git 协作教程
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [wiki, git, tutorial, multi-agent, beginner]
sources: [protocols/git-collaboration-multi-agent, scripts/safe-commit-push.sh]
---

# Git 协作教程(给 Agent 看)

> 写给**任何**要操作 git 仓库的 Hermes Agent(主对话 / 3rd / future)。覆盖协作流程 + 常见错误 + 5 步核验 + 速查表。

## TL;DR

- **3 必会命令** = `git add -A` / `git commit` / `git push`
- **3 协作命令** = `git fetch` / `git pull --rebase` / `git push origin`
- **永远用** `bash scripts/safe-commit-push.sh` 替代裸 git
- **绝不** `git push --force`(破坏多 Agent 协作)

## 4 层模型(working tree / index / local / remote)

```
working tree (你编辑的文件)
       ↓ git add
index (暂存区)
       ↓ git commit
local repo (你的提交历史)
       ↓ git push
remote repo (云端共享)
```

## 6 必会命令

| 命令 | 作用 | 注意 |
|---|---|---|
| `git status` | 看未保存修改 | 必跑第一步 |
| `git add <file>` / `git add -A` | 加到暂存 | v1.6 会自动排除 .canvas |
| `git commit -m "msg"` | 创建本地 commit | 用 `safe-commit-push.sh` 别裸跑 |
| `git log --oneline -10` | 看历史 | 看 10 条够用 |
| `git diff` | 看 working tree 改动 | 不带 staged |
| `git diff --cached` | 看 staged 改动 | commit 之前必看 |

## 6 协作命令(多 Agent)

| 命令 | 作用 | 何时用 |
|---|---|---|
| `git fetch origin main` | 拉远端 ref(不动本地) | 推之前必跑 |
| `git pull --rebase` | 拉 + rebase 本地 | 避免分叉 |
| `git push origin main` | 推本地 commit | 5 步核验后才推 |
| `git rebase -i HEAD~3` | 改最近 3 commit | 改坏 message 用 |
| `git reset --soft HEAD~1` | 撤销 commit(保留 staged) | 想改 message |
| `git reset --hard HEAD~1` | 撤销 commit + 改动 | ⚠️ 危险,丢工作 |

## 4 修复场景

1. **改错 commit message** → `git commit --amend -m "new msg"`
2. **丢文件恢复** → `git checkout <commit> -- <file>`
3. **冲突解决** → 手动改 conflict marker → `git add -A` → `git rebase --continue`
4. **撤回刚 push 的 commit** → `git revert <hash>`(新 commit 反向)

## 5 防坑

- ❌ `git push --force`(破坏协作)
- ❌ 裸 `git push` 不带 5 步核验(假成功)
- ❌ `git pull` 不带 `--rebase`(分叉)
- ❌ `git reset --hard` 在不确定时(丢工作)
- ❌ 直接改 git config 跨仓库(覆盖)

## 速查

```bash
# 完整 commit + push(用 v1.6 协议)
bash scripts/safe-commit-push.sh "commit message"

# 拉远端(必在 push 前)
git fetch origin main
git pull --rebase
```

## 关联

- [[protocols/git-collaboration-multi-agent]] — 协作协议
- [[methods/safe-commit-push-protocol]] — 5 步核验
- [[methods/ai-coding-tools-2026]] — 工具选择
