# gh CLI Setup Checklist (Per-Machine)

> Use this on every new machine (or VM / container) where you need to use `gh`.

## 1. Install (per platform)

- [ ] **Windows**: `winget install --id GitHub.cli`
- [ ] **macOS**: `brew install gh`
- [ ] **Linux**: apt repo + `sudo apt install gh` (see `references/install.md`)
- [ ] **Close and reopen terminal** so PATH updates
- [ ] Verify: `gh --version` shows 2.x+

## 2. Authenticate

Pick one:

- [ ] **Browser login** (dev box): `gh auth login` → follow prompts
- [ ] **Token from env** (CI / headless): `gh auth login --with-token < token.txt`
- [ ] **Reuse existing** (already have a token in `~/.netrc` or `hosts.yml`): just verify `gh auth status` shows logged in

**Required PAT scopes (fine-grained token)**:
- [ ] `Contents: Read and write`
- [ ] `Issues: Read and write`
- [ ] `Pull requests: Read and write`
- [ ] `Metadata: Read-only` (auto-included)
- [ ] `Actions: Read and write` (if you'll trigger workflows)

## 3. Verify

- [ ] `gh auth status` shows "Logged in to github.com as <user>"
- [ ] `gh api /user --jq '.login'` returns your username
- [ ] `gh repo view <owner>/<repo> --json name` works on a repo you have access to

## 4. UX Configuration

- [ ] `gh config set pager cat` (disable less, avoid script blocking)
- [ ] `gh config set git_protocol https` (default protocol for `gh repo clone`)
- [ ] `gh config set editor "code -w"` or your preferred editor (for `gh issue create` interactive)

## 5. Multi-Account (optional)

If you have work + personal accounts:

- [ ] `gh auth login --hostname github.com` (default)
- [ ] `gh auth login --hostname github.com-work` (second)
- [ ] Test switch: `GH_HOST=github.com-work gh api /user --jq '.login'`

## 6. Useful Extensions (optional, install what you'll actually use)

- [ ] `gh extension install dlvhdr/gh-dash` (TUI dashboard)
- [ ] `gh extension install github/gh-copilot` (Copilot integration)
- [ ] `gh extension install kpbird/poi` (clean local branches)

## 7. Done

- [ ] `bash scripts/check-gh-status.sh` (from this skill directory) → all green

---

## Quick verification command (one-liner)

```bash
gh --version && \
gh auth status 2>&1 | grep -q "Logged in" && \
gh api /user --jq '.login'
```

If the last command prints your GitHub username, you're set.

## Common follow-up needs

- **Need to trigger workflows?** Add `workflow` scope to your PAT, re-auth: `gh auth refresh --scopes workflow`
- **Need SSH for git but gh for API?** gh and git are independent; configure both (see `github-auth` skill)
- **CI / cron / batch?** Use a separate machine account (not your personal token) for unattended use
