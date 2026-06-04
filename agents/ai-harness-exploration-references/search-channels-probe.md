---
title: Search Channels Probe — 11 通道实测脚本
created: 2026-06-04
updated: 2026-06-04
type: script
tags: [search, probe, channels, fallback, mcp, tavily, duckduckgo, monthly-cron]
source: ai-harness-exploration-v6.13.0
confidence: high
---

# Search Channels Probe — 11 通道实测脚本

> **目的**:每月 1 号(配额重置后)自动跑一次,确认所有搜索通道的实际可用性。
> **来源**:ai-harness-exploration § 9.0.7 实测脚本(2026-06-04 沉淀)
> **使用方式**:Agent 跑此脚本 → 输出 JSON 状态 → 写入 `wiki/log.md`

## 1. 实测脚本(完整版)

```python
"""
search_channels_probe.py — 验证当前环境所有搜索通道的实际可用性

跑法:  在 execute_code 或 terminal 中直接跑
预期:  输出 JSON, 标记 ✅/❌/🟡

历史案例(2026-06-04 14:00):
  - mcp_minimax_web_search → ✅ 10 organic results
  - mcp_tavily_mcp_google → ✅ 3 results
  - mcp_tavily_mcp_microsoft → ✅ 3 results
  - mcp_tavily_mcp_ggc → ✅ 3 results
  - web_search (Hermes REST) → ❌ Tavily 401
  - curl GitHub raw → ✅ 200, 5.8KB
  - curl arXiv → ✅ 200, 1.6KB
  - curl Bing + UA + -L → ✅ 200, 115KB
  - curl DuckDuckGo + UA + 短 timeout → ✅ 200, 30KB
  - curl Wikipedia → ❌ 国内 000
"""
import json
import time
import subprocess

results = {}

# 1. MCP channels (通过 Hermes tools)
# 这部分需要 Agent 实际调用工具,以下是结果格式示例
mcp_results = {
    "mcp_minimax_web_search": {"status": "unknown", "note": "需要 Agent 调工具验证"},
    "mcp_tavily_mcp_google": {"status": "unknown", "note": "需要 Agent 调工具验证"},
    "mcp_tavily_mcp_microsoft": {"status": "unknown", "note": "需要 Agent 调工具验证"},
    "mcp_tavily_mcp_ggc": {"status": "unknown", "note": "需要 Agent 调工具验证"},
    "web_search": {"status": "unknown", "note": "需要 Agent 调工具验证"},
}

# 2. terminal curl channels (可静态跑)
import httpx

terminal_checks = [
    ("github_raw", "https://raw.githubusercontent.com/anthropics/anthropic-cookbook/main/README.md", 10),
    ("arxiv", "https://export.arxiv.org/api/query?search_query=ai&max_results=1", 10),
    ("bing_with_ua", "https://www.bing.com/search?q=test+probe", 15),
    ("duckduckgo_with_ua", "https://html.duckduckgo.com/html/?q=test+probe", 8),
    ("wikipedia", "https://en.wikipedia.org/api/rest_v1/page/summary/Python_(programming_language)", 10),
    ("github_search", "https://api.github.com/search/repositories?q=hermes", 10),
]

terminal_results = {}
for name, url, timeout in terminal_checks:
    t0 = time.time()
    try:
        is_duckduckgo = "duckduckgo" in name
        r = httpx.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            follow_redirects=True,
            timeout=timeout,
        )
        latency = round((time.time() - t0) * 1000)
        if r.status_code == 200:
            terminal_results[name] = {
                "status": "✅ OK",
                "status_code": r.status_code,
                "size_bytes": len(r.content),
                "latency_ms": latency,
            }
        else:
            terminal_results[name] = {
                "status": f"⚠️ {r.status_code}",
                "status_code": r.status_code,
                "latency_ms": latency,
            }
    except httpx.TimeoutException:
        terminal_results[name] = {"status": "❌ timeout", "timeout_s": timeout}
    except Exception as e:
        terminal_results[name] = {"status": f"❌ {type(e).__name__}", "error": str(e)[:100]}

# 3. 合并
results = {"mcp_channels_placeholder": mcp_results, "terminal_channels": terminal_results}

# 4. 摘要
ok_count = sum(1 for r in terminal_results.values() if "✅" in r.get("status", ""))
fail_count = sum(1 for r in terminal_results.values() if "❌" in r.get("status", ""))
print(f"\n=== Search Channels Probe Summary ===")
print(f"  OK: {ok_count}/{len(terminal_results)}")
print(f"  Fail: {fail_count}/{len(terminal_results)}")
print(f"  Full: {json.dumps(results, indent=2, ensure_ascii=False)}")
```

## 2. Hermes 内运行版(用工具直接调)

