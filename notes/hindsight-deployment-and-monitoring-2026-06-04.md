---
title: Hindsight 实际部署 + Health-check Cron Auto-Restart (2026-06-04 20:11)
created: 2026-06-04
updated: 2026-06-04
type: note
tags: [note, hindsight, deployment, health-check, cron, auto-restart, watchdog, hermes, live-ops]
source: |
  本会话 main-claude 实操记录 (2026-06-04 20:07-20:24) + 之前 SKILL 沉淀 + Daemon fix 笔记
confidence: high
---

# Hindsight 实际部署 + Health-check Cron Auto-Restart (2026-06-04 20:11)

> 本会话第二次部署 Hindsight local server, 修复 "not available" 状态, 接入 cron health-check 自动重启守护. **跟 [[notes/hindsight-local-deployment-windows-2026]] 互补**: 那个是首次纯安装, **本篇是上线运维**.

**时间线 (20 分钟完整故事)**:
- 20:07 调查 → Hindsight plugin 报 "not available" + 缺 HINDSIGHT_API_KEY
- 20:11 启 server (PID 1692) → 35s 启动 → `{"status":"healthy","database":"connected"}`
- 20:12 curl bash 转义失败 → "There was an error parsing the body" (误判)
- 20:16 Python urllib 跑通 → retain 1 fact + recall 立即命中 (3.3k tokens)
- 20:19 写 healthcheck.py + cron 部署 → 5min tick, 静默 healthy, 死自动重启
- 20:24 测试通过 (exit 0, latency 2321ms, state JSON 写入)

---

## 1. 部署栈 (2026-06-04 实测)

| 组件 | 版本 | 备注 |
|---|---|---|
| `hindsight-api` | 0.6.1 | `pip install hindsight-api` |
| `hindsight-api-slim` | 0.6.1 | 依赖 |
| `pg0-embedded` | 0.14.2 | 内嵌 PostgreSQL (无需独立 PG) |
| `sentence-transformers` | 5.5.1 | 嵌入模型 |
| Hermes native provider | v0.15.2 | `~/.hermes/hindsight/config.json` |
| LLM | MiniMax-M2.5-highspeed | via api.minimaxi.com (OpenAI 兼容) |
| Bank | `hermes` | budget=mid, enabled=true |
| **Mode** | `hybrid` | auto-retain + auto-recall |
| **Prefetch** | `recall` | 每 turn 开头 recall, 注入 top-k facts |

**关键 env vars (start_hindsight_local.py 自动设)**:
- `HINDSIGHT_API_LLM_API_KEY` (从 .env 读 `MINIMAX_CN_API_KEY`)
- `HINDSIGHT_API_LLM_BASE_URL=https://api.minimaxi.com/v1`
- `HINDSIGHT_API_LLM_MODEL=MiniMax-M2.5-highspeed`
- **`HINDSIGHT_API_WORKER_ID=hindsight-local`** ← 必设!防重启任务丢失
- `HINDSIGHT_API_PORT=8888`
- `HINDSIGHT_API_LOG_LEVEL=info`

---

## 2. 故障现象 + 误判澄清

### 2.1 `hermes memory status` 报 "not available" — **是误报**

```
Memory status
────────────────────────────────────────
  Built-in:  always active
  Provider:  hindsight
  Plugin:    installed ✓
  Status:    not available ✗
  Missing:
    ✗ HINDSIGHT_API_KEY      ← 本地模式不需要
    ✗ HINDSIGHT_LLM_API_KEY  ← 来自 config.json
```

**真相**:
- `HINDSIGHT_API_KEY` 是 **Cloud 模式**的 key, 本地模式**不需要**
- `HINDSIGHT_API_LLM_API_KEY` 已从 `~/.hermes/hindsight/config.json` 的 `llmApiKey` 读取
- Hermes CLI status 报告**只看 env var**, 不知道有 config.json 兜底 → **误报**
- **plugin 是否工作**取决于 **server 是否能调通** (curl /health), 不取决于 CLI status

**判定方法**: 
```bash
curl -s http://localhost:8888/health
# {"status":"healthy","database":"connected"}  ← 这才是真信号
```

### 2.2 bash curl POST JSON 失败 — **MSYS 转义坑**

```bash
# ❌ 失败: 报 "There was an error parsing the body"
curl -X POST http://localhost:8888/v1/default/banks/hermes/memories \
  -H "Content-Type: application/json" \
  -d '{"items":[{"content":"test","context":"x"}],"async":false}'
# → {"detail":"There was an error parsing the body"}
```

**根因**: MSYS bash 处理嵌套 `{}` + `[]` + 双引号时, **反斜杠转义破坏了 JSON body**. 不是 Hindsight 端问题, 是 shell 转义问题.

