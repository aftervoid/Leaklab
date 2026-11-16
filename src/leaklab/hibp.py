"""Privacy-preserving checks for LeakLab-generated synthetic samples.

Only the first five characters of a locally computed SHA-1 digest are sent
to Have I Been Pwned. This module accepts generator records, not raw input.
No password, full digest, or API response corpus is persisted.
"""
# ruff: noqa: I001
from __future__ import annotations

import hashlib
from collections.abc import Iterable
from urllib.error import URLError
from urllib.request import Request, urlopen


HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/"


def check_synthetic_sample(sample: dict[str, str], timeout: float = 8.0) -> int:
    """Return HIBP prevalence count for one explicitly synthetic fixture.

    HIBP's k-anonymity protocol sends only the first five SHA-1 hex characters.
    The full digest is compared locally; raw samples and hash data are not saved.
    """
    if sample.get("synthetic") != "true" or not sample.get("sample_id", "").startswith("synthetic-"):
        raise ValueError("HIBP checks are restricted to LeakLab-generated synthetic samples")

    digest = hashlib.sha1(sample["password_sample"].encode("utf-8")).hexdigest().upper()
    prefix, suffix = digest[:5], digest[5:]
    request = Request(
        HIBP_RANGE_URL + prefix,
        headers={"Add-Padding": "true", "User-Agent": "LeakLab-Synthetic-Research/1.0"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("ascii", errors="strict")
    except (OSError, URLError, UnicodeError) as exc:
        raise RuntimeError("HIBP Pwned Passwords service is unavailable") from exc

    for line in body.splitlines():
        candidate, separator, count_text = line.strip().partition(":")
        if separator and candidate.upper() == suffix:
            try:
                return int(count_text)
            except ValueError as exc:
                raise RuntimeError("HIBP returned an invalid prevalence count") from exc
    return 0


def summarize_hibp_synthetic_samples(samples: Iterable[dict[str, str]]) -> dict[str, int | str]:
    """Return aggregate-only results; never return sample strings or hashes."""
    checked = 0
    found = 0
    total_prevalence = 0
    for sample in samples:
        count = check_synthetic_sample(sample)
        checked += 1
        if count:
            found += 1
            total_prevalence += count
    return {
        "samples_checked": checked,
        "samples_found_in_hibp": found,
        "total_recorded_occurrences": total_prevalence,
        "source": "Have I Been Pwned Pwned Passwords API",
        "method": "k-anonymity SHA-1 range lookup; aggregate results only",
    }
