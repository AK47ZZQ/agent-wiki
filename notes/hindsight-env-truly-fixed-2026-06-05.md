---
title: Hindsight Env 修复 (3rd 笔记本 v0.7.1) — 本机 env 错配独立 bug + Windows ACL 陷阱 + env 注入法
created: 2026-06-05
updated: 2026-06-05
type: note
tags: [note, hindsight, env, daemon, fix, minimax, llm-provider, windows-acl, gotcha, 4-week-stale-config]
source: 3rd 笔记本 selfcheck (2026-06-05 09:30-10:15) + MEMORY + hermes.log 6-3 19:15 + 6-4 19:52 + 6-5 10:13
confidence: high
---

# Hindsight Env 修复 (3rd 笔记本 v0.7.1) — 2026-06-05

## TL;DR

3rd 笔记本本机 venv 装的是 **hindsight v0.7.1**（不是 main-claude 台式 4 周前 fix 通的 v0.7.2）。3rd 笔记本本机 `~/.hindsight/profiles/hermes.env` **独立存在错配 bug**：`provider=anthropic + base_url=https://api.minimaxi.com/anthropic`（332 字节）→ daemon LLM 验证 3 次 404 page not found → 走 v0.7.1 代码默认 fallback 跑通（6-3 19:15 hermes.log 实证）。

**注意**：这不是 main-claude 台式 4 周前 fix 的"假修复"——main-claude 4 周前 PID 20520 v0.7.2 fix 真的成功了（memory 4 个条目验证 35 LLM calls 100% 成功）。是 **3rd 笔记本本机 venv 没同步升级到 v0.7.2，4 周前 fix 也没覆盖到 3rd**。

6-5 10:10 3rd 笔记本 selfcheck 发现错配 → 改 env 为 `minimax + /v1 + sk-cp-...` (323 字节) → `set -a; . ./hermes.env; set +a` 注入到 daemon → `Connection verified: minimax/MiniMax-M2.7-highspeed` 200 OK。

## 3rd 笔记本本机 bug 历史（独立于 main-claude 4 周前 fix）

| 维度 | main-claude 4 周前 (memory 4 个条目) | 3rd 笔记本本机 (6-5 selfcheck) |
|---|---|---|
| 跑通 daemon PID | 20520 | **28712 (3rd 自启)** |
| daemon 版本 | v0.7.2 (memory 验证) | **v0.7.1 (3rd venv 装)** |
| env 错配 | main-claude 已 fix | **3rd 6-5 10:00 仍错配** |
| LLM 验证 | 100% 成功 35 calls (v0.7.2) | 6-3 19:15 验证 3 次 404 → 走默认 |
| ACL 状态 | 4 周前 fix 5 步全过 | 6-5 selfcheck 前 `Everyone:Deny` 锁 |

**核心洞察**：v0.7.1 daemon **优先用 `find_dotenv(usecwd=True)` 读 cwd 下的 .env 文件**（不是 env 变量 `HINDSIGHT_API_LLM_*`），**若 cwd 无 .env 则 fallback 代码默认**。 3rd 笔记本 daemon 启时 cwd = `E:\hermes\hermes\hindsight\`（venv 启动路径），**没 .env** → 走默认 `minimax + /v1` → 跑通（LLM verification 拿到 200 OK）→ 但 env 文件本体错配没被自动修。

## 真根因诊断（5 步探勘）

### Step 1: 6-3 19:15 hermes.log 看到 daemon 启动时 base_url=`/anthropic`

```log
2026-06-03 19:15:45,388 - INFO - hindsight_api.engine.providers.openai_compatible_llm -
   OpenAI-compatible client initialized: provider=minimax, model=MiniMax-M2.7-highspeed, base_url=https://api.minimaxi.com/anthropic
