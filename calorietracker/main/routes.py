from flask import render_template, request, Blueprint, redirect, url_for
from calorietracker.main.forms import (CalculateCalorie)
from calorietracker.main.utils import save_picture

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET'])
def home():
    page = request.args.get('page', 1, type=int)
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/check_calorie", methods=['GET', 'POST'])
def check_calorie():
    form = CalculateCalorie()
    p_class = None
    p_img = None
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            # predict picture using ml model
            p_class = 'Pizza'
            p_img = url_for('static', filename='food_pics/' + picture_file)

    return render_template('check_calorie.html', form=form, title='Check Calorie', p_class=p_class, p_img=p_img)
