# gh CLI Install — Platform-Specific

## Windows (most common — this is your main box)

### Option A: winget (recommended, pre-installed on Win10/11)

```bash
winget install --id GitHub.cli
```

After install, **close and reopen the terminal** (cmd / PowerShell / MSYS bash). The `gh` binary is placed in `%LOCALAPPDATA%\Microsoft\WindowsApps` which is on PATH by default.

### Option B: scoop

```bash
scoop bucket add github-gh https://github.com/cli/scoop-gh.git
scoop install gh
```

### Option C: MSI installer

Download from https://cli.github.com/ → "Download for Windows" → run the MSI.

### Verify on Windows

```bash
gh --version
# Expected: gh version 2.x.x (2026-06-04 latest is 2.62.0+)

where gh
# Should resolve to a real path. If "INFO: Could not find", your PATH doesn't include the install dir — log out / back in.
```

**MSYS bash gotcha**: gh on Windows uses Windows paths in output. If you pipe to MSYS tools, convert with `cygpath`:

```bash
gh api /repos/owner/repo/contents/some-file --jq '.download_url' | xargs cygpath -u | xargs cat
```

---

## macOS

```bash
brew install gh
```

Or download from https://cli.github.com/ → macOS package.

---

## Linux

### Debian / Ubuntu / Raspberry Pi

```bash
# Add GitHub's apt repo + signing key
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update
sudo apt install gh
```

### Fedora / RHEL / CentOS

```bash
sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install gh
```

### Arch

```bash
sudo pacman -S github-cli
```

### Verify on Linux

```bash
gh --version
type -a gh  # resolves to /usr/bin/gh or similar
```

---

## GitHub Codespaces

Codespaces ship with `gh` pre-installed. No action needed. Verify:

```bash
gh --version
```

---

## GitHub Actions Runners

GitHub-hosted runners ship with `gh` pre-installed and updated weekly. Self-hosted runners must install per the above instructions for their OS.

If you need a specific gh version in a workflow:

```yaml
- name: Install specific gh version
  run: |
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
    sudo apt update
    sudo apt install -y gh
```

---

## Verification (any platform)

```bash
# 1. Binary present
command -v gh

# 2. Version sane
gh --version  # 2.x+

# 3. Auth works
gh auth status

# 4. Read API works (proves auth + network)
gh api /user --jq '.login'
```

If any step fails, jump to `references/troubleshooting.md`.

---

## Update / Upgrade

```bash
# Windows
winget upgrade --id GitHub.cli

# macOS
brew upgrade gh

# Linux
sudo apt update && sudo apt upgrade gh
```

Releases: https://github.com/cli/cli/releases. Starting with v2.93.0, releases are immutable and use Sigstore Build Provenance Attestation for verifiability:

```bash
# Verify a downloaded release
gh at verify -R cli/cli gh_2.62.0_macOS_arm64.zip
```
