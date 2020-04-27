from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from calorietracker import db
from calorietracker.models import Goal
from calorietracker.goals.forms import GoalForm
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
