"""Shared model helpers."""
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class BaseModel:
    id: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)
