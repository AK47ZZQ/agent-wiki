---
title: Hindsight Health-Monitoring 协议 (liveness + auto-restart)
created: 2026-06-04
updated: 2026-06-04
type: method
tags: [method, hindsight, health-check, auto-restart, cron, watchdog, liveness, hermes, multi-agent]
sources:
  - local: ~/.hermes/scripts/hindsight-healthcheck.py
  - local: hermes-all/hermes/skills/install-hindsight-as-hermes-memory/SKILL.md
  - local: hermes-all/hermes/skills/hindsight-watchdog/SKILL.md
  - notes/hindsight-deployment-and-monitoring-2026-06-04.md
  - https://hindsight.vectorize.io/developer/api/quickstart
confidence: high
---

# Hindsight Health-Monitoring 协议 (liveness + auto-restart)

> **3rd 笔记本 + 未来 agent 复用方法**。本协议在 2026-06-04 20:11 main-claude 实测通过, 设计目标 = **不烧 token** + **不与 watchdog 冲突** + **死 server 60s 内自动拉起**。

**适用场景**:
- 单机 Hindsight local server 长跑 (Hermes native provider 模式)
- 多 Agent 共用 Hindsight bank (任何节点死了, cron 5min 内拉起)
- Windows + MSYS bash + Python 3.14
- 数据主权: 数据全本地 (PostgreSQL embedded)

**不适用**:
- Cloud Hindsight (`api.hindsight.vectorize.io`) → server 不可控
- Docker Hindsight → 已有 Docker healthcheck 机制
- 短期 dev (跑完即关) → 浪费监控

---

## 1. 协议 3 原则 (铁律)

### 1.1 不依赖单一信号

判断 Hindsight alive 必须**多信号交叉验证**:
1. **HTTP /health 200** (liveness)
2. **PID alive** (`ps -ef` / `tasklist`)
3. **Retain/Recall API 200** (功能性)
4. **bank facts 可读** (持久化)

**任一失败即 unhealthy** → 触发 auto-restart。

### 1.2 死循环防护

| 设置 | 值 | 原因 |
|---|---|---|
| `MAX_RESTART_ATTEMPTS` | 1 / tick | 防止反复 kill + start |
| Tick 间隔 | 5 min | 给 server 留 5min 健康时间 |
| **Restart 验证** | 必须 /health 200 才算成功 | 防假成功 |
| 失败 fallback | 留 5min 后再试 | 不 panic |

### 1.3 Token 零消耗

- **`no_agent=true`**: script 跑不调 LLM
- **`deliver=local`**: stdout 不送 user
- **Healthy 时** 完全静默 (无 cron output)
- **Unhealthy 时** 只写入 state JSON, 可选 IM 通知

---

## 2. 部署步骤 (4 步可复用)

### Step 1: 装 Hindsight local server (前置)

参考 [[methods/install-hindsight-native-hermes-method]] 完整流程。
本协议**假定** server 已跑在 `http://localhost:8888`, `bank=hermes`。

**最小验证**:
```bash
curl -s http://localhost:8888/health
# {"status":"healthy","database":"connected"}
```

### Step 2: 写 healthcheck 脚本

**位置**: `~/.hermes/scripts/hindsight-healthcheck.py` (~/.hermes/scripts 与 hermes-all/hermes/scripts 是同一目录)

**核心逻辑** (Python urllib 避免 MSYS 转义):
```python
import urllib.request, subprocess, sys, time, json
from pathlib import Path

HINDSIGHT_URL = "http://localhost:8888/health"
START_SCRIPT = Path(r"C:\Users\Administrator\hermes-all\hermes\skills\install-hindsight-as-hermes-memory\scripts\start_hindsight_local.py")
STATE_FILE = Path.home() / ".hermes" / "hindsight" / "health-state.json"
HEALTH_TIMEOUT = 5
MAX_RESTART_ATTEMPTS = 1

def check_health():
    start = time.time()
    try:
        req = urllib.request.Request(HINDSIGHT_URL, method="GET")
        with urllib.request.urlopen(req, timeout=HEALTH_TIMEOUT) as resp:
            return "healthy" in resp.read().decode().lower(), resp.read().decode()[:200], int((time.time()-start)*1000)
    except Exception as e:
        return False, f"{type(e).__name__}: {e}", -1

def restart_server():
    if not START_SCRIPT.exists():
        return False, f"Start script not found: {START_SCRIPT}"
    try:
        r = subprocess.run(
            [sys.executable, str(START_SCRIPT)],
            capture_output=True, text=True, timeout=60,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        return r.returncode == 0, (r.stdout + r.stderr)[-300:]
    except subprocess.TimeoutExpired:
        return False, "Restart timeout (60s)"

def main():
    healthy, body, latency = check_health()
    if healthy:
        STATE_FILE.write_text(json.dumps({
            "timestamp": __import__('datetime').datetime.utcnow().isoformat() + "Z",
            "healthy": True, "latency_ms": latency, "action": "none"
        }, indent=2))
        return 0
    success, detail = restart_server()
    if success:
        time.sleep(3)
        if check_health()[0]:
            return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
```

