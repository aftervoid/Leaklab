# LeakLab

LeakLab is a local, privacy-preserving password research lab. It combines **fictional password samples** with documented, public aggregate research to study password construction patterns. It supports reproducible datasets, transparent shape heuristics, and both CLI and web/API interfaces.

> **Data boundary:** LeakLab does not ingest breach dumps, check passwords against leaked lists, test logins, or collect real account credentials. Generated password strings are fictional test fixtures. Never enter a password used for a real account.

## Features

- Deterministic generation of synthetic password samples.
- Hybrid JSONL + CSV export, including one-million-sample runs.
- Aggregate analysis of length, character-class diversity, and synthetic construction patterns.
- Daily synthetic profile and password datasets generated and committed directly to the repository by GitHub Actions.
- A responsive local research dashboard with overview, password analysis, dataset history, and system-status views.
- Aggregate-only API endpoints for health, configuration, synthetic analysis, and daily dataset manifests.
- Optional HIBP Pwned Passwords checks for generated fixtures using k-anonymity; only aggregate counts are returned.
- GitHub Actions tests across supported Python versions, dependency auditing, and CodeQL static analysis.

The shape score is an educational heuristic, not a security guarantee or crack-time estimate. LeakLab does not import RockYou or other raw credential lists. Its optional HIBP integration checks only generated synthetic fixtures: the first five characters of a locally computed SHA-1 hash are sent to HIBP, the full-hash comparison happens locally, and only aggregate counts are returned. See [Pwned Passwords API documentation](https://haveibeenpwned.com/api/v3#PwnedPasswords).

## License

The LeakLab source code and accompanying project documentation are released under the **MIT License**. See [LICENSE](LICENSE) for the complete terms.

The MIT License does not automatically determine the terms for third-party research sources or separately supplied datasets. Check the relevant dataset manifest and source attribution before reusing those materials.

## Dashboard

Start the local API:

```powershell
uvicorn leaklab.api:app --reload
```

Open http://127.0.0.1:8000. The dashboard includes:

- **Overview:** daily dataset totals and latest-generation snapshot.
- **Password research:** adjustable synthetic sample counts and aggregate pattern/rating charts.
- **Dataset center:** daily manifest history, record counts, chunk status, and reproducibility seeds.
- **System status:** API health, runtime environment, version, and project documentation links.

The dashboard's dataset views read manifest metadata only. They do not return generated record contents or password sample strings.

## API

Interactive API documentation is available at http://127.0.0.1:8000/docs.

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Local API health and synthetic-only policy |
| `GET /api/config` | Public application defaults and version |
| `GET /api/password-lab/summary?count=1000&seed=42` | Aggregate analysis of generated fixtures |
| `GET /api/datasets` | Daily dataset index with aggregate metadata |
| `GET /api/datasets/{YYYY-MM-DD}` | Validated manifest for one daily dataset |
| `GET /api/password-lab/hibp-summary?count=5` | Optional aggregate HIBP check of generated fixtures |

The dataset endpoints expose counts, dates, seeds, chunk names/counts, and aggregate summaries only. They do not expose sample values. See [API notes](docs/api.md).

## Daily dataset generation

The **Daily Synthetic Dataset Generator** workflow runs once per day at **00:17 UTC** and can also be started manually from the Actions tab. By default, each run generates:

- 10,000 fictional profile records (records.jsonl and records.csv).
- 5,000 fictional password samples (password_samples.jsonl and password_samples.csv).
- manifest.json with the UTC date, reproducible seed, record counts, and aggregate password-shape statistics.

The independent **Daily Synthetic Dataset Splitter** workflow runs at **00:29 UTC**. It creates numbered 500-row copies while preserving the original large exports. It can also be started manually. Both workflows use GitHub Actions only: there is no external scheduler, no waiting step, and no GitHub Actions Artifacts. The fixed schedule means the splitter is not guaranteed to start exactly 11 minutes after the generator finishes; GitHub may delay scheduled workflow starts during high-load periods.

Generated files are committed directly to `data/daily-datasets/YYYY-MM-DD/` on `main`. Rerunning the generator on the same UTC date updates that date's original exports; a new date creates a new directory. The seed is derived from the UTC date, so sample values are reproducible for that date. Because these files are committed, Git history and repository size grow over time. See [data/README.md](data/README.md).

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

GitHub Actions runs the same checks automatically, tests Python 3.11–3.13, audits installed dependencies, and runs CodeQL analysis. Dependabot checks Python and GitHub Actions dependencies weekly. See [SECURITY.md](SECURITY.md) and [docs/password-research.md](docs/password-research.md) for the data policy and research scope.
