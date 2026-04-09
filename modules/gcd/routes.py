"""
GCD module — Flask Blueprint routes.
"""

from __future__ import annotations

import pandas as pd
from flask import Blueprint, current_app, flash, render_template, request

from modules.data_io import DataExporter, DataImporter

from .forms import GCDExperimentSpecsForm
from .models import GCDExperimentSpecs
from .services.analyzer import GCDAnalyzer
from .services.calculator import GCDCalculator

gcd_bp = Blueprint("gcd", __name__, url_prefix="/GCD")


@gcd_bp.route("/", methods=["GET", "POST"])
def index():
    form = GCDExperimentSpecsForm()

    if request.method == "POST" and form.validate_on_submit():
        specs = GCDExperimentSpecs(
            level_number=form.level_number.data,
            level_current=[
                float(x.strip()) for x in form.level_currents.data.split(",")
            ],
            level_time=[
                float(x.strip()) for x in form.level_times.data.split(",")
            ],
            material_mass=form.material_mass.data,
            cycle_separated=form.cycles_separated.data == "True",
            level_separated=form.levels_separated.data == "True",
        )

        importer = DataImporter(form.raw_data.data)
        if not importer.result.ok:
            flash(importer.result.status_message, "error")
            return render_template("gcd/index.html", form=form)

        analyzer = GCDAnalyzer(importer.result.data, specs)
        calculator = GCDCalculator(analyzer.unified_data, specs)

        max_rows = current_app.config.get("EXPORT_MAX_ROWS", 200)
        DataExporter().export_gcd(
            calculator.levels_info,
            calculator.level_frames,
            importer.result.file_name,
            max_rows=max_rows,
        )

        dataframe_html = _render_summary_table(calculator.levels_info)
        return render_template("gcd/index.html", form=form, dataframe=dataframe_html)

    return render_template("gcd/index.html", form=form)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _render_summary_table(levels_info: list) -> str:
    """Convert *levels_info* list of dicts to a styled HTML table."""
    df = pd.DataFrame(levels_info)
    styled = df.style.set_properties(
        **{"text-align": "center"}
    ).set_table_styles(
        [
            {
                "selector": "tr:nth-child(even)",
                "props": [("background-color", "rgb(245 245 244)")],
            },
            {
                "selector": "tr:nth-child(odd)",
                "props": [("background-color", "rgb(214 211 209)")],
            },
            {
                "selector": "tr",
                "props": [("border", "solid"), ("padding", "4px 0 4px 0")],
            },
            {
                "selector": "td",
                "props": [("padding", "0 16px 0 16px")],
            },
        ]
    )
    return styled.to_html(justify="center", index=False)