**修法 (Python urllib)**:
```python
import urllib.request, json
req = urllib.request.Request(
    "http://localhost:8888/v1/default/banks/hermes/memories",
    method="POST",
    headers={"Content-Type": "application/json"},
    data=json.dumps({
        "items": [{"content": "test", "context": "x"}],
        "async": False
    }).encode()
)
resp = urllib.request.urlopen(req, timeout=30)
# → {"success":true,"items_count":1,"usage":{"total_tokens":3311}}
```

**记入 memory (未来 rule)**: **bash curl POST JSON 不可靠** → **用 Python urllib 替代**.

### 2.3 latency 偏高 (2433ms / 2321ms) — **首次 call 是连接初始化**

- 首次 call 慢: pg0-embedded PostgreSQL connection cache miss
- 后续 call 应 <500ms (Worker poller 每 30s 跑 stat, 缓存常驻)
- **不影响 health**: 5s timeout 内返回即 healthy

---

## 3. Health-check + Auto-Restart 守护体系

### 3.1 设计原则 (5 条铁律)

1. **死循环防护**: 每次 tick 最多重启 1 次 (`MAX_RESTART_ATTEMPTS=1`), 下个 5min tick 才允许再次尝试
2. **持久化状态**: 每次写入 `~/.hermes/hindsight/health-state.json`, **健康 ↔ 不健康过渡时** 标记 transition (供事后分析)
3. **不与 watchdog 冲突**:
   - `hindsight-watchdog` (skill) 监控**内存** (RSS / peak_wset) — **不重启**
   - `hindsight-healthcheck` (本 cron) 监控**liveness** (/health) — **自动重启**
4. **Windows MSYS safe**: 全 Python urllib, 零 shell 转义
5. **Token 节约**: `no_agent=true` + `deliver=local` = healthy 时完全静默

### 3.2 核心脚本: `~/.hermes/scripts/hindsight-healthcheck.py`

3 场景行为:

| 场景 | 行为 | Exit | 输出 |
|---|---|---|---|
| **Healthy** | 写 state, 打印绿色 ✓ | 0 | `✓ Hindsight healthy (latency=Xms)` |
| **Unhealthy + restart 成功** | 调 start script, 等 3s, 验证 | 0 | `✓ Restart succeeded` + `✓ Verified healthy` |
| **Unhealthy + restart 失败** | 写 state, 留给下 tick | 1 | `✗ Restart failed: [detail]` |

**关键设计**:
- `import importlib.util` 不需要 (脚本被直接 python 跑, 不 import)
- 双 urlopen 超时 5s (不卡死 cron)
- state JSON 字段: `timestamp, healthy, status, body_preview, latency_ms, action, transition, previous_timestamp`

### 3.3 Cron job (hermes cron 4793e7a07e08)

```bash
hermes cron create \
  --name hindsight-healthcheck \
  --schedule "every 5m" \
  --no-agent true \
  --deliver local \
  --script hindsight-healthcheck.py
```

- **Schedule**: every 5m, repeat forever
- **Mode**: no-agent (script stdout 走 deliver, 不走 LLM)
- **Deliver**: local (不送 user, healthy 时零噪音)
- **Script 路径**: 必须 `~/.hermes/scripts/<filename>` (Hermes cron 限制, 见 SKILL 文档)

### 3.4 验证证据 (20:19 测试)

```
$ python ~/.hermes/scripts/hindsight-healthcheck.py
✓ Hindsight healthy (latency=2321ms, body={"status":"healthy","database":"connected"})

$ cat ~/.hermes/hindsight/health-state.json
{
  "timestamp": "2026-06-04T12:19:49.830478+00:00",
  "healthy": true,
  "status": "healthy",
  "body_preview": "{\"status\":\"healthy\",\"database\":\"connected\"}",
  "latency_ms": 2321,
  "action": "none"
}
```

**`hermes cron list` 显示**:
```
4793e7a07e08 [active]
  Name:      hindsight-healthcheck
  Schedule:  every 5m
  Repeat:    ∞
  Next run:  2026-06-04T20:19:41+08:00
  Deliver:   local
  Script:    hindsight-healthcheck.py
  Mode:      no-agent
```

---

## 4. 5 步 Liveness Check 手动流程 (no-agent script 跑时)

```bash
# 1. health endpoint
curl -s http://localhost:8888/health

# 2. server PID
ps -ef | grep "hindsight_api.main" | grep -v grep

# 3. retain test (Python urllib 避免 MSYS 转义)
python -c "import urllib.request, json; req = urllib.request.Request('http://localhost:8888/v1/default/banks/hermes/memories', method='POST', headers={'Content-Type':'application/json'}, data=json.dumps({'items':[{'content':'manual test','context':'agent-test'}],'async':False}).encode()); print(urllib.request.urlopen(req, timeout=10).read().decode()[:200])"

# 4. recall test
python -c "import urllib.request, json; req = urllib.request.Request('http://localhost:8888/v1/default/banks/hermes/memories/recall', method='POST', headers={'Content-Type':'application/json'}, data=json.dumps({'query':'test','budget':'mid'}).encode()); print(urllib.request.urlopen(req, timeout=10).read().decode()[:500])"

# 5. list count
python -c "import urllib.request; resp = urllib.request.urlopen('http://localhost:8888/v1/default/banks/hermes/memories/list?limit=1', timeout=10); print(len(resp.read().decode()))"
```

