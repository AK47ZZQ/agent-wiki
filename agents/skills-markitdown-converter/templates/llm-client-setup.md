# LLM Client Setup Boilerplate

Copy-paste these into your code to set up LLM clients for markitdown.

## OpenAI (most common)

```python
import os
from openai import OpenAI
from markitdown import MarkItDown

client = OpenAI()  # reads OPENAI_API_KEY from env
md = MarkItDown(llm_client=client, llm_model="gpt-4o")

result = md.convert("document.pdf")
print(result.text_content)
```

**Required env var**: `OPENAI_API_KEY`

## Azure OpenAI

```python
import os
from openai import AzureOpenAI
from markitdown import MarkItDown

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview",
)
md = MarkItDown(llm_client=client, llm_model="gpt-4o")

result = md.convert("document.pdf")
```

**Required env vars**:
- `AZURE_OPENAI_ENDPOINT` (e.g. `https://YOUR-RESOURCE.openai.azure.com/`)
- `AZURE_OPENAI_KEY`
- `AZURE_OPENAI_MODEL` (your deployment name; defaults to "gpt-4o" if not set)

## Anthropic (via OpenAI-compatible proxy)

```python
import os
from openai import OpenAI
from markitdown import MarkItDown

client = OpenAI(
    base_url="https://api.anthropic.com/v1/",  # or your proxy URL
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)
md = MarkItDown(llm_client=client, llm_model="claude-3-5-sonnet-20241022")
```

## Local LLM (Ollama)

```python
from openai import OpenAI
from markitdown import MarkItDown

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # ollama doesn't require a real key
)
md = MarkItDown(llm_client=client, llm_model="llama3.2-vision")
```

**Note**: For OCR/vision, the model must be vision-capable (e.g. `llama3.2-vision`, `llava`, `minicpm-v`).

## LiteLLM (any model via LiteLLM proxy)

```python
from openai import OpenAI
from markitdown import MarkItDown

# Start LiteLLM proxy: `litellm --model gpt-4o`
client = OpenAI(
    base_url="http://localhost:4000",
    api_key="anything",  # not validated by LiteLLM
)
md = MarkItDown(llm_client=client, llm_model="gpt-4o")
```

## Vision-Capable Models (for OCR / image description)

| Provider | Model | Vision? |
|---|---|---|
| OpenAI | `gpt-4o` | ✅ |
| OpenAI | `gpt-4o-mini` | ✅ |
| OpenAI | `gpt-4-turbo` | ✅ |
| Anthropic | `claude-3-5-sonnet-20241022` | ✅ |
| Anthropic | `claude-3-opus-20240229` | ✅ |
| Google | `gemini-1.5-pro` | ✅ |
| Google | `gemini-1.5-flash` | ✅ |
| Local (Ollama) | `llama3.2-vision` | ✅ |
| Local (Ollama) | `llava` | ✅ |
| Local (Ollama) | `minicpm-v` | ✅ |

**For OCR specifically**: use a vision-capable model with the `markitdown-ocr` plugin installed.

## Setting Environment Variables

```bash
# Linux / macOS
export OPENAI_API_KEY="sk-..."
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc

# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-...", "User")

# Windows MSYS bash
export OPENAI_API_KEY="sk-..."
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bash_profile
```

## Testing Your Client

Before using with markitdown, verify the client works directly:

```python
from openai import OpenAI

client = OpenAI()  # or your custom client
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Reply with just the word 'ok'."}],
    max_tokens=10,
)
print(response.choices[0].message.content)
# Should print: "ok." (or similar)
```

If this works, markitdown will work.
