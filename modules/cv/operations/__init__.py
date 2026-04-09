"""
Atomic CV operations (stub).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Union

import pandas as pd

from ..config import UNIT_CONVERSION

HeaderDict = Dict[str, Union[str, float, None]]


def split_header(column_name: str) -> HeaderDict:
    """
    Parse a single CV column header of the form ``"Title / unit"`` into a dict.

    Handles duplicate-column suffixes produced by pandas (e.g. ``"Voltage / V.1"``).
    """
    if "." in column_name:
        column_name = column_name.split(".")[0]

    title, unit = column_name.rsplit(" /", 1)
    unit = unit.strip()
    return {
        "title": title.strip(),
        "unit": unit,
        "conversion_multiplier": UNIT_CONVERSION.get(unit),
    }


def split_headers(columns: List[str]) -> List[HeaderDict]:
    """Apply :func:`split_header` to every item in *columns*."""
    return [split_header(col) for col in columns]


def convert_to_si_units(
    raw_data: pd.DataFrame, headers: List[HeaderDict]
) -> pd.DataFrame:
    """Return a copy of *raw_data* with all columns converted to SI units."""
    df = raw_data.copy()
    for i, header in enumerate(headers):
        multiplier: Optional[float] = header["conversion_multiplier"]
        if multiplier is not None:
            df.iloc[:, i] = df.iloc[:, i] * multiplier
        else:
            print(f"Warning: no SI conversion found for unit '{header['unit']}'.")
    df.columns = [h["title"] for h in headers]
    return df
