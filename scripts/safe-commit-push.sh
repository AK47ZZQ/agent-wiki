#!/usr/bin/env bash
# safe-commit-push.sh — 5 步核验 commit + push(防假成功)
# Created: 2026-06-04 (wiki-keeper v1.5)
# Updated: 2026-06-04 (v1.6 — 排除 .canvas / .bak / .obsidian 等)
# Updated: 2026-06-05 (v1.7 — 新 untracked canvas 漏出 v1.6 漏洞根治)
# 用途: 替代裸 `git add -A && git commit && git push`,加 5 步核验
#
# 用法:
#   bash safe-commit-push.sh "commit message" [branch]
#   bash safe-commit-push.sh                # 交互式输入 commit msg
#
# 退出码:
#   0 = 全成功(commit 存在 + push 到远端 + hash 一致)
#   1 = 假成功诊断(commit 失败 / push 失败 / hash 不一致)
#   2 = 冲突未解决
#   3 = Step 2.5 检测到应排除的 untracked 文件没被 .gitignore 盖住(致命 v1.6 漏洞)

set -euo pipefail

# === 颜色输出(便于人眼读) ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

WIKI_ROOT="${WIKI_ROOT:-/c/Users/Administrator/hermes-all/wiki}"
# v1.7 修法: BRANCH 永远从 git branch --show-current 取, 不解析 $@ (subject 也可能在第 1 位置)
# 原 bug: 把 commit message 的 subject (含空格) 当 BRANCH, 导致 push refspec 非法
BRANCH="$(cd "$WIKI_ROOT" 2>/dev/null && git branch --show-current 2>/dev/null || echo "main")"
if [ -z "$BRANCH" ]; then
    BRANCH="main"
fi

# === 进入 wiki 目录 ===
if [ ! -d "$WIKI_ROOT/.git" ]; then
    echo -e "${RED}❌ 错误:${NC} $WIKI_ROOT 不是 git 仓库"
    echo "跑 wiki-keeper sync-protocol.md § 1 首次 setup"
    exit 1
fi

cd "$WIKI_ROOT"

# === 取 commit message (v1.7 终极: here-document 写文件) ===
# 第一个位置参数 = 完整 message (subject + 空行 + body, caller 自己 format)
# 后续 -m "body" / -mbody 累积加 body 段 (用 here-doc 拼, 不用 printf %b 避免 bash 字符串拼接吞换行)
MSG_FILE="$(mktemp -t safe-commit-msg.XXXXXX 2>/dev/null || mktemp)"
trap 'rm -f "$MSG_FILE"' EXIT

if [ $# -ge 1 ]; then
    # 第一个位置参数当 subject
    {
        printf '%s' "$1"
        # 后续 -m body / -mbody 累加 (用 here-doc, 保留所有换行)
        i=2
        while [ $i -le $# ]; do
            arg="${!i}"
            case "$arg" in
                -m)
                    next_i=$((i+1))
                    next_arg="${!next_i}"
                    if [ -n "$next_arg" ] && [ "${next_arg:0:1}" != "-" ]; then
                        printf '\n\n%s' "$next_arg"
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
                *)
                    i=$((i+1))
                    ;;
            esac
        done
    } > "$MSG_FILE"
else
    # 交互模式: 读 stdin
    echo -n "输入 commit message: "
    read -r MSG_INPUT
    printf "%s" "$MSG_INPUT" > "$MSG_FILE"
fi

if [ ! -s "$MSG_FILE" ]; then
    echo -e "${RED}❌ 错误:${NC} commit message 不能为空"
    exit 1
fi
echo -e "${BLUE}📝 commit message 预览:${NC}"
cat "$MSG_FILE"
echo "---"

# === Step 1: 看本地变更 ===
echo ""
echo -e "${BLUE}=== Step 1: git status ===${NC}"
git status --short

