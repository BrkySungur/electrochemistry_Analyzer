from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import *
from wtforms.validators import *
from GCD import *

import pandas as pd
from DataIO import *



app = Flask(__name__)
app.secret_key = '111111'

csrf = CSRFProtect()
csrf.init_app(app)

class GCDExperimentSpecsForm(FlaskForm):
    raw_data = FileField('Choose File',
                         validators=[DataRequired()])
    cycles_seperated = RadioField(label='Cycles Seperated',
                                  choices=[(True, 'True'), (False,'False')],
                                  default=False
                                    )
    levels_seperated = RadioField(label='Levels Seperated',
                                  choices=[(True, 'True'), (False,'False')],
                                  default=False
                                    )
    level_number = IntegerField(
                                'Level Number', 
                                validators=[DataRequired()]
                                )
    level_currents = TextAreaField('Level Currents (Unit: Ampere)',
                            validators=[DataRequired()],
                            render_kw={"placeholder": "Use comma for seperating the level current"}
                            )
    level_times = TextAreaField('Level Times (Unit: Second)',
                            validators=[DataRequired()],
                            render_kw={"placeholder": "Use comma for seperating the level times"}
                            )
    material_mass = FloatField('Material Mass (Unit: Gram)',
                               validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/GCD', methods=['GET', 'POST'])
def gcd():
    form = GCDExperimentSpecsForm()
    if request.method == 'POST' and form.validate_on_submit():
        print('Started')
        GCD_Specs = GCDExperimentSpecs(level_number=form.level_number.data,
                                      level_current= [float(x) for x in form.level_currents.data.split(',')],
                                      level_time= [float(x) for x in form.level_times.data.split(',')],
                                      material_mass=form.material_mass.data,
                                      cycle_separated=form.cycles_seperated.data,
                                      level_separated=form.levels_seperated
                                     )
        Imported_Data = DataImport(form.raw_data.data)

        data = UnifiedDataGCD(Imported_Data.data, GCD_Specs)
        df , list = CalculaterForBattery(data, GCD_Specs)
        
        DataExporterGCD(list, df, Imported_Data.file_name, number_of_rows=200)
        print('Finished')
        dataframe = pd.DataFrame(list)

        dataframe = dataframe.style.set_properties(**{
            'text-align': 'center',
        }).set_table_styles([{
            'selector': 'tr:nth-child(even)',
            'props': [('background-color', 'rgb(245 245 244)')]
        }, {
            'selector': 'tr:nth-child(odd)',
            'props': [('background-color', 'rgb(214 211 209)')]
        },
        {
            'selector': 'tr',
            'props': [('border', 'solid'), ('padding', '4px 0 4px 0')]
        },
        {
            'selector': 'td',
            'props': [('padding', '0 16px 0 16px')]
        }])
        dataframe = dataframe.to_html(justify='center',
                                      index=False,
                                      )
        return render_template('GCD.html', form=form, dataframe=dataframe)
    return render_template('GCD.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, load_dotenv=True)
