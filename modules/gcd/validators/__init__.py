"""
GCD specification validators.

Each function raises :class:`GCDValidationError` when a condition is not met.
"""

from __future__ import annotations

from typing import List

from ..exceptions import GCDValidationError


def validate_level_number(value: int) -> None:
    if not isinstance(value, int) or value <= 0:
        raise GCDValidationError("Level number must be a positive integer.")


def validate_material_mass(value: float) -> None:
    if not isinstance(value, (int, float)) or value <= 0:
        raise GCDValidationError("Active material mass must be a positive number.")


def validate_level_lists(
    level_number: int,
    level_current: List[float],
    level_time: List[float],
) -> None:
    if len(level_current) != level_number or len(level_time) != level_number:
        raise GCDValidationError(
            "Level currents and times must have the same length as level_number."
        )
    if not all(isinstance(x, (int, float)) for x in level_current):
        raise GCDValidationError("All level currents must be numbers.")
    if not all(x > 0 for x in level_time):
        raise GCDValidationError("All level times must be positive numbers.")


def validate_separation_flags(cycle_separated: bool, level_separated: bool) -> None:
    if level_separated and not cycle_separated:
        raise GCDValidationError("Levels cannot be separated if cycles are not.")