```python
# 在 execute_code 里,直接调 MCP 工具
from datetime import datetime
import json

probe_log = {
    "timestamp": datetime.now().isoformat(),
    "channels": {},
}

# 测 1: mcp_minimax_web_search (5 个独立查询,各取 1 个结果)
try:
    # 通过 Hermes 工具调用(实际由 Agent 在 execute_code 中)
    r = mcp_minimax_web_search(query="test probe search")
    probe_log["channels"]["mcp_minimax_web_search"] = {
        "status": "✅ OK" if r.get("organic") else "❌ empty",
        "results_count": len(r.get("organic", [])),
    }
except Exception as e:
    probe_log["channels"]["mcp_minimax_web_search"] = {"status": f"❌ {type(e).__name__}", "error": str(e)[:100]}

# 测 2-4: Tavily MCP×3
for name, fn in [
    ("mcp_tavily_mcp_google", mcp_tavily_mcp_google_tavily_search),
    ("mcp_tavily_mcp_microsoft", mcp_tavily_mcp_microsoft_tavily_search),
    ("mcp_tavily_mcp_ggc", mcp_tavily_mcp_ggc_tavily_search),
]:
    try:
        r = fn(query="test probe", max_results=3, search_depth="basic")
        cnt = len(r.get("results", []))
        probe_log["channels"][name] = {"status": "✅ OK" if cnt else "❌ empty", "results_count": cnt}
    except Exception as e:
        probe_log["channels"][name] = {"status": f"❌ {type(e).__name__}", "error": str(e)[:100]}

# 测 5: web_search (Tavily REST)
try:
    r = web_search(query="test probe", limit=3)
    probe_log["channels"]["web_search"] = {"status": "✅ OK" if r.get("success") else f"❌ {r.get('error', 'unknown')[:50]}"}
except Exception as e:
    probe_log["channels"]["web_search"] = {"status": f"❌ {type(e).__name__}", "error": str(e)[:100]}

# 测 6-9: terminal curl(直接 httpx)
import httpx
for name, url, timeout in [
    ("github_raw", "https://raw.githubusercontent.com/anthropics/anthropic-cookbook/main/README.md", 10),
    ("arxiv", "https://export.arxiv.org/api/query?search_query=ai&max_results=1", 10),
    ("bing_with_ua", "https://www.bing.com/search?q=test+probe", 15),
    ("duckduckgo_with_ua", "https://html.duckduckgo.com/html/?q=test+probe", 8),
]:
    try:
        r = httpx.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            follow_redirects=True,
            timeout=timeout,
        )
        probe_log["channels"][name] = {
            "status": "✅ OK" if r.status_code == 200 else f"⚠️ {r.status_code}",
            "size_bytes": len(r.content) if r.status_code == 200 else 0,
        }
    except Exception as e:
        probe_log["channels"][name] = {"status": f"❌ {type(e).__name__}"}

# 输出
print(json.dumps(probe_log, indent=2, ensure_ascii=False))

# 写 log.md
import os
log_path = os.path.expanduser("~/hermes-all/wiki/log.md")
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"\n## [Search Channels Probe - {probe_log['timestamp']}]\n```json\n{json.dumps(probe_log, indent=2, ensure_ascii=False)}\n```\n\n")
```

## 3. 自动化:cron 每月 1 号跑

> 配 `~/.hermes-all/hermes/cron/search-channels-probe.json` 或加到 `kanban-cronjobs.py`:

```json
{
  "name": "search-channels-monthly-probe",
  "schedule": "0 0 1 * *",
  "prompt": "Run search channels probe. Read references/search-channels-probe.md in ai-harness-exploration skill. Execute the Hermes version, write results to wiki/log.md, and report any channel status changes from last month.",
  "skills": ["ai-harness-exploration"]
}
```

## 4. 结果解读

| 状态 | 含义 | 行动 |
|---|---|---|
| ✅ OK | 通道正常 | 无 |
| ❌ 401/403 | 鉴权失败 | 检查 API key 配置 |
| ❌ 432 | 配额耗尽 | 等下月重置,或换通道 |
| ❌ timeout | 不可达 | 改 UA + 短 timeout 重试,失败则换通道 |
| ⚠️ 30x | 重定向 | 加 `follow_redirects=True` |
| ❌ empty | 无结果 | 换关键词或换通道 |

## 5. 历史结果(2026-06-04)

```json
{
  "timestamp": "2026-06-04T14:00:00",
  "channels": {
    "mcp_minimax_web_search": "✅ 10 results",
    "mcp_tavily_mcp_google": "✅ 3 results (0.82s)",
    "mcp_tavily_mcp_microsoft": "✅ 3 results (0.78s)",
    "mcp_tavily_mcp_ggc": "✅ 3 results (1.05s)",
    "web_search": "❌ Tavily 401 Unauthorized",
    "github_raw": "✅ 200 (5.8KB)",
    "arxiv": "✅ 200 (1.6KB)",
    "bing_with_ua": "✅ 200 (115KB)",
    "duckduckgo_with_ua": "✅ 200 (30KB)"
  }
}
```

## 6. 关联

- SKILL § 9.0 实际可用搜索通道(主文档)
- SKILL § 9.0.2 fallback 决策树
- SKILL § 9.0.6 历史教训
- SKILL § 9.0.7 自检脚本(本文件是扩展版)
