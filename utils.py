from model.models import db, Todo, StatusEnum
from flask import flash


def add_todo(todo_name, description):
    if not todo_name:
        flash("Please enter a task name.", "error")
        return

    new_todo = Todo(name=todo_name, description=description)
    db.session.add(new_todo)
    db.session.commit()

    if new_todo.checked == StatusEnum.COMPLETED:
        flash('Task "{}" completed successfully.'.format(new_todo.name), 'success')


def toggle_todo_status(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.checked = StatusEnum.PENDING if todo.checked == StatusEnum.COMPLETED else StatusEnum.COMPLETED
    db.session.commit()
    flash('Task "{}" status updated.'.format(todo.name), 'success')


def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('Task "{}" deleted successfully.'.format(todo.name), 'success')

    
def get_all_todos():
    return Todo.query.all()
