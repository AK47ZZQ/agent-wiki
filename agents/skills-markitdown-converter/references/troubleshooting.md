# MarkItDown Troubleshooting

## "ModuleNotFoundError: No module named 'pdfminer'"

**Cause**: Installed `markitdown` without the `[pdf]` extra.

**Fix**:
```bash
pip install 'markitdown[pdf]'
# or
pip install 'markitdown[all]'
```

## "Incompatibility with hindsight-api-slim"

**Cause**: Hindsight declares `markitdown[docx,pdf,pptx,xls,xlsx]>=0.1.4` but pip default installs 0.0.2 (the latest compatible pre-0.1.4 version).

**Fix**:
```bash
pip install --upgrade --ignore-requires 'markitdown[all]==0.1.6'
```

## PDF output is empty / mostly whitespace

**Cause**: Scanned PDF (no text layer). markitdown's PDF converter only extracts text, not images of text.

**Fix**: Use Azure Document Intelligence (cloud OCR):
```bash
markitdown scan.pdf --use-doc-intel --endpoint "<endpoint>" --key "<key>"
```

Or install the `markitdown-ocr` plugin (uses LLM Vision):
```bash
pip install markitdown-ocr
# Then in Python:
md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o", enable_plugins=True)
```

## "TypeError: 'NoneType' object is not callable" when using llm_client

**Cause**: `llm_client` is provided but the model doesn't support vision, or the client is misconfigured.

**Fix**:
1. Verify the model is vision-capable: `gpt-4o`, `gpt-4o-mini`, `claude-3-5-sonnet`, etc.
2. Verify the client is instantiated correctly:
   ```python
   from openai import OpenAI
   client = OpenAI()  # reads OPENAI_API_KEY from env
   ```
3. Test the client directly:
   ```python
   client.chat.completions.create(
       model="gpt-4o",
       messages=[{"role": "user", "content": "hello"}]
   )
   ```

## Images in output are paths, not descriptions

**Cause**: `llm_client` is `None` (default). markitdown emits `![](path/to/img)` without LLM Vision description.

**Fix**: Pass an `llm_client`:
```python
md = MarkItDown(llm_client=OpenAI(), llm_model="gpt-4o")
```

## "ConnectionError" or "Timeout" for Azure endpoints

**Cause**: Network, wrong endpoint, expired key.

**Fix**:
1. Verify endpoint URL (no trailing slash)
2. Verify key is valid
3. Test with curl:
   ```bash
   curl -X POST "https://<endpoint>/formrecognizer/documentModels/prebuilt-layout:analyze?api-version=2023-07-31" \
     -H "Ocp-Apim-Subscription-Key: <key>" \
     -H "Content-Type: application/json" \
     -d '{"urlSource": "https://example.com/sample.pdf"}'
   ```

## Excel output is messy (merged cells, multi-level headers)

**Cause**: markitdown flattens complex Excel structure.

**Fix**: Pre-export to CSV:
```python
import pandas as pd
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df.to_csv("data.csv", index=False)
# Then:
markitdown("data.csv")
```

## Large PDF causes MemoryError

**Cause**: markitdown loads entire PDF into memory.

**Fix**:
1. Split PDF first:
   ```python
   from pypdf import PdfReader, PdfWriter
   reader = PdfReader("huge.pdf")
   for i, page in enumerate(reader.pages):
       writer = PdfWriter()
       writer.add_page(page)
       with open(f"page_{i}.pdf", "wb") as f:
           writer.write(f)
   ```
2. Then convert each page:
   ```bash
   for pdf in page_*.pdf; do markitdown "$pdf" -o "${pdf%.pdf}.md"; done
   ```
3. Or use Azure Doc Intel (cloud, no memory limit).

## YouTube transcription fails

**Cause**: Video is private, age-restricted, or has no captions.

**Fix**:
1. Verify URL is public and has captions.
2. If no captions: use Whisper directly on the audio:
   ```python
   import whisper
   model = whisper.load_model("base")
   result = model.transcribe("video_audio.mp3")
   print(result["text"])
   ```

## Azure Content Understanding bills unexpectedly

**Cause**: Each `convert()` call for a CU-routed format is billable.

**Fix**: Restrict formats routed to CU:
```python
from markitdown.converters import ContentUnderstandingFileType
md = MarkItDown(
    cu_endpoint="<endpoint>",
    cu_file_types=[ContentUnderstandingFileType.PDF],  # only PDFs
)
```

## "FileNotFoundError" on Windows paths

**Cause**: Path uses backslashes inside Python string (escape issues).

**Fix**: Use raw strings or forward slashes:
```python
result = md.convert(r"C:\Users\Me\file.pdf")  # raw string
# OR
result = md.convert("C:/Users/Me/file.pdf")  # forward slashes
```

## markitdown works in CLI but Python API raises

**Cause**: Stale install or wrong venv.

**Fix**:
```bash
# Verify the venv you're using
which python
pip show markitdown | grep Location

# Reinstall in the right venv
source .venv/bin/activate
pip install --force-reinstall 'markitdown[all]'
```

## "convert() got unexpected keyword argument"

**Cause**: API mismatch between markitdown versions.

**Fix**: Check your markitdown version vs docs:
```bash
markitdown --version
```

For 0.1.x, see the API reference in this skill (`references/python-api.md`).

---

If your issue isn't here, search https://github.com/microsoft/markitdown/issues (1000+ issues, most edge cases are documented).
