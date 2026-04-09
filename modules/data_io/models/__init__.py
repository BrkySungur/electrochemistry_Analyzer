"""
data_io models — plain data containers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import pandas as pd


@dataclass
class ImportResult:
    """
    Holds the outcome of a single file-import operation.

    Attributes:
        file_path:      Original path supplied by the caller.
        file_name:      Path without the file extension.
        file_type:      Extension without the leading dot (e.g. ``"xlsx"``).
        data:           Loaded DataFrame, or ``None`` on failure.
        status:         HTTP-style status code (200, 204, 400, 404).
        status_message: Human-readable description of *status*.
    """

    file_path: str
    file_name: str
    file_type: str
    data: Optional[pd.DataFrame] = field(default=None, repr=False)
    status: int = 0
    status_message: str = ""

    @property
    def ok(self) -> bool:
        """Return ``True`` when the import succeeded (status 200)."""
        return self.status == 200
