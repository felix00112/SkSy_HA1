from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# creating tables for database

# table for todos
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
    progress = db.Column(db.Integer)
    deadline = db.Column(db.Date)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# table for users
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    todos = db.relationship('Todo', backref='user', lazy='dynamic')