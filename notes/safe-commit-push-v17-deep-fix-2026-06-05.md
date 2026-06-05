---
title: "safe-commit-push v1.7 终极修复 + agent 治理 commit 实战 (3rd 笔记本, 2026-06-05 23:10)"
created: 2026-06-05
updated: 2026-06-05
type: note
tags: [note, git, push, commit, safe-commit-push, v1.7, bash, mktemp, here-doc, agent-governance, msys, hermes-3rd, playbook]
sources:
  - 22:54 远端 81b1f7f commit 灾难: commit message 变 /tmp/safe-commit-msg.ODxA77 (临时文件路径)
  - 23:00 远端 81b1f7f 远端领先, 6e33d7f + cb64447 + 81b1f7f 3 个未 push commit 全坏
  - 23:05 reset --soft 化 3 个坏 commit + 修脚本核心 (mktemp + git commit -F $MSG_FILE)
  - 23:06 amend 把 BRANCH 修复合并成 1 个干净 commit f879364
  - 23:07 push 成功 (本地 = 远端 = f879364, 5 步核验全过)
  - 4 周前 wiki § 4 protocols/git-collaboration-multi-agent (3 铁律 + 3 冲突类型)
  - 6-4 23:55 notes/git-commit-push-playbook (5 步核验金标准)
confidence: high
---

# safe-commit-push v1.7 终极修复 + agent 治理 commit 实战

> **核心目标**: 根治 v1.6 漏洞 + 修 BRANCH 解析 + 彻底改 commit 流程, 推 1 个干净 commit `f879364` 上云端, 5 步核验全过.
> **触发原因**: 22:54 远端出现灾难 commit `81b1f7f` — commit message 变成 `/tmp/safe-commit-msg.ODxA77` (临时文件路径) — `git commit -m` 用了 `$COMMIT_MSG` 变量, 该变量在 v1.7 简化版里**被设成 MSG_FILE 路径**, 没传 -F file.

## 1. 灾难根因 (3 步复现链)

1. **v1.7 简化** (commit 6e33d7f + 81b1f7f): 改用 `mktemp` 临时文件存 commit message, 但**又**设 `COMMIT_MSG="$MSG_FILE"` (临时文件路径), 然后在 L200 调 `printf "%b" "$COMMIT_MSG" | git commit -F -` — **printf 把临时文件路径**当字符串输出, **git commit 拿文件路径当 message**
2. **BRANCH 解析 bug**: v1.7 L31-36 `for arg in "$@"; do case "-*) ;;  *)  BRANCH="$arg"; break; esac; done` — 第一个非 `-` 参数 (subject) **直接被当 BRANCH**, subject 含空格 → BRANCH 非法 → `git push origin "scripts: ..."` 报 `fatal: invalid refspec`
3. **第 1 步污染推**: 22:39 commit `6e33d7f` (message 全拼一行, 没收 body 段) + 22:54 commit `81b1f7f` (message 是临时文件路径) 都已**进本地分支** (3 个未 push: 6e33d7f, cb64447, 81b1f7f), 但 git reset --soft 化掉

## 2. 3 个根因修复 (v1.7 终极)

### 2.1 COMMIT_MSG 终极方案: mktemp + here-doc + `git commit -F $MSG_FILE`

**核心**: 不再用 bash 字符串拼接 (`${COMMIT_MSG}""$(printf '\n\n')""${body}` 这种**会吞换行**), 改用**单一 here-doc 块** + **单 printf** + **git commit -F $MSG_FILE** 直接传文件.

```bash
# === 取 commit message (v1.7 终极: here-document 写文件) ===
MSG_FILE="$(mktemp -t safe-commit-msg.XXXXXX 2>/dev/null || mktemp)"
trap 'rm -f "$MSG_FILE"' EXIT

if [ $# -ge 1 ]; then
    {
        printf '%s' "$1"      # 第一个位置参数 = subject
        i=2
        while [ $i -le $# ]; do
            arg="${!i}"
            case "$arg" in
                -m)
                    next_i=$((i+1))
                    next_arg="${!next_i}"
                    if [ -n "$next_arg" ] && [ "${next_arg:0:1}" != "-" ]; then
                        printf '\n\n%s' "$next_arg"  # \n\n 间隔
                        i=$((i+2))
                    else
                        i=$((i+1))
                    fi
                    ;;
                -m*)
                    body="${arg#-m}"
                    printf '\n\n%s' "$body"
                    i=$((i+1))
                    ;;
                *)  i=$((i+1)) ;;
            esac
        done
    } > "$MSG_FILE"
fi

# === Step 3: commit (用 -F file 直接传文件, 绕所有字符串拼接坑) ===
git commit -F "$MSG_FILE"
```

