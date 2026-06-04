# MarkItDown Command Cheatsheet (Full)

## Install

```bash
pip install 'markitdown[all]'                      # all formats
pip install 'markitdown[pdf,docx,pptx]'           # subset
pip install 'markitdown[pdf]'                      # PDF only
pip install 'markitdown[pptx]'                     # PowerPoint only
pip install 'markitdown[docx]'                     # Word only
pip install 'markitdown[xlsx]'                     # Excel (.xlsx) only
pip install 'markitdown[xls]'                      # Old Excel (.xls)
pip install 'markitdown[outlook]'                  # Outlook .msg
pip install 'markitdown[az-doc-intel]'             # Azure Doc Intel
pip install 'markitdown[az-content-understanding]' # Azure Content Understanding
pip install 'markitdown[audio-transcription]'      # WAV/MP3 transcription
pip install 'markitdown[youtube-transcription]'    # YouTube transcripts
```

## CLI

### Basic

```bash
markitdown <file>              # to stdout
markitdown <file> -o <out>     # to file
markitdown <file> > <out>       # to file (shell redirect)
cat <file> | markitdown         # from stdin
markitdown < <file>             # from stdin (shell redirect)
markitdown --version            # version
markitdown --help               # all flags
```

### Plugins

```bash
markitdown --list-plugins       # show installed 3rd-party plugins
markitdown --use-plugins <file> # enable plugin conversion path
```

### Azure Integrations

```bash
# Content Understanding (multimodal: doc/image/audio/video)
markitdown file.pdf \
  --use-cu \
  --cu-endpoint "https://<your-cu>.services.ai.azure.com/"

# Document Intelligence (document layout analysis)
markitdown file.pdf \
  --use-doc-intel \
  --endpoint "https://<your-doc-intel>.cognitiveservices.azure.com/" \
  --key "<your-key>"

# Custom Content Understanding analyzer
markitdown invoice.pdf \
  --use-cu \
  --cu-endpoint "<endpoint>" \
  --cu-analyzer-id "my-invoice-analyzer"
```

## All CLI Flags (markitdown 0.1.6)

| Flag | Description |
|---|---|
| `filename` | Positional. Path to input file (omit for stdin) |
| `-o, --output` | Output file path (default: stdout) |
| `--list-plugins` | List installed 3rd-party plugins |
| `--use-plugins` | Enable 3rd-party plugin conversion |
| `--use-cu` | Use Azure Content Understanding |
| `--cu-endpoint` | Azure CU endpoint URL |
| `--cu-analyzer-id` | Custom CU analyzer (for domain-specific field extraction) |
| `--cu-file-types` | Restrict which formats route to CU (comma-separated) |
| `--use-doc-intel` | Use Azure Document Intelligence |
| `--endpoint` | Azure Doc Intel endpoint URL |
| `--key` | Azure Doc Intel API key |
| `--llm-client` | OpenAI-compatible client (Python API only) |
| `--llm-model` | Model name (Python API only) |
| `--version` | Show version |
| `--help` | Show help |

## Python API

### MarkItDown Class

```python
from markitdown import MarkItDown

md = MarkItDown(
    llm_client=None,                    # OpenAI-compatible client (or None)
    llm_model=None,                     # model name string
    enable_plugins=False,               # enable 3rd-party plugins
    docintel_endpoint=None,
    docintel_key=None,
    cu_endpoint=None,
    cu_analyzer_id=None,
    cu_file_types=None,                 # list of ContentUnderstandingFileType
    plugins=None,                       # list of custom converters
    mime_type_override=None,            # dict of mime → converter
)
```

### Convert Methods

```python
# 1. convert — auto-detect format
result = md.convert("file.pdf")
result = md.convert("https://example.com/file.pdf")
result = md.convert("archive.zip", page_number=2)  # ZIP entry index

# 2. convert_stream — for in-memory bytes
with open("file.pdf", "rb") as f:
    result = md.convert_stream(f, file_extension=".pdf")

# 3. convert_local — explicit local file
result = md.convert_local("file.pdf", file_extension=".pdf", url=None)

# 4. convert_url — explicit URL
result = md.convert_url("https://example.com/file.pdf")
```

### Result Object

```python
result = md.convert("file.pdf")
result.text_content     # str — Markdown text
result.markdown         # alias for text_content
result.title            # str | None — detected title
result.metadata         # dict — extra metadata (EXIF, etc.)
```

## LLM Client Configurations

### OpenAI

```python
from openai import OpenAI
md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")
```

### Azure OpenAI

```python
import os
from openai import AzureOpenAI
md = MarkItDown(
    llm_client=AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-02-15-preview",
    ),
    llm_model="gpt-4o",
)
```

### Anthropic (via OpenAI-compatible proxy)

```python
from openai import OpenAI
md = MarkItDown(
    llm_client=OpenAI(
        base_url="https://api.anthropic.com/v1/",  # or proxy URL
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    ),
    llm_model="claude-3-5-sonnet-20241022",
)
```

### Local LLM (Ollama)

```python
from openai import OpenAI
md = MarkItDown(
    llm_client=OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"),
    llm_model="llama3.2-vision",
)
```

## Plugin Development

```python
# my_plugin.py
from markitdown.converters import BaseConverter, DocumentConverterResult

class MyConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.priority = 100  # higher = checked first

    def accepts(self, file_stream, file_extension, mime_type, parameters):
        return file_extension.lower() == ".myformat"

    def convert(self, file_stream, file_extension, parameters=None):
        # Your logic here
        return DocumentConverterResult(
            markdown="# My Format\n\nConverted content...",
            title="My Doc",
            metadata={"source": "myformat"},
        )
```

```python
# Usage
from markitdown import MarkItDown
from my_plugin import MyConverter

md = MarkItDown(plugins=[MyConverter()])
result = md.convert("file.myformat")
```

Find community plugins: GitHub hashtag `#markitdown-plugin`.

## Supported Formats (2026-06)

| Format | Extra | Notes |
|---|---|---|
| PDF | `[pdf]` | pdfminer / pdfplumber |
| PowerPoint | `[pptx]` | python-pptx |
| Word | `[docx]` | mammoth |
| Excel | `[xlsx]` | pandas / openpyxl |
| Old Excel | `[xls]` | xlrd |
| Outlook | `[outlook]` | extract-msg |
| Images (OCR) | built-in | PIL + pytesseract (or LLM Vision) |
| Audio (transcription) | `[audio-transcription]` | speech_recognition / Whisper |
| YouTube | `[youtube-transcription]` | youtube-transcript-api |
| HTML | built-in | BeautifulSoup |
| CSV / JSON / XML | built-in | native Python |
| ZIP | built-in | iterates entries |
| EPUB | built-in | ebooklib |
| Azure Doc Intel | `[az-doc-intel]` | cloud layout analysis |
| Azure Content Understanding | `[az-content-understanding]` | multimodal + fields |
