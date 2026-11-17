# Daily generated datasets

The **Daily Synthetic Dataset** GitHub Actions workflow writes its output directly into this directory in the repository.

Each UTC date gets its own folder:

```text
data/daily-datasets/
└── YYYY-MM-DD/
    ├── manifest.json
    ├── records/
    │   ├── records.jsonl
    │   └── records.csv
    └── passwords/
        ├── password_samples.jsonl
        └── password_samples.csv
```

By default, each daily run creates 10,000 fictional profile records and 5,000 fictional password samples. The date-derived seed makes the generated sample values reproducible for that date. Rerunning the workflow on the same date updates that date's folder rather than creating another dated folder.

Only synthetic fixtures are generated. No breach corpus, RockYou records, real passwords, or real account credentials are included.

To generate a bundle locally:

```powershell
python -m pip install .
python -c "from datetime import date; from pathlib import Path; from leaklab.daily import build_daily_bundle; build_daily_bundle(date.today(), Path('data/daily-datasets') / date.today().isoformat())"
```

**Repository growth:** daily files are committed to Git history and therefore accumulate over time. Keep the default dataset sizes modest and review repository size periodically.