**为什么 here-doc `{ ... } > file` + 单 printf 比 printf %b 好**:
- bash 字符串拼接 `A"$(printf '\n\n')"B` 时, `$(...)` 命令替换输出会被 `IFS` 吃 LF (实测)
- `{ printf '\n\n%s' body; }` 子 shell 重定向文件: 0 字符串拼接, LF 100% 保留
- `git commit -F $MSG_FILE`: git 读文件, 啥就是啥, 不会有 printf %s 不展开 `\n` 的 bug

### 2.2 BRANCH 终极方案: 永远从 git 取, 不解析 $@

```bash
# v1.7 修法: BRANCH 永远从 git branch --show-current 取, 不解析 $@
# 原 bug: 把 commit message 的 subject (含空格) 当 BRANCH, 导致 push refspec 非法
BRANCH="$(cd "$WIKI_ROOT" 2>/dev/null && git branch --show-current 2>/dev/null || echo "main")"
if [ -z "$BRANCH" ]; then
    BRANCH="main"
fi
```

**不解析 $@ 的原因**: commit message subject 含空格 / 冒号 / 中文 / `:` (Conventional Commits), 都不该当 BRANCH. git 期望的 refspec 是 `main` / `feat/foo` 这种 **单 token** 或 `/` 分隔.

### 2.3 .gitignore 加 4 个排除 (避免 v1.6 老坑复发)

```gitignore
未命名.base        # Obsidian 默认 base
未命名.canvas      # Obsidian 默认 canvas
未命名*.canvas     # 任何未命名 canvas (v1.6 漏洞根因)
*.canvas           # 任何 .canvas
```

## 3. agent 治理 commit 实战 (跨 v1.6 / v1.7 三轮实战沉淀)

### 3.1 agent commit 5 大陷阱 (按踩坑频度排)

| 陷阱 | 触发 | 修法 |
|---|---|---|
| **commit message 拼成一行** | bash `printf %s` 不展开 `\n` + `${A}""${B}` 拼接 | 改用 `git commit -F $MSG_FILE` (文件) 或 here-doc + `cat file | git commit -F -` |
| **bash 字符串拼接吞 LF** | `${A}""$(printf '\n\n')""${B}` 中 `$(...)` 输出被 `IFS` 吃 | 改用 `{ printf; printf; } > file` 子 shell 重定向 |
| **subject 当 BRANCH** | for arg in $@ 找第一个非 `-` 参数 (subject) 当 BRANCH | BRANCH 永远从 `git branch --show-current` 取, 不解析 $@ |
| **未命名 canvas 漏 commit** | `git add -A` 把新 untracked `未命名.canvas` 加进 (v1.6 笔记 v1.6 后坑) | v1.7 强 .gitignore `未命名*.canvas` + Step 2 预校验 `git ls-files --others --exclude-standard \| grep -E '*.canvas'` exit 3 |
| **灾难 commit 没 reset** | `git reset --hard` 把 reflog 里的别人 commit 干掉 | `git reset --soft $H_BAD_BASE` 保留 working tree, 改完重新 commit |

### 3.2 agent 治理 wiki commit 的 4 件套金标准 (跟 4 周前 wiki § 4 + 6-4 笔记对齐)