# === Step 1.5: 排除 Obsidian 工作区文件(关键!v1.6 加, v1.7 强化) ===
# 这些是 Obsidian 本地 canvas / 备份 / 配置,不应该 commit 到共享 wiki
# v1.6 漏洞: `git rm --cached` 只处理已 tracked 文件, 新 untracked 的
# `未命名.canvas` 在 Step 2 `git add -A` 时仍被加进去 (实测 2026-06-05 误入 commit)
# v1.7 修法: 同时 .gitignore 写入 + Step 2.5 校验 untracked 是否真被 gitignore 盖住
EXCLUDE_PATTERNS=(
  "*.canvas"           # Obsidian Canvas(白板)
  "*.base"             # Obsidian Bases(数据库)
  "*.bak"              # 备份文件
  "*.tmp"              # 临时文件
  "*.swp"              # vim swap
  "*.swo"              # vim swap
  ".obsidian/*"        # Obsidian 配置 + 插件
  ".trash/*"           # Obsidian 回收站
  "Untitled.canvas"    # 特定无标题 canvas (英文版)
  "未命名*.canvas"     # 中文版 (含 "未命名 1.canvas" 等)
)
echo ""
echo -e "${BLUE}=== Step 1.5: 排除 Obsidian 本地文件 (v1.7 强化版) ===${NC}"
for pat in "${EXCLUDE_PATTERNS[@]}"; do
  if git status --short | grep -E "$pat" >/dev/null 2>&1; then
    echo "排除模式: $pat"
    # 从 git index 移除(如果已 tracked)
    git rm --cached -r --ignore-unmatch "$pat" 2>/dev/null || true
  fi
done
# 写一份 .gitignore(防御性,确保未来不 add)
GITIGNORE_ENTRIES=$(printf '%s\n' "${EXCLUDE_PATTERNS[@]}")
if [ -f .gitignore ]; then
  if ! grep -qF "未命名*.canvas" .gitignore 2>/dev/null; then
    # v1.7 检测关键 pattern (中文未命名) 防止 v1.6 的 .canvas 单独检测不全
    echo "" >> .gitignore
    echo "# safe-commit-push.sh v1.7 排除 (2026-06-05 强化)" >> .gitignore
    echo "$GITIGNORE_ENTRIES" >> .gitignore
    git add .gitignore
    echo "✅ .gitignore 更新 (加入 v1.7 排除模式)"
  fi
else
  echo "# safe-commit-push.sh v1.7 排除" > .gitignore
  echo "$GITIGNORE_ENTRIES" >> .gitignore
  git add .gitignore
  echo "✅ .gitignore 创建"
fi

# === Step 2: add 所有 (v1.7 改为先看 untracked 是否被 gitignore 盖住) ===
echo ""
echo -e "${BLUE}=== Step 2: git add -A (v1.7 加 untracked 预校验) ===${NC}"
# 先看 untracked 列表, 跟 EXCLUDE_PATTERNS 比对, 看是否真被 .gitignore 排除
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null || true)
LEAKED=""
for f in $UNTRACKED; do
  for pat in "${EXCLUDE_PATTERNS[@]}"; do
    # fnmatch 风格匹配 (Obsidian 临时文件规则)
    case "$f" in
      $pat) LEAKED="$LEAKED $f" ;;
    esac
  done
done
if [ -n "$LEAKED" ]; then
    echo -e "${RED}❌ 致命: v1.6 漏洞复发! 应排除的 untracked 文件没被 .gitignore 盖住:${NC}"
    for f in $LEAKED; do
      echo "    - $f"
    done
    echo ""
    echo "修法: 检查 .gitignore 是否包含这些 pattern, 或加更多 EXCLUDE_PATTERNS"
    exit 3
fi
git add -A
echo "已 add 所有变更(已排除 Obsidian 本地文件, v1.7 预校验通过)"

# === Step 3: commit ===
echo ""
echo -e "${BLUE}=== Step 3: git commit ===${NC}"
# 如果没变更,跳过 commit
if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  没 staged 变更,跳过 commit${NC}"
    H_LOCAL=$(git rev-parse HEAD)
    echo "本地 HEAD: $H_LOCAL"
