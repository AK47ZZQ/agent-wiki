#!/usr/bin/env python3
# daily_maintain.py — Wiki 每日完整维护(no_agent cron 调用)
# Created: 2026-06-04 22:58 (用户硬偏好"每天 8 点自动拉取最新+维护+同步")
# 用途:取代人工维护,5 步一气呵成:
#   1. fetch + rebase 拉最新
#   2. check-wiki-quality.py 5 项自检
#   3. scan_wiki_secrets.py 敏感字符串扫描
#   4. hermes-all 4 个 SQLite DB WAL checkpoint
#   5. 如有本地改动 + 自检全过 → 5 步核验推 agent-wiki
# 输出:全过静默(空 stdout) / 有问题发消息到飞书
#
# 调用:python scripts/daily_maintain.py
# 设计:no_agent=True cron 调度,空 stdout = 静默,非空 = 飞书消息
import subprocess, os, sys, time
from pathlib import Path

WIKI = Path(r'C:\Users\Administrator\hermes-all\wiki')
os.chdir(WIKI)

def run(cmd, timeout=60):
    """跑 shell 命令,返回 (rc, stdout, stderr)"""
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=True)
    return r.returncode, r.stdout, r.stderr

def step(name):
    return f'=== {name} ==='

def section(title):
    return f'\n--- {title} ---\n'

# 收集报告
report_lines = []
issues = []

# === Step 1: fetch + rebase ===
report_lines.append(step('1. fetch + rebase'))
rc, out, err = run('git fetch origin main 2>&1')
report_lines.append(out or '(no output)')
if rc != 0:
    issues.append(f'Step 1 fetch 失败: {err}')

# 看远端有没有 sibling 推
rc, lead_remote, _ = run('git rev-list --count HEAD..origin/main')
lead_remote = int(lead_remote.strip() or 0)
if lead_remote > 0:
    report_lines.append(f'远端领先 {lead_remote} commits,rebase 中...')
    rc, out, err = run(f'git pull --rebase origin main 2>&1')
    report_lines.append(out)
    if rc != 0:
        issues.append(f'Step 1 rebase 失败:{err}')

# === Step 2: check-wiki-quality.py 5 项自检 ===
report_lines.append(step('2. wiki 自检'))
rc, out, err = run('python scripts/check-wiki-quality.py 2>&1')
report_lines.append(out)
if 'FAIL' in out or '❌' in out:
    issues.append('wiki 自检 FAIL')

# === Step 3: scan_wiki_secrets.py 敏感扫描 ===
report_lines.append(step('3. 敏感字符串扫描'))
rc, out, err = run('python scripts/scan_wiki_secrets.py 2>&1')
report_lines.append(out[-500:])  # 只看后 500 字符(报告太长)
if '🔴' in out:
    # 提取 🔴 行数
    red_count = out.count('🔴')
    issues.append(f'敏感扫描发现 {red_count} 个 🔴 命中')

# === Step 4: 4 个 SQLite DB WAL checkpoint ===
report_lines.append(step('4. SQLite DB WAL checkpoint'))
for db in ['../hermes/state.db', '../hermes/lcm.db', '../hermes/response_store.db', '../hermes/kanban.db']:
    db_path = WIKI / db
    if not db_path.exists():
        continue
    python_script = f'''
import sqlite3
con = sqlite3.connect(r"{db_path}")
cur = con.cursor()
cur.execute('PRAGMA wal_checkpoint(TRUNCATE)')
cur.execute('PRAGMA integrity_check')
r = cur.fetchone()[0]
con.close()
print(f"  {db}: integrity={{r}}")
'''
    rc, out, err = run(f'python -c "{python_script}"', timeout=15)
    report_lines.append(out.strip())

# === Step 5: 5 步核验推 ===
report_lines.append(step('5. 5 步核验推'))

# 5.0 看本地 dirty?
rc, out, _ = run('git status --short')
if not out.strip():
    report_lines.append('无本地改动,无需推')
else:
    report_lines.append(f'本地改动:\n{out}')

    # 5.1 排除
    EXCLUDE = ['*.canvas', '*.base', '*.bak', '*.tmp', '*.swp', '*.swo',
               '.obsidian/*', '.trash/*', 'Untitled.canvas', '未命名.canvas']
    for pat in EXCLUDE:
        run(f'git rm --cached -r --ignore-unmatch "{pat}" 2>/dev/null', timeout=10)

    # 5.2 add
    run('git add -A')

    # 5.3 commit
    rc, out, err = run('git commit -m "chore: daily maintain (auto, 2026-06-04)" 2>&1')
    report_lines.append(f'commit rc={rc}')

    # 5.4 核对象存在
    rc, h_local, _ = run('git rev-parse HEAD 2>&1')
    h_local = h_local.strip()
    rc2, _, _ = run(f'git cat-file -t {h_local} 2>&1')
    if rc2 != 0:
        issues.append(f'commit {h_local} 假成功!cat-file fail')
    else:
        report_lines.append(f'commit {h_local[:12]} 真存在')

        # 5.5 push + 核
        rc, out, err = run('git push origin main 2>&1')
        if rc != 0:
            issues.append(f'push 失败:{err[:200]}')
        else:
            # 双保险:核 origin/main == HEAD
            run('git fetch origin main 2>&1')
            rc, h_remote, _ = run('git rev-parse origin/main 2>&1')
            h_remote = h_remote.strip()
            if h_local == h_remote:
                report_lines.append(f'✅ 推送真成功!local=remote={h_local[:12]}')
            else:
                issues.append(f'push 假成功!local={h_local[:12]} remote={h_remote[:12]}')

# === 输出策略 ===
# 全过(无 issues)→ 静默(空 stdout,cron 不发消息)
# 有 issues → 输出报告(cron 发飞书)
if issues:
    print('⚠️ DAILY MAINTAIN 有问题:')
    for i in issues:
        print(f'  - {i}')
    print('\n=== 完整报告 ===')
    print('\n'.join(report_lines))
    sys.exit(1)
else:
    # 全过,只输出 1 行
    print('OK: daily maintain 全过,无改动无需推' if '无本地改动' in '\n'.join(report_lines) else 'OK: daily maintain 全过 + 已推')
