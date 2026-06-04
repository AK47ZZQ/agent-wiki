# 搜索深度与广度策略

> 扩展 `ai-harness-exploration` 的搜索能力。多引擎、多轮次、多维度。
> 更新于 v6.6.0 — MCP 优先架构，删除已泄漏的 REST API key。

## 一、搜索引擎矩阵

| 引擎 | 最佳用途 | 何时用 | 优先级 |
|:----|:--------|:------|:------|
| `mcp_minimax_web_search` | MiniMax MCP 搜索 | 第一优先 | 🥇 **MiniMax MCP**（150次/5h，CJK最佳） |
| `mcp_tavily_search` | Tavily MCP（google/microsoft/ggc） | MiniMax 冷却时 | 🥈 **Tavily MCP**（3独立key，MCP配额独立于REST） |
| `web_search` | DuckDuckGo（免费） | MCP全灭时 | 🥉 免费回退 |
| `web_extract` | 全文提取 | 找到目标 URL 后 | ⭐ 次选 |
| `browser` | 动态/JS渲染/反爬页面 | `web_extract` 被屏蔽时 | 备用 |
| `Tavily REST` | 结构化结果 | 仅MCP全灭时回退 | 4️⃣ 末位 |
| `arxiv` | 学术论文/研究 | 技术深度深挖 | 按需 |
| `blogwatcher` | RSS/Atom 订阅监控 | 长期追踪主题 | 定时 |
| `session_search` | 过往会话 | 用户提"之前讨论过的" | 历史查询 |
| `lcm_grep` | 当前会话 | 查找本次对话中的内容 | 会话查询 |

### 搜索优先级（MCP优先于REST）

```
同一关键词 ──优先MCP──┌─ mcp_minimax_web_search (MiniMax MCP, 150次/5h, CJK最佳)
                     ├─ Tavily MCP Google (tavily-mcp-google, 独立key ✅ 0.19s)
                     ├─ Tavily MCP Microsoft (tavily-mcp-microsoft, 独立key ✅ 0.26s)
                     ├─ Tavily MCP GGC (tavily-mcp-ggc, 独立key ✅ 0.71s)
                     ├─ Tavily MCP GitHub (tavily-mcp-github, key已432 ❌ 备用)
                     ├─ web_search (DuckDuckGo, 免费)
                     └─ Tavily REST key1/key2 (API, 1000次/月, 仅MCP全灭时回退)
                             ↓
                     7 路优先级排序，MCP通道优先
                     MCP与REST配额独立，REST 432不影响MCP
                     去重后按质量排序输出
```

### GitHub 镜像替补

**首选直连 github.com**，不可用时才用替补。终端环境使用代理前缀：

```python
# 终端环境
if env == "terminal" and github_unreachable:
    url = f"https://ghproxy.net/{url}"
```

## 二、搜索维度矩阵（搜什么）

| 维度 | 搜索方向 | 示例查询 |
|:----|:--------|:--------|
| **概念理解** | `{名} 概念 / introduction / 是什么` | 快速扫盲 |
| **最佳实践** | `{名} best practices / production / architecture` | 工程化 |
| **批判视角** | `{名} criticism / limitations / 缺点 / pitfalls` | 看反面 |
| **对比** | `{名} vs / comparison / alternatives` | 选型 |
| **实战案例** | `{名} case study / 实战 / 踩坑` | 验证可行性 |
| **学术背书** | `{名} paper / arxiv / research` | 理论深度 |
| **社区评价** | `{名} reddit / HN / twitter` | 真实口碑 |
| **最新动态** | `{名} 2026 / latest / update` | 时效性 |

## 三、搜索轮次策略（4 轮递进）

```
Round 1: 广撒网（2-3 次搜索）
  目的：理解基本概念和范围
  方法：概念理解 × 1 + 最新动态 × 1
  产出：3-5 个关键 URL，1 个初步理解
  门控：找到了 3+ 个独特来源？→ 进入 Round 2
        找不到？→ 换搜索词或换引擎

Round 2: 深挖（3-4 次搜索）
  目的：深入理解关键方面
  方法：最佳实践 × 1 + 批判/对比 × 1 + 实战案例 × 1
  产出：每个方向 1-2 个高质量来源，核心观点提取
  门控：观点覆盖了 70% 以上已知维度？→ 进入 Round 3
        发现重大分歧 → 额外搜 1 次验证

Round 3: 交叉验证（1-2 次搜索）
  目的：验证已提取观点的可靠性
  方法：对关键争议点、关键数据点做定向搜索
  产出：确认/修正已提取的观点
  门控：所有主要观点都有来源支持？→ 进入 Round 4
        有未解决的矛盾 → 记录在 wiki 的 contested 字段

Round 4: 补漏（0-1 次搜索）
  目的：搜索是否有遗漏的维度
  方法：宽泛查询 × 1（提取深度评估中标记的关注点）
  产出：确认无重大遗漏
  门控：当前理解已经完整？→ 开始形式化
        发现新维度 → 退回 Round 2 追加
```

