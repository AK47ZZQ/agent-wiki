---
name: github-gh-cli
description: "Use when the user asks to interact with GitHub from the terminal via gh CLI (create/list/view PRs, issues, releases, repos, workflows, API calls), check gh installation/auth status, script gh for automation, or install gh extensions. Covers detection, authentication, command cookbook, JSON/jq output, scripting patterns, and common footguns. Pairs with github-pr-workflow / github-issues / github-code-review which describe task flows — this skill is the gh-tool foundation."
emoji: 🐙
vibe: "The terminal-native GitHub toolbox — install, auth, command, script, extend"
color: cyan
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, gh-cli, CLI, devtools, automation, scripting]
    related_skills: [github-auth, github-pr-workflow, github-issues, github-code-review, github-repo-management]
---

# GitHub CLI (gh) Skill

The `gh` tool foundation layer. Use this when the user wants to **do something with GitHub from the terminal** and `gh` is the right hammer. Pairs with task-oriented skills (pr-workflow, issues, code-review) — those describe *what* to do, this describes *how the tool works*.

## When to Use

- User asks "用 gh 查 / 创建 / 列出 PR / issue / release / workflow"
- User wants a JSON / `--jq` pipeline against GitHub data
- User asks to script a GitHub workflow (cron, batch, CI)
- User wants to install a `gh extension` or write one
- User asks "gh 装了吗 / 认证了吗" → run detection block

