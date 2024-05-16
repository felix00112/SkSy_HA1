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

@todo.route('/edit-todo/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def edit_todo(todo_id):
    # Get the todo item from the database
    todo_item = Todo.query.get_or_404(todo_id)

    # Check if the current user is the owner of the todo item
    if todo_item.user_id != current_user.id:
        flash('You do not have permission to edit this todo', 'error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        # Get data from form
        todo_text = request.form.get('todo-text')
        deadline_str = request.form.get('deadline')
        progress = request.form.get('progress')

        # Check if todos are valid
        if not todo_text or not deadline_str or not progress:
            flash('All fields are required', 'error')
            return redirect(url_for('todo.edit_todo', todo_id=todo_id))

        # Convert datetime so sqlalchemy can work with it
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid deadline', 'error')
            return redirect(url_for('todo.edit_todo', todo_id=todo_id))

        # Update todo item with new data
        todo_item.data = todo_text
        todo_item.deadline = deadline
        todo_item.progress = int(progress)

        # Commit changes to the database
        db.session.commit()
        flash('Todo updated', category='success')
        return redirect(url_for('views.home'))

    return render_template('edit-todo.html', user=current_user, todo=todo_item)


@todo.route('/delete-todo', methods=['GET', 'POST'])
@login_required
def delete_todo():
    # todo: implement method for deleting todos
    pass
