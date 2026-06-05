---
title: Safe Commit-Push Protocol
created: 2026-06-04
updated: 2026-06-05
type: method
tags: [wiki, git, safety, verification, multi-agent, v1.6]
sources: [methods/git-tutorial, protocols/git-collaboration-multi-agent, methods/using-knowledge-base]
---

# Safe Commit-Push Protocol — 5 步核验(防假成功)

> 写给所有 git 协作 agent(主对话 / 3rd 笔记本 / 任何 commit + push 的智能体)。
> **必读**:本会话(2026-06-04)5-6 次 commit + push 报告"成功"但实际 git 没记录,内容从来没真推。本协议 = 防御。

## TL;DR

- **永远不**依赖 `git push` 输出"成功"
- **永远** 跑 5 步核验(`git status` → `add` → `commit` → `cat-file -t` → `push` + `rev-parse` 对比)
- **自动脚本**:`bash scripts/safe-commit-push.sh "msg"` 一步完成 + 5 步核验 + 失败自动回滚
- **wiki-keeper v1.5** 是 Hermes 内部 skill,本协议是它的对外版

## 1. 为什么需要(本会话的真实事件)

**2026-06-04 17:00** 我(主对话)在 commit `e59a9e3` 报告"成功" → 实际 git 没记录这个 commit(`git cat-file -t e59a9e3` 报 "Not a valid object name")。

**之前 5-6 次 commit + push 都类似**:输出"成功"看着像,**实际**:
- shell 输出截断 → 看不到错误信息
- `git commit` 失败但被静默忽略
- `git push` 报 "Everything up-to-date" 但实际没推
- 3rd 推了之后我 push 不上,我以为成功

**累积 5+ 次假成功 → 668 行内容从来没真推**。**直到 3rd 端 wiki-keeper 跑了 4 commit,迫使我 pull rebase,才发现本地和远端不一致**。

## 2. 5 步核验流程(硬协议)

```bash
# Step 1: 看本地变更
git status --short

# Step 2: add 所有
git add -A

# Step 3: commit
git commit -m "..."

# Step 4: 验证 commit 真存在(关键!防假成功 #1)
git log --oneline -1
# ↑ 看到 commit hash 出现 = commit 成功
# ↑ 没出现 = 假成功!重试或诊断

# 双重核验:用 cat-file 确认 commit 对象存在
git cat-file -t HEAD
# ↑ 输出 "commit" = 对象真存在
# ↑ 报错 = commit 从未创建

# Step 5: push + 核验远端 hash(关键!防假成功 #2)
git push origin $(git branch --show-current)
H_LOCAL=$(git rev-parse HEAD)
git fetch origin $(git branch --show-current)
H_REMOTE=$(git rev-parse origin/$(git branch --show-current))

if [ "$H_LOCAL" = "$H_REMOTE" ]; then
    echo "✅ 推送成功(本地 = 远端 = $H_LOCAL)"
else
    echo "❌ 假成功!本地 = $H_LOCAL,远端 = $H_REMOTE"
    echo "诊断:可能是 sibling 推了 / 网络断 / hook 拒绝"
    exit 1
fi
```

**5 步核验的核心**:**不依赖任何单一信号**。`git commit` 输出"成功" + `git push` 输出"成功" **不**等于真成功。**必须** commit 对象存在 + 远端 hash 一致。

## 3. 自动化脚本 — v1.6

`scripts/safe-commit-push.sh` 封装 5 步核验 + 1.5 步排除为 1 个命令:

```bash
bash scripts/safe-commit-push.sh "commit message"
```

### 3.1 v1.6 升级(2026-06-04 18:58,3rd 反馈驱动)

| 升级点 | v1.5 | v1.6 |
|---|---|---|
| 排除 `.canvas` / `.base` / `.bak` / `.tmp` / `.swp` / `.swo` / `.obsidian/*` / `.trash/*` | ❌ | ✅ |
| 自动写 `.gitignore`(防御性) | ❌ | ✅ |
| Step 1.5: 排除 Obsidian 本地文件 | ❌ | ✅ |
| 6 步核验(原 5 步 + Step 1.5) | 5 步 | 6 步 |

### 3.2 v1.6 解决的具体问题

3rd 笔记本报 `c030a77` commit 反馈:`safe-commit-push.sh v1.5` 的 `git add -A` 把 `未命名.canvas`(Obsidian 白板)意外 add — 污染 wiki 仓库。**v1.6 修法**:Step 1.5 排除 10 个 EXCLUDE_PATTERNS + 自动写 `.gitignore`。

### 3.3 脚本特性
- 5 步顺序跑,任一步失败立即 `exit 1`
- 输出彩色日志(绿/黄/红)
- 自动诊断假成功根因(commit 失败 / push 失败 / hash 不一致)
- **不**自动 force-push(危险)

**使用场景**:
- 平时 commit + push → `bash scripts/safe-commit-push.sh "msg"`
- 调试 commit 失败 → 跑脚本看 Step 4 输出
- 调试 push 失败 → 跑脚本看 Step 5 远端 hash 对比

## 4. 11 速查(陷阱信号 → 正确动作)

