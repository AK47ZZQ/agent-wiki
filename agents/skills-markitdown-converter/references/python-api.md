# MarkItDown Python API Reference

## Core Class

```python
class MarkItDown:
    def __init__(
        self,
        llm_client: Optional[object] = None,
        llm_model: Optional[str] = None,
        enable_plugins: bool = False,
        docintel_endpoint: Optional[str] = None,
        docintel_key: Optional[str] = None,
        cu_endpoint: Optional[str] = None,
        cu_analyzer_id: Optional[str] = None,
        cu_file_types: Optional[list] = None,
        plugins: Optional[list[BaseConverter]] = None,
        mime_type_override: Optional[dict] = None,
        exiftool_path: Optional[str] = None,
    ):
        ...
```

## Convert Methods

### `convert()`

```python
def convert(
    self,
    source: str,                          # file path or URL
    file_extension: Optional[str] = None,  # hint if extension ambiguous
    page_number: Optional[int] = None,     # for ZIP, which entry
    url: Optional[str] = None,             # explicit URL override
    parameters: Optional[dict] = None,     # extra params for converters
) -> DocumentConverterResult:
    ...
```

**Returns**: `DocumentConverterResult` (see below).

### `convert_stream()`

```python
def convert_stream(
    self,
    file_stream: BinaryIO,                 # file-like object (must be binary)
    file_extension: Optional[str] = None,
    mime_type: Optional[str] = None,
    parameters: Optional[dict] = None,
) -> DocumentConverterResult:
    ...
```

### `convert_local()`

```python
def convert_local(
    self,
    file_path: str,
    file_extension: Optional[str] = None,
    url: Optional[str] = None,
    parameters: Optional[dict] = None,
) -> DocumentConverterResult:
    ...
```

### `convert_url()`

```python
def convert_url(
    self,
    url: str,
    file_extension: Optional[str] = None,
    parameters: Optional[dict] = None,
) -> DocumentConverterResult:
    ...
```

## Result Object

```python
class DocumentConverterResult:
    markdown: str                          # The Markdown content
    title: Optional[str] = None            # Detected title
    metadata: dict = {}                    # Extra metadata (EXIF, etc.)

# Backward-compat alias
DocumentConverterResult.text_content  # == .markdown
```

## Custom Converter (Plugin)

```python
from markitdown.converters import BaseConverter, DocumentConverterResult

class BaseConverter:
    def __init__(self):
        self.priority: int = 100           # higher = checked first

    def accepts(
        self,
        file_stream: BinaryIO,
        file_extension: Optional[str],
        mime_type: Optional[str],
        parameters: Optional[dict],
    ) -> bool:
        """Return True if this converter handles this file type."""
        ...

    def convert(
        self,
        file_stream: BinaryIO,
        file_extension: Optional[str],
        parameters: Optional[dict] = None,
    ) -> DocumentConverterResult:
        """Convert and return DocumentConverterResult."""
        ...
```

### Example: CSV with custom delimiter

```python
import csv
from io import StringIO
from markitdown.converters import BaseConverter, DocumentConverterResult

class PipeDelimitedConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.priority = 100

    def accepts(self, file_stream, file_extension, mime_type, parameters):
        return (
            file_extension and file_extension.lower() == ".psv"
        ) or (parameters and parameters.get("delimiter") == "|")

    def convert(self, file_stream, file_extension, parameters=None):
        delimiter = parameters.get("delimiter", "|") if parameters else "|"
        text = file_stream.read().decode("utf-8")
        reader = csv.reader(StringIO(text), delimiter=delimiter)
        rows = list(reader)
        if not rows:
            return DocumentConverterResult(markdown="(empty)")
        header = rows[0]
        body = rows[1:]
        md = "| " + " | ".join(header) + " |\n"
        md += "|" + "|".join(["---"] * len(header)) + "|\n"
        for row in body:
            md += "| " + " | ".join(row) + " |\n"
        return DocumentConverterResult(markdown=md)
```

```python
# Use
from markitdown import MarkItDown
md = MarkItDown(plugins=[PipeDelimitedConverter()])
with open("data.psv", "rb") as f:
    result = md.convert_stream(f, file_extension=".psv")
print(result.markdown)
```

## LLM Client Protocol

markitdown uses an OpenAI-compatible client interface. Any object that supports `chat.completions.create(messages=...)` works.

```python
class LLMClient:
    def chat(self) -> Chat:
        ...

class Chat:
    def completions(self) -> Completions:
        ...

class Completions:
    def create(
        self,
        messages: list[dict],     # [{"role": "user", "content": "..."}, ...]
        model: str,               # model name
        **kwargs,
    ) -> Response:
        ...
```

### Tested Clients

- `openai.OpenAI()` — OpenAI API
- `openai.AzureOpenAI()` — Azure OpenAI
- Any OpenAI-compatible proxy (LiteLLM, Portkey, etc.)
- Custom clients that implement the protocol above

### Vision Support

For image description, the client must support image inputs (vision-capable model):

```python
md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")  # vision
md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o-mini")  # vision
```

## Azure Content Understanding

```python
from markitdown import MarkItDown
from markitdown.converters import ContentUnderstandingFileType

# Zero-config (auto-selects analyzer per file type)
md = MarkItDown(cu_endpoint="https://<endpoint>")
result = md.convert("report.pdf")   # documentSearch
result = md.convert("meeting.mp4")  # videoSearch
result = md.convert("call.wav")     # audioSearch

# Restrict formats routed to CU
md = MarkItDown(
    cu_endpoint="https://<endpoint>",
    cu_file_types=[ContentUnderstandingFileType.PDF],  # only PDFs use CU
)

# Custom analyzer (for field extraction)
md = MarkItDown(
    cu_endpoint="https://<endpoint>",
    cu_analyzer_id="my-invoice-analyzer",
)
result = md.convert("invoice.pdf")
# Output: YAML front matter with extracted fields + markdown body
```

## Azure Document Intelligence

```python
md = MarkItDown(
    docintel_endpoint="https://<endpoint>.cognitiveservices.azure.com/",
    docintel_key="<key>",
)
result = md.convert("complex-scan.pdf")  # high-quality layout analysis
```

## MIME Type Override

```python
md = MarkItDown(
    mime_type_override={
        "application/x-custom-format": "my_custom_converter",  # string or class
    },
)
```

## EXIF Tool Path

For advanced EXIF extraction (used by image / audio converters):

```python
md = MarkItDown(exiftool_path="/usr/local/bin/exiftool")
```
