import json
from datetime import date

from fastapi.testclient import TestClient

from leaklab import api


client = TestClient(api.app)


def test_health_reports_synthetic_only_policy():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["data_policy"] == "synthetic-only"


def test_password_summary_returns_aggregate_data_only():
    response = client.get("/api/password-lab/summary?count=12&seed=7")
    assert response.status_code == 200
    payload = response.json()
    assert payload["samples_analyzed"] == 12
    assert "password_sample" not in payload


def test_password_summary_rejects_out_of_range_count():
    response = client.get("/api/password-lab/summary?count=100001")
    assert response.status_code == 422


def test_dataset_index_reads_manifests_only(tmp_path, monkeypatch):
    dataset_dir = tmp_path / "2026-11-20"
    dataset_dir.mkdir()
    manifest = {
        "dataset_date": "2026-11-20",
        "seed": 20261120,
        "split_complete": True,
        "records_per_format": {"jsonl": 10000, "csv": 10000},
        "password_samples_per_format": {"jsonl": 5000, "csv": 5000},
        "records_files": {"jsonl": ["records-0001.jsonl"]},
        "password_sample_files": {"jsonl": ["password-samples-0001.jsonl"]},
        "password_sample_summary": {
            "average_length": 15.5,
            "patterns": {"mixed_random": 5000},
        },
    }
    (dataset_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(api, "DATASET_DIR", tmp_path)

    response = client.get("/api/datasets")
    assert response.status_code == 200
    payload = response.json()
    assert payload["dataset_count"] == 1
    assert payload["latest"]["dataset_date"] == "2026-11-20"
    assert payload["latest"]["records_chunks"] == 1
    assert "password_sample" not in payload


def test_dataset_detail_validates_iso_date_and_manifest(tmp_path, monkeypatch):
    dataset_dir = tmp_path / date(2026, 11, 20).isoformat()
    dataset_dir.mkdir()
    manifest = {"dataset_date": "2026-11-20", "split_complete": True}
    (dataset_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(api, "DATASET_DIR", tmp_path)

    assert client.get("/api/datasets/2026-11-20").json() == manifest
    assert client.get("/api/datasets/2026-02-31").status_code == 404
    assert client.get("/api/datasets/../../SECURITY.md").status_code == 404