else
    # v1.7 改: 用 -F file 直接传 message 文件 (绕 printf %b 字符串拼接吞换行坑)
    git commit -F "$MSG_FILE"
    echo ""
fi

# === Step 4: 验证 commit 真存在(关键!防假成功 #1)===
echo ""
echo -e "${BLUE}=== Step 4: 核验 commit 真存在 ===${NC}"
H_LOCAL=$(git rev-parse HEAD)
COMMIT_MSG_ACTUAL=$(git log -1 --format='%s')
echo "本地 HEAD: $H_LOCAL"
echo "commit message: $COMMIT_MSG_ACTUAL"

# 双保险:用 git cat-file 核对象存在
if ! git cat-file -t "$H_LOCAL" >/dev/null 2>&1; then
    echo -e "${RED}❌ 假成功诊断!${NC} commit hash $H_LOCAL 不存在"
    echo "git cat-file -t 报 'Not a valid object name'"
    exit 1
fi
echo -e "${GREEN}✅ commit 真存在${NC}"

# === Step 5: push + 核验远端 hash(关键!防假成功 #2)===
echo ""
echo -e "${BLUE}=== Step 5: push + 5 步核验 ===${NC}"

# 5a. fetch 更新 origin ref
git fetch origin "$BRANCH" 2>&1 | head -3 || true

# 5b. 看远端有没有新 commit(我该拉?)
H_REMOTE_BEFORE=$(git rev-parse "origin/$BRANCH" 2>/dev/null || echo "NONE")
echo "远端 origin/$BRANCH (推送前): $H_REMOTE_BEFORE"

# 5c. 看本地有没有领先远端
LEAD_COUNT=$(git rev-list --count "$H_REMOTE_BEFORE"..HEAD 2>/dev/null || echo 0)
echo "本地领先远端的 commit 数: $LEAD_COUNT"

if [ "$LEAD_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  本地没领先远端的 commit,无需 push?${NC}"
    echo "可能原因: 远端有更新,先 pull --rebase"
    exit 2
fi

# 5d. push
echo ""
echo -e "${BLUE}>>> git push origin $BRANCH${NC}"
if ! git push origin "$BRANCH" 2>&1; then
    echo -e "${RED}❌ push 失败${NC}"
    exit 1
fi

# 5e. 核验远端 hash = 本地 hash(关键!)
git fetch origin "$BRANCH" 2>&1 | head -3 || true
H_REMOTE_AFTER=$(git rev-parse "origin/$BRANCH")
H_LOCAL_AFTER=$(git rev-parse HEAD)

echo ""
echo "本地 HEAD:   $H_LOCAL_AFTER"
echo "远端 HEAD:   $H_REMOTE_AFTER"

if [ "$H_LOCAL_AFTER" = "$H_REMOTE_AFTER" ]; then
    echo -e "${GREEN}✅ 推送成功!本地 = 远端 = $H_LOCAL_AFTER${NC}"
    echo ""
    echo -e "${BLUE}=== 5 步核验全部通过 ===${NC}"
    echo "1. ✅ git status"
    echo "2. ✅ git add -A"
    echo "3. ✅ git commit (hash = $H_LOCAL_AFTER)"
    echo "4. ✅ commit 真存在(cat-file 验证)"
    echo "5. ✅ push + hash 一致"
    exit 0
else
    echo -e "${RED}❌ 假成功诊断!${NC} push 后远端 hash 不一致"
    echo "  本地: $H_LOCAL_AFTER"
    echo "  远端: $H_REMOTE_AFTER"
    echo "可能原因:"
    echo "  - 推送时 sibling 同时推了(3rd wiki-keeper 自动 push 抢)"
    echo "  - 网络中断 push 实际没成功"
    echo "  - pre-push hook 拒绝(内容不符)"
    exit 1
fi
