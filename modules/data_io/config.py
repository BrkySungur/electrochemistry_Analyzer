"""
data_io module configuration.

All tuneable parameters for the Data I/O module live here so that
callers never need magic strings or numbers scattered across the code.
"""

# ---------------------------------------------------------------------------
# Supported file extensions (lower-case, without leading dot)
# ---------------------------------------------------------------------------
SUPPORTED_FILE_TYPES: list[str] = ["xlsx", "xls", "csv"]

# ---------------------------------------------------------------------------
# HTTP-style status codes used by DataImporter
# ---------------------------------------------------------------------------
STATUS_MESSAGES: dict[int, str] = {
    200: "Success: Data loaded successfully.",
    204: "Warning: File is empty.",
    400: "Warning: File format is invalid.",
    404: "Warning: File was not found.",
}
