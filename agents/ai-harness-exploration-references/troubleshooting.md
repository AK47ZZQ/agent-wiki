# 🔧 探勘故障排除手册

> 当搜索引擎/工具/工作流出现异常时的快速诊断和修复方案。

## 1. 搜索故障

### 1.1 web_search 返回空 / 少结果

| 现象 | 可能原因 | 修复 |
|:----|:--------|:----|
| 返回 0 结果 | 搜索词太精确/小众 | 去限定词，用更宽泛的同义词 |
| 返回 1-2 个无关结果 | CJK 引擎不匹配 | 中英混合搜索，短词改长词组 |
| 返回 5+ 但全是 SEO 农场 | 主题被 SEO 污染 | 加 `-site:medium.com -site:dev.to` 排除 |
| 200 状态但空 body | 限流/网关问题 | 等待 30 秒重试，或用 mcp_tavily 替补 |

### 1.2 web_extract 全部 Blocked

| 现象 | 可能原因 | 修复 |
|:----|:--------|:----|
| "Blocked: Private/Internal network" | 飞书/网关级封锁 | 先发 1 个试探 → Blocked → 切 browser |
| Timeout | 目标站点慢/大 | 超大页面（arxiv PDF 等）直接超时，改用 web_search snippets |
| 403 Forbidden | 目标站点反爬 | 切 browser 渲染 |
| 返回空 markdown | JS 动态渲染 | 切 browser 等 JS 加载 |

### 1.3 browser 故障

| 现象 | 可能原因 | 修复 |
|:----|:--------|:----|
| 403 / 429 | 目标站点检测到 bot | 无代理运行，部分站点会拦截；尝试 web_search 替代 |
| Timeout | 页面过大 | 先 scroll 再 snapshot，避免一次性加载 |
| 白屏 / 无内容 | 需要登录 | 跳过该来源，标记"需登录" |
| 中文乱码 | 编码问题 | 切换页面编码检测 |

### 1.4 MCP 服务器故障

| 现象 | 可能原因 | 修复 |
|:----|:--------|:----|
| mcp_minimax 超时/失败 | MiniMax MCP 服务暂时不可用 | 降级到 Tavily MCP，MiniMax 冷却后自动恢复 |
| `hermes mcp test minimax` 报 `errlog` 参数错误 | MCP Python SDK 版本过旧（<1.0） | 升级：`pip install -U mcp`（0.9.1→1.27.2 已验证修复） |
| mcp_tavily 返回 432 | Tavily MCP GitHub key 耗尽 | 切 Tavily MCP google/microsoft/ggc（3个独立key） |
| mcp_tavily 全部失败 | Tavily MCP 服务异常 | 降级到 web_search(DuckDuckGo) → Tavily REST |
| 所有 MCP 全部失败 | MCP 基础设施故障 | 执行全引擎故障兜底策略 |

### 1.5 镜像全部失效

| 现象 | 可能原因 | 修复 |
|:----|:--------|:----|
| 所有第三方镜像 403/404/Timeout | 镜像已失效或对浏览器不可用 | 直连 github.com；终端用 ghproxy 代理 |
| ghproxy 连接失败 | 代理服务不稳定 | 等待几分钟重试，或改用 git config 全局代理 |

## 2. 并行搜索故障

### 2.1 delegate_task 子代理超时

| 现象 | 可能原因 | 修复 |
|:----|:--------|:----|
| 子代理 60+ 秒无返回 | 搜索量过大或目标站点慢 | 标记"部分失败"，用已有结果继续 |
| 子代理返回空 | 搜索词在子代理上下文无意义 | 重新下发时加更具体的 context |
| 多个子代理失败 | 主引擎可能全局故障 | 执行全引擎故障兜底策略 |

### 2.2 token 成本过高

| 现象 | 可能原因 | 优化 |
|:----|:--------|:----|
| 3 路并行后上下文溢出 | 每个子代理返回了大量结果 | 减少并行数到 2，或限制子代理 `toolsets` |
| 子代理返回全量原文 | 子代理没有做提取/压缩 | 在 goal 中加"只返回关键点，不要全文" |

## 3. 产出故障

### 3.1 wiki 页面创建失败

| 现象 | 可能原因 | 修复 |
|:----|:--------|:----|
| write_file 写入内容为空 | content 参数空 | 检查 Extract 步骤是否完成了提取 |
| frontmatter 断裂 | YAML 语法错误 | patch 修正 frontmatter |
| index.md 计数不匹配 | 遗漏了计数更新 | read_file index.md 检查 Total 行，patch 修正 |
| log.md 记录格式不一致 | 本次格式写错了 | 参考 log.md 已有格式追加 |

### 3.2 skill 注入失败

| 现象 | 可能原因 | 修复 |
|:----|:--------|:----|
| skill_view 报错"missing frontmatter" | 缺少 `---` 分隔线 | patch 补全 frontmatter |
| skill 加载但 triggers 不命中 | triggers 没有对应的中文触发词 | 追加到 frontmatter triggers |
| skill 加载但版本混乱 | version bump 遗漏 | skill_manage patch version |

### 3.3 hermes dashboard 启动失败

| 现象 | 可能原因 | 修复 |
|:----|:--------|:----|
| `ModuleNotFoundError: No module named 'hermes_cli.dashboard_auth'` | pip 安装时未提取 `plugins/dashboard_auth/` 目录 | 检查版本；等待更新；或用 `hermes gateway` 替代（portable 模式） |
| 启动后无响应/秒退 | NODE_ENV/端口冲突 | `--skip-build` + `--no-open` 避免 npm build 和浏览器打开 |

## 4. 快速诊断表

| 你遇到 | 查哪里 | 大概率是什么 |
|:-------|:------|:-----------|
| "怎么没找到X" | Step 1.2 搜索策略 | 搜索词不准或引擎不够 |
| "搜索结果不对" | 搜索结果质量评估 | 来源质量不够高 |
| "产出太浅" | Step 2 Extract | 只读了 README 没深入 |
| "重复创建了已有的概念" | Step 0a 知识校验 | 忘了先查 wiki 目录 |
| "index.md 总数不对" | Step 5 Verify | 忘了更新 index.md |
| "技能不触发" | frontmatter triggers | triggers 关键词不匹配 |
| "子代理没返回" | 并行搜索容错 | 子代理超时或目标站点慢 |
| "web_extract 全废了" | 引擎切换规则 | 网关封锁，切 browser |
