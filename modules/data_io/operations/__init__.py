"""
Atomic file-system operations for the data_io module.

Each function does exactly one thing and raises a standard Python
exception on failure so that the service layer can decide how to handle it.
"""

from __future__ import annotations

import os
from typing import Tuple

import pandas as pd


def extract_name_and_extension(path: str) -> Tuple[str, str]:
    """
    Split *path* into ``(name_without_extension, extension_without_dot)``.

    Examples::

        >>> extract_name_and_extension("data/experiment.xlsx")
        ('data/experiment', 'xlsx')
    """
    name, ext = os.path.splitext(path)
    return name, ext.lstrip(".")


def read_excel(path: str) -> pd.DataFrame:
    """Load an Excel file and return a DataFrame."""
    return pd.read_excel(path)


def read_csv(path: str) -> pd.DataFrame:
    """Load a CSV file and return a DataFrame."""
    return pd.read_csv(path)