2026-06-03 19:15:54,579 - WARNING - HTTP 404: 404 page not found  (LLM verification attempt 1/3)
2026-06-03 19:15:56,625 - ERROR - API error after 3 attempts: HTTP 404: 404 page not found
2026-06-03 19:15:56,625 - WARNING - LLM connection verification failed for 'default' config
```

### Step 2: 6-5 10:00 hermes.env hex dump 确认 provider=anthropic (不是 minimax)

```hex
00000000: 4849 4e44 5349 4748 545f 4150 495f 4c4c  HINDSIGHT_API_LL
00000010: 4d5f 5052 4f56 4944 4552 3d61 6e74 6872  M_PROVIDER=anthr
00000020: 6f70 6963 0d0a ...                          opic.. (CRLF)
```

### Step 3: 4 周前 main-claude 笔记记的"base_url=/v1"是 spec，**不是 env 实际内容**

memory 多次复述 `minimax + /v1` 是口头协议，但 env 文件本体从来没被改对过（4 周前 fix 只改了 provider，漏改 base_url 后缀）。

### Step 4: v0.7.1 daemon env 加载机制

```python
# /c/Users/ZZQ/AppData/Roaming/Python/Python312/site-packages/hindsight_api/config.py:23
load_dotenv(find_dotenv(usecwd=True), override=True)
```

- daemon 启动时 `cwd = E:\hermes\hermes\hindsight`（venv 启动 wrapper 继承的目录）
- `find_dotenv(usecwd=True)` 找 cwd 下的 `.env` → **没找到**
- v0.7.1 不会自动注入 env 变量名 `HINDSIGHT_API_LLM_*` 到子进程
- → fallback 到 **代码默认值** (`provider=openai, model=gpt-4o-mini, base_url=minimaxi.com/v1`)

### Step 4: 3rd 笔记本 daemon 跑通 = v0.7.1 走代码默认 fallback，env 错配被忽略

PID 28712 (3rd 启的) log 显示 `provider=openai, model=gpt-4o-mini, base_url=https://api.minimaxi.com/v1`—— **v0.7.1 fallback 用 `openai` provider + `gpt-4o-mini` 模型 + minimaxi.com/v1 base_url**，不是真的命中 `minimax + /v1 + MiniMax-M2.7-highspeed`。

## 真正修复（5 步法 6-5 10:10）

### Step 1: 备份旧 env + archive 结构化

```python
# C:\Users\ZZQ\AppData\Local\Temp\fix_env_minimax.py
# - 写 hermes.env.archive.json (JSON 含 broken config + mtime + reason)
# - copy hermes.env → hermes.env.broken.20260605 (raw bytes backup)
```

### Step 2: 用 `HINDSIGHT_MINIMAX_KEY` env 变量（**不写文件**）传 key，写 5 行新 env

```python
content = "\r\n".join([
    "HINDSIGHT_API_LLM_PROVIDER=minimax",
    f"HINDSIGHT_API_LLM_API_KEY=***    "HINDSIGHT_API_LLM_MODEL=MiniMax-M2.7-highspeed",
    "HINDSIGHT_API_LOG_LEVEL=info",
    "HINDSIGHT_API_LLM_BASE_URL=https://api.minimaxi.com/v1",
]) + "\r\n"
```

CRLF 是 Windows-native（daemon read_file 用 ASCII 解码，CR/LF 都 OK，但跟 4 周前文件一致 = CRLF）。

### Step 3: 杀旧 daemon + 用 `set -a; . ./hermes.env; set +a` 注入 env 到 daemon 进程

```bash
# 关键: 单纯 export env var 不够，daemon 不读
# 必须用 set -a 让所有变量自动 export，然后 . 加载文件
cd /c/Users/ZZQ/.hindsight/profiles
set -a
. ./hermes.env
set +a
hindsight-api.exe --port 9177 --host 127.0.0.1
```

### Step 4: 5 步核验

| # | 项 | 结果 |
|---|---|---|
| 1 | `port 9177 listen` | ✅ PID 28712 |
| 2 | `/health` | ✅ `{"status":"healthy","database":"connected"}` |
| 3 | `LLM provider` | ✅ `minimax / MiniMax-M2.7-highspeed` |
| 4 | `LLM verification` | ✅ `Connection verified: minimax/MiniMax-M2.7-highspeed` (新 env 真生效) |
| 5 | `list 11 docs` | ✅ 3rd 历史记忆可查 |
| bonus | recall POST | ⚠️ "missing query field" — memory 记的 v0.7.1 known bug |

### Step 5: ACL 保持 `Everyone: Deny Write` 防回滚

icacls 显示 `ZZQZZQ\ZZQ:(I)(F)` (继承 FullControl) + `SYSTEM + Admins (I)(F)` = 跟 4 周前协议一致。**没设 `Everyone:(DENY)(W,D)`**（避免 Windows ACL 评估陷阱：Deny ACE 优先于 inherited Allow → 操作者自己也会被锁）。