| 陷阱 | 信号 | 正确动作 |
|---|---|---|
| `origin/HEAD → main` ≠ main 有内容 | `git log origin/main` 是空 | `git ls-remote` 核 hash |
| `curl 401` | API 鉴权失败 | `git ls-remote` 核 hash(API 401 ≠ push 失败) |
| `error: src refspec main does not match any` | 本地没 main 分支 | `git branch --show-current` |
| `non-fast-forward` rejected | 远程有新 commit | `fetch` + 看差异,问用户 force |
| push 看起来 hang | 12K+ insertions 慢 | background + `ls-remote` 核 |
| CWD 是错的 | `pwd` 不在 wiki | `find` 找真 wiki,绝对路径 |
| **`commit 假成功`**(本协议重点) | `git log -1` 报 "Not a valid object name" | `git cat-file -t <hash>` 核对象存在 |
| **`push 假成功`**(本协议重点) | `git push` 报 "Everything up-to-date" 但实际没推 | `git rev-parse origin/main` ≠ `git rev-parse HEAD` |
| **`push 静默非快进`** | `git push` 输出空,但本地 ≠ 远端 | 必看 5 步核验 step 5 |
| **403 Write access not granted** | PAT 没 write 权限 | 改 fine-grained token 权限为 `Contents: Read and write` |
| **5 步核验后假成功诊断** | local = 远端 = 不同 hash | 跑 `safe-commit-push.sh` 自动诊断回滚 |
| **脚本不可用 + 手动 5 步** | `bash scripts/safe-commit-push.sh` exit 1 无诊断 | 手动执行: `commit` → `cat-file -t HEAD` → `stash` → `pull --rebase` → `push` → `ls-remote == rev-parse` (见 git-push-cheatsheet § 2.0) |
| **commit 被 rebase 吞掉** | `pull --rebase` 后 `git log` 看不见自己 commit | `git reflog -5` 找回 hash → `git reset --hard <hash>` (reflog 保留 90 天不丢数据) |

## 5. 多 Agent 协作场景(3rd + 主对话)

**两台机器的 wiki-keeper 默认都装本协议**(v1.5+),但**两台机器的 cron / 手动 push 可能撞车**(同时改同文件)。

**3 步必走**(协议 v1.1 § 2):

```
[1] git fetch origin main           (拉远端最新)
[2] git log --oneline origin/main ^main   (看远端领先我的)
    git log --oneline main ^origin/main   (看我领先远端的)
[3] git pull --rebase origin main   (拉到本地,有冲突停下)
[4] 5 步核验 + push
```

**冲突时**(git pull rebase 报 CONFLICT):
- **不**自动 `--theirs` / `--ours`
- **不**自动 force push
- 写 log 标记 + 通知用户决定
- 参考 [[protocols/git-collaboration-multi-agent]] v1.1

## 6. 实测案例(本会话 2026-06-04 17:00)

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

**修法**:5 步核验 + 自动化脚本(本协议 § 2 + § 3)。

## 7. wiki-keeper skill 关联

**Hermes 内部**:`hermes/skills/autonomous-ai-agents/wiki-keeper/`(v1.5)有完整 SKILL.md + 4 references + 2 scripts。

**本协议 vs wiki-keeper**:
- **本协议**(wiki/methods/safe-commit-push-protocol.md) = **对外版**,任何 agent 看 wiki 都能理解
- **wiki-keeper skill** = **对内版**,Hermes 框架使用,触发词 + 维护模式 + 写入协议

**3rd 端升级路径**:
- 跑 `init-3rd.sh` 首次配置 → 自动拉 wiki + 装 wiki-keeper
- 装 v1.5 = 装 safe-commit-push.sh + 5 步核验
- 之后每次 commit 用 `bash scripts/safe-commit-push.sh "msg"`

## 8. 何时用 5 步核验

**永远用**。`git commit` + `git push` 是高风险操作(可能丢工作、丢协作、假成功),**不**值得省 5 秒。

**反例**(本会话 5 次假成功根因):
- ❌ 觉得"commit 信息简单,不用核"
- ❌ 觉得"push 输出 up-to-date = 成功"
- ❌ 觉得"wiki-keeper 跑了就 OK,不用我自己核"

**正确做法**:
- ✅ 5 步核验是默认
- ✅ 自动化脚本是工具
- ✅ 核验失败 = 立即诊断,不重试到成功(可能掩盖真问题)

## 9. 推荐资源

- [[protocols/git-collaboration-multi-agent]] v1.1 — 多人 push 协议
- [[methods/git-tutorial]] — git 协作教程
- [[agents/coordination-cheatsheet]] — main-claude ↔ hermes-3rd cheat sheet
- [[indexes/knowledge-map]] — wiki 总览
- **GitHub Pro Git** ch 1-3:https://git-scm.com/book/en/v2

## 10. 相关页面

- [[protocols/git-collaboration-multi-agent]] — v1.1 协作协议
- [[methods/git-tutorial]] — git 教程
- `scripts/safe-commit-push.sh` (本地) — 自动化脚本
- [[agents/main-claude]] — 主对话身份
- [[agents/hermes-3rd]] — 笔记本身份
