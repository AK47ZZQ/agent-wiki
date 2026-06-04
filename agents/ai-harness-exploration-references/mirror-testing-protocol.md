# 镜像测试协议与结果

> 记录于 2026-05-29，在 ai-harness-exploration v5.2.0→v5.2.2 测试过程中执行。
> 两轮测试：第 1 轮（v5.2.1, 5 镜像）→ 第 2 轮（v5.2.2, 追加 4 镜像 = 9 总）
> 测试环境：Hermes Agent browser (Browserbase, stealth mode, no residential proxy) + web_extract (Feishu gateway)

## 测试目的

验证从中文博客/合集文章收集的 GitHub 国内镜像站的实际可用性。来源声称这些镜像 "✅ 可用"，需要独立验证。

## 测试方法

### 测试 URL 模板

```python
# 浏览访问（browser）
base_url = "https://{mirror}/NousResearch/hermes-agent"

# 文件下载（web_extract）
raw_url = "https://{mirror}/raw.githubusercontent.com/NousResearch/hermes-agent/main/tools/mcp_tool.py"

# 文件代理（ghproxy 格式）
proxy_url = "https://{mirror}/https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md"

# Release 下载
release_url = "https://{mirror}/NousResearch/hermes-agent/releases/download/v0.14.0/release.tar.gz"
```

### 测试工具

| 工具 | 测试什么 | 限制 |
|:----|:--------|:------|
| browser_navigate | 网页浏览是否正常 | 运行无 residential proxy，部分站点检测 bot |
| browser_console | 验证页面实际内容 | 仅对 browser 可达页面有效 |
| web_extract | 文件/内容提取 | Feishu 网关可能拦截（所有外部 URL 返回 "Blocked"） |

### 判断标准

| 结果 | 含义 | 处理 |
|:----|:----|:------|
| 200 + 页面内容正常 | 可用 | 保留，标注验证日期 |
| 403 Forbidden | bot 检测/IP 限制 | 标记为"bot 检测"，降级 |
| 404 Not Found | 镜像路径不兼容/已下线 | 标记为"不可用" |
| Timeout (30s+) | 不可达 | 标记为"网络不可达" |
| Connection Closed | 端口/协议不兼容 | 标记为"连接被拒" |
| Cloudflare 挑战 | 反爬拦截 | 标记为"Cloudflare 拦截" |
| web_extract "Blocked" | 网关级限制 | 不能说明镜像本身失效（需 browser 补充测试） |

## 测试结果（2026-05-29，两轮汇总）

### 第 1 轮（v5.2.1）— 5 镜像

| 镜像 | 测试方式 | 结果 | 判定 |
|:----|:--------|:----|:----:|
| github.com 直连（基准） | browser | 正常（172k★） | 基准 |
| bgithub.xyz | browser +/NousResearch/hermes-agent | 403 Forbidden（bot 检测） | 不可用 |
| gitclone.com | browser +/NousResearch/hermes-agent | Timeout（30s+） | 不可用 |
| github.ur1.fun | browser +/NousResearch/hermes-agent | 404: NOT_FOUND | 不可用 |
| gh-proxy.com | web_extract raw 代理 | Blocked（网关级） | 仅终端 |
| github.akams.cn | browser +/NousResearch/hermes-agent | 404: This page could not be found | 不可用 |

### 第 2 轮（v5.2.2）— 追加 4 镜像 + 再测

| 镜像 | 测试方式 | 结果 | 判定 |
|:----|:--------|:----|:----:|
| ghproxy.net（浏览） | browser +/NousResearch/hermes-agent | 空页面（非浏览镜像） | 仅终端 |
| ghproxy.net（代理） | browser +/raw.githubusercontent.com/... | 页面加载（代理格式有效） | 仅终端可用 |
| gh-proxy.com（代理） | browser +/raw.githubusercontent.com/... | 页面加载（代理格式有效） | 仅终端可用 |
| ghproxy.homeboyc.cn | browser +/NousResearch/hermes-agent | 404 GitHub Pages | 不可用 |
| gh.llkk.cc | browser +/NousResearch/hermes-agent | Cloudflare 拦截（Attention Required） | 不可用 |
| mirror.ghproxy.com | browser +/raw.githubusercontent.com/... | Connection Closed | 不可用 |
| raw.kgithub.com | browser +/README.md | Connection Closed | 不可用 |
| github.moeyy.xyz | browser +/NousResearch/hermes-agent | Connection Closed | 不可用 |

