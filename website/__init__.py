import logging

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
import logging

logging.basicConfig(level=logging.INFO)
basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ABCDEFGHIJKLMNOPQRST'
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, DB_NAME)
    db.init_app(app)

    from .views import views
    from .todo import todo
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(todo, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Todo

    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    db_path = os.path.join('website', DB_NAME)
    full_path = os.path.join(app.instance_path, db_path)
    if not os.path.exists(full_path):
        with app.app_context():
            db.create_all()
            print('Database created successfully')
    else:
        print('Database already exists')