from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class GoalForm(FlaskForm):
    weight = IntegerField('Weight to Loose', validators=[DataRequired()])
    days = IntegerField('Days to achieve Goal', validators=[DataRequired()])
    start_date = DateField('Start Date',validators=[DataRequired()])
    submit = SubmitField('Go')