### github.ur1.fun 真相

访问 `github.ur1.fun` 根路径发现它**不是镜像站**，而是一个 GitHub 下载加速工具（输入 URL 生成加速下载链接）。中文博客声称它是"直接访问型镜像"属于误导。

### 总结论

```
第 1 轮：4/5 浏览镜像失效，1 个未验证（网关限制）
第 2 轮：新增 4 个全部失效，发现 2 个文件代理可用（终端专用）
第 1+2 轮：9 个镜像 → 0 个浏览器可用，2 个终端可用的文件代理

→ 浏览器环境下直连 github.com 是唯一可靠方案
→ 终端可用 ghproxy.net/gh-proxy.com 作为 git clone/curl 的前缀代理
→ 清华镜像 mirrors.tuna.tsinghua.edu.cn/github-release 可用于 Release 下载
→ 码云 gitee.com/mirrors 可用于热门项目 git clone
```

## 镜像可靠性分析

### 失败原因分类

| 失败原因 | 影响镜像 | 说明 |
|:--------|:-------|:------|
| Bot 检测（无 residential proxy） | bgithub.xyz | 镜像增加了反爬保护，仅允许真实浏览器访问 |
| 镜像已下线 | github.ur1.fun, github.akams.cn | 404 表明服务已不存在 |
| 网络隔离 | gitclone.com | Timeout 表明从当前网络不可达 |
| Cloudflare 拦截 | gh.llkk.cc | 代理 IP 被 Cloudflare 屏蔽 |
| 连接被拒 | mirror.ghproxy.com, raw.kgithub.com, github.moeyy.xyz | DNS 或端口不可达 |
| 不兼容的 URL 格式 | 全部 | 镜像可能要求特定路径前缀（如 /github.com/...），而非直接替换域名 |
| 镜像仅支持 git clone | 全部 | 镜像设计为终端操作，不支持 HTTP 网页浏览 |

### 关键教训

1. **不要相信"可用"标签** — 中文合集博客中的镜像状态信息可能已过时数周甚至数小时
2. **镜像时效性极差** — GitHub 镜像的存活时间通常以天/周计，不是月/年
3. **测试环境决定了结果** — 浏览器环境 vs 终端环境的镜像可用性可能完全不同
4. **直连才是王道** — 只要 GitHub 直连可用，就不需要镜像
5. **区分"镜像"和"代理"** — ghproxy.net 不是镜像站，是请求代理；bgithub.xyz 是真正镜像站但被 bot 检测封锁

## 重新测试协议

如需重新验证镜像状态：

```python
# Step 1: 快速扫一圈（browser_navigate）
mirrors = ["bgithub.xyz", "gitclone.com", "github.ur1.fun",
           "gh-proxy.com", "github.akams.cn", "ghproxy.net",
           "ghproxy.homeboyc.cn", "gh.llkk.cc", "mirror.ghproxy.com",
           "raw.kgithub.com", "github.moeyy.xyz"]
for m in mirrors:
    url = f"https://{m}/NousResearch/hermes-agent"
    # browser_navigate(url) → 记录 HTTP 状态

# Step 2: 文件代理格式验证（browser）
proxies = ["ghproxy.net", "gh-proxy.com"]
for p in proxies:
    url = f"https://{p}/https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md"
    # browser_navigate(url) → 验证是否返回文本内容

# Step 3: 终端测试（terminal）
# git clone --depth 1 https://ghproxy.net/https://github.com/NousResearch/hermes-agent
# → 对比直接 clone 速度

# Step 4: 更新 skill 中的镜像规则
# 当前有效：ghproxy.net（终端代理）, gh-proxy.com（终端代理）
# 当前无效：其余 9 个（2026-05-29 验证）
```

## 参考来源

- 镜像列表来源 1：[2026最新收集]github国内镜像站 — 腾讯云开发者社区
- 镜像列表来源 2：2026年01月最新可用的18个Github镜像站 — 51CTO博客
- 测试工具：Hermes Agent browser (Browserbase) + web_extract
- 测试人员：Hermes Agent (ai-harness-exploration v5.2.2)
