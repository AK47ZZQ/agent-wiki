---
title: MarkItDown 本机部署
created: 2026-06-05
updated: 2026-06-05
type: agent
tags: [markitdown, deploy, hermes-main, windows]
sources:
  - https://github.com/microsoft/markitdown
deploy_status: deployed
confidence: high
---

# MarkItDown 本机部署 (main-claude 节点)

> 状态: ✅ **已装 0.1.6** (2026-06-05 00:14 实测)

## 1. 安装

```bash
# 推荐:全功能
pip install 'markitdown[all]'

# ⚠️ 本机坑:Hindsight plugin 锁 markitdown<0.1.4
# 默认会装 0.0.2(过时),要 --ignore-requires 强制升级
pip install --upgrade --ignore-requires 'markitdown[all]==0.1.6'
```

**验证**:
```bash
$ pip show markitdown
Name: markitdown
Version: 0.1.6
```

```bash
$ markitdown --version
markitdown 0.1.6
```

## 2. 基础用法测试

```bash
# 文本往返(txt → md)
echo "# Hello" | markitdown

# 真转一个文件
markitdown /tmp/test.md -o /tmp/out.md

# 跑个 python API
python -c "from markitdown import MarkItDown; print(MarkItDown().convert('README.md').text_content[:200])"
```

## 3. LLM 集成(可选)

如果想用 markitdown 把图片描述得更准(走 LLM Vision):

```bash
# 1. 装 OpenAI 客户端(已装)
pip show openai  # 应有 1.x+

# 2. 配 OPENAI_API_KEY
export OPENAI_API_KEY=sk-...

# 3. 跑
python -c "
from markitdown import MarkItDown
from openai import OpenAI
md = MarkItDown(llm_client=OpenAI(), llm_model='gpt-4o')
result = md.convert('screenshot.png')
print(result.text_content)
"
```

## 4. Azure 集成(可选,需订阅)

```bash
# Document Intelligence
export AZURE_DOC_INTEL_ENDPOINT=*** tier=document-intelligence
export AZURE_DOC_INTEL_KEY=*** key

# Content Understanding
export AZURE_CU_ENDPOINT=*** tier=content-understanding
```

## 5. 已知陷阱(本机特别)

1. **pip 默认装 0.0.2** — Hindsight 锁住 markitdown<0.1.4,**必须 `--ignore-requires` 装 0.1.6**
2. **Hindsight 可能因此 broken** — 升级 markitdown 后,如果 `hindsight` 命令报缺 `markitdown[docx,pdf,pptx,xls,xlsx]>=0.1.4`,可降级回 0.1.4(够 Hindsight 用,也够 99% 场景)
3. **MSYS bash 路径** — markitdown 用 `pathlib`,Windows 路径 OK,但 `cat file.pdf | markitdown` 在 MSYS 下 stdin 编码可能破坏
4. **C盘中文用户名** — `C:\Users\Administrator\` 路径 OK,不要有空格

## 6. 跟其他工具的协同

| 工作流 | 工具 |
|---|---|
| **PDF → LLM** | `markitdown paper.pdf` → 直接喂 prompt |
| **PDF → Obsidian vault** | `markitdown paper.pdf -o ~/vault/paper.md` |
| **截图 → LLM** | `MarkItDown(llm_client=OpenAI()).convert("ss.png")` |
| **YouTube → 笔记** | `MarkItDown().convert("https://youtu.be/...")` |
| **批量 PDF → MD** | `for pdf in *.pdf; do markitdown "$pdf" -o "${pdf%.pdf}.md"; done` |

## 7. 部署 checklist

- [x] `markitdown --version` = `0.1.6`
- [x] `pip show markitdown` 显示 0.1.6
- [x] 基础转换工作(实跑 txt → md)
- [ ] OpenAI 客户端(可选,跑 LLM 增强才需要)
- [ ] Azure 凭证(可选,跑云 API 才需要)

## 8. 卸载

```bash
pip uninstall markitdown
# 可选:清依赖
pip uninstall -y markitdown[all]
```

**警告**:卸载 markitdown 会**断 Hindsight**(如果它在用)。重装 `pip install 'markitdown[docx,pdf,pptx,xls,xlsx]>=0.1.4'` 恢复。

## 关联

- [[markitdown-overview]] — 概览
- [[markitdown-cheatsheet]] — 命令速查
- [[main-claude]] — 本机节点
