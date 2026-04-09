"""
GCD experiment specification model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from ..validators import (
    validate_level_lists,
    validate_level_number,
    validate_material_mass,
    validate_separation_flags,
)


@dataclass
class GCDExperimentSpecs:
    """
    Immutable value object describing the conditions of one GCD experiment.

    Attributes:
        level_number:     Number of current levels in each cycle.
        level_current:    List of current values (A) for each level.
        level_time:       List of time durations (s) for each level.
        material_mass:    Active material mass (g).
        cycle_separated:  True when each cycle occupies its own column pair.
        level_separated:  True when each level occupies its own column pair
                          (requires *cycle_separated* to also be True).
    """

    level_number: int
    level_current: List[float]
    level_time: List[float]
    material_mass: float
    cycle_separated: bool = False
    level_separated: bool = False

    def __post_init__(self) -> None:
        validate_level_number(self.level_number)
        validate_material_mass(self.material_mass)
        validate_level_lists(self.level_number, self.level_current, self.level_time)
        validate_separation_flags(self.cycle_separated, self.level_separated)
