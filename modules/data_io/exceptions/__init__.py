"""
data_io exceptions.
"""


class DataIOError(Exception):
    """Base exception for all data I/O errors."""


class UnsupportedFileFormatError(DataIOError):
    """Raised when the file extension is not supported."""


class EmptyFileError(DataIOError):
    """Raised when the imported file contains no data."""


class FileLoadError(DataIOError):
    """Raised when the file cannot be read (missing, permission error, etc.)."""
