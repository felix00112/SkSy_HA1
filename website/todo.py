from flask import Blueprint, render_template, request
from flask_login import current_user, login_user, logout_user, login_required

todo = Blueprint('todo', __name__)

@todo.route('/new-todo', methods=['GET', 'POST'])
@login_required
def new_todo():
    return render_template('new-todo.html', user=current_user)

@todo.route('/edit-todo', methods=['GET', 'POST'])
@login_required
def edit_todo():
    return render_template('edit-todo.html', login_user())
