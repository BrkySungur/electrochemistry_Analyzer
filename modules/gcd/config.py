"""
GCD module configuration.

Unit-conversion tables and column-name constants are defined here so that
no magic strings are scattered across services or operations.
"""

# ---------------------------------------------------------------------------
# SI unit-conversion multipliers
# ---------------------------------------------------------------------------
UNIT_CONVERSION: dict[str, float] = {
    "s": 1e0,
    "ms": 1e-3,
    "us": 1e-6,
    "V": 1e0,
    "mV": 1e-3,
    "uV": 1e-6,
}

# ---------------------------------------------------------------------------
# Canonical column names used throughout the GCD pipeline
# ---------------------------------------------------------------------------
COL_TIME = "Time / s"
COL_CURRENT = "Current / A"
COL_POTENTIAL = "Potential / V"
COL_SPECIFIC_CAPACITY = "Specific Capacity / mAh/g"
COL_ENERGY_DENSITY = "Energy Density / Wh/kg"
COL_POWER_DENSITY = "Power Density / W/kg"
