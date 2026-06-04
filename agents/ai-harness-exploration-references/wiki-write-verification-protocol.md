---
title: Wiki Write Verification Protocol — 5-step + 11 速查陷阱
created: 2026-06-04
updated: 2026-06-04
type: reference
tags: [wiki, git, verification, 5-step, multi-agent, protocol, fake-success]
source: 2026-06-04 ai-harness-exploration v6.17.0 § 4.0.9 + § 9.1.5
related_to: hermes-all/wiki-keeper skill v1.5, wiki/methods/safe-commit-push-protocol
---

# Wiki Write Verification Protocol — 5-step + 11 速查陷阱

> 写给所有 git 协作 agent(主对话 / 3rd 笔记本 / 任何 commit + push 的智能体)。
> **必读**:本会话(2026-06-04)5-6 次 commit + push 报告"成功"但实际 git 没记录,668 行内容从来没真推。本协议 = 防御。

## TL;DR

- **永远不**依赖 `git push` 输出"成功"
- **永远** 跑 5 步核验(`git status` → `add` → `commit` → `cat-file -t` → `push` + `rev-parse` 对比)
- **自动脚本**:`bash scripts/safe-commit-push.sh "msg"` 一步完成 + 5 步核验 + 失败自动回滚
- **用户硬偏好**: author = `Hermes <hermes@hermes.local>`, 唯一远端 = `AK47ZZQ/agent-wiki`
- **hermes-all 远端已被用户彻底删除** — 不再使用

## 1. 5 步核验流程(任何 wiki 写入必走)

```bash
# Step 1: 看本地变更
git status --short

# Step 2: add 所有
git add -A

# Step 3: commit
git commit -m "..."

# Step 4: 验证 commit 真存在(关键!防假成功 #1)
git log --oneline -1
git cat-file -t HEAD
# ↑ 输出 "commit" = 对象真存在
# ↑ 报错 = commit 从未创建, 假成功!

# Step 5: push + 核验远端 hash(关键!防假成功 #2)
git pull --rebase origin main  # 必先拉, 3rd 可能已推
git push origin main
H_LOCAL=$(git rev-parse HEAD)
git fetch origin main
H_REMOTE=$(git rev-parse origin/main)
[ "$H_LOCAL" = "$H_REMOTE" ] && echo "✅ 推送成功" || (echo "❌ 假成功! 本地=$H_LOCAL 远端=$H_REMOTE"; exit 1)
```

## 2. 11 速查陷阱表

| # | 陷阱 | 信号 | 正确动作 |
|---|---|---|---|
| 1 | `origin/HEAD → main` ≠ main 有内容 | `git log origin/main` 是空 | `git ls-remote --heads origin` 核 hash |
| 2 | `curl 401` | API 鉴权失败 | `git ls-remote` 核 hash (API 401 ≠ push 失败) |
| 3 | `error: src refspec main does not match any` | 本地没 main 分支 | `git branch --show-current` |
| 4 | `non-fast-forward` rejected | 远程有新 commit (3rd 推了) | `git pull --rebase origin main` + 看差异 |
| 5 | push 看起来 hang | 12K+ insertions 慢 | background + `ls-remote` 核 |
| 6 | CWD 是错的 | `pwd` 不在 wiki | `find` 找真 wiki,绝对路径 |
| 7 | **`commit 假成功`**(本会话 e59a9e3) | `git log -1` 报 "Not a valid object name" | `git cat-file -t <hash>` 核对象存在 |
| 8 | **`push 假成功`** | `git push` 报 "Everything up-to-date" 但实际没推 | `git rev-parse origin/main` ≠ `git rev-parse HEAD` |
| 9 | **`push 静默非快进`** | `git push` 输出空, 但本地 ≠ 远端 | 必看 5 步核验 step 5 |
| 10 | **403 Write access not granted** | PAT 没 write 权限 | 改 fine-grained token 权限为 `Contents: Read and write` |
| 11 | **5 步核验后假成功诊断** | local = 远端 = 不同 hash | 跑 `safe-commit-push.sh` 自动诊断回滚 |

