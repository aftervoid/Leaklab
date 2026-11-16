"""Local HTTP API and static dashboard entry point."""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from leaklab import __version__
from leaklab.config import settings

app = FastAPI(
    title="LeakLab",
    version=__version__,
    description="Local API for a synthetic-only dataset lab.",
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


@app.get("/")
def dashboard():
    index = FRONTEND_DIR / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"name": "LeakLab", "message": "Frontend scaffold not found"}
