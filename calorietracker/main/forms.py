from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user


class CalculateCalorie(FlaskForm):
    picture = FileField('Add food item to check calorie', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Check')
