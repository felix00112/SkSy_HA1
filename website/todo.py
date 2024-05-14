from flask import Blueprint, render_template

todo = Blueprint('todo', __name__)

@todo.route('/new-todo', methods=['GET', 'POST'])
def new_todo():
    return render_template('new-todo.html')

@todo.route('/edit-todo', methods=['GET', 'POST'])
def edit_todo():
    return render_template('edit-todo.html')