"""Command-line entry point for synthetic dataset generation."""

import argparse
import json
from pathlib import Path

from leaklab.config import settings
from leaklab.dataset import generate_dataset
from leaklab.password_lab import export_password_samples, summarize_synthetic_samples


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="leaklab", description="Synthetic password research lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="generate fictional profile fixtures")
    generate.add_argument("--count", type=int, default=settings.default_records)
    generate.add_argument("--seed", type=int, default=settings.random_seed)
    generate.add_argument("--format", choices=("jsonl", "csv", "both"), default="both")
    generate.add_argument("--output", type=Path, default=Path("data/generated"))

    passwords = subparsers.add_parser("passwords", help="generate fictional password samples")
    passwords.add_argument("--count", type=int, default=settings.default_records)
    passwords.add_argument("--seed", type=int, default=settings.random_seed)
    passwords.add_argument("--format", choices=("jsonl", "csv", "both"), default="both")
    passwords.add_argument("--output", type=Path, default=Path("data/passwords"))

    analyze = subparsers.add_parser("analyze", help="summarize generated password fixtures")
    analyze.add_argument("--count", type=int, default=1000)
    analyze.add_argument("--seed", type=int, default=settings.random_seed)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "generate":
        result = generate_dataset(args.count, args.output, args.seed, args.format)
        print(json.dumps({"output": str(args.output), "records_per_format": result}, indent=2))
    elif args.command == "passwords":
        result = export_password_samples(args.count, args.output, args.seed, args.format)
        print(json.dumps({"output": str(args.output), "samples_per_format": result}, indent=2))
    elif args.command == "analyze":
        print(json.dumps(summarize_synthetic_samples(args.count, args.seed), indent=2))


if __name__ == "__main__":
    main()
