"""
CVAnalyzer service (stub).

Converts raw CV data into a unified DataFrame with SI units.
"""

from __future__ import annotations

import pandas as pd

from ..operations import convert_to_si_units, split_headers


class CVAnalyzer:
    """
    Unify raw CV data by converting column units to SI.

    Usage::

        analyzer     = CVAnalyzer(raw_df)
        unified_data = analyzer.unified_data   # pandas DataFrame
    """

    def __init__(self, raw_data: pd.DataFrame) -> None:
        self.raw_data = raw_data
        self.headers = split_headers(raw_data.columns.tolist())
        self.unified_data: pd.DataFrame = convert_to_si_units(raw_data, self.headers)
