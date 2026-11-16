# LeakLab

LeakLab is a privacy-preserving lab for exploring **synthetic** exposure-style datasets. The initial scaffold targets one million generated records and provides both a command-line interface and a local web interface.

> **Safety boundary:** this project is designed for synthetic test data only. It does not collect, import, search, validate, or distribute real leaked personal information, passwords, tokens, or other credentials. Generated identities use reserved example domains and are not real people.

## Project goals

- Generate a reproducible dataset of 1,000,000 synthetic records on demand.
- Support a hybrid storage/export format: JSON Lines (`.jsonl`) and CSV.
- Offer both CLI and HTTP/web interfaces.
- Keep generated data local and avoid external data sources.

## Quick start

Requires Python 3.11 or newer.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

python -m pip install -e ".[dev]"
python -m leaklab.cli generate --count 1000000 --format both --output data/generated
uvicorn leaklab.api:app --reload
```

Open http://127.0.0.1:8000 for the API and http://127.0.0.1:8000/docs for the development API docs. The frontend scaffold is in `frontend/`; it can be served by any static file server and will connect to the local API.

## Configuration

Defaults are intentionally conservative. See `.env.example`. The generator accepts a seed so test runs can be reproduced.

## Repository layout

- `src/leaklab/`: generator, data model, CLI, and API.
- `frontend/`: lightweight browser dashboard.
- `tests/`: automated tests.
- `docs/`: architecture and development notes.

## Current status

This commit establishes the initial project structure. Dataset generation, API routes, and the browser dashboard are intentionally small starting points and will be expanded in later steps.

## Development

```bash
pytest
```

See [SECURITY.md](SECURITY.md) for the project's data-handling boundary.