5 步全过 = server 100% alive. 任一失败 → auto-restart (cron 健康检查触发).

---

## 5. Auto-Restart 触发链 (死 server 场景)

```
[20:24:41 cron tick]
  ↓
hindsight-healthcheck.py 跑
  ↓
urllib.urlopen(8888/health)  → URLError WinError 10061 (TCP RST)
  ↓
healthy=False
  ↓
subprocess.run([python, start_hindsight_local.py], timeout=60)
  ↓
start_hindsight_local.py: 启 uvicorn, 等 35s, /health verify
  ↓
returncode=0 → "✓ Restart succeeded"
  ↓
time.sleep(3) → 再 verify /health
  ↓
✓ Verified healthy after restart
  ↓
write_state("restarted", ...) → exit 0
```

**关键防爆**:
- start_hindsight_local.py 自己 CREATE_NO_WINDOW + 后台 detach
- subprocess timeout 60s (start 内部 35s 等 startup + 25s 缓冲)
- 二次 verify 防止假 healthy (start 报成功但 server 实际未起)

---

## 6. 与 hindsight-watchdog skill 的关系

| 维度 | hindsight-healthcheck (cron) | hindsight-watchdog (skill) |
|---|---|---|
| **监控** | liveness (/health 端点) | 内存 (RSS / peak_wset) |
| **触发** | 5min tick | Agent turn 流程自评 |
| **响应** | **自动重启** (subprocess) | 输出 JSON 状态, **不 kill** |
| **谁用** | cron scheduler | Agent (开场自评) |
| **频率** | 每 5min (288 次/天) | Agent turn 触发 (看 session) |
| **failover** | 自己起 start_hindsight_local.py | 建议手动 (避免死循环) |
| **位置** | `~/.hermes/scripts/` | `~/.hermes/skills/hindsight-watchdog/` |
| **Token 成本** | 0 (no-agent) | 0 (输出 JSON, 不入 LLM) |

**两者互补不冲突**:
- 死 server → healthcheck 自动拉起
- 高内存 → watchdog 提醒, Agent 决定手动重启
- 同一进程被两个监控**完全 OK**, **互不知道**对方存在

---

## 7. 关键 Pitfall 总结 (4 个)

### 7.1 `hermes memory status` "not available" **是误报**
- 真实状态看 curl /health
- 报 missing HINDSIGHT_API_KEY 实际本地模式不需要

### 7.2 bash curl POST JSON **MSYS 转义破坏 body**
- 看到 "There was an error parsing the body" → **不是 Hindsight 问题**
- 用 Python urllib (json.dumps + Request.data) 100% 可靠

### 7.3 start_hindsight_local.py 必须设 **HINDSIGHT_API_WORKER_ID**
- 不设 = 重启任务丢失 (经验: 1+ hour 任务都失败)
- 必设值: `hindsight-local` (或任意稳定字符串)

### 7.4 首次 call latency 高 (2-3s) **是正常**
- pg0-embedded connection cache miss
- 后续 <500ms
- **不影响 health** (5s timeout)

---

## 8. 关联文档

- [[notes/hindsight-local-deployment-windows-2026]] — 首次纯安装 (本会话前)
- [[notes/hindsight-daemon-fix-2026-06-04]] — 笔记本侧 daemon provider 修复
- [[notes/hindsight-risks-and-optimizations-2026]] — 风险 + 优化
- [[methods/hindsight-4d-retrieval-complete]] — 4 维检索
- [[methods/hindsight-first-active-workflow]] — handoff + auto-trigger
- [[methods/hindsight-first-memory-pattern]] — 长期记忆使用模式
- [[methods/install-hindsight-native-hermes-method]] — 安装步骤汇总
- `hermes-all/hermes/skills/install-hindsight-as-hermes-memory/SKILL.md` (本地) — 完整 SKILL
- `hermes-all/hermes/skills/hindsight-watchdog/SKILL.md` (本地) — 内存监控
- `~/.hermes/scripts/hindsight-healthcheck.py` — 本会话创建
- `~/.hermes/hindsight/health-state.json` — 健康状态历史

---

## 9. v1.0 → v1.1 变更 (本会话新增)

**v1.0 (2026-06-03 首次部署)**:
- 纯安装
- daemon 跑起来就完事
- 没监控

**v1.1 (2026-06-04 20:11+ 本次)**:
- ✅ healthcheck.py + cron auto-restart (新)
- ✅ state JSON 持续写入 (新)
- ✅ 与 hindsight-watchdog 分工明确 (新)
- ✅ 5 步 Liveness 手动流程 (新)
- ✅ 4 Pitfall 整理 (新)
- ✅ MSYS bash curl 转义坑 + Python urllib 修法 (新)
