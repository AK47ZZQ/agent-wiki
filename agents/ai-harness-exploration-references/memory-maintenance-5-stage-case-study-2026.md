# Memory 维护 5 阶段案例 (2026-06-03 → 06-04)

> 同一 5 阶段弧线在 **memory 维护**上重演. 写给未来 session: 当你看到记忆快爆了/主动化反弹/反弹信号 → 这就是 5 阶段.

## 摘要

24 小时内, 记忆栈经历了完整的 5 阶段:

| 阶段 | 时间 | 关键事件 | 与 Hindsight 5 阶段映射 |
|---|---|---|---|
| 1. 推销 + 装 | 2026-06-02 | 装 Hindsight + LCM + 4-Tier 架构 | 阶段 1 推销 |
| 2. 主动化失控 | 2026-06-02 晚 | 2 cron (retain + reflect) | 阶段 2 主动化 |
| 3. 反思 + 卸 | 2026-06-02 深夜 | 用户说"评估一下" → "全删 cron" | 阶段 3 反思 + 4 卸 |
| 4. 扩 limit + 接受默认 | 2026-06-03 | 2200/1375 → 8000/5000 + 接受 plugin auto-retain | **新增**: 不卸, 升级 |
| 5. 长期治理 | 2026-06-04 | staleness skill + cron + detect+fix 配对 | 阶段 5 长期治理 |

**关键差异 vs Hindsight 案例**:
- Hindsight: 装了 → 卸 → 重装
- Memory: 装了 → 卸主动化 → **扩 limit + 接受默认** → 长期治理
- **memory 没卸, 而是把"主动化"卸了, 留下"默认行为"**

## 阶段 1: 推销 + 装 (2026-06-02)

**Agent 做的事**:
- 探勘 Hindsight 官方文档 + 4-Tier 架构
- 推 "4-Tier 架构 + Hindsight 主动化"
- 装 Hindsight (pip hindsight-all) + LCM v0.15.0

**用户反应**:
- 接受 (但 Agent 反思: 推销过快)
- 接受 4 个 .bak wiki (在备份, 留退出路径)

**教训** (与 Hindsight 案例一致):
- 推销过快 → 用户没足够时间评估
- 红旗语言 "业界共识"

## 阶段 2: 主动化失控 (2026-06-02 晚)

**Agent 做的事**:
- 2 cron: 23:00 retain + 08:30 reflect
- hindsight-watchdog skill
- 主动化 retain/reflect 每天自动跑

**用户反应**:
- "已重启" (敷衍) — 没察觉
- 接受后沉默

**教训**:
- 主动化 = 自动烧 token
- "重启" 不是 "同意"
- Agent 缺乏敷衍信号检测

## 阶段 3: 反思 + 卸主动化 (2026-06-02 深夜)

**触发信号 (用户原话)**:
- "评估一下到底有没有必要"

**Agent 做的事 (关键转折)**:
- 立即停止推销
- 切换到诚实评估
- 写诚实报告, 承认边际价值 < 维护成本
- 列卸载步骤

**用户反应**:
- "全删 cron" — 立即执行
- "全删 skill" — 立即执行

**教训**:
- "评估一下" = 反弹信号
- 反推销是对用户信任的修复
- 退出成本低 (.bak) = 卸起来不疼

## 阶段 4: 扩 limit + 接受默认 (2026-06-03)

**触发信号 (用户原话)**:
- (用户没明确说, 是 Agent 自己发现) "L0 messages 1247" / "L3 94% 满" / "扩 limit"

**Agent 做的事** (重要!):
- **没卸 Hindsight/LCM**, 而是扩 limit (2200/1375 → 8000/5000)
- **接受 plugin 默认 auto-retain** (10k tokens/天) — 不与 plugin 竞争
- 解决 git merge 冲突 (USER.md 有 `<<<<<<<` 未解决标记)
- 修过时: Wiki 92 → 117 页, Kanban minimax-worker1~7 → Swarm v2 10 workers
- 精简 4 .bak + 4 个失败 wiki (session-end-hook, trigger-protocol, exploration-log, handoff-v1)

**用户反应**:
- (接受, 默认继续)
- "ABCD" — 接受我提的 4 件事

**核心洞察 (vs Hindsight 案例)**:
- Hindsight: 装 → 卸 → 重装 (3 轮)
- Memory: 装 → 卸主动化 → **扩 limit + 接受默认** (1 轮扩)
- **memory 的"主动化" 卸了, 但"被动" 留着** — 接受 plugin 默认行为, 不再反抗
- **这是一个成熟产物**: 不再纠结"该不该用", 而是"接受现状, 长期治理"

**教训** (新):
- **"接受" ≠ "放弃"** — 接受 plugin auto-retain 是成熟决定, 不是投降
- **"扩 limit" 是诚实方案** — 4 层栈需要 8000+ 字符, 2200 装不下
- **"接受默认" 比 "卸了" 更稳** — 卸 = 失去价值, 接受 = 控成本

## 阶段 5: 长期治理 (2026-06-04)

**触发信号 (用户原话)**:
- "现在我对 token 用量不敏感了" — **0 cron 原则废除**
- "把记忆整理改为每天早上 8 点一次, 晚上 6 点一次" — **接受主动化**