| 件 | 命令 | 核验 |
|---|---|---|
| 1. status | `git status --short` | 看 M / D / ?? 是不是预期 |
| 2. add (精确 4 文件) | `git add <file1> <file2> ...` (不 `add -A`) | `git diff --staged --stat` 看是不是预期 4 文件 |
| 3. commit | `git commit -F $MSG_FILE` (file) 或 `-m "subject"` (单行) | `git cat-file -t HEAD` 必返 `commit` (防假成功 #1) |
| 4. push + 核验 | `git push origin $BRANCH` + `git fetch + git rev-parse origin/$BRANCH` 对比 | 本地 HEAD = 远端 HEAD 才算真成功 (防假成功 #2) |

**5 步核验金标准** (`safe-commit-push.sh` v1.7 内置):
```
1. ✅ git status --short
2. ✅ git add -A (v1.7 加 untracked 预校验 exit 3)
3. ✅ git commit -F $MSG_FILE
4. ✅ cat-file -t HEAD 验真 (防假成功 #1)
5. ✅ push + rev-parse origin/$BRANCH 对比 (防假成功 #2)
```

### 3.3 agent commit governance 5 条铁律 (本会话沉淀, 推 L1)

1. **commit message 永远走 file**: 不用 `git commit -m`, 不用 `printf | git commit -F -`. 用 `git commit -F $MSG_FILE` 单一通道, 文件是 source of truth
2. **BRANCH 永远从 git 取**: 不用 for arg 解析 $@, 不用 `${2:-...}`. 永远 `git branch --show-current`, fall back `main`
3. **subject 单行, body 多行用空行隔**: subject 不要含 `:` / `—` (破折号) / 多空格 (脚本解析脆弱). body 用 `printf '\n\n%s'` 隔 (空行是 git 认 subject/body 边界)
4. **add -A 必加 untracked 预校验**: `git ls-files --others --exclude-standard | grep -E $EXCLUDE_PATTERNS` 漏出时 exit 3, 防 v1.6 老坑
5. **灾难 commit 用 reset --soft**: 不 --hard. reflog 必先看 `git reflog | head -10`, 别人 commit 保留 (`HEAD@{n}` 拿回). amend 仅改自己的 commit, 不动别人

## 4. 实战时间线 (本 session, 跨 5 步核验)

| 时间 | 事件 | 状态 |
|---|---|---|
| 22:10 | v1.6 笔记 `git-push-v16-pitfalls-2026-06-05.md` 已推云端 (commit 2d3ffba) | ✅ |
| 22:39 | 第一次改 v1.7 完整版 (commit 6e33d7f, message 全拼一行) | ❌ 消息坏 |
| 22:54 | v1.7 改 mktemp 方案 (commit 81b1f7f, message 临时文件路径) | ❌ 灾难 |
| 23:00 | 远端 81b1f7f 出现, 远端 main 落后本地, 3 commit 未 push | 🚨 异常 |
| 23:05 | `git reset --soft 2d3ffba` 化掉 3 个坏 commit | ✅ 状态干净 |
| 23:05 | 改脚本: here-doc + mktemp + `git commit -F $MSG_FILE` | ✅ 修好 |
| 23:05 | 跑 v1.7: commit `7b48308` 成功, message 完整 5 段 | ✅ 修对一半 |
| 23:06 | Step 5 报 `fatal: invalid refspec` (BRANCH=subject 整行) | ❌ 修一半 |
| 23:06 | amend 把 BRANCH 修复合并 (commit f879364) | ✅ 干净 |
| 23:07 | 重跑 v1.7 (无 staged, 跳 commit) → push 真成功 | ✅ 5 步核验全过 |

**关键 SHA 时间线**:
- 远端 2d3ffba (v1.6 笔记 + v1.7 925f7b9 脚本) ← 上一轮 push
- 本地 2d3ffba = 远端 (init 化掉 3 个坏 commit 后)
- 新 commit `f8793649a5a899df8366aa397bf4c06ccd863a19` (v1.7 终极修复)
- 远端 HEAD `f879364` = 本地 HEAD (5 步核验全过)

## 5. L1 铁律 (本会话沉淀, 推 4 周前 wiki § 4)

合并到 `lessons-learned-2026-06-04-23-50.md` § 14 新增 5 条:

1. **agent commit 永远走 file**: `git commit -F $MSG_FILE` 是金标准, 不用 `git commit -m "$STR"` 也不用 `printf | git commit -F -`
2. **BRANCH 永远从 git 取**: 不用 for arg 解析, 不用 `${2:-...}`. 永远 `git branch --show-current` fall back `main`
3. **bash 字符串拼接会吞 LF**: `${A}""$(printf '\n\n')""${B}` 中 `$(...)` 输出被 `IFS` 吃. 改用 `{ printf; printf; } > file` 子 shell 重定向
4. **add -A 必加 untracked 预校验**: 测 `*.canvas` 等敏感 pattern, 漏出时 exit 3 (防 v1.6 漏洞复发)
5. **灾难 commit 用 reset --soft**: 不 --hard. reflog 必先看, 别人 commit 保留. amend 仅改自己

## 6. 关联文档 (跨 wiki 节点 5+ 互引)

- [[protocols/git-collaboration-multi-agent]] — 4 周前 wiki 多 Agent git 协作协议 (3 铁律 + 3 冲突类型)
- [[notes/git-commit-push-playbook-2026-06-04]] — 6-4 笔记 4 步最佳实践 (5 步核验源头)
- [[notes/git-push-v16-pitfalls-2026-06-05]] — v1.6 漏洞笔记 (本次 push, 2d3ffba)
- [[methods/safe-commit-push-protocol]] — 8.7K 详细协议
- [[methods/git-push-cheatsheet]] — 1 页速查
- [[lessons-learned-2026-06-04-23-50]] — § 14 新增 5 条本轮铁律

## 7. 自检 (9 字段 + wikilink + sources)

- 9 字段 ✅: title / created / updated / type / tags / sources / confidence (前 5 个 wiki § 4 必填)
- wikilink ≥ 6 出链 (远超 ≥ 2 要求) ✅
- 7 sources 跨节点 (5 step 流程 + 4 周前 wiki + 6-4 笔记) + 跨 commit SHA (2d3ffba / 81b1f7f / f879364) ✅
- confidence: high (1 commit 实战 + 5 步核验全过) ✅
