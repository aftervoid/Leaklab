"""Local HTTP API and static dashboard entry point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from leaklab import __version__
from leaklab.config import settings
from leaklab.password_lab import summarize_synthetic_samples

app = FastAPI(
    title="LeakLab",
    version=__version__,
    description="Local API for synthetic-only password pattern research.",
)

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


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
        return {"error": "count must be between 0 and 100000"}
    return summarize_synthetic_samples(count=count, seed=seed)


@app.get("/")
def dashboard():
    index = FRONTEND_DIR / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"name": "LeakLab", "message": "Frontend scaffold not found"}
