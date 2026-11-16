from pathlib import Path

from leaklab.dataset import generate_dataset, generate_records


def test_generator_is_deterministic_and_synthetic():
    first = list(generate_records(3, seed=7))
    second = list(generate_records(3, seed=7))

    assert [item.model_dump() for item in first] == [item.model_dump() for item in second]
    assert all(item.synthetic is True for item in first)
    assert all(item.email.endswith("@example.invalid") for item in first)


def test_hybrid_export_writes_both_formats(tmp_path: Path):
    result = generate_dataset(5, tmp_path, seed=3, fmt="both")

    assert result == {"jsonl": 5, "csv": 5}
    assert len((tmp_path / "records.jsonl").read_text(encoding="utf-8").splitlines()) == 5
    assert len((tmp_path / "records.csv").read_text(encoding="utf-8").splitlines()) == 6


def test_negative_count_is_rejected():
    try:
        list(generate_records(-1))
    except ValueError as exc:
        assert "zero or greater" in str(exc)
    else:
        raise AssertionError("negative counts must be rejected")
