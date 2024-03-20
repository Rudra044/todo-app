from flask import Flask, render_template, request, redirect, url_for
from model.models import db
from flask_migrate import Migrate
from utils import add_todo, toggle_todo_status, delete_todo, get_all_todos


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
        add_todo(todo_name, description)
        return redirect(url_for("home"))
    
    todos = get_all_todos()
    return render_template("index.html", items=todos)


@app.route("/checked/<int:todo_id>", methods=["POST", "PUT"])
def checked_todo(todo_id):
    toggle_todo_status(todo_id)
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo_route(todo_id):
    delete_todo(todo_id)
    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
