import json
from datetime import date

from leaklab.daily import build_daily_bundle


def test_daily_bundle_splits_exports_into_small_numbered_chunks(tmp_path):
    manifest = build_daily_bundle(date(2026, 11, 17), tmp_path, 1200, 1001)

    assert manifest["seed"] == 20261117
    assert manifest["chunk_size"] == 500
    assert manifest["records_per_format"] == {"jsonl": 1200, "csv": 1200}
    assert manifest["password_samples_per_format"] == {"jsonl": 1001, "csv": 1001}
    assert len(manifest["records_files"]["jsonl"]) == 3
    assert len(manifest["records_files"]["csv"]) == 3
    assert len(manifest["password_sample_files"]["jsonl"]) == 3
    assert len(manifest["password_sample_files"]["csv"]) == 3

    assert manifest["records_files"]["jsonl"] == [
        "records-0001.jsonl", "records-0002.jsonl", "records-0003.jsonl"
    ]
    assert manifest["password_sample_files"]["csv"][-1] == "password-samples-0003.csv"
    assert not (tmp_path / "records" / "records.jsonl").exists()
    assert not (tmp_path / "records" / "records.csv").exists()
    assert not (tmp_path / "passwords" / "password_samples.jsonl").exists()
    assert not (tmp_path / "passwords" / "password_samples.csv").exists()

    first_record_chunk = (tmp_path / "records" / "records-0001.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    assert len(first_record_chunk) == 500
    last_password_chunk = (tmp_path / "passwords" / "password-samples-0003.csv").read_text(
        encoding="utf-8"
    ).splitlines()
    assert len(last_password_chunk) == 2  # header plus the final row

    saved_manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert saved_manifest["data_policy"].startswith("Synthetic fixtures only")
    preview = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "records-0001.jsonl" in preview
    assert "password-samples-0001.csv" in preview
    assert "user00000001@example.invalid" in preview
    assert '"password_sample":' not in preview
