from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
    progress = db.Column(db.Integer)
    deadline = db.Column(db.DateTime)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    todos = db.relationship('Todo', backref='user', lazy='dynamic')