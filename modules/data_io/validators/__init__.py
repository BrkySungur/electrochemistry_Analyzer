"""
data_io validators.

These functions return True/False and raise no exceptions themselves —
exceptions are the responsibility of the caller (services layer).
"""

from __future__ import annotations

import pandas as pd

from ..config import SUPPORTED_FILE_TYPES


def is_supported_file_type(file_type: str) -> bool:
    """Return True if *file_type* (without dot) is in the supported list."""
    return file_type.lower() in SUPPORTED_FILE_TYPES


def is_non_empty_dataframe(df: pd.DataFrame) -> bool:
    """Return True when *df* has at least one column and one row."""
    return len(df.columns) > 0 and len(df.index) > 0
