"""
GCD custom exceptions.
"""


class GCDError(Exception):
    """Base exception for all GCD-module errors."""


class GCDValidationError(GCDError):
    """Raised when experiment specifications fail validation."""
