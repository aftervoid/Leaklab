from leaklab.password_lab import (
    assess_password_shape, export_password_samples, generate_password_samples,
    summarize_synthetic_samples,
)


def test_password_fixtures_are_deterministic_and_marked_synthetic():
    first = list(generate_password_samples(12, seed=9))
    second = list(generate_password_samples(12, seed=9))
    assert first == second
    assert all(row["synthetic"] == "true" for row in first)
    assert all(row["sample_id"].startswith("synthetic-") for row in first)


def test_shape_assessment_is_bounded_and_explained():
    result = assess_password_shape("Cobalt-Maple-2030!")
    assert result["length"] == 18
    assert 0 <= result["shape_score"] <= 4
    assert result["rating"] in {"very_short", "limited", "moderate", "good", "strong"}


def test_summary_contains_only_aggregates():
    result = summarize_synthetic_samples(30, seed=1)
    assert result["samples_analyzed"] == 30
    assert sum(result["patterns"].values()) == 30
    assert "password_sample" not in result


def test_hybrid_password_export(tmp_path):
    result = export_password_samples(7, tmp_path, seed=2, fmt="both")
    assert result == {"jsonl": 7, "csv": 7}
    assert len((tmp_path / "password_samples.jsonl").read_text().splitlines()) == 7
    assert len((tmp_path / "password_samples.csv").read_text().splitlines()) == 8
