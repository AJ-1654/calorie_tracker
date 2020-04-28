from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from calorietracker import db
from calorietracker.models import Goal, Day
from calorietracker.goals.forms import GoalForm, DayForm
from calorietracker.goals.utils import save_picture
from datetime import date

goals = Blueprint('goals', __name__)


@goals.route("/goal", methods=['GET'])
@login_required
def display_goal():
    goal = Goal.query.filter_by(person=current_user).first()
    if goal:
        date_today = date.today()
        diff = (date_today - goal.start_date).days
        return render_template('goal.html', goal=goal, diff=diff)
    else:
        return render_template('goal.html')


@goals.route("/goal/new", methods=['GET', 'POST'])
@login_required
def add_goal():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal(weight=form.weight.data, days=form.days.data, start_date=form.start_date.data,
                    person=current_user)
        db.session.add(goal)
        db.session.commit()
        flash('Your Goal has been created!', 'success')
        return redirect(url_for('goals.display_goal'))
    return render_template('add_goal.html', title='New Goal', form=form, legend='New Goal')


@goals.route("/goal/<int:goal_id>/update", methods=['GET', 'POST'])
@login_required
def update_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.person != current_user:
        abort(403)
    form = GoalForm()
    if form.validate_on_submit():
        goal.weight = form.weight.data
        goal.days = form.days.data
        goal.start_date = form.start_date.data
        db.session.commit()
        flash('Your Goal has been updated', 'success')
        return redirect(url_for('goals.display_goal'))
    elif request.method == 'GET':
        form.weight.data = goal.weight
        form.days.data = goal.days
        form.start_date.data = goal.start_date
    return render_template('add_goal.html', title='Update Goal', form=form,
                           legend='Update Goal')


@goals.route("/goal/<int:goal_id>/delete", methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.person != current_user:
        abort(403)
    db.session.delete(goal)
    db.session.commit()
    flash('Your Goal has been deleted', 'success')
    return redirect(url_for('goals.display_goal'))


@goals.route("/goal/<int:goal_id>/day/", methods=['GET', 'POST'])
@login_required
def day(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.person != current_user:
        abort(403)
    date_today = date.today()
    diff = (date_today - goal.start_date).days
    day = Day.query.filter_by(day_date=date.today()).first()
    if day == None:
        day = Day(goal=goal)
        db.session.add(day)
        db.session.commit()

    form = DayForm()
    if form.validate_on_submit():
        if form.breakfast_pic.data:
            pf = save_picture(form.breakfast_pic.data)
            day.breakfast_img_file = pf
            # predict calories in breakfast, pf is the picture
            # cal = predict(pf)
            #day.breakfast = cal

        if form.lunch_pic.data:
            pf = save_picture(form.lunch_pic.data)
            day.lunch_img_file = pf
            # predict calories in lunch, pf is the picture
            # cal = predict(pf)
            #day.lunch = cal

        if form.dinner_pic.data:
            pf = save_picture(form.dinner_pic.data)
            day.dinner_img_file = pf
            # predict calories in dinner, pf is the picture
            # cal = predict(pf)
            #day.dinner = cal

        db.session.commit()
        flash('Meal for the day updated successfully', 'success')
        return redirect(url_for('goals.day', goal_id=goal.id))

    b_img = url_for('static', filename='food_pics/' +
                    day.breakfast_img_file)
    l_img = url_for('static', filename='food_pics/' +
                    day.lunch_img_file)
    d_img = url_for('static', filename='food_pics/' +
                    day.dinner_img_file)
    return render_template('day.html', goal=goal, diff=diff, day=day, b_img=b_img, l_img=l_img, d_img=d_img, form=form)


@goals.route("/goal/<int:goal_id>/days/view", methods=['GET'])
@login_required
def display_days(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.person != current_user:
        abort(403)
    days = Day.query.filter_by(goal=goal)

    return render_template('all_days.html', days=days, goal=goal)
