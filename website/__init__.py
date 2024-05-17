from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
import logging

logging.basicConfig(level=logging.INFO)
basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app(config_name=None):
    app = Flask(__name__)
    if config_name == 'testing':
        app.config.from_object('website.config.TestConfig')
    else:
        app.config.from_object('website.config.Config')

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
    with app.app_context():
        if not os.path.exists(os.path.join(basedir, DB_NAME)):
            db.create_all()
            print('Database created successfully')
        else:
            print('Database already exists')
