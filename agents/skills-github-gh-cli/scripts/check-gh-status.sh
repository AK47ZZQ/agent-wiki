#!/usr/bin/env bash
# check-gh-status.sh - Reusable gh detection block
# Source this file or call directly. Exit code: 0=ready, 1=auth-needed, 2=not-installed
#
# Usage: bash check-gh-status.sh
# Output: structured status report with color coding

set +e  # Don't exit on first failure; we want full report

# Color codes (auto-disabled if not a terminal)
if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    RED='\033[0;31m'
    NC='\033[0m'
else
    GREEN=''
    YELLOW=''
    RED=''
    NC=''
fi

# 1. Binary check
if command -v gh >/dev/null 2>&1; then
    GH_VERSION=$(gh --version 2>/dev/null | head -1)
    echo -e "${GREEN}OK${NC}  gh installed: $GH_VERSION"
    GH_INSTALLED=1
else
    echo -e "${RED}FAIL${NC}  gh NOT installed"
    echo "       Install: winget install --id GitHub.cli   (Windows)"
    echo "                brew install gh                  (macOS)"
    echo "                sudo apt install gh             (Linux Debian/Ubuntu)"
    GH_INSTALLED=0
fi

# 2. Auth check
GH_AUTHED=0
if [ "$GH_INSTALLED" -eq 1 ]; then
    AUTH_OUTPUT=$(gh auth status 2>&1)
    if echo "$AUTH_OUTPUT" | grep -q "Logged in to"; then
        AUTH_LINE=$(echo "$AUTH_OUTPUT" | grep "Logged in to" | head -1)
        echo -e "${GREEN}OK${NC}  gh authenticated: $AUTH_LINE"
        GH_AUTHED=1
    else
        echo -e "${YELLOW}WARN${NC}  gh installed but not authenticated"
        echo "       Run: gh auth login"
        GH_AUTHED=0
    fi
fi

# 3. API sanity
if [ "$GH_AUTHED" -eq 1 ]; then
    API_USER=$(gh api /user --jq '.login' 2>/dev/null)
    if [ -n "$API_USER" ]; then
        echo -e "${GREEN}OK${NC}  API call works: user=$API_USER"
    else
        echo -e "${RED}FAIL${NC}  API call failed (auth or network issue)"
        echo "       Try: gh auth status"
    fi
fi

# 4. Pager config
if [ "$GH_INSTALLED" -eq 1 ]; then
    PAGER_CFG=$(gh config get pager 2>/dev/null)
    if [ "$PAGER_CFG" = "cat" ] || [ -z "$PAGER_CFG" ]; then
        echo -e "${GREEN}OK${NC}  pager OK (cat or unset, scripts safe)"
    else
        echo -e "${YELLOW}WARN${NC}  pager is '$PAGER_CFG' (will block scripts)"
        echo "       Fix: gh config set pager cat"
    fi
fi

# Summary
echo ""
if [ "$GH_INSTALLED" -eq 1 ] && [ "$GH_AUTHED" -eq 1 ]; then
    echo "Status: READY"
    exit 0
elif [ "$GH_INSTALLED" -eq 1 ]; then
    echo "Status: INSTALLED_BUT_NOT_AUTHED"
    exit 1
else
    echo "Status: NOT_INSTALLED"
    exit 2
fi
