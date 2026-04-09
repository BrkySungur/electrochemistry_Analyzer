"""
DataExporter service.

Writes analysis results to Excel workbooks with a summary sheet and a
details sheet (one block of columns per level).
"""

from __future__ import annotations

from typing import List

import pandas as pd
from openpyxl import Workbook


class DataExporter:
    """
    Export GCD analysis results to a multi-sheet Excel file.

    Usage::

        exporter = DataExporter()
        exporter.export_gcd(levels_info, levels_details, "output/experiment")
    """

    def export_gcd(
        self,
        levels_info: List[dict],
        levels_details: List[pd.DataFrame],
        file_path: str,
        max_rows: int = 200,
    ) -> None:
        """
        Write summary and per-level detail data to an Excel workbook.

        Args:
            levels_info:    List of dicts describing each level (summary rows).
            levels_details: List of DataFrames with per-level detailed data.
            file_path:      Destination path **without** extension.  The method
                            appends ``" Results.xlsx"`` automatically.
            max_rows:       Maximum number of detail rows written per level.
        """
        output_path = f"{file_path} Results.xlsx"
        df_summary = pd.DataFrame(levels_info)

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df_summary.to_excel(writer, index=False, sheet_name="Summary")

            workbook: Workbook = writer.book

            for index, items in enumerate(levels_details):
                items = self._downsample(items, max_rows)

                items.to_excel(
                    writer,
                    index=False,
                    sheet_name="Details",
                    startcol=7 * index,
                    startrow=1,
                )

                sheet = workbook["Details"]
                sheet.cell(row=1, column=7 * index + 1, value="Level ID")
                sheet.cell(row=1, column=7 * index + 2, value=index + 1)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _downsample(df: pd.DataFrame, max_rows: int) -> pd.DataFrame:
        """Return a version of *df* with at most *max_rows* rows."""
        if len(df) > max_rows:
            step = max(len(df) // max_rows, 1)
            df = df.iloc[::step]
        return df.head(max_rows)
