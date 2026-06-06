---
title: "Git 提交 + 拉取 4 步最佳实践 (笔记本 Windows 11 + MSYS + GitHub 公仓, 2026-06-04 23:55 实战)"
created: 2026-06-04
updated: 2026-06-04
type: note
tags: [note, git, github, push, pull, commit, ssh, msyS, gh013, secret-scanning, 5-step-verification, hermes-3rd, playbook]
sources:
  - 23:30 第一次 push 真成功 (commit 42268e4, A1 Hindsight idle timeout)
  - 23:50 第二次 push 真成功 (commit 802afd9, A2 0.6.1 vs 0.7.2 跨机器)
  - 5 失败模式 (公网 Connection reset / GH013 / Authentication failed / non-fast-forward / rebase 冲突)
  - 4 周前 wiki § 4 git-collaboration-multi-agent (3 铁律)
  - 4 周前 wiki § 4.3 PAT 应急流程
confidence: high
source: git-3rd-notebook-2026-06
---

# Git 提交 + 拉取 4 步最佳实践 (笔记本 Windows 11 + MSYS + GitHub 公仓, 2026-06-04 23:55 实战)

> **核心目标**: 让 3rd 笔记本侧 commit + push 到 `github.com/AK47ZZQ/agent-wiki` (公开仓) **成功率 100%**, 避免 23:00-23:50 期间的 6 次失败 (公网/GH013/Authentication/冲突等).

> **B2 L2 永久方案** = 走 SSH (6-1 已配 id_ed25519 公钥) + Windows 原生 ssh.exe (绕 MSYS 截断) + remote URL 改 SSH 形式 + `Hermes <hermes@hermes.local>` author.

## 1. Step 0: 一次性配置 (笔记本 6-1 已配, 未来 0 改)

```bash
# 1. 配 SSH (绕 MSYS 截断 @, 必用 Windows 原生 ssh.exe)
git config --global core.sshCommand "C:/Windows/System32/OpenSSH/ssh.exe -o StrictHostKeyChecking=no"
# 2. 改 remote URL 走 SSH
git remote set-url origin "git@github.com:AK47ZZQ/agent-wiki.git"
# 3. 验证
git ls-remote origin
# → 应返 f3afbe93...  远端 HEAD
```

**为什么走 SSH 不走 HTTPS**:
- `git push` 走 HTTPS = 调 Windows credential manager 里的旧 PAT (4 周前撤销的 `9dfc` 截断版)
- 你 23:15 改的 token 权限 = fine-grained, 但 credential manager 缓存的是旧 token 凭据
- 走 SSH = 纯公钥鉴权, 0 token 风险, 永不失效 (除非你 6-1 公钥 GitHub 删)
- **MSYS 截断 @ 解决**: 用 `core.sshCommand` 让 git 走 Windows 原生 ssh.exe, 不经 MSYS bash

## 2. Step 1: 写 wiki 笔记 (本地, 0 依赖公网)

**MSYS 路径坑**:
- `write_file("/tmp/...")` 解释成 `C:\tmp\...` (OUTSIDE workspace)
- **修法**: 用 `cp "C:/tmp/..." /c/Users/ZZQ/AppData/Local/Temp/wiki-test/agent-wiki/...` 同步

**9 字段 frontmatter 必齐**:
```yaml
title: "..."
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: note | concept | method | comparison | entity
tags: [tag1, tag2, ...]
sources:
  - 来源 1
  - 来源 2 (≥ 2 跨节点/跨笔记)
confidence: high | medium | low
# 可选: contested / contradictions
```

**3 质量门**:
- ≥ 2 wikilink 出链 (避免孤岛)
- sources 列 ≥ 2 来源 (跨节点/跨笔记)
- 克制 2 件 (不超 4 件套, wiki-write-boundary § 3 反模式 B 警告)

## 3. Step 2: 4 件套同步 (本地)

- `index.md`: 加新条目 + 顶部状态计数 (如 100→102 .md) + 类目计数 (Concepts 17→18→19)
- `log.md` 顶部: 加 `## [YYYY-MM-DD HH:MM] 3rd: ...` 格式
- 旧页 bump: **不** (反模式 B)
- 主页 entities/hermes-3rd.md wikilink 后续 bump (本会话单独做)

