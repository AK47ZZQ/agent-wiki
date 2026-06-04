---
title: Git Push Cheatsheet — 5 步核验 + 假成功防御
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [git, cheatsheet, verification, safety, multi-agent, push]
sources: [wiki-keeper-v1.8, safe-commit-push-protocol, AGENTS-v2, using-knowledge-base]
confidence: high
---

# Git Push Cheatsheet — 5 步核验 + 假成功防御

> **写给**:任何要往 GitHub 推 commit 的 Hermes Agent(本机 / 3rd / 未来 agent)。
> **TL;DR**:`git commit` 报 "success" 不等于真成功,`git push` 报 "Everything up-to-date" 也不等于真推。**永远走 5 步核验**。

## 1. 3 个用户硬偏好(必走)

| 偏好 | 配置 | 为什么 |
|---|---|---|
| **author** | `user.name = "Hermes"` + `user.email = "hermes@hermes.local"` | 用户 2026-06-04 17:00 硬要求,不是默认值 |
| **远端** | `origin = https://github.com/AK47ZZQ/agent-wiki.git` | 用户 2026-06-04 18:00 删了 `AK47ZZQ/hermes` 仓库,所有 wiki 写入走 agent-wiki |
| **5 步核验** | 永远走,不裸 `git commit` + `git push` | 5+ 次假成功教训(668 行内容从来没真推过) |

## 2. 5 步核验(必走)

```bash
# Step 1: 看本地变更
git status --short

# Step 2: add 所有
git add -A

# Step 3: commit
git commit -m "msg"
# ⚠️ 不要看 "create mode" 输出就信 — 看下一行

# Step 4: 验证 commit 真存在(关键!防假成功 #1)
git log --oneline -1
# 看到 commit hash = 真成功
# 没看到 = 假成功,重试或诊断

# Step 5: push + 核验(关键!防假成功 #2)
git push origin $(git branch --show-current)
git fetch origin $(git branch --show-current)
H_LOCAL=$(git rev-parse HEAD)
H_REMOTE=$(git rev-parse origin/$(git branch --show-current))
if [ "$H_LOCAL" = "$H_REMOTE" ]; then
    echo "✅ 真成功 (本地 = 远端 = $H_LOCAL)"
else
    echo "❌ 假成功!local=$H_LOCAL remote=$H_REMOTE"
    exit 1
fi
```

**Python 替代**(Windows MSYS bash 安全):
```python
import subprocess
subprocess.run(['git','add','-A'], check=True)
subprocess.run(['git','commit','-m', msg], check=True)
h_local = subprocess.run(['git','rev-parse','HEAD'], capture_output=True, text=True).stdout.strip()
subprocess.run(['git','cat-file','-t', h_local], check=True)  # 双保险
subprocess.run(['git','push','origin','main'], check=True)
subprocess.run(['git','fetch','origin','main'], check=True)
h_remote = subprocess.run(['git','rev-parse','origin/main'], capture_output=True, text=True).stdout.strip()
assert h_local == h_remote, f"假成功!local={h_local} remote={h_remote}"
```

## 3. 4 类假成功陷阱(踩过)

### 假成功 #1: commit 没真创建
- **症状**:`git commit` 输出"成功" → `git log -1` 没新 commit
- **根因**:`branch.main.merge = refs/heads/master` 残留,rebase 失败时后续 commit 被 reset
- **核验**:`git cat-file -t <hash>` 报 "Not a valid object name" = 假成功

### 假成功 #2: push 没真推
- **症状**:`git push` 报 "Everything up-to-date" → 远端 hash 没变
- **核验**:必走 `git rev-parse origin/main` 对比

### 假成功 #3: 401 vs 403 含义不同
- **401 Unauthorized** = PAT 失效/撤销 → **换 PAT**
- **403 Write access not granted** = PAT 有效但**没写权限** → **改 token 权限**(fine-grained `Contents: Read and write`),**不是**换新 PAT
- 错误信息关键短语:`Bad credentials`(401) / `Write access to repository not granted`(403)

### 假成功 #4: .canvas / .obsidian 污染
- **症状**:`git add -A` 把 Obsidian 工作区文件(`.canvas` / `.base` / `.obsidian/*` / `.trash/*`)一起 add
- **修法**:`safe-commit-push.sh` v1.6 Step 1.5 自动排除 + 写 `.gitignore`

