from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ABCDEFGHIJKLMNOPQRST'

    from .views import views
    from .todo import todo

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(todo, url_prefix='/')

    return app