## 4. Step 3: 5 步核验 push (走 SSH, 公网依赖)

```bash
# 1. git status
git status --short

# 2. git add 精确 4 文件 (不 -A, 避免 .canvas 污染)
git add <file1> <file2> <file3> <file4>

# 3. git commit
git commit -m "..."

# 4. 防假成功 #1: git cat-file -t HEAD
git cat-file -t HEAD  # 必返 "commit", 否则假成功

# 5. 防假成功 #2: pull rebase + push + rev-parse 对比
git fetch origin
git pull --rebase origin main  # 必先拉, 防 sibling 推
# 冲突解决: python 精确合并 (3 个 conflict 都保留, 用 HTML 注释包)
git push origin main
H_LOCAL=$(git rev-parse HEAD)
H_REMOTE=$(git rev-parse origin/main)
[ "$H_LOCAL" = "$H_REMOTE" ] && echo "✅ 真成功" || echo "❌ 假成功"
```

**author 必改** (4 周前 wiki § 4 用户硬偏好):
```bash
git config user.name "Hermes"
git config user.email "hermes@hermes.local"
```

## 5. Step 4: GH013 Secret Scanning 应急

- **触发条件**: log.md 含 `ghp_` 真 token 残留 (4 周前 main-claude 笔记就有)
- **不要 amend 改 log.md** (改 commit history, 5 步核验全失效)
- **真修法**: 浏览器点 GitHub 报的 unblock URL
  - URL 格式: `https://github.com/AK47ZZQ/agent-wiki/security/secret-scanning/unblock-secret/<id>`
- **或**: 浏览器手动修 log.md line 295+321 把 `ghp_...` 替换为 `<REDACTED-GH-PAT>`, commit, pull rebase

## 6. 5 类失败模式 + 真实根因 (23:00-23:50 全部遇到)

| 失败 | 根因 | 修法 |
|---|---|---|
| `Recv failure: Connection was reset` | 公网 github.com 断 (波动) | 等 + curl github.com |
| `GH013: Push cannot contain secrets` | log.md 老 ghp_ token | unblock URL 或脱敏 |
| `Authentication failed` | credential manager 缓存旧 PAT | 改走 SSH (Step 0) |
| `non-fast-forward` rejected | 远端 sibling 新 commit | pull --rebase + 解决冲突 |
| `Could not apply` + conflict | rebase 冲突 (main-claude 跟 3rd) | python 精确合并 + rebase --continue |

## 7. 3 类不擅自做的边界

| 边界 | 3rd 不做什么 |
|---|---|
| **不擅自 force** | 永不 `git push --force` / `--force-with-lease` (4 周前 wiki § 1.1 三铁律) |
| **不擅自接管凭据** | 不让用户在对话粘贴完整 PAT 明文, 不擅自清 Windows credential manager, 不擅自调 `git credential reject` |
| **不擅自 unblock** | GH013 unblock URL 永远让你点, 3rd 不点 |
| **不擅自动 commit history** | 改 8 commit author 这种事, 必先 ask, 不擅自 `git rebase -i` amend 老 commit |

## 8. Rebase 冲突解决 (跟 23:00 J3 / 23:50 A2 一样流程)

**5 步走 rebase**:
```bash
# 1. 拉新
git pull --rebase origin main  # 触发冲突
# 2. 看冲突文件
git diff --name-only --diff-filter=U
# 3. python 精确合并 (保留两版, HTML 注释包)
python << 'PYEOF'
import re
path = r'C:\Users\ZZQ\AppData\Local\Temp\wiki-test\agent-wiki\index.md'
with open(path, encoding='utf-8') as f: content = f.read()
pattern = re.compile(r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> \w+[^\n]*\n', re.DOTALL)
new = pattern.sub(lambda m: f'<!-- BEGIN merge (远端 + 3rd 都保留) -->\n{m.group(1)}{m.group(2)}<!-- END merge -->\n', content)
with open(path, 'w', encoding='utf-8') as f: f.write(new)
PYEOF
# 4. git add 冲突文件
git add <conflicted_file>
# 5. rebase --continue
GIT_EDITOR=true git rebase --continue
```

