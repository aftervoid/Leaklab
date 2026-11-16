# LeakLab

LeakLab is a local, privacy-preserving password research lab. It combines **fictional password samples** with documented, public aggregate research to study password construction patterns. It supports reproducible datasets, transparent shape heuristics, and both CLI and web/API interfaces.

> **Data boundary:** LeakLab does not ingest breach dumps, check passwords against leaked lists, test logins, or collect real account credentials. Generated password strings are fictional test fixtures. Never enter a password used for a real account.

## Features

- Deterministic generation of synthetic password samples.
- Hybrid JSONL + CSV export, including one-million-sample runs.
- Aggregate analysis of length, character-class diversity, and synthetic construction patterns.
- Local web dashboard and API preview that returns aggregate statistics only.
- GitHub Actions tests on pushes, pull requests, and manual runs.

The shape score is an educational heuristic, not a security guarantee, breach lookup, or crack-time estimate. Public research should be added only as aggregate statistics with source attribution and compatible terms; do not import raw credential datasets.

## Quick start (Windows PowerShell)

Requires Python 3.11+.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m leaklab.cli passwords --count 1000000 --format both --output data/passwords
uvicorn leaklab.api:app --reload
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs.

## Tests

```powershell
python -m pytest -q
python -m ruff check src tests
```

GitHub Actions runs the same checks automatically. See [SECURITY.md](SECURITY.md) and [docs/password-research.md](docs/password-research.md) for the data policy and research scope.
