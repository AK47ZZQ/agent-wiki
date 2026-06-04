---
name: markitdown-converter
description: "Use when the user wants to convert PDF, Word, PowerPoint, Excel, images (with OCR), audio (with transcription), HTML, YouTube URLs, or other files to Markdown for LLM consumption or Obsidian ingestion. Covers CLI usage, Python API, optional LLM-enhanced image descriptions, Azure integrations, plugin development, and known pitfalls. Pairs with obsidian-ingest workflows."
emoji: 📝
vibe: "File-to-Markdown for LLM ingestion — Microsoft's quiet workhorse"
color: amber
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [markitdown, conversion, pdf, llm, ocr, ocr-and-documents, obsidian, ingestion]
    related_skills: [ocr-and-documents, obsidian, pdf-extract, feishu-doc-read]
---

# MarkItDown — File-to-Markdown Converter

Microsoft's lightweight Python utility for converting various file formats to Markdown. **Designed for LLM ingestion** — output is meant to be fed to text analysis tools, not for high-fidelity human reading.

## When to Use

- User has a PDF / DOCX / PPTX / XLSX file and wants to chat with it
- User wants to convert a screenshot or image to text (OCR + LLM description)
- User wants YouTube video transcription as Markdown
- User wants to extract structured data from CSVs / JSONs / XMLs to MD tables
- User wants to feed an Office file to a downstream LLM / RAG pipeline
- User wants to convert ZIP contents to MD for batch ingestion
- User wants to write a custom converter (plugin) for a new format

**Don't use for**:
- "Edit my PDF" / "modify this Word doc" → use proper Office tools (nano-pdf, etc.)
- "High-fidelity conversion for human reading" → use Pandoc (markitdown is LLM-targeted)
- "Convert Markdown TO something else" → use Pandoc, not markitdown

---

## 0. Detection

```bash
# Is markitdown installed?
command -v markitdown && markitdown --version || echo "NOT_INSTALLED"

# Or check via Python
python -c "import markitdown; print(markitdown.__version__ if hasattr(markitdown, '__version__') else 'imported OK')"
```

**Decision matrix**:

| Installed | Action |
|---|---|
| ✅ | Proceed with `markitdown` CLI or Python API |
| ❌ | Install: `pip install 'markitdown[all]'` (or `[pdf,docx,pptx,xlsx]` for specific formats) |
| ❌ + Hindsight in env | `pip install --upgrade --ignore-requires 'markitdown[all]==0.1.6'` (Hindsight locks old version) |

---

## 1. Install

Reference: `references/install.md`.

```bash
# Full features (recommended)
pip install 'markitdown[all]'

# Specific formats only (smaller footprint)
pip install 'markitdown[pdf,docx,pptx]'

# Single formats
pip install 'markitdown[pdf]'
pip install 'markitdown[pptx]'
pip install 'markitdown[xlsx]'
pip install 'markitdown[audio-transcription]'
pip install 'markitdown[youtube-transcription]'
```

**Verify**:
```bash
markitdown --version  # expect 0.1.x
```

---

## 2. CLI Quick Reference

```bash
# File to stdout
markitdown file.pdf

# File to output file
markitdown file.pdf -o output.md
markitdown file.pdf > output.md

# Stdin
cat file.pdf | markitdown
markitdown < file.pdf

# List installed plugins
markitdown --list-plugins

# Enable 3rd-party plugins (e.g. markitdown-ocr)
markitdown --use-plugins file.pdf

# Azure Content Understanding (high quality cloud conversion)
markitdown file.pdf --use-cu --cu-endpoint "<endpoint>"

# Azure Document Intelligence
markitdown file.pdf --use-doc-intel --endpoint "<endpoint>" --key "<key>"
```

Full cheatsheet: `references/command-cheatsheet.md`.

---

## 3. Python API

```python
from markitdown import MarkItDown

# Basic (offline, no LLM)
md = MarkItDown()
result = md.convert("file.pdf")
print(result.text_content)  # Markdown string

# With LLM-enhanced image descriptions
from openai import OpenAI
md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")
result = md.convert("screenshot.png")
# Output: LLM describes the image content + EXIF + OCR

# Stream API (for in-memory bytes)
with open("file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")
    print(result.text_content)

# URL (e.g. YouTube)
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
print(result.text_content)  # Full transcript with timestamps

# Azure Content Understanding
md = MarkItDown(cu_endpoint="<endpoint>")
result = md.convert("report.pdf")  # YAML front matter + fields
```

Full API reference: `references/python-api.md`.

---

## 4. Common Workflows

### 4a. PDF → Obsidian Vault

```bash
markitdown paper.pdf -o ~/Obsidian/vault/papers/paper.md
```

### 4b. PDF → LLM prompt

```bash
PROMPT=$(cat prompt.md)
CONTENT=$(markitdown paper.pdf)
echo "$PROMPT

$CONTENT" | llm-cli
```

### 4c. Screenshot → structured description

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")
result = md.convert("screenshot.png")
# Save to Obsidian or paste into chat
```

### 4d. Batch conversion

```bash
for pdf in *.pdf; do
  echo "Converting $pdf"
  markitdown "$pdf" -o "${pdf%.pdf}.md"
done
```

### 4e. YouTube video → transcript

```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
# result.text_content has full transcript with timestamps
```

---

## 5. LLM Client Setup

markitdown uses an OpenAI-compatible client for image description and OCR.

```python
# OpenAI
from openai import OpenAI
md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")