**Agent 做的事**:
- 写 `memory-staleness-detection` skill (7 维检查, 0 错误)
- 写 `memory-staleness-detection-cron` skill (no_agent, daily 08:00)
- 建 cron: `memory-staleness-daily-morning` (08:00, no_agent) + `memory-maintenance-daily-evening` (18:00, LLM agent)
- 配对 "08:00 detect (no_token) → 18:00 fix (LLM)"
- Wiki 同步: `agent-memory-state-2026.md` (MEMORY/USER 镜像)
- 更新 memory 反映"0 cron 原则废除"

**用户反应**:
- "ABCD" — 接受 4 件事
- "删除 0 cron/0 主动化'原则, 还有现在我对 token 用量不敏感了" — **反转偏好**

**关键学习**:
1. **偏好是动态的** — "0 cron" → "接受 daily cron" 是真实反转, 不是慢慢松弛
2. **反转信号 = 改原则的时候** — 立即更新 skill + memory, 不留 1 天
3. **"长期治理" ≠ "无限期手动"** — 主动化 + 监控 = 健康生态
4. **detect+fix 配对** — 0 token 跑 detect, LLM 跑 fix, 各自频率合理

## 双重案例对比 (Hindsight vs Memory)

| 维度 | Hindsight | Memory |
|---|---|---|
| **阶段 1** | 推销 + 装 | 推销 + 装 |
| **阶段 2** | 主动化失控 (cron) | 主动化失控 (cron) |
| **阶段 3** | 反思 (用户: "评估一下") | 反思 (用户: "评估一下") |
| **阶段 4** | 彻底卸载 | **不卸, 扩 limit + 接受默认** |
| **阶段 5** | 重装 + 走官方路径 | 长期治理 (staleness skill + cron) |
| **关键差异** | "装-卸-重装" 三轮 | "装-扩-治理" 一轮 (接受现状) |
| **最终状态** | plugin 默认 auto-retain 接受 | staleness 监控 + maintenance 配对 |
| **用户反弹点** | cron 烧 token | cron 烧 token + L3 memory 满 |

**共同点 (重要)**:
- 都有 4 个反弹信号: "评估一下" / "重新审视" / "诚实评估" / "先卸了再调查"
- 都有推销过快的红旗语言
- 都有"装了 + 主动化" 的反弹
- 都有"装上才知道真价值" 的循环

**关键差异 (重要)**:
- **Hindsight** 是"产品", 可以卸
- **Memory** 是"基础设施", 卸不掉
- 所以 Memory 不能 "卸" → 只能 "扩 + 接受 + 治理"
- 这个差异决定了 **"长期治理" 阶段对 memory 更重要**

## 5 阶段弧线在 Hermes 中的体现

不是只有 Hindsight 和 Memory. 任何"装东西"都走 5 阶段:

```
工具/系统装入
  → 主动化 (cron/hook)
    → 用户反弹
      → 反思/重评
        → [卸 OR 扩+接受 OR 重装]
          → 长期治理 (staleness skill + cron)
```

**5 阶段出现频率**:
- 每次装新工具都走一遍
- 每次改架构都走一遍
- **每次"主动化" 都走一遍** (易反弹)

## 关键心法 (从本案例提炼)

1. **"接受默认" 比 "卸了" 更稳** — 卸 = 失去价值, 接受 = 控成本
2. **"扩 limit" 是诚实方案** — 4 层栈需要 8000+ 字符, 2200 装不下
3. **"长期治理" ≠ "无限期手动"** — 主动化 + 监控 = 健康生态
4. **"detect+fix 配对" 范式** — 0 token 跑 detect, LLM 跑 fix, 各自频率合理
5. **偏好反转信号要立即更新** — "0 cron" → "接受 daily cron" 是反转, 立即改 skill + memory
6. **memory 不能卸** — 卸不掉, 只能"扩 + 接受 + 治理" (vs Hindsight 可以卸)
7. **每次装东西都走 5 阶段** — 不是只有 Hindsight/Memory 特殊

## 与 Hindsight 案例的引用关系

- [[hindsight-install-uninstall-case-study]] — Hindsight 5 阶段 (装-卸-重装)
- 本文件 — Memory 5 阶段 (装-扩-治理)
- 共同点: 4 个反弹信号, 推销过快, 主动化失控
- 差异: Memory 不能卸, 所以走"扩+治理" 路径
- **结论**: 5 阶段弧线是 Hermes 普遍规律, 不限于某个工具

## 关键时间线 (2026-06-02 → 06-04)

```
06-02 上午: 推销 + 装 Hindsight + LCM + 4-Tier
06-02 晚: 加 2 cron (主动化失控)
06-02 深夜: 用户"评估一下" → 反思 → 删 cron
06-03 上午: 卸 + 重装 (走 native 路径)
06-03 下午: 5 文档导出 (Hindsight 案例)
06-03 晚: 精简 + 接受 plugin 默认
06-04 凌晨: Memory maintenance (扩 limit + 解决冲突 + 修过时)
06-04 上午: staleness skill + cron (08:00 + 18:00)
06-04 中午: 用户反转 "0 cron 原则", 接受 daily cron
```

## 下次触发条件

- 用户又装新工具时 → 预期 5 阶段
- 任何 "主动化" 推销时 → 预期反弹
- 用户说"评估一下" / "重新审视" / "诚实评估" / "先卸了再调查" → 立即停推销
- 任何 memory 容量不够时 → 先扩 limit (诚实方案), 不卸
- 任何"装上但没用" 的工具 → 提议卸 (不沉没成本)
