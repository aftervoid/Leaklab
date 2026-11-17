import json
from datetime import date

from leaklab.daily import build_daily_bundle
from leaklab.split_daily import split_daily_bundle


def test_generator_keeps_large_original_exports_then_splitter_adds_chunks(tmp_path):
    manifest = build_daily_bundle(date(2026, 11, 17), tmp_path, 1200, 1001)

    assert manifest["seed"] == 20261117
    assert manifest["split_complete"] is False
    assert (tmp_path / "records" / "records.jsonl").is_file()
    assert (tmp_path / "records" / "records.csv").is_file()
    assert (tmp_path / "passwords" / "password_samples.jsonl").is_file()
    assert (tmp_path / "passwords" / "password_samples.csv").is_file()
    assert not list((tmp_path / "records").glob("records-*.jsonl"))

    split_manifest = split_daily_bundle(tmp_path)
    assert split_manifest["chunk_size"] == 500
    assert split_manifest["split_complete"] is True
    assert len(split_manifest["records_files"]["jsonl"]) == 3
    assert len(split_manifest["records_files"]["csv"]) == 3
    assert len(split_manifest["password_sample_files"]["jsonl"]) == 3
    assert len(split_manifest["password_sample_files"]["csv"]) == 3

    assert split_manifest["records_files"]["jsonl"] == [
        "records-0001.jsonl", "records-0002.jsonl", "records-0003.jsonl"
    ]
    assert split_manifest["password_sample_files"]["csv"][-1] == "password-samples-0003.csv"

    # The second workflow must never remove the large source exports.
    assert (tmp_path / "records" / "records.jsonl").is_file()
    assert (tmp_path / "records" / "records.csv").is_file()
    assert (tmp_path / "passwords" / "password_samples.jsonl").is_file()
    assert (tmp_path / "passwords" / "password_samples.csv").is_file()

    first_record_chunk = (tmp_path / "records" / "records-0001.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    assert len(first_record_chunk) == 500
    last_password_chunk = (tmp_path / "passwords" / "password-samples-0003.csv").read_text(
        encoding="utf-8"
    ).splitlines()
    assert len(last_password_chunk) == 2

    saved_manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert saved_manifest["data_policy"].startswith("Synthetic fixtures only")
    assert saved_manifest["split_complete"] is True
    preview = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "records-0001.jsonl" in preview
    assert "password-samples-0001.csv" in preview
    assert "user00000001@example.invalid" in preview
    assert '"password_sample":' not in preview
