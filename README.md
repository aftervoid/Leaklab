# LeakLab

LeakLab is a local, privacy-preserving password research lab. It combines **fictional password samples** with documented, public aggregate research to study password construction patterns. It supports reproducible datasets, transparent shape heuristics, and both CLI and web/API interfaces.

> **Data boundary:** LeakLab does not ingest breach dumps, check passwords against leaked lists, test logins, or collect real account credentials. Generated password strings are fictional test fixtures. Never enter a password used for a real account.

## Features

- Deterministic generation of synthetic password samples.
- Hybrid JSONL + CSV export, including one-million-sample runs.
- Aggregate analysis of length, character-class diversity, and synthetic construction patterns.
- Daily synthetic profile and password datasets generated and committed directly to the repository by GitHub Actions.
- Optional HIBP Pwned Passwords checks for generated fixtures using k-anonymity; only aggregate counts are returned.
- Local web dashboard and API preview that returns aggregate statistics only.
- GitHub Actions tests on pushes, pull requests, and manual runs.

The shape score is an educational heuristic, not a security guarantee or crack-time estimate. LeakLab does not import RockYou or other raw credential lists. Its optional HIBP integration checks only generated synthetic fixtures: the first five characters of a locally computed SHA-1 hash are sent to HIBP, the full-hash comparison happens locally, and only aggregate counts are returned. See [Pwned Passwords API documentation](https://haveibeenpwned.com/api/v3#PwnedPasswords).

## Daily dataset generation

The **Daily Synthetic Dataset** workflow runs once per day at 00:17 UTC and can also be started manually from the Actions tab. By default, each run generates:

- 10,000 fictional profile records (records.jsonl and records.csv).
- 5,000 fictional password samples (password_samples.jsonl and password_samples.csv).
- manifest.json with the UTC date, reproducible seed, record counts, and aggregate password-shape statistics.

Generated files are committed directly to data/daily-datasets/YYYY-MM-DD/ on main. Rerunning the workflow on the same UTC date updates that date's directory; a new date creates a new directory. The seed is derived from the UTC date, so sample values are reproducible for that date. Because these files are committed, Git history and repository size grow over time. See [data/README.md](data/README.md).

## Quick start (Windows PowerShell)

Requires Python 3.11+.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m leaklab.cli passwords --count 1000000 --format both --output data/passwords
uvicorn leaklab.api:app --reload
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs. The optional /api/password-lab/hibp-summary?count=5 endpoint checks up to 10 generated fixtures against HIBP and returns aggregate counts only.

## Tests

```powershell
python -m pytest -q
python -m ruff check src tests
```

GitHub Actions runs the same checks automatically. See [SECURITY.md](SECURITY.md) and [docs/password-research.md](docs/password-research.md) for the data policy and research scope.
