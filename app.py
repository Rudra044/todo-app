from flask import Flask, render_template, request, redirect, url_for, abort, flash 
from model.models import db, Todo, StatusEnum
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        todo_name = request.form["todo_name"]
        description = request.form.get("description", "")
        if not todo_name:  
            flash("Please enter a task name.", "error")
            return redirect(url_for("home"))
        new_todo = Todo(name=todo_name , description=description)
        if new_todo.checked == StatusEnum.COMPLETED:
            flash('Task "{}" completed successfully.'.format(new_todo.name), 'success')
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("home"))
    todos = Todo.query.all()
    return render_template("index.html", items=todos)

@app.route("/checked/<int:todo_id>", methods=["POST"])
def checked_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.checked = StatusEnum.COMPLETED if todo.checked == StatusEnum.PENDING else StatusEnum.PENDING
    db.session.commit()
    flash('Task "{}" marked as completed.'.format(todo.name), 'success')
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('Task "{}" deleted successfully.'.format(todo.name), 'success')
    return redirect(url_for("home"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

with app.app_context():
    db.create_all()

if __name__== "__main__":
    app.run(debug=True)