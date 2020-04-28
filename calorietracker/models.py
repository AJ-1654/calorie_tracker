from flask import current_app
from calorietracker import db, login_manager
from datetime import datetime, date
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    goal = db.relationship('Goal', backref='person', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.now())
    start_date = db.Column(db.Date, nullable=False, default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    days_list = db.relationship('Day', backref='goal', lazy=True)


class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breakfast = db.Column(db.Integer, nullable=False, default=0)
    breakfast_img_file = db.Column(db.String(20), nullable=False,
                                   default='default.jpeg')
    lunch = db.Column(db.Integer, nullable=False, default=0)
    lunch_img_file = db.Column(db.String(20), nullable=False,
                               default='default.jpeg')
    dinner = db.Column(db.Integer, nullable=False, default=0)
    dinner_img_file = db.Column(db.String(20), nullable=False,
                                default='default.jpeg')
    day_date = db.Column(db.Date, nullable=False, default=date.today())
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)
