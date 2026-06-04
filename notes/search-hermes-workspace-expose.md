---
title: Hermes Workspace 内网穿透方案研究
created: 2026-05-31
updated: 2026-06-04
type: analysis
tags: [networking, tunnel, workspace, deployment, decision]
confidence: high
related: [[notes/hindsight-local-deployment-windows-2026]]
source: Hermes workspace 内网穿透方案研究 2026-06
---

# Hermes Workspace 内网穿透方案研究报告

> 调研日期: 2026-05-31
> 环境: Windows 11, Docker Desktop
> 当前服务: Gateway :8642 | Dashboard :9119 | Workspace :3000
> Tailscale: 未安装 | Cloudflared: 未安装 | Ngrok: 未安装

> **2026-06-04 重构**: 从 `kanban/workspace/hermes-workspace-expose/` 迁到 `wiki/wiki/notes/`
> (kanban 是状态目录,不该放调研报告)

---

## 一、方案全景对比

### 对比总表

| 维度 | Tailscale Funnel | Cloudflare Tunnel | Ngrok (Free) | bore (localtunnel) | FRP |
|:-----|:-----------------|:-----------------|:-------------|:-------------------|:----|
| **上手难度** | ⭐ 最简单 | ⭐⭐ 中等 | ⭐ 简单 | ⭐ 简单 | ⭐⭐⭐⭐ 高 |
| **零成本** | ✅ 免费 (100设备) | ✅ 免费 | ⚠️ 2隧道/40conn/min | ✅ 开源免费 | ✅ 开源免费 |
| **需要域名** | ❌ 不用 (ts.net 子域名) | ✅ 需自有域名 | ❌ 不用 (ngrok.io) | ❌ 不用 | ✅ 需公网VPS |
| **公网VPS** | ❌ 不用 | ❌ 不用 | ❌ 不用 | ❌ 不用 | ✅ 必须自备 |
| **HTTPS** | ✅ 自动 | ✅ 自动(Cloudflare) | ✅ 自动 | ⚠️ 需自签/Let's Encrypt | ⚠️ 需自配 |
| **手机端访问** | ✅ 需装Tailscale App | ✅ 浏览器直接访问 | ✅ 浏览器直接访问 | ✅ 浏览器直接访问 | ✅ 浏览器直接访问 |
| **密码保护** | ❌ 无内置 | ✅ Access Policies | ✅ Basic Auth | ❌ 无 | ❌ 无 |
| **速度** | ⭐⭐⭐⭐ P2P直连 | ⭐⭐⭐⭐⭐ CDN全球 | ⭐⭐ 限速 | ⭐ 限速 | ⭐⭐⭐ VPS带宽决定 |
| **持久连接** | ✅ 始终在线 | ✅ 始终在线 | ❌ 免费版重启换URL | ✅ 始终在线 | ✅ 始终在线 |
| **Windows支持** | ✅ 原生GUI | ✅ cloudflared.exe | ✅ ngrok.exe | ✅ cargo/npx | ✅ frpc.exe |
| **多端口** | ✅ 多个Funnel | ✅ 多Hostname | ❌ 免费版1个隧道 | ❌ 单端口 | ✅ 多端口配置 |

---

## 二、各方案详解

### 🥇 方案A: Cloudflare Tunnel — 推荐方案

**核心优势**: 零成本 + 自有域名 + 全球CDN加速 + 内置DDoS防护 + HTTPS自动

#### 原理
Cloudflare Tunnel (cloudflared) 在您的 Windows 机器和 Cloudflare 边缘节点之间建立一个加密隧道。用户访问您的域名 → Cloudflare CDN → 加密隧道 → localhost:3000。

#### 适合场景
- 已有 Cloudflare 管理的域名
- 需要从浏览器直接访问（手机、电脑都不需装软件）
- 需要 HTTPS、CDN 加速、安全策略

#### 部署步骤 (Windows)

**前置条件**:
- 一个域名 (如 example.com)，DNS 已托管到 Cloudflare (免费套餐)
- Windows 11 管理员权限

**Step 1: 下载 cloudflared**
```powershell
# 下载 Windows amd64 版
# 从 https://github.com/cloudflare/cloudflared/releases 下载 cloudflared-windows-amd64.exe
# 重命名为 cloudflared.exe，放到 C:\cloudflared\

# 添加到 PATH (管理员 PowerShell)
[Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";C:\cloudflared", [EnvironmentVariableTarget]::Machine)
```

**Step 2: 登录认证**
```powershell
cloudflared tunnel login
# 浏览器打开，选择域名授权
```

**Step 3: 创建 Tunnel**
```powershell
cloudflared tunnel create hermes-workspace
# 生成凭证文件: ~\.cloudflared\<uuid>.json
```