**Don't use for**:
- "Make me a commit" / "push my branch" → use `git` (gh doesn't replace git)
- Web-only tasks (multi-file diff review, long Actions logs) → use GitHub web
- **Task-level GitHub workflows** (PR lifecycle, issue triage, code review) → use `github-pr-workflow` / `github-issues` / `github-code-review` which **call into** gh via this skill

---

## 0. Detection — Always Run First

Before any gh command, confirm gh is installed and authenticated. If not, see **§ 1. Install** or **§ 2. Auth**.

```bash
# Is gh installed?
command -v gh && gh --version || echo "NOT_INSTALLED"

# Is gh authenticated?
gh auth status 2>&1 | head -10

# Quick READ-only sanity test (works on any repo)
gh api /user --jq '.login' 2>/dev/null || echo "NOT_AUTHED"
```

**Decision matrix**:

| Installed | Authed | Action |
|---|---|---|
| ✅ | ✅ | Proceed with `gh` commands |
| ✅ | ❌ | Jump to § 2. Auth |
| ❌ | n/a | Jump to § 1. Install (winget / brew / apt) |
| ❌ | ❌ | No gh, use `git + curl + GITHUB_TOKEN` fallback (see `github-pr-workflow` for the fallback block) |

**Don't print tokens**. The detection above uses `gh auth status` and `gh api /user --jq '.login'` — both safe. If you need the token for a sub-process, use `gh auth token` and pass via env var, never `echo`.

---

## 1. Install

Reference the full install block for your platform: `references/install.md`.

**One-liners (most common)**:

```bash
# Windows (winget — usually pre-installed)
winget install --id GitHub.cli

# macOS
brew install gh

# Linux Debian/Ubuntu
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh

# Verify
gh --version  # expect 2.x+
```

After install, **close and reopen your terminal** so PATH updates. On Windows MSYS bash specifically, you may need to log out / back in for `%APPDATA%` to refresh.

---

## 2. Authenticate

**Three flows** (pick by environment):

### 2a. Browser login (interactive dev box)

```bash
gh auth login
# → GitHub.com
# → HTTPS
# → Login with a web browser (recommended)
```

### 2b. Token from stdin (CI / headless)

```bash
# Write token to a file (don't echo it):
echo "$GH_TOKEN_FROM_SECRET" > /tmp/gh.token
gh auth login --with-token < /tmp/gh.token
rm -f /tmp/gh.token
```

**Required scopes for fine-grained PATs**: `Contents: Read and write`, `Issues: Read and write`, `Pull requests: Read and write`, `Metadata: Read-only` (auto).

### 2c. Reuse existing credential (no new login)

If `~/.netrc` or `%APPDATA%\GitHub CLI\hosts.yml` already has a working token:

```bash
# Just check — gh will use the host's token from hosts.yml
gh auth status
# If it shows "Logged in", you're done. No `gh auth login` needed.
```

For multi-account setups, see § 8.

---

## 3. Command Cookbook (Core Workflows)

Full command reference: `references/command-cheatsheet.md`. Highlights below.

### Pull Requests

```bash
# List (always use --json + --limit for scripts)
gh pr list --state open --json number,title,author,url --limit 50

# View details
gh pr view 123 --json number,title,state,additions,deletions,changedFiles,url

# Checkout PR locally
gh pr checkout 123

# Create PR
gh pr create --base main --head feature-x --title "feat: X" --body "..."
gh pr create --fill      # auto-fill title/body from commits
gh pr create --draft     # open as draft

# Review
gh pr review 123 --approve
gh pr review 123 --request-changes -b "..."
gh pr review 123 --comment -b "LGTM"

# Merge
gh pr merge 123 --squash --delete-branch
```

### Issues

```bash
gh issue list --state open --label bug --assignee @me --limit 30
gh issue view 456
gh issue create --title "bug: X" --body "..." --label bug
gh issue close 456 --reason "not planned"
gh issue comment 456 -b "Same problem here"
```

### Repos

```bash
gh repo clone owner/repo
gh repo create my-repo --public --source=. --push
gh repo fork owner/repo --clone
gh repo view owner/repo --json name,stargazerCount,description
```

### Releases

```bash
gh release list --limit 20
gh release view v1.0.0
gh release create v1.0.0 ./dist/*.tar.gz --title "v1.0.0" --notes "..."
gh release download v1.0.0 --pattern "*.tar.gz"
```

### Workflows / Actions

```bash
gh workflow list
gh workflow run ci.yml --ref feature-x
gh run list --limit 20
gh run view 12345 --log
gh run watch 12345   # blocking
gh run rerun 12345 --failed
```

### Search (high footgun area)

```bash
# ⭐ The -- separator is MANDATORY when query starts with a filter
gh search issues -- "is:open -label:wontfix label:bug"
gh search prs -- "is:open author:@me"
gh search code -- "TODO repo:owner/myrepo"
```

### Secrets / Variables

```bash
gh secret set MY_SECRET --body "value"
gh secret list
gh variable set MY_VAR --body "value"
```

### API (REST + GraphQL)

```bash
# REST with jq
gh api /user --jq '.login'
gh api /repos/owner/repo/issues --paginate --jq '.[] | {n: .number, t: .title}'

# POST
gh api -X POST /repos/owner/repo/issues \
  -f title="bug" -f body="..." -f 'labels[]=bug'

# GraphQL
gh api graphql -F query='
  query { viewer { login } }
'
```

---

## 4. Scripting Patterns

The whole point of `gh` over `curl` is **structured output + auth handling**. Use these patterns.

### 4a. JSON + jq pipeline

```bash
# Find PRs waiting on review
gh pr list --state open --json number,title,reviewDecision \
  | jq -r '.[] | select(.reviewDecision == "REVIEW_REQUIRED") | "#\(.number) \(.title)"'

# Count issues per label
gh issue list --state all --limit 1000 --json labels \
  | jq -r '.[].labels[].name' | sort | uniq -c | sort -rn
```

### 4b. Cross-repo batch

```bash
# Iterate over a list of repos
for r in owner/repo-a owner/repo-b owner/repo-c; do
  echo "=== $r ==="
  gh pr list --repo "$r" --state open --json number,title --jq '.[] | "#\(.number) \(.title)"'
done
```

### 4c. Watch a run until done (block)

```bash
gh run watch 12345 --exit-status
```

### 4d. Page through large result sets

```bash
gh api /repos/owner/repo/issues --paginate --jq '.[] | .number'
```

### 4e. Capture URL only (don't print full objects)

```bash
NEW_PR_URL=$(gh pr create --fill | tail -1)
echo "Created: $NEW_PR_URL"
```

---

## 5. Multi-Account Setup

For users with multiple GitHub accounts (work + personal):

```bash
# Log in to each
gh auth login --hostname github.com        # default
gh auth login --hostname github.com-work   # adds second host

# Switch with GH_HOST
GH_HOST=github.com-work gh api /user --jq '.login'

# Get token for a specific host (for sub-processes)
GH_HOST=github.com-work gh auth token | <some-sub-process>
```

`GH_TOKEN` env var is also respected but is **host-agnostic** — prefer `GH_HOST + gh auth token` for clarity.

---

## 6. gh Extensions (Install / Write)

140+ community extensions at https://github.com/topics/gh-extension. Full guide: `references/extension-development.md`.

```bash
# Install
gh extension install owner/gh-<name>
gh extension install dlvhdr/gh-dash       # TUI PR/issue dashboard
gh extension install github/gh-copilot    # Copilot integration

# Manage
gh extension list
gh extension upgrade <name>
gh extension remove <name>
gh extension create <name>   # scaffolds a new one
```

**To write your own extension** (Go binary named `gh-<name>`):

```go
// main.go
package main

import (
    "fmt"
    "github.com/cli/go-gh/v2/pkg/api"
    "github.com/cli/go-gh/v2/pkg/repository"
)

func main() {
    base, _ := repository.Current()           // current repo
    client, _ := api.DefaultRESTClient()      // auth-aware HTTP

    var resp struct{ Login string `json:"login"` }
    client.Get("user", &resp)
    fmt.Printf("repo: %s/%s, user: %s\n",
        base.RepoOwner(), base.Name(), resp.Login)
}
```

```bash
go mod init github.com/<you>/gh-mytool
go get github.com/cli/go-gh/v2
go build -o gh-mytool
gh extension install .   # install from local dir
```

Repo convention: name the repo `gh-<name>`, tag releases, add topic `gh-extension`. Done.

---

## 7. Configuration & UX

```bash
# Stop pager from blocking scripts
gh config set pager cat

# Default editor
gh config set editor "code -w"

# Default git protocol
gh config set git_protocol https

# View all config
gh config list
```

**Config file locations**:
- Linux: `~/.config/gh/config.yml` + `hosts.yml`
- macOS: `~/Library/Application Support/gh/`
- Windows: `%APPDATA%\GitHub CLI\config.yml` + `hosts.yml`

---

## 8. Common Pitfalls

1. **`--` separator in search**: Forgetting `--` before a query that starts with a filter (`-label:bug`, `is:open`) means the shell interprets the dash as a flag. **Always**: `gh search issues -- "is:open -label:bug"`.

2. **Pager in scripts**: `gh issue list` opens `less` by default, which blocks non-interactive scripts. Set `gh config set pager cat` once.

3. **JSON field case sensitivity**: `--json Number` fails (uppercase N). All field names are lowercase: `--json number,title,state`.

4. **Rate limits**: Unauthenticated = 60 req/h, authenticated = 5000 req/h. Watch for `403 rate limit exceeded` in `gh api` loops.

5. **`GH_TOKEN` is host-agnostic**: For multi-account, use `GH_HOST` not `GH_TOKEN`. `GH_TOKEN` overwrites for ALL hosts.

6. **Enterprise Server hostname**: `gh auth login` defaults to `github.com`. For GHES, pass `--hostname ghes.example.com`. Cookies/tokens are hostname-isolated.

7. **`gh` is not a `git` proxy**: Unlike `hub`, `gh` doesn't wrap `git`. Push/merge with `git`, then use `gh` for PR/release layers.

8. **MSYS bash + gh output**: `gh` is a Windows binary; output paths use Windows-style. If piping to MSYS tools, use `cygpath` to convert. Don't `gh api ... | xargs` paths directly.

9. **Token rotation requires re-auth**: If a PAT is revoked, `gh` will fail with `401 Bad credentials`. Re-run `gh auth login` or update `hosts.yml` manually.

10. **`gh api` GraphQL cost**: GraphQL queries have a "complexity cost" — overly nested queries can hit rate limits even at low call frequency. Test with smaller queries first.

11. **`gh run watch --exit-status` blocks until run finishes**: Useful for CI dependencies. Don't run it from a non-terminal context.

12. **The `gh` and `git` credential stores are SEPARATE**: `gh` uses `%APPDATA%\GitHub CLI\hosts.yml`, `git` uses `~/.netrc` or credential helper. Rotating one does not affect the other.

---

## 9. Verification Checklist

After using this skill, verify:

- [ ] `gh --version` returns 2.x+ (not "command not found")
- [ ] `gh auth status` shows "Logged in to github.com as <user>"
- [ ] `gh api /user --jq '.login'` returns the expected username
- [ ] For scripted gh: `gh config set pager cat` is set (no less blocking)
- [ ] For multi-account: `GH_HOST=<host>` switches correctly
- [ ] For extensions: `gh extension list` shows installed ones

---

## 10. One-Shot Recipes

### "List all my open PRs across multiple repos"

```bash
for r in owner/repo-a owner/repo-b; do
  gh pr list --repo "$r" --state open --json number,title,url \
    --jq '.[] | "\(.number)\t\(.title)\t\(.url)"'
done | column -t -s $'\t'
```

### "Create a release with auto-generated notes"

```bash
gh release create v$(date +%Y.%m.%d) ./dist/*.tar.gz \
  --generate-notes \
  --title "Release v$(date +%Y.%m.%d)"
```

### "Audit: PRs that failed CI in last 7 days"

```bash
gh pr list --state all --search "is:closed merged:>=$(date -d '7 days ago' +%Y-%m-%d)" \
  --json number,title,mergeCommit,statusCheckRollup \
  --jq '.[] | select(.statusCheckRollup | tostring | contains("FAILURE")) | "#\(.number) \(.title)"'
```

### "Block until a specific run finishes, then report"

```bash
gh run watch <run-id> --exit-status && \
  gh run view <run-id> --json conclusion,name,headBranch,url
```

---

## 11. Related Skills

- `github-auth` — authentication setup (this skill assumes auth done; refer there for token/SSH)
- `github-pr-workflow` — task flow: open a PR, get it reviewed, merge (uses `gh` under the hood)
- `github-issues` — task flow: triage, create, link, close
- `github-code-review` — task flow: review a PR
- `github-repo-management` — task flow: clone, fork, sync, archive

When the user says "do X with GitHub", pick the **task** skill (e.g. `github-pr-workflow`). This skill loads when the user says "how does gh work" or "set up gh" or "script this gh command".

## 12. References

- `references/install.md` — platform-specific install + verification
- `references/command-cheatsheet.md` — full L1-L2 command reference
- `references/extension-development.md` — writing your own gh extension (Go)
- `references/troubleshooting.md` — common errors + fixes (auth fail, rate limit, 404, 422)
- `scripts/check-gh-status.sh` — detection block as reusable script
- `templates/setup-gh-auth.md` — checklist for setting up gh on a new machine
