---
title: Hindsight 主动化工作流（端到端执行手册）
created: 2026-06-02
updated: 2026-06-02
type: workflow
tags: [workflow, automation, cron, hindsight, memory, lcm]
sources:
  - local: ~/hermes-all/hermes/config.yaml
  - local: ~/hermes-all/hermes/scripts/
confidence: high
source: hindsight-deployment-2026-06
---

# Hindsight 主动化工作流

> 把 [[methods/hindsight-first-memory-pattern]] 落地为可执行脚本 + cron + 看门狗的完整工作流。

## 端到端架构

```
┌──────────────────────────────────────────────────────────────┐
│  触发层 (Trigger)                                             │
│  ├─ cron 23:00 nightly-retain (批量)                         │
│  ├─ cron 08:00 morning-reflect (拉今日上下文)                │
│  └─ turn 内 self-check (context_pct > 50% 触发)              │
├──────────────────────────────────────────────────────────────┤
│  写入层 (Retain)                                              │
│  ├─ hindsight_retain(bank_id="hermes", content=fact)         │
│  └─ pg0 embedded PostgreSQL (实体/关系/事实)                 │
├──────────────────────────────────────────────────────────────┤
│  读取层 (Reflect)                                             │
│  ├─ hindsight_reflect(bank_id="hermes", query=...)           │
│  └─ M3 LLM 合成结构化答案                                    │
├──────────────────────────────────────────────────────────────┤
│  存档层 (Archive)                                             │
│  ├─ lcm.db (完整 session 记录, 只写不读)                     │
│  └─ Git backup (auth.json/env/lcm.db)                        │
└──────────────────────────────────────────────────────────────┘
```

## 脚本 1: nightly-retain.py

**作用**：每晚 23:00 把当天 LCM session 摘要批量 retain 到 Hindsight。

**位置**：`~/hermes-all/hermes/scripts/hindsight-nightly-retain.py`

```python
"""Hindsight nightly retain: 把当天 LCM session 摘要批量入库。
输入: 当天 lcm.db 写入的 messages
处理: 提取"事实/偏好/教训"3 类, 丢弃对话流水
输出: hindsight_retain() 多次调用, 每次 1 个事实
"""
import os
import sys
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from dotenv import dotenv_values

# 加载 .env (Hindsight 不展开 ${VAR})
for k, v in dotenv_values(r"C:\Users\Administrator\hermes-all\hermes\.env").items():
    if v: os.environ[k] = v

# 输出 stdout 会被 cron 当作报告
def log(msg):
    print(f"[{datetime.now().isoformat()}] {msg}", flush=True)

def main():
    log("=== Hindsight nightly-retain started ===")

    # 1. 查当天 LCM session 列表
    lcm_db = r"C:\Users\Administrator\hermes-all\hermes\lcm.db"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log(f"Querying LCM sessions for {today}...")

    try:
        conn = sqlite3.connect(lcm_db)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        # 查当天有更新的 session (通过 lifecycle_updated_at)
        cur.execute("""
            SELECT DISTINCT current_session_id as sid
            FROM lcm_lifecycle_state
            WHERE DATE(updated_at, 'unixepoch') = DATE('now')
              AND current_session_id NOT LIKE 'cron%'
        """)
        sessions = [r["sid"] for r in cur.fetchall()]
        conn.close()
    except Exception as e:
        log(f"❌ LCM query failed: {e}")
        return 1

    log(f"Found {len(sessions)} sessions to process")

    if not sessions:
        log("No sessions to retain, exit 0")
        return 0

    # 2. 启 Hindsight server
    from hindsight import HindsightServer, HindsightClient
    server = HindsightServer(
        db_url="pg0",
        llm_provider=os.environ["HINDSIGHT_API_LLM_PROVIDER"],
        llm_api_key=os.environ["HINDSIGHT_LLM_API_KEY"],
        llm_model=os.environ["HINDSIGHT_API_LLM_MODEL"],
        llm_base_url=os.environ["HINDSIGHT_API_LLM_BASE_URL"],
    )
    server.start()
    client = HindsightClient(base_url=server.url)
    bank_id = os.environ.get("HINDSIGHT_BANK_ID", "hermes")

    # 3. 对每个 session: 提取事实 → retain
    total_retained = 0
    for sid in sessions:
        try:
            # 3.1 提取 session 消息文本 (从 LCM)
            facts = extract_facts_from_session(sid)
            log(f"  Session {sid[:16]}...: {len(facts)} facts extracted")

            # 3.2 逐条 retain
            for fact in facts:
                result = client.retain(bank_id=bank_id, content=fact)
                if result.success:
                    total_retained += 1
        except Exception as e:
            log(f"  ⚠ Session {sid[:16]} failed: {e}")
            continue

    log(f"=== Hindsight nightly-retain done: {total_retained} facts retained ===")
    return 0

def extract_facts_from_session(session_id: str) -> list[str]:
    """从 LCM session 提取 事实/偏好/教训 3 类事实。
    简化版: 直接把所有 user/assistant 消息打包成一个 retain 输入,
    让 Hindsight 的 LLM 自己抽取 (这是 retain 的设计意图)。
    """
    conn = sqlite3.connect(r"C:\Users\Administrator\hermes-all\hermes\lcm.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 查该 session 的所有 user + assistant 消息
    try:
        cur.execute("""
            SELECT role, content FROM messages
            WHERE session_id = ?
              AND role IN ('user', 'assistant')
              AND length(content) < 5000
            ORDER BY timestamp
            LIMIT 50
        """, (session_id,))
        rows = cur.fetchall()
    except Exception:
        conn.close()
        return []
    conn.close()

    # 合并成一个长文本 (Hindsight retain 会自动 LLM 抽取)
    combined = "\n\n".join([f"[{r['role']}] {r['content']}" for r in rows])
    if len(combined) > 10000:
        combined = combined[:10000]  # 截断避免 LLM 过长

    return [combined] if combined else []

if __name__ == "__main__":
    sys.exit(main())
```

