"""Build a reproducible, synthetic-only daily dataset bundle."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from leaklab.dataset import generate_dataset
from leaklab.password_lab import export_password_samples, summarize_synthetic_samples

CHUNK_SIZE = 500


def _split_export(source: Path, output_dir: Path, stem: str, suffix: str,
                  chunk_size: int = CHUNK_SIZE) -> list[str]:
    """Split a large line-oriented export into small, numbered files."""
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")

    # Remove chunks from a previous run so changing counts cannot leave stale parts.
    for old_part in output_dir.glob(f"{stem}-[0-9][0-9][0-9][0-9]{suffix}"):
        old_part.unlink()

    with source.open(encoding="utf-8", newline="") as stream:
        header = stream.readline() if suffix == ".csv" else None
        names: list[str] = []
        part_number = 1
        row_count = 0
        target = None

        def open_part(number: int):
            name = f"{stem}-{number:04d}{suffix}"
            path = output_dir / name
            handle = path.open("w", encoding="utf-8", newline="")
            if header is not None:
                handle.write(header)
            names.append(name)
            return handle

        try:
            for line in stream:
                if row_count % chunk_size == 0:
                    if target is not None:
                        target.close()
                    target = open_part(part_number)
                    part_number += 1
                target.write(line)
                row_count += 1
        finally:
            if target is not None:
                target.close()

    return names


def _write_preview(output_dir: Path, manifest: dict[str, Any]) -> None:
    """Write a compact GitHub-renderable overview without exposing password samples."""
    records_dir = output_dir / "records"
    first_records_file = records_dir / manifest["records_files"]["jsonl"][0]
    preview_records: list[dict[str, Any]] = []
    with first_records_file.open(encoding="utf-8") as stream:
        for line in stream:
            if len(preview_records) == 5:
                break
            if line.strip():
                preview_records.append(json.loads(line))

    lines = [
        "# Daily synthetic dataset",
        "",
        f"**Date:** {manifest['dataset_date']}  ",
        f"**Seed:** {manifest['seed']}  ",
        f"**Profile records:** {manifest['records_per_format']['jsonl']} per format  ",
        f"**Synthetic password samples:** {manifest['password_samples_per_format']['jsonl']} per format  ",
        f"**Chunk size:** {manifest['chunk_size']} rows per file",
        "",
        "> Large exports are split into numbered chunks so each file stays manageable in GitHub.",
        "> All records and samples are synthetic; no real credentials or breach data are included.",
        "",
        "## Preview: first 5 profile records",
        "",
        "| Record ID | Username | Email | Source | Type |",
        "|---|---|---|---|---|",
    ]
    for record in preview_records:
        lines.append(
            f"| {record['record_id']} | {record['username']} | {record['email']} "
            f"| {record['source_label']} | {record['record_type']} |"
        )

    summary = manifest["password_sample_summary"]
    lines.extend([
        "",
        "## Password-sample aggregate",
        "",
        f"- Samples analyzed: **{summary['samples_analyzed']}**",
        f"- Average length: **{summary['average_length']}** characters",
        "",
        "| Pattern | Count |",
        "|---|---:|",
    ])
    for pattern, count in summary["patterns"].items():
        lines.append(f"| {pattern} | {count} |")

    lines.extend(["", "## Profile records"])
    for fmt, label in (("jsonl", "JSONL"), ("csv", "CSV")):
        lines.extend(["", f"**{label} chunks**"])
        lines.extend(f"- [{name}](records/{name})" for name in manifest["records_files"][fmt])

    lines.extend(["", "## Synthetic password samples"])
    for fmt, label in (("jsonl", "JSONL"), ("csv", "CSV")):
        lines.extend(["", f"**{label} chunks**"])
        lines.extend(
            f"- [{name}](passwords/{name})"
            for name in manifest["password_sample_files"][fmt]
        )

    lines.extend(["", "- [Machine-readable manifest](manifest.json)", ""])
    (output_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def build_daily_bundle(
    run_date: date,
    output_dir: Path,
    record_count: int = 10_000,
    password_count: int = 5_000,
) -> dict[str, object]:
    """Create chunked daily JSONL/CSV fixtures, a manifest, and a short preview."""
    if record_count < 0 or password_count < 0:
        raise ValueError("dataset counts must be zero or greater")

    seed = int(run_date.strftime("%Y%m%d"))
    output_dir.mkdir(parents=True, exist_ok=True)
    records_dir = output_dir / "records"
    passwords_dir = output_dir / "passwords"
    records_dir.mkdir(parents=True, exist_ok=True)
    passwords_dir.mkdir(parents=True, exist_ok=True)

    records = generate_dataset(record_count, records_dir, seed=seed, fmt="both")
    passwords = export_password_samples(
        password_count, passwords_dir, seed=seed, fmt="both"
    )

    record_files = {
        "jsonl": ["records.jsonl"],
        "csv": ["records.csv"],
    }
    password_files = {
        "jsonl": ["password_samples.jsonl"],
        "csv": ["password_samples.csv"],
    }

    manifest: dict[str, Any] = {
        "dataset_date": run_date.isoformat(),
        "seed": seed,
        "chunk_size": CHUNK_SIZE,
        "split_complete": False,
        "records_per_format": records,
        "password_samples_per_format": passwords,
        "records_files": record_files,
        "password_sample_files": password_files,
        "password_sample_summary": summarize_synthetic_samples(password_count, seed=seed),
        "data_policy": "Synthetic fixtures only; no breach corpus or real account credentials.",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_preview(output_dir, manifest)
    return manifest
