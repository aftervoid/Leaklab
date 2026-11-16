"""Command-line entry point."""

import argparse
import json
from pathlib import Path

from leaklab.config import settings
from leaklab.dataset import generate_dataset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="leaklab", description="Synthetic dataset lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="generate fictional test records")
    generate.add_argument("--count", type=int, default=settings.default_records)
    generate.add_argument("--seed", type=int, default=settings.random_seed)
    generate.add_argument("--format", choices=("jsonl", "csv", "both"), default="both")
    generate.add_argument("--output", type=Path, default=Path("data/generated"))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "generate":
        result = generate_dataset(args.count, args.output, args.seed, args.format)
        print(json.dumps({"output": str(args.output), "records_per_format": result}, indent=2))


if __name__ == "__main__":
    main()