### Step 3: 创建 cron job

```bash
hermes cron create \
  --name hindsight-healthcheck \
  --schedule "every 5m" \
  --no-agent true \
  --deliver local \
  --script hindsight-healthcheck.py
```

**关键参数**:
- `--no-agent true`: 不调 LLM, 直接走 deliver
- `--deliver local`: stdout 不送 user (healthy 静默)
- `--script`: 必须是 `~/.hermes/scripts/` 下的相对文件名

**验证**:
```bash
hermes cron list
# 4793e7a07e08 [active]
#   Name:      hindsight-healthcheck
#   Schedule:  every 5m
#   Deliver:   local
#   Script:    hindsight-healthcheck.py
#   Mode:      no-agent
```

### Step 4: 验证监控体系

**手动跑一次**:
```bash
python ~/.hermes/scripts/hindsight-healthcheck.py
# 预期: ✓ Hindsight healthy (latency=Xms), exit 0
```

**检查 state file**:
```bash
cat ~/.hermes/hindsight/health-state.json
# {"timestamp": "...", "healthy": true, "latency_ms": X, "action": "none"}
```

**等下一个 tick (≤ 5 min)**:
- `hermes cron list` 显示 `last_run_at` 更新
- `~/.hermes/hindsight/health-state.json` `timestamp` 推进

---

## 3. 多 Agent 复用模式

### 3.1 同台双实例 (不推荐, 但支持)

如果一台机跑 2 个 Hindsight (port 8888 + 8889):
- 复制脚本: `hindsight-healthcheck-8888.py` + `hindsight-healthcheck-8889.py`
- 改 `HINDSIGHT_URL` 各自 port
- 创建 2 个 cron job

### 3.2 跨机多节点 (推荐, wiki 协作标配)

**每台 Hermes 笔记本** 独立装本协议:
- main-claude (台式 Windows) → healthcheck 跑 server PID 1692
- hermes-3rd (笔记本) → healthcheck 跑 笔记本 server PID XXXX
- 未来 agent → 同款

**跨机不冲突** 因为:
- 每台 server 独立 PID + port 8888
- bank 可同名 (hermes) 但**数据物理隔离** (本地 PostgreSQL embedded)
- 跨机同步走 [[protocols/git-collaboration-multi-agent]] (wiki 仓库)

### 3.3 共享 health endpoint (高级)

如果未来要做 fleet 监控:
- 1 台机 / 1 容器聚合所有节点的 health
- 用 [[entities/mission-control]] 风格 dashboard
- **不在本协议 v1.0 范围**, 留作 v2.0

---

## 4. 与 hindsight-watchdog skill 关系

| 维度 | hindsight-healthcheck (本协议) | hindsight-watchdog (skill) |
|---|---|---|
| **监控目标** | liveness (/health 端点) | 内存 (RSS / peak_wset) |
| **触发方式** | cron 5min tick | Agent turn 流程自评 |
| **响应** | **自动重启** (subprocess) | 输出 JSON, **不 kill** (防死循环) |
| **谁用** | cron scheduler | Agent 自身 (开场自评) |
| **频率** | 288 次/天 | 每次 Agent turn |
| **位置** | `~/.hermes/scripts/` | `~/.hermes/skills/hindsight-watchdog/` |
| **Token 成本** | 0 (no-agent) | 0 (JSON 输出不入 LLM) |

**两者职责分离**:
- 死 server → healthcheck 自动拉起
- 内存泄漏 → watchdog 提醒, Agent 决定手动重启
- **绝不同时改同一进程** (避免竞态)

---

## 5. 异常场景 + 修复表