## 4. 多 Agent 协作(本机 + 3rd)

### 4.1 三条铁律
1. **永不复位远端** — 禁止 `git push --force` / `--force-with-lease`(除非显式协调)
2. **推送前必先拉取** — `git pull --rebase` 后无冲突才能 push
3. **冲突由人类裁决** — 自动合并失败时停下,写 log,等用户决定

### 4.2 Push 前必走 3 件套
```bash
git fetch origin main
git log --oneline origin/main ^main   # 远端领先本地的 commit
git log --oneline main ^origin/main   # 本地领先远端的 commit
# 有差异 → pull --rebase + 修冲突
# 无差异 + 自检 PASS → push(走 5 步核验)
```

### 4.3 3rd 端"假提交"诊断
**症状**:用户报告"3rd 提交了",但 `fetch` 后 `origin/main` 没变。
**5 个常见根因**:
1. 3rd 没走 `init-3rd.sh`,直接 `git push` 弹 username/password,3rd 不知道输 PAT
2. 3rd 配 SSH key 但 repo 用 HTTPS → `Permission denied (publickey)`
3. 3rd 推到错误分支(默认是 `master` 不是 `main`)
4. 3rd 推到自己的 fork 不是 origin
5. 3rd commit 了本地但没 push

**核验命令**:
```bash
git fetch origin main
git log --oneline origin/main ^main   # 0 行 = 远端没新东西 = 3rd 没真推
git log --oneline main ^origin/main   # N 行 = 本地有未推
```

## 5. 5 个必走配置(第一次)

```bash
# 1. author
git config user.name "Hermes"
git config user.email "hermes@hermes.local"

# 2. 远端 URL
git remote set-url origin https://github.com/AK47ZZQ/agent-wiki.git

# 3. 上游分支(避免 "Everything up-to-date" 假成功)
git branch --set-upstream-to=origin/main main

# 4. .netrc 鉴权(避免 PAT 泄露到 .git/config)
# Windows: C:\Users\Administrator\_netrc
# macOS/Linux: ~/.netrc
# 内容:
#   machine github.com login <PAT> password x-oauth-basic
# chmod 600 ~/.netrc  (Linux/macOS)

# 5. .gitignore 防御 Obsidian 污染(safe-commit-push.sh v1.6 自动写)
# 见 scripts/safe-commit-push.sh EXCLUDE_PATTERNS
```

## 6. 速查决策树

```
要 commit + push?
  │
  ├─ 是 → 走 5 步核验(§ 2)
  │       │
  │       ├─ commit 假成功? → git cat-file -t <hash> 核对象
  │       ├─ push 401?    → 换 PAT
  │       ├─ push 403?    → 改 token 权限(Contents:write)
  │       └─ push 假成功? → git rev-parse origin/main 对比
  │
  ├─ 冲突? → 写 log.md + 通知用户,**不** force
  │
  └─ 远端有 sibling 新 commit?
      → git pull --rebase + 看 author 区分来源
```

## 7. 完整协议(详细)

不在 cheatsheet,见:
- [[methods/safe-commit-push-protocol]] — 5 步核验详细(8.7K)
- `wiki-keeper` skill (26 个 pitfall, v1.8) — 完整故障排查
- `AGENTS.md` v2 § 3 — 协议命令
- `scripts/safe-commit-push.sh` v1.6 — 自动化实现

## 8. 实战真成功证据(2026-06-04)

| commit | 内容 | 验证 |
|---|---|---|
| `aa0bcb0` | 24 changes, 1148 lines | 5 步核验过,本地=远端 |
| `6ab1161` | 5 files, 1.0 MB | 5 步核验过 |
| `49adbe6` | 3rd: Hindsight PATCH bank | sibling 协作 |
| `05fee7a` | Hindsight cron validation | 5 步核验过 |

**假成功事件**:
- `e59a9e3` — 输出"成功",`git cat-file -t` 报 "Not a valid object name" → **commit 从未存在**
- 668 行内容因假成功从来没真推,5+ 次累积

## 9. 一句话总结

> **永远 5 步核验,永远不裸 push,永远先看 `git rev-parse origin/main` 对比。**
