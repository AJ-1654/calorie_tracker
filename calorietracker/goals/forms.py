from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed


class GoalForm(FlaskForm):
    weight = IntegerField('Weight to Loose', validators=[DataRequired()])
    days = IntegerField('Days to achieve Goal', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    submit = SubmitField('Go')


class DayForm(FlaskForm):
    breakfast_pic = FileField('Breakfast', validators=[
        FileAllowed(['jpg', 'png'])])
    lunch_pic = FileField('Lunch', validators=[
        FileAllowed(['jpg', 'png'])])
    dinner_pic = FileField('Dinner', validators=[
        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Go')
