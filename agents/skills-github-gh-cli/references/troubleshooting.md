# gh CLI Troubleshooting

## "gh: command not found"

**Cause**: gh not installed, or PATH not refreshed.

**Fix**:
1. Install (see `references/install.md`)
2. **Close and reopen terminal** so PATH updates
3. On Windows: log out and back in if winget install didn't refresh `%APPDATA%`
4. Verify: `command -v gh` (Unix) / `where gh` (Windows)

## "gh auth status" shows "You are not logged into any GitHub hosts"

**Cause**: No token in `%APPDATA%\GitHub CLI\hosts.yml` (Windows) / `~/.config/gh/hosts.yml` (Unix).

**Fix**:
```bash
gh auth login
# Choose: GitHub.com, HTTPS, web browser (or token)
```

## "401 Bad Credentials"

**Cause**: Token revoked, expired, or wrong host.

**Fix**:
1. Check token status: visit https://github.com/settings/tokens
2. If revoked → create new PAT, then `gh auth login --with-token < new.token`
3. If wrong host: `GH_HOST=correct-host gh auth login`

## "403 API rate limit exceeded"

**Cause**: 60 req/h unauth, 5000 req/h auth.

**Fix**:
```bash
# Check current rate
gh api /rate_limit --jq '.resources.core'

# Wait or authenticate to bump limit
gh auth login

# Add --paginate intentionally to avoid hammering
gh api /repos/owner/repo/issues --paginate | head -100
```

## "404 Not Found" on `gh api /...`

**Cause**: Wrong endpoint, wrong repo, or no read access.

**Fix**:
1. Verify endpoint: `gh api <path> --jq '.'`
2. For repos: confirm `owner/name` is correct, you have read access
3. For orgs: your token may lack `read:org` scope — `gh auth refresh --scopes read:org`

## "422 Unprocessable Entity"

**Cause**: Malformed request body (missing required field, wrong type).

**Fix**:
1. Check the field names: `gh api -X POST /repos/owner/repo/issues -f title=... -f body=...`
2. Use `-F` (multipart) for nested arrays: `-F 'labels[]=bug'`
3. Inspect what's expected: `gh api --method POST /path/of/same -f dummy=x` to see error JSON

## "Could not resolve host: github.com"

**Cause**: Network issue, DNS, or proxy.

**Fix**:
1. Test: `curl -I https://api.github.com/`
2. If behind proxy: `export HTTPS_PROXY=http://proxy:8080` or set in `~/.gitconfig` for git
3. gh respects `HTTPS_PROXY` env var (since v2.20+)

## Pager blocks script

**Cause**: `gh` defaults to `less` for output > 1 screen.

**Fix** (one-time):
```bash
gh config set pager cat
```

Or per-call:
```bash
GH_PAGER=cat gh issue list
PAGER=cat gh issue list
```

## "GraphQL: Field 'X' doesn't exist on type 'Y'"

**Cause**: Schema mismatch — your query references outdated or wrong fields.

**Fix**:
1. Introspect: `gh api graphql -F query='{ __type(name:"PullRequest") { fields { name } } }'`
2. Compare to https://docs.github.com/en/graphql/reference/objects

## "XDG_CONFIG_HOME not set" or config file not found

**Cause**: Non-standard config dir on Linux/WSL.

**Fix**:
- Linux: `~/.config/gh/`
- macOS: `~/Library/Application Support/gh/`
- Windows: `%APPDATA%\GitHub CLI\`

Override: `GH_CONFIG_DIR=/path/to/dir gh auth status`

## gh extension won't install

**Cause**: Repo not named `gh-<name>`, or no releases.

**Fix**:
1. Check repo name: must start with `gh-`
2. Check releases exist: `gh release list -R owner/gh-name`
3. Try with explicit version: `gh extension install owner/gh-name@latest`

## gh and git token rotation mismatch

**Cause**: You rotated the PAT in `~/.netrc` but gh uses `%APPDATA%\GitHub CLI\hosts.yml`. They are independent stores.

**Fix**:
```bash
# After creating a new PAT, update BOTH stores
echo "machine github.com login ghp_xxx password x-oauth-basic" > ~/.netrc  # git
gh auth login --with-token < new_token.txt                                       # gh
```

## Multi-account: "Bad credentials" when using GH_HOST

**Cause**: `gh auth token --hostname <host>` not called, or the wrong host.

**Fix**:
```bash
# Add the host
gh auth login --hostname github.com-work

# Verify all logged-in hosts
gh auth status

# Use specific host
GH_HOST=github.com-work gh api /user --jq '.login'
```

## gh run watch hangs

**Cause**: `--exit-status` waits for terminal state but run is queued.

**Fix**:
- Add timeout: `gh run watch 12345 --exit-status` (default 5min timeout, configurable)
- If you just want to know when it's done: drop `--exit-status`, capture and parse later

## gh is slow on Windows

**Cause**: Antivirus scanning, or output redirection through Windows console.

**Fix**:
- Add `C:\Program Files\GitHub CLI\` to Windows Defender exclusions
- Avoid piping through `more` / `findstr` (use `grep` / `jq` instead)
- On MSYS bash, prefer `gh ... | jq` over `gh ... | xargs`

---

If your issue isn't here, search https://github.com/cli/cli/issues (3000+ issues archived, almost all edge cases are documented).
