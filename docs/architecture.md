# Architecture

## Application layers

- `src/leaklab/password_lab.py`: deterministic synthetic password fixture generation,
  streaming JSONL/CSV export, and transparent shape heuristics.
- `src/leaklab/cli.py`: CLI commands for synthetic profile fixtures, password samples,
  and aggregate analysis.
- `src/leaklab/api.py`: local FastAPI health/config endpoints and aggregate-only
  password research summary.
- `frontend/`: browser dashboard that reads local API status and aggregate summaries.
- `tests/`: unit tests for reproducibility, synthetic labeling, export formats,
  and analysis summaries.

## Data flow

The generator yields one fictional sample at a time. Exporters stream records to disk
rather than retaining the full dataset in memory. The summary analyzer counts pattern
categories and ratings, returning aggregate values without returning sample strings.

## Research and privacy boundary

The current analyzer measures length and character-class diversity. It does not estimate
cracking time, compare against breached-password corpora, or establish that a password
is safe. Public research can be represented as cited aggregate statistics; raw credential
lists and real account passwords are out of scope.

See [password-research.md](password-research.md) and [SECURITY.md](../SECURITY.md).
