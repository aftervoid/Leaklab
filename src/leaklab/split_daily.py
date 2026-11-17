"""Split an already-generated daily bundle while preserving original exports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from leaklab.daily import CHUNK_SIZE, _split_export, _write_preview


def split_daily_bundle(output_dir: Path) -> dict[str, Any]:
    manifest_path = output_dir / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Daily manifest not found: {manifest_path}")

    manifest: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    records_dir = output_dir / "records"
    passwords_dir = output_dir / "passwords"

    record_files = {
        "jsonl": _split_export(records_dir / "records.jsonl", records_dir, "records", ".jsonl"),
        "csv": _split_export(records_dir / "records.csv", records_dir, "records", ".csv"),
    }
    password_files = {
        "jsonl": _split_export(
            passwords_dir / "password_samples.jsonl",
            passwords_dir,
            "password-samples",
            ".jsonl",
        ),
        "csv": _split_export(
            passwords_dir / "password_samples.csv",
            passwords_dir,
            "password-samples",
            ".csv",
        ),
    }

    manifest["chunk_size"] = CHUNK_SIZE
    manifest["split_complete"] = True
    manifest["records_files"] = record_files
    manifest["password_sample_files"] = password_files
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _write_preview(output_dir, manifest)
    return manifest
