from flask import Blueprint
from flask import render_template, request, Blueprint
# from calorietracker.models import Post
from calorietracker.main.forms import (CalculateCalorie)
from calorietracker.main.utils import save_picture

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home",methods=['GET', 'POST'])
def home():
    form  = CalculateCalorie()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            # predict picture using model


    page = request.args.get('page', 1, type=int)
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')

