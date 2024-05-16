from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

from website import db
from website.models import Todo

# all routes handling todos

todo = Blueprint('todo', __name__)

@todo.route('/new-todo', methods=['GET', 'POST'])
@login_required
def new_todo():
    # getting data from form
    if request.method == 'POST':
        todo_text = request.form.get('todo-text')
        deadline_str = request.form.get('deadline')
        progress = request.form.get('progress')
        # check if todos are valid
        if not todo_text or not deadline_str or not progress:
            flash('all fields are required', 'error')
            return redirect(url_for('todo.new_todo'))
        # convert datetime so sqlalchemy can work with it
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        except ValueError:
            flash('invalid deadline', 'error')
            return redirect(url_for('todo.new_todo'))

        # adding new_todo to database
        new_todo = Todo(data=todo_text, deadline=deadline, progress=int(progress), user_id=current_user.id)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added', category='success')
        return redirect(url_for('views.home'))  # Ensure to return the result of redirect

    return render_template('new-todo.html', user=current_user)

@todo.route('/edit-todo', methods=['GET', 'POST'])
@login_required
def edit_todo():
    # todo: implement method for editing todos
    return render_template('edit-todo.html', user=current_user)

@todo.route('/delete-todo', methods=['GET', 'POST'])
@login_required
def delete_todo():
    # todo: implement method for deleting todos
    pass
