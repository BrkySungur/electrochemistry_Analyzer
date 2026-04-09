"""
DataImporter service.

Wraps the atomic file operations and validators into a single high-level
class that is safe to use from routes or scripts.
"""

from __future__ import annotations

from ..config import STATUS_MESSAGES
from ..exceptions import EmptyFileError, FileLoadError, UnsupportedFileFormatError
from ..models import ImportResult
from ..operations import extract_name_and_extension, read_csv, read_excel
from ..validators import is_non_empty_dataframe, is_supported_file_type


class DataImporter:
    """
    Import tabular data from ``xlsx``, ``xls``, or ``csv`` files.

    Usage::

        importer = DataImporter("path/to/file.xlsx")
        result   = importer.result          # ImportResult dataclass
        df       = importer.result.data     # pandas DataFrame
    """

    def __init__(self, path: str) -> None:
        file_name, file_type = extract_name_and_extension(path)
        self.result = ImportResult(
            file_path=path,
            file_name=file_name,
            file_type=file_type,
        )
        self._load()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """Populate *self.result* with loaded data or an error status."""
        if not is_supported_file_type(self.result.file_type):
            self._set_status(400)
            return

        try:
            df = self._read_file()
        except Exception as exc:
            self._set_status(404)
            return

        if not is_non_empty_dataframe(df):
            self._set_status(204)
            return

        self.result.data = df
        self._set_status(200)

    def _read_file(self):
        """Dispatch to the correct atomic reader based on file type."""
        ft = self.result.file_type.lower()
        if ft in ("xlsx", "xls"):
            return read_excel(self.result.file_path)
        return read_csv(self.result.file_path)

    def _set_status(self, code: int) -> None:
        self.result.status = code
        self.result.status_message = STATUS_MESSAGES.get(code, "Unknown status.")
