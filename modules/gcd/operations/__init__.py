"""
Atomic GCD operations.

These are pure, stateless functions that transform data.  They have no
knowledge of Flask, file I/O, or application state.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Union

import pandas as pd

from ..config import UNIT_CONVERSION, COL_CURRENT, COL_POTENTIAL, COL_TIME


# ---------------------------------------------------------------------------
# Header / unit operations
# ---------------------------------------------------------------------------

HeaderDict = Dict[str, Union[str, float, None]]


def split_header(column_name: str) -> HeaderDict:
    """
    Parse a single column header of the form ``"Title / unit"`` into a dict.

    Handles duplicate-column suffixes produced by pandas (e.g. ``"Time / s.1"``).

    Returns a dict with keys ``title``, ``unit``, and ``conversion_multiplier``.
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
    """
    Return a copy of *raw_data* with all columns converted to SI units.

    Columns without a recognised unit are kept as-is (a warning is printed).
    The column names are replaced with their title-only versions.
    """
    df = raw_data.copy()
    for i, header in enumerate(headers):
        multiplier: Optional[float] = header["conversion_multiplier"]
        if multiplier is not None:
            df.iloc[:, i] = df.iloc[:, i] * multiplier
        else:
            print(f"Warning: no SI conversion found for unit '{header['unit']}'.")
    df.columns = [h["title"] for h in headers]
    return df


# ---------------------------------------------------------------------------
# Data-unification operations
# ---------------------------------------------------------------------------

def unify_separated(
    data: pd.DataFrame,
    level_current: List[float],
    level_number: int,
) -> pd.DataFrame:
    """
    Build a unified DataFrame from data where every level has its own
    column pair (time + potential).

    The output contains triplets of columns:
    ``[COL_TIME, COL_CURRENT, COL_POTENTIAL]`` repeated for every level.
    """
    frames: List[pd.DataFrame] = []
    for i in range(data.shape[1] // 2):
        frame = pd.DataFrame(
            {
                COL_TIME: data.iloc[:, 2 * i],
                COL_CURRENT: level_current[i % level_number],
                COL_POTENTIAL: data.iloc[:, 2 * i + 1],
            }
        )
        frames.append(frame)
    return pd.concat(frames, axis=1)
