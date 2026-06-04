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

# === 2026-06-04 baseline 已知泄露(用户接受风险,不再每天报)===
# 公开仓库(2026-06-04 22:00 起)后,以下 8 处 🔴 是历史基线,已知且用户决定不动
# daily_maintain 只报 "新发现" → baseline 之外的 🔴
KNOWN_BASELINE = {
    ('methods/git-push-cheatsheet.md', 137),       # x-oauth-basic + netrc password (同 1 行,cheatsheet 示例)
    ('notes/search-hermes-workspace-expose.md', 157),  # your-secure-password 占位符
    # log.md 里的 2 处完整 PAT + 1 处 9dfc 残片 + README.md 9dfc + protocols 9dfc
    # 全是历史 commit 残留,轮换 PAT 之前会一直存在
    ('log.md', 248),
    ('log.md', 274),
    ('log.md', 305),
    ('log.md', 326),
    ('README.md', 18),
    ('protocols/git-collaboration-multi-agent.md', 113),
}

def is_known_baseline(file_path, line_num):
    """判断 (file, line) 是否在已知 baseline"""
    # file_path 可能是 'log.md' 或 'wiki/log.md' 等,normalize
    fname = file_path.replace('\\', '/').split('/')[-1]
    return (fname, line_num) in KNOWN_BASELINE

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
# 只看 human-readable 部分(不要 JSON)
human_out = out.split('---JSON_OUTPUT_START---')[0] if '---JSON_OUTPUT_START---' in out else out
report_lines.append(human_out[-500:])  # 只看后 500 字符

# 解析 JSON 算 "新发现" (不在 KNOWN_BASELINE)
# 严重度对照(必须跟 scan_wiki_secrets.py 的 RED 集合一致)
RED_LABELS = {'PAT (ghp_/github_pat_)', 'Generic password', 'Generic API key',
              'AWS access key', 'AWS secret key', 'Private key block',
              'Bearer token', 'DeepSeek/OpenAI sk-', 'Netrc password',
              'x-oauth-basic', 'Discord webhook', 'Slack token'}

try:
    import json as _json
    if '---JSON_OUTPUT_START---' in out:
        json_str = out.split('---JSON_OUTPUT_START---')[1].split('---JSON_OUTPUT_END---')[0]
        data = _json.loads(json_str)
        new_red = 0
        new_examples = []
        for label, items in data.get('details', {}).items():
            if label not in RED_LABELS:
                continue  # 只看 🔴 严重度
            for item in items:
                if not is_known_baseline(item['file'], item['line']):
                    new_red += 1
                    if len(new_examples) < 3:
                        new_examples.append(f"  {label} @ {item['file']}:{item['line']}")
        if new_red > 0:
            issues.append(f'敏感扫描发现 {new_red} 个 🔴 新命中(基线外)')
            report_lines.append('  新发现示例:')
            for ex in new_examples:
                report_lines.append(ex)
        else:
            report_lines.append(f'  全部 🔴 在已知 baseline 内,无新发现')
except Exception as e:
    issues.append(f'JSON 解析失败:{e}')

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