**规则：** 4 轮搜索总次数控制在 6-10 次。超过 10 次仍未理解 → 切换策略。

## 四、搜索结果质量评估

| 指标 | 🟢 高质量 | 🟡 可接受 | 🔴 低质量 |
|:----|:---------|:---------|:---------|
| 域名 | .edu / 官方文档 / 知名作者 | 技术博客 / 中型社区 | SEO 农场 / 聚合站 |
| 时效 | < 6 个月 | 6 月 - 2 年 | > 2 年 |
| 引用 | 被其他来源引用 | 有参考链接 | 无引用 |
| 深度 | 全量分析 + 数据 | 有结构 + 部分数据 | 表面/广告 |
| 客观性 | 平衡视角 + 承认局限 | 有偏向但有数据 | 纯推广 |

**规则：**
- 3+ 个高质量来源 → 高置信度
- 1-2 个高质量 + 多个可接受 → 中置信度
- 全部低质量 / 只有 1 个来源 → 低置信度

## 五、搜索词优化技巧

### 无效搜索词诊断

```
搜索返回 < 3 条有用结果 → 优化搜索词

优化方向：
  1. 加限定词："{名} tutorial" → "{名} 2026 tutorial python"
  2. 换语言：中文无结果 → 换英文 / 反之
  3. 换站点：用 site: 限定知名站点
  4. 换同义词：tutorial → guide / introduction → getting started
  5. 加引号找精确匹配："{精确术语}"
  6. 减限定词：过于具体 → 退到更一般的搜索词

搜索词优化不超过 2 次。2 次后无结果 → 换搜索引擎或换搜索方向。
```

### CJK 搜索注意事项

```
中文搜索时 FTS5 和部分搜索引擎分词效果差：
  - 太短的词（2 字以下）→ 用更长词组
  - 全中文无结果 → 混合英文关键词
  - 尝试中英文同搜：web_search("{中文名} OR {English name}")
```

## 六、搜索深度评估日志

每次探勘结束后，记录搜索有效性：

```
搜索统计：
  ├─ 总搜索次数：N
  ├─ 使用引擎：web_search / web_extract / browser / arxiv
  ├─ 搜索轮次：Round 1/2/3/4 分布
  ├─ 有用结果率：N 有用 / N 总 × 100%
  ├─ 搜索词优化次数：N
  └─ 有效性评估：
       > 80% → 高效搜索
       50-80% → 正常
       < 50% → 下次需要重新设计搜索策略
```

## 七、工具链集成

### 与 ai-harness-exploration 各步骤的配合

| Skill 步骤 | 搜索任务 | 搜索轮次 | 引擎偏好 |
|:----------|:--------|:--------|:--------|
| Step 0 质量评估 | 搜来源背景 | Round 1 | mcp_minimax / mcp_tavily |
| Step 1.2 外部搜索 | 搜 5 个方向 | Round 1-2 | mcp_minimax + mcp_tavily + web_search |
| Step 1.3 概念提取 | 搜学术背书 | Round 2 | arxiv + mcp_tavily |
| Step 1.5 已知对比 | 搜已有知识 | Round 3 | session_search + lcm_grep |
| Step 1.7 学派定位 | 搜交叉验证 | Round 3 | mcp_tavily |
| Step 5 验证 | 搜争议确认 | Round 4 | mcp_minimax |
| 深度追踪 | RSS 监控 | 持续 | blogwatcher |

## 八、Tavily 432 自恢复机制

**优先MCP通道**，MCP配额独立于REST。Tavily REST 432 不影响 Tavily MCP（实测 ~0.3s）。

当 web_search（Tavily REST）返回 432 时：
```
1. 尝试 Tavily REST key2（独立配额，1000次/月）
2. 如果 key2 也 432 → 切回 MCP 通道
3. MCP Tavily google/microsoft/ggc 不受 REST 配额影响
4. 全部失败 → MiniMax MCP → DuckDuckGo → 报告"暂不可用"

Worker 执行路径：
  第1层: mcp_minimax_web_search(query) → MiniMax MCP（第一优先）
  第2层: mcp_tavily_search(query) → Tavily MCP Google/Microsoft/GGC（3独立key）
  第3层: web_search(query) → DuckDuckGo（免费）
  第4层: Tavily REST key1（仅MCP全灭时回退）
  第5层: Tavily REST key2（仅MCP全灭时回退）
```
