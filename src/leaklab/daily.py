"""Build a reproducible, synthetic-only daily dataset bundle."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from leaklab.dataset import generate_dataset
from leaklab.password_lab import export_password_samples, summarize_synthetic_samples


def build_daily_bundle(
    run_date: date,
    output_dir: Path,
    record_count: int = 10_000,
    password_count: int = 5_000,
) -> dict[str, object]:
    """Create daily JSONL/CSV fixtures and an aggregate-only manifest."""
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
    return manifest
