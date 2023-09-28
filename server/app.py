from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)


@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    todo_list = []
    for todo in todos:
        todo_list.append({"id": todo.id, "task": todo.task, "done": todo.done})
    return jsonify(todo_list)

@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    task = data.get("task")
    if task:
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({"message": "Todo created successfully"}), 201
    else:
        return jsonify({"error": "Task is required"}), 400

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    task = data.get("task")
    done = data.get("done")
    todo = Todo.query.get(todo_id)
    if todo:
        if task is not None:
            todo.task = task
        if done is not None:
            todo.done = done
        db.session.commit()
        return jsonify({"message": "Todo updated successfully"})
    else:
        return jsonify({"error": "Todo not found"}), 404

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return "", 204  # Return a 204 status code for successful deletion
    else:
        return jsonify({"error": "Todo not found"}), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)