| 异常 | 表现 | 修复 |
|---|---|---|
| `URLError WinError 10061` (TCP RST) | healthcheck 报 unhealth | 自动 restart (设计内) |
| `URLError timeout` (5s 过) | healthcheck 报 unhealth | 自动 restart + start 失败手动 |
| `Restart timeout (60s)` | start_hindsight_local.py 死锁 | **不自动 retry**, 下 tick 再试 |
| `Start script not found` | 配置错位 | 改 START_SCRIPT 路径, manual run |
| `memory mode 跑偏` | recall 拿不到数据 | 不属本协议, 改 `~/.hermes/hindsight/config.json` |
| **Server 频繁死 (每小时)** | restart 多次 | **关 cron**, 查根因 (内存/资源/启动失败) |

---

## 6. 关闭 + 卸载协议

**暂停 cron**:
```bash
hermes cron pause 4793e7a07e08
```

**恢复**:
```bash
hermes cron resume 4793e7a07e08
```

**彻底删除**:
```bash
hermes cron remove 4793e7a07e08
# 同时: rm ~/.hermes/scripts/hindsight-healthcheck.py
# 同时: rm ~/.hermes/hindsight/health-state.json
```

**注意**: 删除 cron **不会停止 Hindsight server**, 仍跑。停 server 需手动:
```bash
taskkill /F /PID <PID>
# 或
ps -ef | grep hindsight_api.main | grep -v grep | awk '{print $2}' | xargs kill
```

---

## 7. 监控指标 + 告警 (v2.0 路线图)

当前 v1.0 只输出 state JSON, **不告警**。v2.0 计划加:

| 指标 | 阈值 | 告警方式 |
|---|---|---|
| restart_failed_count (24h) | ≥ 3 | 飞书 / 邮件 |
| latency_ms 持续 | > 3000 | 飞书 warning |
| memory 增长 | RSS > 1GB | 飞书 critical |
| server uptime | < 1h 后死 | Slack/IM |

**v2.0 不在本协议** 范围 — 跟 watchdog 共建即可。

---

## 8. 验证清单 (新节点复用)

- [ ] `pip show hindsight-api` → 0.6.1+
- [ ] `curl http://localhost:8888/health` → `{"status":"healthy",...}`
- [ ] `python ~/.hermes/scripts/hindsight-healthcheck.py` → exit 0
- [ ] `hermes cron list` → 看到 `hindsight-healthcheck` active
- [ ] `cat ~/.hermes/hindsight/health-state.json` → `healthy: true`
- [ ] 等 5min: `timestamp` 自动推进
- [ ] 故意 kill server: 5min 内自动 restart (测一次即可, 慎用)
- [ ] 恢复: 记录经验到本地 [[notes/hindsight-deployment-and-monitoring-2026-06-04]]

---

## 9. 关联文档

- [[notes/hindsight-deployment-and-monitoring-2026-06-04]] — 本次部署实战笔记 (本协议源)
- [[methods/install-hindsight-native-hermes-method]] — 完整安装流程 (前置依赖)
- [[notes/hindsight-local-deployment-windows-2026]] — Windows 部署细节
- [[notes/hindsight-risks-and-optimizations-2026]] — 风险 + 优化
- [[notes/hindsight-daemon-fix-2026-06-04]] — 笔记本侧 daemon 修复
- [[concepts/hindsight-in-hermes-ecosystem-2026]] — Hindsight 真实定位
- [[methods/hindsight-4d-retrieval-complete]] — 4 维检索
- [[protocols/git-collaboration-multi-agent]] — 多 Agent 协作
- `hermes-all/hermes/skills/install-hindsight-as-hermes-memory/SKILL.md` (本地)
- `hermes-all/hermes/skills/hindsight-watchdog/SKILL.md` (本地)
- `~/.hermes/scripts/hindsight-healthcheck.py` — 本协议核心脚本
- `~/.hermes/hindsight/health-state.json` — 状态持久化

---

## 10. 版本历史

- **v1.0 (2026-06-04 20:11)**:
  - ✅ healthcheck.py 4.8KB
  - ✅ cron 5min tick, no-agent, local deliver
  - ✅ 3 原则 (multi-signal / loop-safe / token-zero)
  - ✅ 4 步可复用 setup
  - ✅ 与 hindsight-watchdog 职责分离
  - ✅ 多 Agent 复用模式 (同台/跨机)
