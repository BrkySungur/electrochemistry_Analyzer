"""
GCDCalculator service.

Derives battery-relevant properties (specific capacity, energy density,
power density) for every charge/discharge level.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import pandas as pd
from scipy.integrate import cumulative_trapezoid

from ..config import (
    COL_CURRENT,
    COL_ENERGY_DENSITY,
    COL_POTENTIAL,
    COL_POWER_DENSITY,
    COL_SPECIFIC_CAPACITY,
    COL_TIME,
)
from ..models import GCDExperimentSpecs


class GCDCalculator:
    """
    Calculate per-level battery properties from a unified GCD DataFrame.

    Usage::

        calc              = GCDCalculator(unified_data, specs)
        level_frames      = calc.level_frames   # List[pd.DataFrame]
        levels_info       = calc.levels_info    # List[dict]
    """

    def __init__(
        self, unified_data: pd.DataFrame, specs: GCDExperimentSpecs
    ) -> None:
        self.levels_info: List[Dict] = []
        self.level_frames: List[pd.DataFrame] = []
        self._calculate(unified_data, specs)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _calculate(
        self, data: pd.DataFrame, specs: GCDExperimentSpecs
    ) -> None:
        mass = specs.material_mass

        for i in range(data.shape[1] // 3):
            frame = self._build_level_frame(data, i, mass)
            self.level_frames.append(frame)
            self.levels_info.append(self._summarise(frame, i, specs))

    @staticmethod
    def _build_level_frame(
        data: pd.DataFrame, index: int, mass: float
    ) -> pd.DataFrame:
        """Extract one level from *data* and compute derived columns."""
        frame = pd.DataFrame(
            {
                COL_TIME: data.iloc[:, 3 * index],
                COL_CURRENT: data.iloc[:, 3 * index + 1],
                COL_POTENTIAL: data.iloc[:, 3 * index + 2],
            }
        )

        frame[COL_SPECIFIC_CAPACITY] = abs(
            (frame[COL_TIME] / 3600) * (frame[COL_CURRENT] * 1000) / mass
        )
        frame[COL_ENERGY_DENSITY] = abs(
            cumulative_trapezoid(
                frame[COL_SPECIFIC_CAPACITY],
                x=frame[COL_POTENTIAL],
                initial=0,
            )
        )
        frame[COL_POWER_DENSITY] = (
            frame[COL_ENERGY_DENSITY] / (frame[COL_TIME] / 3600)
        )
        return frame.dropna()

    @staticmethod
    def _summarise(
        frame: pd.DataFrame, index: int, specs: GCDExperimentSpecs
    ) -> Dict:
        return {
            "ID": index + 1,
            "Cycle": index // specs.level_number + 1,
            "Level": index % specs.level_number + 1,
            COL_CURRENT: frame[COL_CURRENT].iloc[-1],
            COL_TIME: frame[COL_TIME].iloc[-1],
            COL_SPECIFIC_CAPACITY: frame[COL_SPECIFIC_CAPACITY].iloc[-1],
            COL_ENERGY_DENSITY: frame[COL_ENERGY_DENSITY].iloc[-1],
            COL_POWER_DENSITY: frame[COL_POWER_DENSITY].iloc[-1],
        }