# Azure OpenAI
from openai import AzureOpenAI
md = MarkItDown(
    llm_client=AzureOpenAI(
        azure_endpoint="https://YOUR.openai.azure.com/",
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-02-15-preview",
    ),
    llm_model="gpt-4o",
)

# Local LLM (e.g. via ollama)
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
md = MarkItDown(llm_client=client, llm_model="llama3.2-vision")
```

---

## 6. Custom Converters (Plugins)

```python
# my_format_converter.py
from markitdown.converters import BaseConverter, DocumentConverterResult

class MyFormatConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.priority = 100

    def accepts(self, file_stream, file_extension, mime_type, parameters):
        return file_extension.lower() == ".myformat"

    def convert(self, file_stream, file_extension, parameters=None):
        # Your conversion logic
        return DocumentConverterResult(markdown="# Converted\n\n...")
```

```python
# main.py
from markitdown import MarkItDown
from my_format_converter import MyFormatConverter

md = MarkItDown(plugins=[MyFormatConverter()])
result = md.convert("file.myformat")
```

Find community plugins: GitHub hashtag `#markitdown-plugin`.

---

## 7. Common Pitfalls

1. **pip installs old version (0.0.2)** when Hindsight is in the environment. **Fix**: `pip install --upgrade --ignore-requires 'markitdown[all]==0.1.6'`.

2. **Empty PDF output** for scanned PDFs (no text layer). **Fix**: Install `markitdown-ocr` plugin + provide `llm_client` for LLM Vision OCR.

3. **Images become `![](path)`** in output, not base64-embedded. The LLM won't see them in the markdown itself. **Fix**: Provide `llm_client` so markitdown describes images inline.

4. **Excel complex tables are flattened** (merged cells, multi-level headers). **Fix**: Pre-export to CSV and pass that to markitdown.

5. **Large PDFs cause OOM** (100+ MB). **Fix**: Split PDF into pages first (`pypdf` / `pdftk`), or use `--use-doc-intel` for cloud-based chunked processing.

6. **YouTube transcription may fail** for private/live streams. **Fix**: Use `youtube-transcript-api` directly with fallback to `youtube-dl` for download + Whisper for transcription.

7. **Azure CU bills per call**. **Fix**: Use `cu_file_types` to restrict routing.

8. **CLI flag is `--use-plugins` (with hyphen)**, not `--use-plugin`.

9. **Default `llm_client` is `None`**, so image descriptions are auto-generated by alt-text only (no LLM Vision).

10. **`convert_local` vs `convert_stream`**: use the former for file paths, the latter for in-memory bytes. They have different signatures.

11. **MIME type detection can be wrong on Windows** if the extension is uppercase. **Fix**: Always pass `file_extension` explicitly.

12. **Hindsight breaks if you remove markitdown**. The Hindsight plugin declares it as a hard dependency.

---

## 8. Verification Checklist

- [ ] `markitdown --version` returns 0.1.x (not 0.0.2)
- [ ] `markitdown README.md` works on a small test file
- [ ] For PDF: `markitdown paper.pdf` produces non-empty output
- [ ] For OCR: if installing `markitdown-ocr`, verify with a screenshot
- [ ] For LLM enhancement: `OPENAI_API_KEY` is set and `llm_client=OpenAI()` works
- [ ] For Azure: endpoints and keys are configured; test with `--use-cu` or `--use-doc-intel`

---

## 9. One-Shot Recipes

### "Convert all PDFs in a directory to Markdown, preserving structure"

```bash
mkdir -p converted
for pdf in *.pdf; do
  markitdown "$pdf" -o "converted/${pdf%.pdf}.md"
done
ls -la converted/
```

### "Convert a PDF and check the token count"

```bash
markitdown paper.pdf -o paper.md
# Rough estimate: chars / 4 ≈ tokens
echo "Approx tokens: $(wc -c < paper.md | awk '{print int($1/4)}')"
```

### "Convert a screenshot with LLM description"

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")
result = md.convert("ui-screenshot.png")
with open("ui-screenshot.md", "w") as f:
    f.write(result.text_content)
```

### "Convert a YouTube video and save transcript"

```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
with open("transcript.md", "w") as f:
    f.write(result.text_content)
```

### "Batch convert multiple file types"

```bash
for file in *.{pdf,docx,pptx,xlsx}; do
  [ -f "$file" ] || continue
  ext="${file##*.}"
  markitdown "$file" -o "${file%.*}.md"
done
```

---

## 10. Related Skills

- `ocr-and-documents` — earlier OCR-only workflows; markitdown supersedes for many cases
- `obsidian` — receives Markdown output; use together for "PDF → Obsidian" workflows
- `pdf-extract` — alternative for raw PDF text (no structure preservation)
- `feishu-doc-read` — reads Feishu documents as text (different source, same Markdown goal)
- `nano-pdf` — edits PDFs (not conversion)

---

## 11. References

- `references/install.md` — platform-specific install + verification
- `references/command-cheatsheet.md` — full CLI reference
- `references/python-api.md` — full Python API surface
- `references/troubleshooting.md` — common errors + fixes
- `scripts/convert-file.sh` — wrapper for "convert + check size + report" workflow
- `templates/llm-client-setup.md` — boilerplate for LLM client configuration
