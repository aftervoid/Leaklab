"""Application settings with safe local defaults."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str = os.getenv("LEAKLAB_ENV", "development")
    host: str = os.getenv("LEAKLAB_HOST", "127.0.0.1")
    port: int = int(os.getenv("LEAKLAB_PORT", "8000"))
    default_records: int = int(os.getenv("LEAKLAB_DEFAULT_RECORDS", "1000000"))
    random_seed: int = int(os.getenv("LEAKLAB_RANDOM_SEED", "42"))


settings = Settings()
