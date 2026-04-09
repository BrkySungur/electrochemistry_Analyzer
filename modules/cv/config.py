"""
CV module configuration.

Unit-conversion tables for Cyclic Voltammetry data are defined here.
"""

UNIT_CONVERSION: dict[str, float] = {
    "V": 1e0,
    "mV": 1e-3,
    "uV": 1e-6,
    "A": 1e0,
    "mA": 1e-3,
    "uA": 1e-6,
    "nA": 1e-9,
    "pA": 1e-12,
    "fA": 1e-15,
}
