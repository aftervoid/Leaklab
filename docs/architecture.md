# Architecture

## Initial shape

LeakLab starts as a small Python application with two user-facing interfaces:

1. **CLI** for reproducible generation and export jobs.
2. **Web UI + HTTP API** for local status and future dataset summaries.

The data layer yields records lazily so a one-million-row run does not need to keep the entire dataset in memory.

## Hybrid dataset

The same deterministic generator can export to:
- JSON Lines (`records.jsonl`), one JSON object per line.
- CSV (`records.csv`), with a header row.

Both formats are generated independently from the same seed and record ordering.

## Privacy boundary

All records are fictional. Email addresses use `example.invalid`, usernames are generated labels, and no password or token fields exist. The application is not an ingestion pipeline for real breach material.

## Planned increments

- Add streaming progress reporting for large exports.
- Add summary endpoints and visualizations over generated local fixtures.
- Add integration tests for the HTTP API.
