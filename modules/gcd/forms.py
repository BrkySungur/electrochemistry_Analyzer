"""
GCD module — Flask-WTF form definitions.
"""

from __future__ import annotations

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import FloatField, IntegerField, RadioField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class GCDExperimentSpecsForm(FlaskForm):
    """Form for capturing GCD experiment parameters and raw data upload."""

    raw_data = FileField("Choose File", validators=[FileRequired()])

    cycles_separated = RadioField(
        label="Cycles Separated",
        choices=[("True", "True"), ("False", "False")],
        default="False",
    )
    levels_separated = RadioField(
        label="Levels Separated",
        choices=[("True", "True"), ("False", "False")],
        default="False",
    )

    level_number = IntegerField("Level Number", validators=[DataRequired()])

    level_currents = TextAreaField(
        "Level Currents (Unit: Ampere)",
        validators=[DataRequired()],
        render_kw={"placeholder": "Use comma for separating the level currents"},
    )
    level_times = TextAreaField(
        "Level Times (Unit: Second)",
        validators=[DataRequired()],
        render_kw={"placeholder": "Use comma for separating the level times"},
    )

    material_mass = FloatField(
        "Material Mass (Unit: Gram)", validators=[DataRequired()]
    )

    submit = SubmitField("Submit")
