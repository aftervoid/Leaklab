"""Local HTTP API and static dashboard entry point."""

import json
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from leaklab import __version__
from leaklab.config import settings
from leaklab.hibp import summarize_hibp_synthetic_samples
from leaklab.password_lab import generate_password_samples, summarize_synthetic_samples

app = FastAPI(
    title="LeakLab",
    version=__version__,
    description="Local API for synthetic password research and privacy-preserving HIBP aggregate checks.",
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATASET_DIR = PROJECT_ROOT / "data" / "daily-datasets"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


def _load_manifest(dataset_path: Path) -> dict[str, object] | None:
    """Read a dataset manifest without exposing the underlying sample files."""
    manifest_path = dataset_path / "manifest.json"
    if not manifest_path.is_file():
        return None
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _dataset_card(manifest: dict[str, object]) -> dict[str, object]:
    records = manifest.get("records_per_format", {})
    passwords = manifest.get("password_samples_per_format", {})
    record_files = manifest.get("records_files", {})
    password_files = manifest.get("password_sample_files", {})
    summary = manifest.get("password_sample_summary", {})
    if not isinstance(records, dict):
        records = {}
    if not isinstance(passwords, dict):
        passwords = {}
    if not isinstance(record_files, dict):
        record_files = {}
    if not isinstance(password_files, dict):
        password_files = {}
    if not isinstance(summary, dict):
        summary = {}
    return {
        "dataset_date": manifest.get("dataset_date"),
        "seed": manifest.get("seed"),
        "split_complete": bool(manifest.get("split_complete")),
        "record_count": records.get("jsonl", 0),
        "password_sample_count": passwords.get("jsonl", 0),
        "average_length": summary.get("average_length", 0),
        "patterns": summary.get("patterns", {}),
        "records_chunks": len(record_files.get("jsonl", [])),
        "password_chunks": len(password_files.get("jsonl", [])),
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment, "data_policy": "synthetic-only"}


@app.get("/api/config")
def public_config() -> dict[str, int | str]:
    return {"default_records": settings.default_records, "version": __version__}


@app.get("/api/password-lab/summary")
def password_lab_summary(count: int = 1000, seed: int = 42) -> dict[str, object]:
    """Return aggregate analysis of generated fixtures only."""
    if count < 0 or count > 100_000:
        raise HTTPException(status_code=422, detail="count must be between 0 and 100000")
    return summarize_synthetic_samples(count=count, seed=seed)


@app.get("/api/datasets")
def list_datasets() -> dict[str, object]:
    """List daily dataset metadata; never return generated record or sample values."""
    datasets: list[dict[str, object]] = []
    if DATASET_DIR.is_dir():
        for folder in sorted(DATASET_DIR.iterdir(), reverse=True):
            if not folder.is_dir():
                continue
            manifest = _load_manifest(folder)
            if manifest is None:
                continue
            card = _dataset_card(manifest)
            if card["dataset_date"] == folder.name:
                datasets.append(card)
    return {
        "dataset_count": len(datasets),
        "latest": datasets[0] if datasets else None,
        "datasets": datasets,
        "data_policy": "Synthetic fixtures only; aggregate metadata only.",
    }


@app.get("/api/datasets/{dataset_date}")
def get_dataset(dataset_date: str) -> dict[str, object]:
    """Return a validated daily manifest for the requested ISO date."""
    try:
        parsed_date = date.fromisoformat(dataset_date)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Dataset not found") from exc
    if parsed_date.isoformat() != dataset_date:
        raise HTTPException(status_code=404, detail="Dataset not found")

    manifest = _load_manifest(DATASET_DIR / dataset_date)
    if manifest is None or manifest.get("dataset_date") != dataset_date:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return manifest


@app.get("/api/password-lab/hibp-summary")
def hibp_summary(count: int = 5, seed: int = 42) -> dict[str, int | str]:
    """Check a small batch of generated fixtures using HIBP k-anonymity."""
    if count < 1 or count > 10:
        raise HTTPException(status_code=422, detail="count must be between 1 and 10")
    try:
        samples = generate_password_samples(count=count, seed=seed)
        return summarize_hibp_synthetic_samples(samples)
    except RuntimeError:
        raise HTTPException(status_code=503, detail="HIBP service is temporarily unavailable") from None


@app.get("/")
def dashboard():
    index = FRONTEND_DIR / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"name": "LeakLab", "message": "Frontend scaffold not found"}
