# Environment Setup

Use this setup for the learning projects unless a project states otherwise.

## Prerequisites

- Python 3.10 or newer.
- `git`.
- A shell or terminal.
- Local checkout of the CaeReflex repository.

## Install CaeReflex for learning

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[all,dev]"
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Verify the CLI

```bash
caereflex version
caereflex examples list
```

You should see the installed package version and the bundled examples.

## Offline-first rule

The learning projects are designed to work offline by default. Use mocked CrossRef responses when learning literature workflows so results are deterministic.

## REST/OpenAPI setup

For REST projects, start the server from the repository root:

```bash
caereflex serve --host 127.0.0.1 --port 8765 --workspace .
```

Then check:

```bash
curl http://127.0.0.1:8765/health
curl http://127.0.0.1:8765/openapi.yaml
```

Do not expose the server outside localhost unless you configure an API key and understand the workspace boundary.

## Recommended checks for contributors

```bash
python wiki/scripts/validate_wiki.py
pytest tests/test_wiki.py tests/test_docs_presence.py
```

Use the full test suite before a release or broad documentation update.
