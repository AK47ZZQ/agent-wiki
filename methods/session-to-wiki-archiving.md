---
title: "Method: Session-to-Wiki Archiving"
created: 2026-05-28
updated: 2026-05-28
type: method
tags: [method, workflow, automation, archive]
confidence: high
source: hermes-session-archiver
---

# Session-to-Wiki Archiving

## Problem
Hermes conversations contain valuable knowledge (decisions, code, workflows) that's trapped in ephemeral sessions. Needs to be captured as persistent, interconnected wiki pages.

## Approach
A single-file Python archiver reads the Hermes SQLite state.db, extracts structured content, and writes markdown pages with `` for Obsidian Graph View.

## When to Use
- After any productive conversation session
- Before closing a session that produced decisions or code
- Daily via cron for automated capture

## When NOT to Use
- Session content is trivial (hellos, one-line questions)
- Wiki maintenance is running (avoid concurrent writes)

## Steps
1. **Run archiver** — `python3 archiver.py` (or `--all` for batch)
2. **Verify** — Check `~/wiki/wiki/entities/hermes-session-{id}.md`
3. **Check links** — Open in Obsidian, verify Graph View shows the new node
4. **Optional cleanup** — `--force` to overwrite if content was stale

## Verification
- [ ] Session page exists in `~/wiki/wiki/entities/`
- [ ] Skill stub pages exist for skills used
- [ ] `` connect session → skill stubs
- [ ] Index and log are updated
- [ ] Obsidian Graph View shows the new node

## Related
- [[hermes-skill-wiki-archive]]
- [[hermes-skill-llm-wiki]]
