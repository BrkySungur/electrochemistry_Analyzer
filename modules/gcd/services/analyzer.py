"""
GCDAnalyzer service.

Converts raw imported data into a unified DataFrame ready for
:class:`GCDCalculator`.
"""

from __future__ import annotations

import pandas as pd

from ..models import GCDExperimentSpecs
from ..operations import (
    convert_to_si_units,
    split_headers,
    unify_separated,
)


class GCDAnalyzer:
    """
    Unify raw GCD data by converting units and restructuring columns.

    Usage::

        analyzer     = GCDAnalyzer(raw_df, specs)
        unified_data = analyzer.unified_data   # pandas DataFrame
    """

    def __init__(
        self, raw_data: pd.DataFrame, specs: GCDExperimentSpecs
    ) -> None:
        self.raw_data = raw_data
        self.headers = split_headers(raw_data.columns.tolist())
        si_data = convert_to_si_units(raw_data, self.headers)
        self.unified_data: pd.DataFrame = self._unify(si_data, specs)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _unify(
        self, data: pd.DataFrame, specs: GCDExperimentSpecs
    ) -> pd.DataFrame:
        if specs.cycle_separated and specs.level_separated:
            return unify_separated(data, specs.level_current, specs.level_number)
        return pd.DataFrame()
