"""
CV custom exceptions.
"""


class CVError(Exception):
    """Base exception for all CV-module errors."""


class CVValidationError(CVError):
    """Raised when CV experiment specifications fail validation."""