**Step 4: 配置 config.yml**
```yaml
# C:\Users\Administrator\.cloudflared\config.yml
tunnel: hermes-workspace
credentials-file: C:\Users\Administrator\.cloudflared\<uuid>.json

ingress:
  # Workspace (主界面)
  - hostname: workspace.example.com
    service: http://localhost:3000
  # Gateway API
  - hostname: gateway.example.com
    service: http://localhost:8642
  # Dashboard
  - hostname: dash.example.com
    service: http://localhost:9119
  # 兜底
  - service: http_status:404
```

**Step 5: 配置 DNS 路由 (Zero Trust Dashboard 模式)**

方法A — Zero Trust 面板 (推荐):
  1. 登录 https://one.dash.cloudflare.com
  2. 左侧菜单 → Networks → Tunnels → 选择 hermes-workspace
  3. 点击 "Public Hostname" → "Add a public hostname"
  4. 依次添加三个子域名:
     - workspace.example.com → HTTP://localhost:3000
     - gateway.example.com → HTTP://localhost:8642
     - dash.example.com → HTTP://localhost:9119
  5. Cloudflare 自动创建 DNS 记录 + HTTPS 证书

方法B — 本地 config.yml (需手动加DNS):
  - 在 Cloudflare DNS 面板手动添加 CNAME:
    - workspace → tunnel-id.cfargotunnel.com
    - gateway → tunnel-id.cfargotunnel.com
    - dash → tunnel-id.cfargotunnel.com

**Step 6: 运行隧道**
```powershell
# 前台运行 (测试)
cloudflared tunnel run hermes-workspace

# 安装为 Windows 服务 (生产)
cloudflared service install
# 之后在 Services.msc 中启动 "Cloudflare Tunnel"
```

**Step 7: 验收**
```powershell
# 从外网手机/电脑访问:
# https://workspace.example.com → 应该打开 Hermes Workspace
# https://gateway.example.com  → Gateway API
# https://dash.example.com     → Dashboard
```

#### 安全配置 (可选但推荐)

在 Cloudflare Zero Trust → Access → Applications 中:
- 添加 **Access Policy**: 要求登录 Google/GitHub 账号才能访问
- 设置 **IP 白名单**: 只允许特定 IP 段访问
- 启用 **WAF 规则**: 防SQL注入、XSS

#### 需要修改的 Hermes 配置

**config.yaml 或 .env 中**:
```yaml
# 允许来自 Cloudflare 的反代请求
ALLOWED_ORIGINS: https://workspace.example.com,https://gateway.example.com,https://dash.example.com

# 如果使用密码认证
HERMES_PASSWORD: your-secure-password
```

> 注意: Workspace/Gateway 默认绑定 127.0.0.1 而非 0.0.0.0，这是安全的——cloudflared 从 localhost 连接，无需对外暴露端口。

---

### 🥈 方案B: Tailscale Funnel — 备选方案 (如果不想用域名/Cloudflare)

**核心优势**: 步骤最少、无需域名、私密访问(仅限你的设备)

#### 原理
Tailscale 建立 WireGuard VPN 网络，所有设备通过 100.x.x.x 虚拟IP互联。Tailscale Funnel 将 localhost 端口公开到公网(ts.net 子域名)。

Tailscale Serve (私密): 只有你的Tailscale设备能访问
Tailscale Funnel (公网): 任何互联网用户都能访问

#### 部署步骤

```powershell
# Step 1: 安装 Tailscale (Windows)
# 从 https://tailscale.com/download 下载安装包
# 运行安装程序，使用 Microsoft/GitHub 账号登录

# Step 2: 验证安装
tailscale status

# Step 3a: 私密访问 (Tailscale Serve) — 推荐，无需暴露到公网
# 在其他设备上安装 Tailscale，登录同账号
# 直接访问 http://100.x.x.x:3000
tailscale serve --https 443 localhost:3000

# Step 3b: 公网暴露 (Tailscale Funnel) — 暴露到公网
# 在 Tailscale Admin Console (https://login.tailscale.com) 启用 Funnel
tailscale funnel localhost:3000
# 输出: https://machine-name.ts.net → localhost:3000
```

#### 手机端访问
- Android/iOS: 安装 Tailscale App → 登录同账号 → 浏览器访问 100.x.x.x:3000
- 不需要 Tailscale 公网Funnel也能访问

#### 缺点
- 对方手机也必须装 Tailscale App（如果用私密模式）
- Funnel 模式暴露的 ts.net URL 无密码保护
- 中国大陆延迟较高（无官方中继服务器）
- HTTPS 自动，但证书是 Tailscale 签发的

---

### 🥉 方案C: Ngrok (Free) — 临时调试方案

**核心优势**: 一行命令搞定、适合临时演示

