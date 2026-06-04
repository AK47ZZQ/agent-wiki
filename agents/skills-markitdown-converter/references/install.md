# MarkItDown Install — Platform-Specific

## Python Requirement

**Python 3.10 or higher**. Use a virtual environment to avoid dependency conflicts.

## Windows

```bash
# Standard pip
python -m venv .venv
.venv\Scripts\activate
pip install 'markitdown[all]'
```

## macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install 'markitdown[all]'
```

## Using `uv` (faster alternative)

```bash
uv venv --python=3.12 .venv
source .venv/bin/activate
# Use 'uv pip install' not 'pip install' to install in this venv
uv pip install 'markitdown[all]'
```

## Using Anaconda

```bash
conda create -n markitdown python=3.12
conda activate markitdown
pip install 'markitdown[all]'
```

## Common Pitfalls

### 1. Hindsight in the environment locks markitdown<0.1.4

If you have `hindsight` or `hindsight-api-slim` installed, pip will try to install markitdown 0.0.2 (the latest compatible version):

```
$ pip install 'markitdown[all]'
hindsight-api-slim 0.6.1 requires markitdown[docx,pdf,pptx,xls,xlsx]>=0.1.4, but you have markitdown 0.0.2 which is incompatible.
```

**Fix**:
```bash
pip install --upgrade --ignore-requires 'markitdown[all]==0.1.6'
```

This forces the latest version. The "incompatibility" warning can be ignored — Hindsight's actual usage of markitdown is compatible with 0.1.x.

If Hindsight still complains after the upgrade, downgrade to 0.1.4:
```bash
pip install --ignore-requires 'markitdown[all]==0.1.4'
```

### 2. Optional dependency missing

If you install without `[all]` and try to convert a format you didn't install support for:
```
$ markitdown paper.pdf
ModuleNotFoundError: No module named 'pdfminer'
```

**Fix**: install the missing extra:
```bash
pip install 'markitdown[pdf]'
```

### 3. Python version too old

```
$ pip install 'markitdown[all]'
ERROR: markitdown requires Python >=3.10
```

**Fix**: Upgrade Python or use a newer venv:
```bash
conda create -n markitdown python=3.12
```

## Verify Install

```bash
markitdown --version
# Expected: markitdown 0.1.x
```

```bash
python -c "from markitdown import MarkItDown; md = MarkItDown(); print(md.convert('README.md').text_content[:100])"
# Should print the first 100 chars of README.md as Markdown
```

## Uninstall

```bash
pip uninstall markitdown
```

**Warning**: If Hindsight depends on markitdown, uninstalling it will break Hindsight.
