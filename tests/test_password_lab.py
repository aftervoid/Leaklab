from leaklab.password_lab import (
    assess_password_shape,
    export_password_samples,
    generate_password_samples,
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


def test_hibp_rejects_non_synthetic_records():
    from leaklab.hibp import check_synthetic_sample

    try:
        check_synthetic_sample({"sample_id": "user-1", "password_sample": "not-for-use", "synthetic": "false"})
    except ValueError as exc:
        assert "synthetic" in str(exc)
    else:
        raise AssertionError("non-synthetic record must be rejected")


def test_hibp_k_anonymity_lookup_uses_only_hash_prefix(monkeypatch):
    import hashlib
    from leaklab.hibp import check_synthetic_sample

    sample = next(generate_password_samples(1, seed=42))
    digest = hashlib.sha1(sample["password_sample"].encode("utf-8")).hexdigest().upper()
    seen = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def read(self):
            return f"{digest[5:]}:17\\r\\n".encode("ascii")

    def fake_urlopen(request, timeout):
        seen["url"] = request.full_url
        seen["padding"] = request.get_header("Add-padding")
        seen["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr("leaklab.hibp.urlopen", fake_urlopen)
    assert check_synthetic_sample(sample) == 17
    assert digest not in seen["url"]
    assert digest[:5] in seen["url"]
    assert seen["padding"] == "true"


def test_hibp_summary_returns_aggregates_only(monkeypatch):
    from leaklab.hibp import summarize_hibp_synthetic_samples

    monkeypatch.setattr("leaklab.hibp.check_synthetic_sample", lambda sample: 0)
    result = summarize_hibp_synthetic_samples(generate_password_samples(3))
    assert result["samples_checked"] == 3
    assert result["samples_found_in_hibp"] == 0
    assert "password_sample" not in result