## 9. 1 个简化决策树 (下次操作时直接套)

```
要 commit + push wiki 笔记?
│
├─ 是 → 走 4 步流程 (Step 0 SSH + Step 1 笔记 + Step 2 4 件套 + Step 3 5 步核验)
│       ├─ commit 假成功? → git cat-file -t HEAD
│       ├─ push Authentication failed? → 检查 core.sshCommand + remote URL 走 SSH
│       ├─ push GH013? → 浏览器点 unblock URL
│       ├─ push 假成功? → git rev-parse origin/main 对比
│       └─ rebase 冲突? → python 精确合并保留两版
│
├─ 冲突 (强制 5 步核验) → 写 log.md + 通知用户, **不** force
│
└─ 远端有 sibling 新 commit? → git pull --rebase + 看 author 区分来源
```

## 10. 关键 SHA 时间线 (跨会话可查)

| 时间 | 事件 | commit |
|---|---|---|
| 6-4 19:50-19:53 | 3rd 5 commit 推 (author 错 `Hermes 3rd`) | 2cdf8cb, 0fcf066, 3a83b0c, 22b386e, 2a051b9, c7e4e3e, f5e124d, c030a77 |
| 6-4 22:00 | 改 public | n/a |
| 6-4 22:45 | fetch 5 commit (ai-harness-exploration 132K) | 34a843c..2143206 |
| 6-4 23:00 | GH013 阻 push (log.md 老 ghp_) | 94e3760 → 0be0dc7 |
| 6-4 23:30 | J3 + K1 unblock + push 真成功 (A1) | 42268e4 |
| 6-4 23:50 | A2 + B2 SSH 永久方案 + push 真成功 | 802afd9 |
| 6-4 23:55 | 本笔记沉淀 (本文件) | (待 push) |

## 11. 4 周前 wiki § 4 PAT 决策矩阵 → B2 L2 采纳

| 方案 | 优劣 | 当前状态 |
|---|---|---|
| A. 各自独立 PAT | 一边失效不影响另一边 | ❌ |
| **B. SSH key (per 机器)** | 永不失效 | ✅ **B2 L2 23:50 采纳** |
| C. GitHub Actions 自动 sync | 0 PAT 过期 | ❌ |
| D. 共享 PAT (现状) | 简单 | ❌ 当前不用 |

## 12. 关联文档

- [[protocols/git-collaboration-multi-agent]] — 4 周前 wiki 多 Agent git 协作协议 (3 铁律 + 3 冲突类型)
- [[methods/git-push-cheatsheet]] — 1 页速查 (5 步核验 + 假成功防御)
- [[methods/safe-commit-push-protocol]] — 5 步核验详细 (8.7K)
- [[methods/hindsight-idle-timeout-watchdog]] — 0.7.2 笔记本无 cron 守护法
- [[concepts/hindsight-0.7.2-idle-timeout-mechanism]] — 0.7.2 1800s SIGTERM 机制
- [[concepts/hindsight-0.6.1-vs-0.7.2-evolution]] — 0.6.1→0.7.2 实战差异
- [[comparisons/hindsight-0.6.1-vs-0.7.2-cross-machine-comparison]] — 跨机器对比
- [[notes/hindsight-deployment-and-monitoring-2026-06-04]] — main-claude 台式 0.6.1 + cron 守护
- [[notes/hindsight-0.7.2-bank-config-migration]] — 3rd 笔记本 0.7.2 迁移
- [[notes/hindsight-daemon-fix-2026-06-04]] — 3rd 14:25 base_url 修复

## 13. 9 字段 + wikilink + sources 自检

- 9 字段 ✅: title / created / updated / type / tags / sources / confidence + (前 5 个 wiki § 4 必填)
- wikilink ≥ 10 出链 (远超 ≥ 2 要求) ✅
- 5 sources 跨节点 + 跨失败模式 + 跨 commit SHA ✅
- confidence: high (跨 2 节点实战 2 次 push 成功) ✅