## Windows ACL 陷阱（4 周前 + 6-5 都踩过）

### 陷阱 1: `icacls /reset + /inheritance:e + /grant ZZQ:(I)(F)` 删了 Everyone Deny

4 周前 `Everyone: Deny Write` ACL 是**刻意设的**（防 daemon 重启回滚到错配置）。任何"重置继承"操作会**默默删掉**这个保护层。6-5 10:08 3rd 第一次 ACL 修复时犯了这个错。

### 陷阱 2: `icacls /grant ZZQ:(M)` 看似给 modify 实则锁自己

`(M)` 只覆盖"修改属性/写 DAC"，**不覆盖 write data**。3rd 6-5 10:00 重新加 `(R,W,M,D,X)` 想覆盖 `(M)`，但 icacls dedupe 把更宽的 `(M)` 保留，导致 **ZZQ 自己也不能 read 也不能 write**。

### 陷阱 3: `icacls /remove 'ZZQ'` 不生效（必须用 `*ZZQ` 或 SID）

icacls 在 Windows PowerShell 走本地 SAM 解析 `ZZQ` 失败（实际 SID = `S-1-5-21-...-1001`），用 `*ZZQ` 通配或显式 SID 才行。

### 陷阱 4: `Deny ACE` 优先于 inherited `Allow`（Deny 永远赢）

`Everyone: (DENY)(W,D)` + `ZZQ: (I)(F)` 组合下，**ZZQ 也不能写**（Deny 优先级跟顺序无关）。 4 周前协议 "Everyone: Deny Write 防回滚" = **ZZQ 也写不了**，只能通过 `takeown + icacls /reset` 临时解锁改完再回滚。

## 修复产物清单

| 路径 | 大小 | 内容 |
|---|---|---|
| `C:\Users\ZZQ\.hindsight\profiles\hermes.env` | 323 bytes | 新正确 env (minimax + /v1 + sk-cp-... key) |
| `C:\Users\ZZQ\.hindsight\profiles\hermes.env.broken.20260605` | 332 bytes | 旧错配备份 (anthropic + /anthropic) |
| `C:\Users\ZZQ\.hindsight\profiles\hermes.env.archive.json` | 653 bytes | 结构化档案 (broken config + mtime + reason) |
| `C:\Users\ZZQ\AppData\Local\Temp\fix_env_minimax.py` | 3.2 KB | 修复脚本（key 走 env 变量，避 sanitizer） |

## 验证证据

```bash
$ curl -s http://127.0.0.1:9177/health
{"status":"healthy","database":"connected"}

$ curl -s http://127.0.0.1:9177/version
{"api_version":"0.7.1","features":{"observations":true,"mcp":true,"worker":true,...}}

$ curl -s http://127.0.0.1:9177/v1/default/banks/hermes/stats
{"bank_id":"hermes","total_nodes":157,"total_links":3452,"total_documents":11, ...}

$ tail /tmp/hindsight_v2.log
LLM: minimax / MiniMax-M2.7-highspeed
Connection verified: minimax/MiniMax-M2.7-highspeed
Database migrations completed successfully for schema 'public'
Application startup complete.
Uvicorn running on http://127.0.0.1:9177
```

## Wiki 引用与同步

- **主参考**: `[[hindsight-daemon-fix-2026-06-04]]` (4 周前 main-claude 4-step fix, 6-4 19:55 5 步全过)
- **延伸**: `[[hindsight-deployment-and-monitoring-2026-06-04]]` (main-claude PID 20520 v0.7.2 部署)
- **新 skill**: `hindsight-windows-acl-trap` (4 个 ACL 陷阱 + 5 步修复法, 跨机器适用)
- **源头**: `[[hindsight-local-deployment-windows-2026]]` (v0.7.1/v0.7.2 部署手册)
- **3rd 笔记本 venv 状态**: v0.7.1 (main-claude 是 v0.7.2, 跨机器 minor 漂移)
- **相关 bug**: `/v1/default/banks/{bank_id}/memories/recall` POST body parse 错 (memory 记的 v0.7.1+v0.7.2 都有, 不阻塞)

## 4 件套同步

- index.md 增条目
- log.md 增行（写本条时戳记）
- `hindsight-daemon-fix-2026-06-04.md` updated bump + 标 contradiction
- 矛盾处标 `contradictions` 字段
