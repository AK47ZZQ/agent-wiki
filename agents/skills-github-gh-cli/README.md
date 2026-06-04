# github-gh-cli skill — Mirror in Wiki

> This directory is a **mirror** of the live skill at
> `hermes-all/hermes/skills/github/github-gh-cli/` on the main-claude machine.
>
> The 3rd laptop can pull this mirror via `git pull origin main` and copy it
> into its own `hermes-all/hermes/skills/github/github-gh-cli/` to activate.

## Why a mirror

The main-claude `hermes-all` git remote is **deleted** (per user hard preference, 2026-06-04 18:00).
This means in-repo skills added on main-claude don't auto-sync to 3rd.
The wiki (agent-wiki) is the **only surviving shared git remote**, so skills
that should be cross-machine get a copy here.

## Activation on 3rd

```bash
# On 3rd laptop, after pulling wiki
cd ~/hermes-all  # or wherever 3rd's hermes-all lives
cp -r /path/to/wiki/agents/skills-github-gh-cli hermes/skills/github/
# Restart Hermes session (skill loader is per-session)
```

## Source of truth

The **live** skill is at `hermes-all/hermes/skills/github/github-gh-cli/`
on main-claude. When main-claude updates the skill, re-mirror:

```bash
# On main-claude
rm -rf wiki/agents/skills-github-gh-cli
cp -r hermes/skills/github/github-gh-cli wiki/agents/skills-github-gh-cli
# Then: add, commit, push via 5-step verification
```

## Skill version

- **Mirror updated**: 2026-06-04 23:45
- **Live version**: v1.0.0
- **Files**: SKILL.md (14.5K) + 4 references + 1 script + 1 template = 60K total

## Differences from live

None. The mirror is byte-identical. If main-claude has changes that aren't
here, mirror is stale — re-run the `cp -r` above.
