import os, re, sys
from pathlib import Path

WIKI = Path(sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Administrator\hermes-all\wiki')
os.chdir(WIKI)

SKIP = {'.git', '.obsidian', '.trash', '_archive', 'node_modules', '__pycache__', '_drafts', 'raw', 'scripts', 'agents/ai-harness-exploration'}

# Use plain strings; construct regex with chr(92) for backslash if needed.
BS = chr(92)  # single backslash

PATTERNS = {
    'PAT (ghp_/github_pat_)':   r'gh[ps]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}',
    'Generic password':         r'(?i)password\s*[:=]\s*["\']?[A-Za-z0-9!@#$%^&*()_+\-]{6,}',
    'Generic API key':          r'(?i)(api[_-]?key|apikey|secret[_-]?key|secret)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{16,}',
    'AWS access key':           r'AKIA[0-9A-Z]{16}',
    'AWS secret key':           r'(?i)aws[_-]?secret[_-]?access[_-]?key',
    'Private key block':        r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
    'Bearer token':             r'Bearer\s+[A-Za-z0-9_\-\.=]{20,}',
    'Email (real-looking)':     r'\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b',
    'Private IP':               r'\b(?:10|127|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    'Localhost URL':            r'localhost:\d+|127\.0\.0\.1:\d+',
    'Windows path C:Users':     r'C:\\Users\\Administrator',
    'DeepSeek/OpenAI sk-':      r'sk-[A-Za-z0-9]{20,}',
    'Hindsight env var':        r'HINDSIGHT_API_KEY',
    'Hindsight local port':     r'localhost:?\s*8888',
    'Netrc password':           r'machine\s+github\.com\s+login\s+\S+\s+password',
    'x-oauth-basic':            r'x-oauth-basic',
    'Discord webhook':          r'https://(?:discord(?:app)?\.com|canary\.discord\.com)/api/webhooks/',
    'Slack token':              r'xox[bpars]-[A-Za-z0-9-]{10,}',
}

# Severity map
RED = {'PAT (ghp_/github_pat_)', 'Generic password', 'Generic API key',
       'AWS access key', 'AWS secret key', 'Private key block',
       'Bearer token', 'DeepSeek/OpenAI sk-', 'Netrc password',
       'x-oauth-basic', 'Discord webhook', 'Slack token'}
YEL = {'Hindsight env var', 'Email (real-looking)', 'Private IP',
       'Localhost URL', 'Windows path C:Users', 'Hindsight local port'}

hits = {}
count_files = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        if not f.endswith(('.md', '.py', '.sh', '.yaml', '.yml', '.json', '.txt', '.toml', '.cfg', '.ini')):
            continue
        path = Path(root) / f
        count_files += 1
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for line_num, line in enumerate(content.splitlines(), 1):
            for label, pat in PATTERNS.items():
                m = re.search(pat, line)
                if m:
                    hits.setdefault(label, []).append((str(path), line_num, m.group(0), line.strip()[:160]))

print(f'扫了 {count_files} 文件\n')
print('='*72)
print('命中汇总(严重度=🔴 真敏感 / 🟡 边界 / 🟢 低)')
print('='*72)
total_red, total_yel = 0, 0
for label, results in sorted(hits.items(), key=lambda x: -len(x[1])):
    n = len(results)
    if label in RED:
        sev = '🔴'; total_red += n
    elif label in YEL:
        sev = '🟡'; total_yel += n
    else:
        sev = '🟢'
    print(f'\n{sev} {label}: {n} 处')
    for r in results[:6]:
        path, ln, matched, content = r
        print(f'  {path}:{ln}  match="{matched[:50]}"')
        print(f'    → {content[:130]}')
    if n > 6:
        print(f'  ... +{n-6} more')

print(f'\n{"="*72}')
print(f'总计: {sum(len(v) for v in hits.values())} 处命中 / 🔴 {total_red} 严重 / 🟡 {total_yel} 边界 / {len(hits)} 种模式')

# === 2026-06-04 加 JSON 输出(给 daily_maintain.py 用)===
import json
output = {
    'files_scanned': count_files,
    'total': sum(len(v) for v in hits.values()),
    'red': total_red,
    'yellow': total_yel,
    'patterns': len(hits),
    'details': {label: [{'file': f, 'line': ln, 'match': m[:80], 'context': c[:160]}
                          for f, ln, m, c in results]
                for label, results in hits.items()}
}
print('---JSON_OUTPUT_START---')
print(json.dumps(output, ensure_ascii=False, indent=2))
print('---JSON_OUTPUT_END---')
