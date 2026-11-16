"""Synthetic-only password quality research fixtures.

This module never imports breach corpora or accepts account credentials.
All generated strings are fictional test samples.
"""
from __future__ import annotations

import csv
import json
import random
import string
from collections import Counter
from pathlib import Path
from collections.abc import Iterator

WORDS = ("cobalt", "maple", "orbit", "velvet", "harbor", "comet", "willow", "pixel",
         "canyon", "ember", "lunar", "meadow", "quartz", "ripple", "thunder", "spruce")
PATTERNS = ("lowercase_digits", "three_word_phrase", "mixed_random")


def generate_password_samples(count: int, seed: int = 42) -> Iterator[dict[str, str]]:
    """Yield deterministic fictional password samples; never use for real accounts."""
    if count < 0:
        raise ValueError("count must be zero or greater")
    rng = random.Random(seed)
    alphabet = string.ascii_letters + string.digits + "!@#$%&*?"
    for index in range(count):
        pattern = PATTERNS[index % len(PATTERNS)]
        if pattern == "lowercase_digits":
            value = rng.choice(WORDS) + str(rng.randrange(10, 10000))
        elif pattern == "three_word_phrase":
            value = "-".join(rng.sample(WORDS, 3))
        else:
            value = "".join(rng.choice(alphabet) for _ in range(rng.randint(14, 22)))
        yield {"sample_id": f"synthetic-{index + 1:08d}", "password_sample": value,
               "pattern": pattern, "synthetic": "true"}


def assess_password_shape(value: str) -> dict[str, int | str]:
    """Return transparent shape heuristics, not a crack-time or breach-match claim."""
    length = len(value)
    classes = sum((any(c.islower() for c in value), any(c.isupper() for c in value),
                   any(c.isdigit() for c in value), any(not c.isalnum() for c in value)))
    score = min(4, int(length >= 12) + int(length >= 16) + int(classes >= 3)
                + int(length >= 20 and classes >= 2))
    return {"length": length, "character_classes": classes, "shape_score": score,
            "rating": ("very_short", "limited", "moderate", "good", "strong")[score]}


def summarize_synthetic_samples(count: int = 1000, seed: int = 42) -> dict[str, object]:
    """Aggregate only generated fixtures; no sample strings are returned."""
    patterns: Counter[str] = Counter()
    ratings: Counter[str] = Counter()
    total_length = 0
    total = 0
    for sample in generate_password_samples(count, seed):
        assessment = assess_password_shape(sample["password_sample"])
        patterns[sample["pattern"]] += 1
        ratings[str(assessment["rating"])] += 1
        total_length += int(assessment["length"])
        total += 1
    return {"samples_analyzed": total, "average_length": round(total_length / total, 2) if total else 0,
            "patterns": dict(patterns), "ratings": dict(ratings),
            "notice": "Synthetic fixtures only; heuristic shape analysis, not breach checking."}


def export_password_samples(count: int, output_dir: Path, seed: int = 42,
                            fmt: str = "both") -> dict[str, int]:
    if fmt not in {"jsonl", "csv", "both"}:
        raise ValueError("format must be jsonl, csv, or both")
    output_dir.mkdir(parents=True, exist_ok=True)
    result: dict[str, int] = {}
    for kind in (("jsonl", "csv") if fmt == "both" else (fmt,)):
        path = output_dir / f"password_samples.{kind}"
        written = 0
        with path.open("w", encoding="utf-8", newline="") as stream:
            if kind == "csv":
                writer = csv.DictWriter(stream, fieldnames=("sample_id", "password_sample", "pattern", "synthetic"))
                writer.writeheader()
                for row in generate_password_samples(count, seed):
                    writer.writerow(row)
                    written += 1
            else:
                for row in generate_password_samples(count, seed):
                    stream.write(json.dumps(row, ensure_ascii=False) + "\n")
                    written += 1
        result[kind] = written
    return result