## 脚本 2: morning-reflect.py (no_agent 风格)

**作用**：每天 08:00 拉出"今日该关注什么"，可作为人类早晨阅读摘要。

**位置**：`~/hermes-all/hermes/scripts/hindsight-morning-reflect.py`

```python
"""Hindsight morning reflect: 拉出近期用户关注 + 关键事实。
输出到 stdout (cron 当作报告投递)。
"""
import os
import sys
from dotenv import dotenv_values
from datetime import datetime

for k, v in dotenv_values(r"C:\Users\Administrator\hermes-all\hermes\.env").items():
    if v: os.environ[k] = v

def main():
    print(f"=== Hindsight morning reflect: {datetime.now().isoformat()} ===\n")

    from hindsight import HindsightServer, HindsightClient
    server = HindsightServer(
        db_url="pg0",
        llm_provider=os.environ["HINDSIGHT_API_LLM_PROVIDER"],
        llm_api_key=os.environ["HINDSIGHT_LLM_API_KEY"],
        llm_model=os.environ["HINDSIGHT_API_LLM_MODEL"],
        llm_base_url=os.environ["HINDSIGHT_API_LLM_BASE_URL"],
    )
    server.start()
    client = HindsightClient(base_url=server.url)
    bank_id = os.environ.get("HINDSIGHT_BANK_ID", "hermes")

    # 2 段查询: 项目状态 + 关键偏好
    queries = [
        ("当前在做的项目", "用户最近 7 天关注什么项目？进展如何？"),
        ("关键偏好与决策", "用户做过哪些架构决策？偏好什么工具/方法？"),
    ]
    for title, q in queries:
        print(f"## {title}\n")
        result = client.reflect(bank_id=bank_id, query=q)
        # 提取回答
        answer = ""
        for attr in ["answer", "response", "text", "content"]:
            if hasattr(result, attr):
                v = getattr(result, attr)
                if v: answer = v; break
        print(answer[:1500] if answer else "(no result)")
        print()

    return 0

if __name__ == "__main__":
    sys.exit(main())
```

## 脚本 3: 上下文看门狗 (turn 内 self-check)

**作用**：作为 Agent 的 turn 行为守则，**不**作为独立脚本（不浪费 token）。

**位置**：`~/hermes-all/hermes/skills/agent-behavior/hindsight-watchdog.md`（建议作为 skill）

**核心规则**：

```markdown
# Hindsight 看门狗协议

每次 turn 结束前,Agent 必须:
1. 调用 lcm_status 检查 context_pct
2. 如果 > 50%:
   a. 调用 hindsight_retain() 把本 turn 关键结论存档
   b. 调用 hindsight_reflect() 拉相关历史
   c. 在下次回复开头通知用户: "上下文到 X%,已存档"
3. 如果 > 80%:
   a. 强制建议用户: "建议 /new 启动新 session,本 session 关键结论已存档"
4. 如果 < 30%:
   a. 静默,不做任何事 (节省 token)
```

## Cron 注册

加到 `hermes cron create` 或 `~/hermes-all/hermes/cron/jobs.yaml`:

```yaml
- name: hindsight-nightly-retain
  schedule: "0 23 * * *"
  prompt: "Run hindsight nightly retain to archive today's LCM sessions into Hindsight bank 'hermes'."
  script: "hindsight-nightly-retain.py"
  no_agent: true
  workdir: "~/hermes-all/hermes"

- name: hindsight-morning-reflect
  schedule: "0 8 * * *"
  prompt: "Run hindsight morning reflect to summarize user's recent focus."
  script: "hindsight-morning-reflect.py"
  no_agent: true
  workdir: "~/hermes-all/hermes"
```

## 验证步骤

1. **手动跑** `python hindsight-nightly-retain.py` 一次，确认 stdout 有合理输出
2. **手动跑** `python hindsight-morning-reflect.py` 一次，确认 reflect 有内容
3. **写** lcm.db mock 测试：插入 1 个 fake session 跑脚本，看是否成功 retain
4. **注册** cron 后等次日 8:00，看飞书是否收到摘要
5. **跑** lcm_doctor 看是否有 lifecycle fragmentation

## 陷阱

- ⚠ **不要在 cron 里启 server 太多次**——每跑一次启 server 都要 30s 加载嵌入模型。如果 23:00 和 23:30 都跑，模型反复加载。建议错开或共享 server
- ⚠ **retain 输入不要超过 10K 字符**——LLM 抽取能力有上限，超长会被截断
- ⚠ **Hindsight server 启动慢**——首次跑会下载 cross-encoder (90MB)，30-60s
- ⚠ **token 双计入**——不要同时启 LCM 主动压缩 + Hindsight 主动 retain，会双倍消耗
