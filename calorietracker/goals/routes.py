from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from calorietracker import db
from calorietracker.models import Goal
from calorietracker.goals.forms import GoalForm


goals = Blueprint('goals', __name__)


@goals.route("/goal", methods=['GET'])
@login_required
def display_goal():
    # goal = Goal.query.filter_by(person=current_user).first()
    # if goal:
    #     return render_template('goal.html', goal=goal)
    # else:
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
    return render_template('add_goal.html',title='New Goal',form=form, legend='New Goal')


# @goals.route("/goal/new", methods=['GET', 'POST'])
# @login_required
# def new_goal():
#     form = GoalForm()
#     if form.validate_on_submit():
#         goal = Goal(weight=form.weight.data, days=form.days.data, start_date=form.start_date.data,
#                     person=current_user)
#         db.session.add(goal)
#         db.session.commit()
#         flash('Your Goal has been created!', 'success')
#         return redirect(url_for('main.home'))
#     return render_template('create_goal.html', title='New Post', form=form, legend='New Post')


# @posts.route("/post/<int:post_id>")
# def post(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template('post.html', title=post.title, post=post)


# @posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
# @login_required
# def update_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash('Your post has been updated', 'success')
#         return redirect(url_for('posts.post', post_id=post.id))
#     elif request.method == 'GET':
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template('create_post.html', title='New Post', form=form,
#                            legend='Update Post')


# @posts.route("/post/<int:post_id>/delete", methods=['POST'])
# @login_required
# def delete_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted', 'success')
#     return redirect(url_for('main.home'))
