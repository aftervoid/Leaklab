# Architecture

## Application layers

- `src/leaklab/password_lab.py`: deterministic synthetic password fixture generation,
  streaming JSONL/CSV export, and transparent shape heuristics.
- `src/leaklab/cli.py`: CLI commands for synthetic profile fixtures, password samples,
  and aggregate analysis.
- `src/leaklab/api.py`: local FastAPI health/config endpoints, aggregate-only password
  research summaries, and read-only daily dataset metadata endpoints.
- `frontend/`: responsive browser dashboard with overview, research, dataset-center,
  and system-status views.
- `data/daily-datasets/`: reproducible daily exports, chunked copies, manifests, and
  compact repository previews.
- `tests/`: unit and API tests for reproducibility, synthetic labeling, export formats,
  aggregate summaries, and dataset metadata validation.

## Data flow

The generator yields one fictional sample at a time. Exporters stream records to disk
rather than retaining the full dataset in memory. The summary analyzer counts pattern
categories and ratings, returning aggregate values without returning sample strings.

The dashboard requests data from the local API. Its dataset center reads each daily
`manifest.json` and returns only dates, seeds, counts, chunk metadata, and aggregate
password-shape statistics. Dataset detail requests validate the ISO date and return
the corresponding manifest. Neither endpoint reads or returns the generated sample
contents.

## API surface

- `GET /api/health`: runtime health and synthetic-only policy.
- `GET /api/config`: public application defaults and version.
- `GET /api/password-lab/summary`: aggregate analysis of generated fixtures.
- `GET /api/datasets`: read-only daily dataset index.
- `GET /api/datasets/{YYYY-MM-DD}`: validated daily manifest.
- `GET /api/password-lab/hibp-summary`: optional aggregate-only HIBP check for
  generated synthetic fixtures.

## Research and privacy boundary

The current analyzer measures length and character-class diversity. It does not estimate
cracking time, compare against breached-password corpora, or establish that a password
is safe. Public research can be represented as cited aggregate statistics; raw credential
lists and real account passwords are out of scope.

See [password-research.md](password-research.md) and [SECURITY.md](../SECURITY.md).
