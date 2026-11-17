# Daily generated datasets

The daily dataset pipeline uses two independent GitHub Actions workflows.

1. **Generator** creates the full synthetic exports and commits them directly to the repository.
2. **Splitter** starts only after the generator workflow completes successfully, waits **11 minutes**, then creates numbered 500-row copies. It never deletes or modifies the original large exports.

Each UTC date gets its own folder:

```text
data/daily-datasets/
└── YYYY-MM-DD/
    ├── manifest.json
    ├── README.md
    ├── records/
    │   ├── records.jsonl
    │   ├── records.csv
    │   ├── records-0001.jsonl
    │   ├── records-0001.csv
    │   └── ...
    └── passwords/
        ├── password_samples.jsonl
        ├── password_samples.csv
        ├── password-samples-0001.jsonl
        ├── password-samples-0001.csv
        └── ...
```

By default, each daily run creates 10,000 fictional profile records and 5,000 fictional password samples. The date-derived seed makes the generated sample values reproducible for that date. Rerunning the generator on the same date updates that date's original exports; the splitter then refreshes the numbered copies.

The original monolithic JSONL and CSV files remain in the repository alongside the smaller numbered copies. No GitHub Actions Artifacts are used; both workflows commit their outputs directly to the repository.

Only synthetic fixtures are generated. No breach corpus, RockYou records, real passwords, or real account credentials are included.

To generate a bundle locally:

```powershell
python -m pip install .
python -c "from datetime import date; from pathlib import Path; from leaklab.daily import build_daily_bundle; build_daily_bundle(date.today(), Path('data/daily-datasets') / date.today().isoformat())"
```

To split an existing bundle locally after generation:

```powershell
python -c "from datetime import date; from pathlib import Path; from leaklab.split_daily import split_daily_bundle; split_daily_bundle(Path('data/daily-datasets') / date.today().isoformat())"
```

**Repository growth:** original exports and their numbered copies are both committed to Git history, so storage grows faster than when only one representation is kept. Review repository size periodically.