```powershell
# 注册 → 获取 authtoken
ngrok config add-authtoken YOUR_TOKEN

# 暴露 Workspace
ngrok http 3000
# 输出: https://xxxx-xxxx-xxxx.ngrok-free.app → localhost:3000
```

**免费版限制**:
- 每月 2 个并发隧道
- 每分钟 40 个连接
- 随机域名 (每次重启不同)
- 带宽受限
- 不可自定义域名

**不适合**: 长期稳定运行

---

### 方案D: bore (localtunnel) — 极简/研究用

```powershell
# 需要 Rust 编译器
cargo install bore-cli

# 暴露服务 (需要公共 bore 服务器)
bore local 3000 --to bore.pub
# 输出: bore.pub:12345 → localhost:3000
```

**缺点**:
- 无加密 (裸TCP隧道)
- 公共服务器不稳定
- 无域名/HTTPS
- 适合测试，不适合生产

---

### 方案E: FRP — 自建方案 (如果你已有公网VPS)

```
┌─────────────┐     ┌──────────┐     ┌──────────────┐
│ 外网手机/电脑 │────▶│frps(VPS) │◀────│frpc(Windows) │
│ (浏览器)      │     │:7000     │     │ :3000        │
└─────────────┘     └──────────┘     └──────────────┘
```

```ini
# frpc.ini (Windows)
[common]
server_addr = your-vps-ip
server_port = 7000

[workspace]
type = http
local_port = 3000
custom_domains = workspace.example.com

[gateway]
type = http
local_port = 8642
custom_domains = gateway.example.com

[dashboard]
type = http
local_port = 9119
custom_domains = dash.example.com
```

**缺点**: 需要购买公网VPS (最低¥30/月)、需自行配置HTTPS、运维复杂度高

---

## 三、推荐方案

### 🏆 首选: Cloudflare Tunnel

理由:
1. **零成本** — Cloudflare 免费套餐即可
2. **零安装** — 访问端什么都不用装，浏览器直接访问
3. **全自动 HTTPS** — Cloudflare 自动签发和续期
4. **全球 CDN 加速** — 手机/电脑访问速度极快
5. **安全第一** — 可以加 Access Policy 做 OAuth 登录验证
6. **多端口支持** — 一个 Tunnel 同时暴露 Workspace:3000 + Gateway:8642 + Dashboard:9119
7. **Windows 原生支持** — cloudflared.exe + Windows Service

### 🥈 备选: Tailscale Serve (不暴露到公网)

如果你不需要从外部公网访问，仅需要在你的多台设备间访问 Hermes Workspace，Tailscale（私密组网）是更好的选择——安全性最高，不需要注册域名。

---

## 四、需求总结: Hermes 配置变更清单

| 配置文件 | 需修改项 | 说明 |
|:---------|:---------|:-----|
| `config.yaml` | `ALLOWED_ORIGINS` | 添加 Cloudflare 域名到 CORS 白名单 |
| or `.env` | `HERMES_PASSWORD` | 添加/确认访问密码 |
| (无) | 服务绑定地址 | 确认绑定 127.0.0.1 (安全，cloudflared 可连接) |
| `config.yaml` | `CSP / Content-Security-Policy` | 如需允许 CDN 资源加载 |

---

## 五、快速启动指南 (10分钟内完成)

```powershell
# === 5分钟 Cloudflare Tunnel 快速搭建 ===

# 1. 下载 cloudflared
curl -L -o cloudflared.exe https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe

# 2. 认证
cloudflared tunnel login

# 3. 创建隧道
cloudflared tunnel create hermes-workspace

# 4. 启动隧道 (映射所有三个端口)
# 创建 config.yml (见上文 Step 4)
# 前台测试:
cloudflared tunnel run hermes-workspace

# 5. 在 Cloudflare Zero Trust 面板添加 Public Hostname
# 添加三个子域名分别映射到 :3000, :8642, :9119

# 6. 浏览器访问验证
# https://workspace.yourdomain.com
```

---

## 六、来源

| 来源 | URL | 内容 |
|:-----|:----|:-----|
| Cloudflare Tunnel 文档 | cloudflare.com | Tunnel 架构/配置参考 |
| cloudflared GitHub | github.com/cloudflare/cloudflared | Windows 二进制下载 |
| Tailscale 博客 | tailscale.com/blog | Serve/Funnel 功能对比 |
| CSDN 实战教程 | blog.csdn.net/waxinics/article/details/157291398 | Cloudflare Tunnel Windows 部署 |
| CSDN 详细指南 | blog.csdn.net/weixin_45333779/article/details/147304348 | cloudflared 配置示例 |
| frp GitHub | github.com/fatedier/frp | 开源反向代理 |
| awesome-tunneling | github.com/okoye/awesome-tunneling | 隧道工具对比大合集 |

---

*报告完毕。推荐方案: Cloudflare Tunnel，详细部署步骤见第三章。*
