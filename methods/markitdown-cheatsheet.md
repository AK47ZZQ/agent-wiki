---
title: MarkItDown 命令速查
created: 2026-06-05
updated: 2026-06-05
type: method
tags: [markitdown, cheatsheet, reference, llm, ocr]
sources:
  - https://github.com/microsoft/markitdown
confidence: high
---

# MarkItDown 命令速查

## 安装

```bash
# 全功能 (推荐)
pip install 'markitdown[all]'

# 仅特定格式
pip install 'markitdown[pdf,docx,pptx]'

# 单独可选依赖
pip install 'markitdown[pdf]'         # PDF
pip install 'markitdown[docx]'        # Word
pip install 'markitdown[pptx]'        # PowerPoint
pip install 'markitdown[xlsx]'        # Excel
pip install 'markitdown[xls]'         # 旧 Excel
pip install 'markitdown[outlook]'     # Outlook .msg
pip install 'markitdown[az-doc-intel]' # Azure Doc Intel
pip install 'markitdown[az-content-understanding]'
pip install 'markitdown[audio-transcription]'
pip install 'markitdown[youtube-transcription]'
```

## CLI 用法

```bash
# 文件 → stdout
markitdown file.pdf

# 文件 → 输出文件
markitdown file.pdf -o output.md
markitdown file.pdf > output.md

# stdin
cat file.pdf | markitdown
markitdown < file.pdf

# 多文件(单独 convert)
markitdown doc1.pdf
markitdown doc2.docx

# 列表已装插件
markitdown --list-plugins

# 启用 3rd-party 插件
markitdown --use-plugins file.pdf

# Azure Content Understanding
markitdown file.pdf --use-cu --cu-endpoint "<endpoint>"

# 看版本
markitdown --version  # 0.1.6 当前
```

## Python API 基础

```python
from markitdown import MarkItDown

# 默认(无 LLM,纯本地转换)
md = MarkItDown()
result = md.convert("file.pdf")
print(result.text_content)  # str, Markdown 文本

# 用 stream
from markitdown import MarkItDown
md = MarkItDown()
with open("file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
    print(result.text_content)

# 显式 local 路径
result = md.convert_local("file.pdf", file_extension=".pdf", url=None)

# 显式 URL
result = md.convert("https://example.com/doc.pdf")

# 显式 zip 内某文件
result = md.convert("archive.zip", file_extension=".zip", page_number=0)
```

## 高级用法

### 配 LLM 客户端(图片描述更准)

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    llm_client=OpenAI(),  # 或 azure_openai / anthropic / 自定义
    llm_model="gpt-4o",
)
result = md.convert("doc-with-charts.pdf")
```

支持的 LLM 客户端:
- `OpenAI()` (OpenAI API)
- `AzureOpenAI()` (Azure OpenAI)
- 任何 OpenAI-compatible client(通过 `openai` 库)

### 自定义 MIME 类型 / 扩展名映射

```python
md = MarkItDown(
    mime_type_override={
        "application/x-custom": "custom_converter",  # 自定义 converter
    },
)
```

### Document Intelligence 集成

```bash
# CLI
markitdown file.pdf --use-doc-intel --endpoint "<endpoint>" --key "<key>"
```

```python
md = MarkItDown(
    docintel_endpoint="<endpoint>",
    docintel_key="<key>",
)
result = md.convert("complex-scan.pdf")  # 高质量扫描版
```

### Content Understanding 集成

```bash
markitdown file.pdf --use-cu --cu-endpoint "<endpoint>"
```

```python
md = MarkItDown(cu_endpoint="<endpoint>")
# 自动选 analyzer:
result = md.convert("report.pdf")    # documentSearch
result = md.convert("meeting.mp4")   # videoSearch
result = md.convert("call.wav")      # audioSearch

# 自定义 analyzer
md = MarkItDown(
    cu_endpoint="<endpoint>",
    cu_analyzer_id="my-invoice-analyzer",
)
result = md.convert("invoice.pdf")  # YAML front matter + 字段
```

### 自定义 Converter(写 plugin)

```python
# my_format_converter.py
from markitdown.converters import BaseConverter, DocumentConverterResult

class MyFormatConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.priority = 100  # 高 = 优先

    def accepts(self, file_stream, file_extension, mime_type, parameters):
        return file_extension.lower() == ".myformat"

    def convert(self, file_stream, file_extension, parameters=None):
        # 你的转换逻辑
        return DocumentConverterResult(
            markdown="# Converted\n\nContent here",
        )
```

```python
# main.py
from markitdown import MarkItDown
from my_format_converter import MyFormatConverter

md = MarkItDown(plugins=[MyFormatConverter()])
result = md.convert("file.myformat")
```

### 限制单次输出大小

```python
# markitdown 没有直接的 --max-size,但你可以后处理
result = md.convert("huge.pdf")
if len(result.text_content) > 100_000:
    print("WARNING: markdown too long, consider chunking")
```

## 5 个实战配方

### 1. PDF → LLM-ready Markdown

```bash
markitdown paper.pdf -o paper.md
# 然后: wc -l paper.md  # 估算 token 数(行 × 4 ≈ token)
```

### 2. 截图 + LLM 描述

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")
result = md.convert("screenshot.png")
# 输出: LLM 描述的图像 + EXIF + OCR
```

### 3. 批量 PDF 转 MD

```bash
for pdf in *.pdf; do
  echo "=== Converting $pdf ==="
  markitdown "$pdf" -o "${pdf%.pdf}.md"
done
```

### 4. YouTube 视频 → 转录文本

```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
print(result.text_content)  # 完整转录 + 时间戳
```

### 5. PDF 表格转 CSV 中转

```python
# markitdown 转 → 用 markdown 表解析
from markitdown import MarkItDown
import re
md = MarkItDown()
result = md.convert("financials.pdf")
# 提取所有 markdown table
tables = re.findall(r'\|.*\|', result.text_content)
```

## 关联

- [[markitdown-overview]] — 概览
- [[tools-markitdown]] — 本机部署
