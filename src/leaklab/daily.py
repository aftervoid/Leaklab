"""Build a reproducible, synthetic-only daily dataset bundle."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from leaklab.dataset import generate_dataset
from leaklab.password_lab import export_password_samples, summarize_synthetic_samples


def _write_preview(output_dir: Path, manifest: dict[str, object]) -> None:
    """Write a compact GitHub-renderable overview without exposing password samples."""
    records_path = output_dir / "records" / "records.jsonl"
    preview_records: list[dict[str, object]] = []
    with records_path.open(encoding="utf-8") as stream:
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
        f"**Profile records per format:** {sum(manifest['records_per_format'].values()) // 2}  ",
        f"**Password samples per format:** {sum(manifest['password_samples_per_format'].values()) // 2}",
        "",
        "> This page is a compact preview. The complete JSONL and CSV files are linked below.",
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

    lines.extend([
        "",
        "## Full datasets",
        "",
        "- [Profile records (JSONL)](records/records.jsonl)",
        "- [Profile records (CSV)](records/records.csv)",
        "- [Password samples (JSONL)](passwords/password_samples.jsonl)",
        "- [Password samples (CSV)](passwords/password_samples.csv)",
        "- [Machine-readable manifest](manifest.json)",
        "",
    ])
    (output_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def build_daily_bundle(
    run_date: date,
    output_dir: Path,
    record_count: int = 10_000,
    password_count: int = 5_000,
) -> dict[str, object]:
    """Create daily JSONL/CSV fixtures, an aggregate manifest, and a short preview."""
    if record_count < 0 or password_count < 0:
        raise ValueError("dataset counts must be zero or greater")

    seed = int(run_date.strftime("%Y%m%d"))
    output_dir.mkdir(parents=True, exist_ok=True)

    records = generate_dataset(record_count, output_dir / "records", seed=seed, fmt="both")
    passwords = export_password_samples(
        password_count, output_dir / "passwords", seed=seed, fmt="both"
    )
    manifest: dict[str, object] = {
        "dataset_date": run_date.isoformat(),
        "seed": seed,
        "records_per_format": records,
        "password_samples_per_format": passwords,
        "password_sample_summary": summarize_synthetic_samples(password_count, seed=seed),
        "data_policy": "Synthetic fixtures only; no breach corpus or real account credentials.",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_preview(output_dir, manifest)
    return manifest
