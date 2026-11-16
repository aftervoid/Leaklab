"""Deterministic synthetic record generation and hybrid export."""

import csv
import random
from pathlib import Path
from collections.abc import Iterable, Iterator

from leaklab.models import SyntheticRecord

SOURCES = ("sample-forum", "demo-directory", "training-fixture")
RECORD_TYPES = ("profile", "contact", "account-metadata")


def generate_records(count: int, seed: int = 42) -> Iterator[SyntheticRecord]:
    """Yield fictional records. No real-world data or credentials are used."""
    if count < 0:
        raise ValueError("count must be zero or greater")

    rng = random.Random(seed)
    for index in range(count):
        number = index + 1
        yield SyntheticRecord(
            record_id=f"ll-{number:08d}",
            username=f"demo_user_{number:08d}",
            email=f"user{number:08d}@example.invalid",
            source_label=rng.choice(SOURCES),
            observed_at="2025-01-01T00:00:00Z",
            record_type=rng.choice(RECORD_TYPES),
        )


def export_jsonl(records: Iterable[SyntheticRecord], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(record.model_dump_json() + "\n")
            written += 1
    return written


def export_csv(records: Iterable[SyntheticRecord], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(SyntheticRecord.model_fields)
    written = 0
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for record in records:
            row = record.model_dump(mode="json")
            writer.writerow(row)
            written += 1
    return written


def generate_dataset(count: int, output_dir: Path, seed: int = 42, fmt: str = "both") -> dict[str, int]:
    """Generate one or both supported formats without keeping all rows in memory."""
    if fmt not in {"jsonl", "csv", "both"}:
        raise ValueError("format must be jsonl, csv, or both")

    results: dict[str, int] = {}
    if fmt in {"jsonl", "both"}:
        results["jsonl"] = export_jsonl(
            generate_records(count, seed), output_dir / "records.jsonl"
        )
    if fmt in {"csv", "both"}:
        results["csv"] = export_csv(
            generate_records(count, seed), output_dir / "records.csv"
        )
    return results