## 3. 多 Agent 协作场景(3rd + 主对话)

**3 步必走**(协议 v1.1 § 2):
```
[1] git fetch origin main
[2] git log --oneline origin/main ^main   (看远端领先)
    git log --oneline main ^origin/main   (看本地领先)
[3] git pull --rebase origin main
[4] 5 步核验 + push
```

**冲突时**: 不自动 `--theirs` / `--ours` / `--force` / `--force-with-lease`。写 log 标记 + 通知用户决定。

## 4. 用户硬偏好(2026-06-04 配置)

```bash
# 任意仓库 .git/config:
[user]
    name = Hermes
    email = hermes@hermes.local
[remote "origin"]
    url = https://github.com/AK47ZZQ/agent-wiki.git
```

- **唯一远端**: `https://github.com/AK47ZZQ/agent-wiki` (用户明确说"我的仓库是 agent-wiki")
- **author**: `Hermes <hermes@hermes.local>` (用户明确说"上传称名称改为 Hermes")
- **hermes-all 远端已被用户彻底删除** — 不再使用,所有内容走 agent-wiki

**3 步配置**(任何新机器 / 新仓库):
```bash
git config user.name "Hermes"
git config user.email "hermes@hermes.local"
git remote set-url origin https://github.com/AK47ZZQ/agent-wiki.git
```

## 5. 实测案例(本会话 2026-06-04 17:00)

**场景**:commit `e59a9e3` 假成功

```bash
# 我跑
git add -A
git commit -m "feat: x"     # 输出 "[main e59a9e3] feat: x"
git push                     # 输出 "Everything up-to-date"

# 我以为成功,实际:
git cat-file -t e59a9e3
# fatal: Not a valid object name e59a9e3
# ↑ commit 从未存在!

git rev-parse origin/main
# c7e4e3e  ← 远端是 3rd 推的,不是我的
```

**根因**:
1. `branch.main.merge = refs/heads/master` 残留 bug → `git pull --rebase` 失败
2. 失败被静默忽略 → 后续 commit 实际没真创建
3. shell 输出截断 → 我看不到 commit 错误信息
4. `git push` 报 "Everything up-to-date" → 我以为成功

**修法**:5 步核验(本协议 § 1)。

## 6. safe-commit-push.sh 位置

- **在 agent-wiki 仓库**: `wiki/scripts/safe-commit-push.sh` (v1.5, 4403B, 5 步核验自动化)
- **在 hermes-all 仓库**: `hermes/skills/autonomous-ai-agents/wiki-keeper/scripts/safe-commit-push.sh` (同源, v1.5 同步)

**注意**: hermes-all 远端已被用户删除, **wiki/scripts/safe-commit-push.sh 才是有效副本**。

## 7. 何时必须跑 5 步核验

**永远**。**反例**(本会话 5 次假成功根因):
- ❌ 觉得"commit 信息简单, 不用核"
- ❌ 觉得"push 输出 up-to-date = 成功"
- ❌ 觉得"wiki-keeper 跑了就 OK, 不用我自己核"

**正确做法**:
- ✅ 5 步核验是默认
- ✅ 自动化脚本是工具
- ✅ 核验失败 = 立即诊断,不重试到成功(可能掩盖真问题)

## 8. 相关页面

- **ai-harness-exploration § 4.0.9** — 5 步核验硬协议(本 skill 内的完整定义)
- **ai-harness-exploration § 9.1.5** — 本会话用户纠正 #5 案例
- **wiki/methods/safe-commit-push-protocol** — agent-facing 协议(给所有 agent 看)
- **hermes-all/hermes/skills/autonomous-ai-agents/wiki-keeper** v1.5 — 内部 skill(本协议在 hermes 框架的对应实现)
- **protocols/git-collaboration-multi-agent** v1.1 — 多 agent 协作协议
- **wiki/methods/git-tutorial** — git 基础教程
