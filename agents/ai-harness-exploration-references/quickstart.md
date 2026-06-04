# AI Harness 探勘法 — 快速启动卡 v6.6.0

> 无需加载整个 skill。关键步骤序列速查。

## 6 步探勘法

```
Step 0: 来源质量评估 → 已有知识校验 → 多样性检查
Step 1: Analyze (结构→搜索→概念→反向→对比→G×S→学派)
Step 2: Extract (Concept/Method/Workflow)
Step 3: Formalize (Skill/Method/Concept/AGENTS.md)
Step 4: Deliver (报告 + 关键洞察)
Step 5: Verify (18 项清单 + Ralph 6 信条)
Step 6: Debrief (记忆+同步+兜底+凝练)
```

## MCP 优先搜索（v6.x 新架构）

```
同一关键词 ──优先MCP──┌─ mcp_minimax_web_search (MiniMax MCP, 150次/5h, 第一优先)
                     ├─ Tavily MCP Google (独立key ✅ 0.19s)
                     ├─ Tavily MCP Microsoft (独立key ✅ 0.26s)
                     ├─ Tavily MCP GGC (独立key ✅ 0.71s)
                     ├─ web_search (DuckDuckGo, 免费)
                     └─ Tavily REST key1/key2 (仅MCP全灭时回退)
                             ↓
                     MCP通道优先，配额独立于REST
                     REST 432不影响MCP
```

**R1 门控：** MiniMax MCP 2次无结果 → 切 Tavily MCP，不再逐个回退。

## 最常用的子步骤

### 1. 仓库分析：双通道法
```
第一通道（5min）: README → AGENTS.md → 目录树 → scripts → 清单
第二通道（15-30min）: 每个子目录读 AGENTS.md → 读内容 → 交叉引用
用 delegate_task 并行：3 个子代理各自深入一个子目录
```

### 2. 并行搜索模式（3 种策略）

| 模式 | 墙钟 | 配额 | 适用 |
|:----|:----:|:----:|:----|
| 🚀 快速并行 | ~30s | 3次(MCP) | 扫盲 |
| 🎯 标准并行 | ~60s | 3次(MCP) | 默认 |
| 🧠 深度并行 | ~120s | 最多6次(MCP) | 全量分析 |

**部分价值模式：** 子代理全部 completed 但 2/3 是"不存在"结论时，有产出的子代理正常提取，无产出的跳过标记。

### 3. 全引擎故障兜底
```
第1层: MCP优先(默认) → 全部无结果时:
第2层: 放宽/收窄/换语言搜索词
第3层: 改用已知知识库(session_search/lcm_grep/wiki)
第4层: 报告"无公开可用信息"
```

### 4. 验证 18 项清单核心
- wiki 页面 → read_file 检查
- skill → skill_view 检查
- index.md 总数正确
- log.md 记录一致
- frontmatter 完整
- wikilink ≥ 2 出链
- related_skills 双向引用
- 单源仓库声明→1次搜索验证存在性
- Ralph 6 信条（代理系统分析用）

## 深度延续搜索（用户说"继续"时）

```
Phase 1: 缺口分析 → 当前知道什么？缺什么维度？
Phase 2: 多角度搜索 → 技术/实践/对比/陷阱/生态/中文 6 域
Phase 3: 横向扩展 → 替代方案/批评/上下游/跨源验证
Phase 4: 纵向深入 → 最有价值 1-3 来源全量分析
Phase 5: 交叉合成 → wiki 更新 + 新连接 + 模式识别
Phase 6: 增量交付 → 只报"比上次多了什么"
收敛规则：3 轮搜索后 80%+ 重复已知 → 停
```

## 规则速记

- **宁多勿少**：技能部分相关也加载
- **先查历史**：lcm_grep/session_search 再问用户
- **成本优先**：web_search < web_extract < browser < delegate_task
- **知识去重**：新来源先查 wiki 有没有
- **confidence 升级**：单源=medium，多源=high，冲突=降级
- **MCP优先**：MiniMax MCP → Tavily MCP → DuckDuckGo → Tavily REST
- **MCP配额独立**：REST 432不影响MCP通道
- **中断恢复**：确认状态→处理未完结果→继续
