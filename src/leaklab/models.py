"""Typed schemas for fictional LeakLab records."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SyntheticRecord(BaseModel):
    """A fictional exposure-style record; it contains no real credentials."""

    model_config = ConfigDict(extra="forbid")

    record_id: str = Field(pattern=r"^ll-[0-9]{8}$")
    username: str
    email: str
    source_label: str
    observed_at: datetime
    record_type: Literal["profile", "contact", "account-metadata"]
    synthetic: Literal[True] = True
