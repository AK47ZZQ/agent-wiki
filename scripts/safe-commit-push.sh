#!/usr/bin/env bash
# safe-commit-push.sh — 5 步核验 commit + push(防假成功)
# Created: 2026-06-04 (wiki-keeper v1.5)
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

set -euo pipefail

# === 颜色输出(便于人眼读) ===
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

WIKI_ROOT="${WIKI_ROOT:-/c/Users/Administrator/hermes-all/wiki}"
BRANCH="${2:-$(cd "$WIKI_ROOT" 2>/dev/null && git branch --show-current)}"

# === 进入 wiki 目录 ===
if [ ! -d "$WIKI_ROOT/.git" ]; then
    echo -e "${RED}❌ 错误:${NC} $WIKI_ROOT 不是 git 仓库"
    echo "跑 wiki-keeper sync-protocol.md § 1 首次 setup"
    exit 1
fi

cd "$WIKI_ROOT"

# === 取 commit message ===
if [ -z "${1:-}" ]; then
    echo -n "输入 commit message: "
    read -r COMMIT_MSG
else
    COMMIT_MSG="$1"
fi

if [ -z "$COMMIT_MSG" ]; then
    echo -e "${RED}❌ 错误:${NC} commit message 不能为空"
    exit 1
fi

# === Step 1: 看本地变更 ===
echo ""
echo -e "${BLUE}=== Step 1: git status ===${NC}"
git status --short

# === Step 2: add 所有 ===
echo ""
echo -e "${BLUE}=== Step 2: git add -A ===${NC}"
git add -A
echo "已 add 所有变更"

# === Step 3: commit ===
echo ""
echo -e "${BLUE}=== Step 3: git commit ===${NC}"
# 如果没变更,跳过 commit
if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  没 staged 变更,跳过 commit${NC}"
    H_LOCAL=$(git rev-parse HEAD)
    echo "本地 HEAD: $H_LOCAL"
else
    git commit -m "$COMMIT_MSG"
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
