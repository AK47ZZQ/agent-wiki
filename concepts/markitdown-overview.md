---
title: MarkItDown 概览
created: 2026-06-05
updated: 2026-06-05
type: concept
tags: [markitdown, microsoft, conversion, pdf, llm, ocr]
sources:
  - https://github.com/microsoft/markitdown
  - https://pypi.org/project/markitdown/
confidence: high
---

# MarkItDown 概览

## 一句话定义

**Microsoft 出品的轻量级 Python 工具,把各种文件格式转 Markdown** — 专为 LLM 文本分析设计,不是给人类阅读的"高保真"转换器。

## 核心定位

| 维度 | markitdown | Pandoc | textract | Azure Document Intelligence |
|---|---|---|---|---|
| **目标输出** | Markdown (LLM 友好) | 多格式 | 纯文本 | JSON + Markdown |
| **LLM 优化** | ✅ 主目标 | ❌ 通用 | ❌ | ❌ |
| **离线** | ✅ 全本地 | ✅ | ✅ | ❌ 云 API |
| **PDF** | ✅ pdfminer/pdfplumber | ✅ | ✅ | ✅(高质量) |
| **Office** | ✅ pptx/docx/xlsx | ✅ | ✅ | ❌ |
| **图片 OCR** | ✅ EXIF + 内置 | ❌ | ✅ | ✅ |
| **音频转录** | ✅ speech_recognition | ❌ | ✅ | ❌ |
| **YouTube** | ✅ youtube-transcript-api | ❌ | ❌ | ❌ |
| **插件** | ✅ 3rd-party | ✅ 滤镜 | ❌ | ❌ |
| **⭐** | 11万+ | 35K+ | 4K+ | 闭源 |

## 支持的文件格式(2026-06 最新)

- **文档**: PDF, PowerPoint (pptx), Word (docx), Excel (xlsx/xls)
- **图片**: PNG/JPG/BMP/WebP(EXIF 元数据 + 内置 OCR)
- **音频**: WAV/MP3(EXIF + speech-to-text via Whisper / Google)
- **网页**: HTML
- **结构化数据**: CSV, JSON, XML
- **压缩包**: ZIP(迭代内部)
- **URL**: YouTube 链接(自动取转录)
- **电子书**: EPUB
- **Outlook**: msg 文件
- **Azure 集成**: Document Intelligence + Content Understanding

## 三大使用模式

### 1. CLI(最简单)

```bash
markitdown file.pdf > out.md
markitdown file.pdf -o out.md
cat file.pdf | markitdown
```

### 2. Python API(可编程)

```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("file.pdf")
print(result.text_content)  # markdown 字符串
```

### 3. 插件 + LLM 增强

```python
from markitdown import MarkItDown
from openai import OpenAI
md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")
result = md.convert("doc-with-images.pdf")  # LLM 看图 + 描述
```

## 为什么选 Markdown(给 LLM 喂)

- ✅ LLM 训练数据含大量 Markdown,**natively "speak" Markdown**(GPT-4o 默认响应带 MD 格式)
- ✅ Markdown 接近纯文本,**token-efficient**(比 HTML 少 30-50% tokens)
- ✅ 保留结构(标题/列表/表格/链接)而不带格式噪音(字体/颜色/布局)
- ✅ 输出可直接喂给 RAG / context / prompt,无需清洗

## 与本机其他工具的关系

| 工具 | 用途 | 与 markitdown 关系 |
|---|---|---|
| `pdf-extract` skill | PDF 文本提取 | 替代场景(纯文本) |
| `ocr-and-documents` skill | PDF/图片 OCR | markitdown 已含 OCR |
| `nano-pdf` skill | PDF 编辑 | 完全不同方向(edit vs convert) |
| `obsidian` skill | 写 MD 到 vault | **互补**:markitdown 转,Obsidian 接收 |
| `feishu_doc_read` skill | 读飞书文档 | 不同源(飞书 vs 本地文件) |

## 安装状态(本机 2026-06-05)

```
$ pip show markitdown
Version: 0.1.6
```

✅ 已装。⚠️ **冲突**:Hindsight plugin 要求 `markitdown[docx,pdf,pptx,xls,xlsx]>=0.1.4`,已装 0.1.6 → OK;但 pip 默认会装 0.0.2,**需要 `--ignore-requires`** 强制升级。

## 5 个最常见 footgun

1. **PDF 转出来是空**:可能是扫描版 PDF(没文字层)→ 用 `markitdown-ocr` 插件 + LLM Vision
2. **图片不显示**:markitdown 默认把图片描述成 `![](path)`,不会内嵌 base64 → 喂 LLM 前手动处理
3. **大文件 OOM**:100+ MB PDF 一次 convert 会爆 → 用 `--keep-data-uris` + 切片
4. **表格丢失**:Excel 复杂表头/合并单元格会被打平 → 先 `.to_csv()` 再 markitdown
5. **Hindsight 锁版本**:Hindsight 要求 markitdown>=0.1.4,但默认装 0.0.2 → 装新版本要 `--ignore-requires`

## 关联

- [[markitdown-cheatsheet]] — L1-L2 命令 + API 速查
- [[tools-markitdown]] — 本机部署 + 验证
- [[main-claude]] — 用 markitdown 的实际场景
