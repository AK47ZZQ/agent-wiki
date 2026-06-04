# markitdown-converter skill — Mirror in Wiki

> Mirror of the live skill at `hermes-all/hermes/skills/productivity/markitdown-converter/`
> on the main-claude machine.

## Activation on 3rd

```bash
cd ~/hermes-all  # 3rd's hermes-all
cp -r /path/to/wiki/agents/skills-markitdown-converter hermes/skills/productivity/
# Restart Hermes session
```

## Skill version

- **Mirror updated**: 2026-06-05 00:30
- **Live version**: v1.0.0
- **Files**: SKILL.md (10.9K) + 4 references + 1 script + 1 template = ~37K total

## Source of truth

Live skill: `hermes-all/hermes/skills/productivity/markitdown-converter/` on main-claude.

To re-mirror after main-claude changes:
```bash
rm -rf wiki/agents/skills-markitdown-converter
cp -r hermes/skills/productivity/markitdown-converter wiki/agents/skills-markitdown-converter
# Then add, commit, push via 5-step verification
```
