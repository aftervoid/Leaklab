import json
from datetime import date

from leaklab.daily import build_daily_bundle


def test_daily_bundle_contains_only_expected_synthetic_exports(tmp_path):
    manifest = build_daily_bundle(date(2026, 11, 17), tmp_path, 12, 9)

    assert manifest["seed"] == 20261117
    assert manifest["records_per_format"] == {"jsonl": 12, "csv": 12}
    assert manifest["password_samples_per_format"] == {"jsonl": 9, "csv": 9}
    assert manifest["password_sample_summary"]["samples_analyzed"] == 9
    assert (tmp_path / "records" / "records.jsonl").exists()
    assert (tmp_path / "records" / "records.csv").exists()
    assert (tmp_path / "passwords" / "password_samples.jsonl").exists()
    assert (tmp_path / "passwords" / "password_samples.csv").exists()

    saved_manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert saved_manifest["data_policy"].startswith("Synthetic fixtures only")

    preview = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "first 5 profile records" in preview
    assert "user00000001@example.invalid" in preview
    assert "Password samples (JSONL)" in preview
    assert "password_sample" not in preview
