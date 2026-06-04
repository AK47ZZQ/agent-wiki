# Hermes Workspace 部署 + 远程访问（Tailscale/Frp）

## 部署架构总结

```
手机/外网 ── Tailscale/Frp ──▶ Workspace Server (:3000)
                                  │
                          /api/claude-proxy/*
                                  │
                                  ▼
                       DeepSeek API (或自定义后端)
```

## 生产构建与启动

```bash
cd ~/hermes-all/projects/hermes-workspace

# 生产构建（跳过 HMR WebSocket，frp 隧道友好）
pnpm exec vite build

# 启动生产服务器（注意：必须用 server-entry.js，不是 vite dev）
HOST=0.0.0.0 CLAUDE_API_URL=https://api.deepseek.com/v1 \
  CLAUDE_API_TOKEN=<DEEPSEEK_API_KEY> \
  HERMES_PASSWORD=<随机密码> \
  node server-entry.js
```

## 远程访问 3 种方案对比

| 方案 | 延迟 | 外网需要 | 手机端安装 | 推荐度 |
|:----|:----:|:--------|:---------|:-----:|
| **Tailscale** | 极低（P2P） | 无 | Tailscale App | 🥇 首选 |
| **Sakura Frp** | 中（中转） | frp 域名 | 无 | 🥈 TCP 免装 |
| **Cloudflare Tunnel** | 低（CDN） | 域名 | 无 | 🥉 |

## 关键陷阱

### 1. Gateway 绑定 127.0.0.1（不可从 Tailscale 访问）

Hermes Gateway (:8642) 默认只监听 `127.0.0.1`，无法通过 Tailscale/Frp 从外网直接访问。

**解决：** Workspace 内置代理 `/api/claude-proxy/*` 做服务器端转发，手机 JS 不走直接连接。

### 2. Gateway 需要自己的 API key

即使从 `127.0.0.1` 调用，Gateway 也需要 `Authorization: Bearer <token>`。常用的 provider key（如 DEEPSEEK_API_KEY）**不保证被接受**。

**最佳方案：** 绕过 Gateway，让 Workspace 直连 LLM 提供商：
```
CLAUDE_API_URL=https://api.deepseek.com/v1
CLAUDE_API_TOKEN=<DEEPSEEK_API_KEY>
```

### 3. Workspace 代理 auth 链

proxyRequest 函数读取 auth token 的顺序：
```javascript
process.env.HERMES_API_TOKEN ?? process.env.CLAUDE_API_TOKEN ?? BEARER_TOKEN
```

其中 `BEARER_TOKEN` 来自：
```javascript
process.env.HERMES_API_TOKEN ?? process.env.CLAUDE_API_TOKEN ?? ""
```

**如果均未设置 → 代理调用后端时不带 Authorization header → 后端返回 401。**

### 4. HOST=0.0.0.0 的安全锁

Workspace 拒绝绑定 `0.0.0.0` 除非设置了：
- `HERMES_PASSWORD=<strong-secret>`（推荐）
- 或 `HERMES_ALLOW_INSECURE_REMOTE=1`（不推荐）

安全锁信息：
```
[workspace] refusing to start.
HOST is set to "0.0.0.0" (non-loopback), but HERMES_PASSWORD is unset.
This would expose a high-privilege control plane (terminals, files, agents)
to anyone who can reach the port.
```

### 5. Dashboard (port 9119) 依赖 dashboard_auth 模块

Hermes v0.15.2 pip 安装包缺少 `hermes_cli/dashboard_auth/` 模块。需要手动创建：
- `__init__.py` — 导出 `DashboardAuthProvider`
- `providers.py` — 注册器 + 基类
- `routes.py` — FastAPI 路由
- `middleware.py` — `gated_auth_middleware`
- `audit.py` — `AuditEvent`
- `ws_tickets.py` — WebSocket ticket
- `prefix.py` — URL 前缀正规化

### 6. `hermes gateway start --replace` 不稳定

`--replace` 在某些情况下不被识别（`unrecognized arguments`），即使帮助文档说它支持。备选方案：
```bash
# 方式 1：查 PID + 手动杀
cmd.exe //c "netstat -ano | findstr :8642"
taskkill /F /PID <PID>
hermes gateway start

# 方式 2：重试 start --replace（有时第二次生效）
hermes gateway start --replace

# 方式 3：直接前台 run（Ctrl+C 停止）
hermes gateway run
```

### 7. 环境变量不传播到子进程

Gateway 重启后，Worker 子进程从 gateway 进程继承的环境变量不会自动更新。修改 Worker `.env` 后必须重启 Gateway：
```bash
hermes gateway stop
# 或
taskkill /F /IM python.exe  # 谨慎
hermes gateway start
```

## 文件结构

```
~/hermes-all/
├── projects/hermes-workspace/    ← Workspace 源码
│   ├── server-entry.js           ← 生产服务器入口
│   ├── start-tailscale.bat       ← Tailscale 启动脚本
│   ├── .env                      ← 后端 API 配置
│   └── dist/server/assets/       ← 构建产物
├── sakura_frp/                   ← Frp 隧道文件
│   ├── frpc.exe
│   ├── .env
│   └── start-tunnels.bat
└── hermes/                       ← Hermes 配置
    ├── config.yaml
    ├── .env
    └── auth.json
```

## 快速启动备忘（电脑重启后）

```bash
# 1. 确认 Gateway 运行
curl http://127.0.0.1:8642/health

# 2. 启动 Workspace（Tailscale 模式）
C:\Users\Administrator\hermes-all\projects\hermes-workspace\start-tailscale.bat
# 或
cd ~/hermes-all/projects/hermes-workspace
HOST=0.0.0.0 CLAUDE_API_URL=https://api.deepseek.com/v1 ... node server-entry.js

# 3. 启动 Frp 隧道（外网备用）
C:\Users\Administrator\sakura_frp\start-tunnels.bat

# 4. 手机访问
# Tailscale: http://<tailscale-ip>:3000
# Frp:       https://<frp-domain>:<port>
```
