import unittest
import json
from app import app, db, Todo

TEST_DB = "test.db"

class TodoApiTests(unittest.TestCase):

    # Set up the test environment
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{TEST_DB}"
        self.app = app.test_client()
        with app.app_context():  # Create an application context
            db.create_all()

    # Tear down the test environment
    def tearDown(self):
        with app.app_context():  # Create an application context
            db.session.remove()
            db.drop_all()

    # Helper method to create a test todo item
    def create_todo(self, todo_text):
        with app.app_context():  # Create an application context
            todo = Todo(task=todo_text)
            db.session.add(todo)
            db.session.commit()
            
    def test_create_todo(self):
        todo_data = {"task": "Test todo item"}
        response = self.app.post("/todos", json=todo_data)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["message"], "Todo created successfully")

    def test_get_all_todos(self):
        self.create_todo("Todo 1")
        self.create_todo("Todo 2")
        response = self.app.get("/todos")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

    def test_update_todo(self):
        self.create_todo("Todo to update")
        todo_data = {"task": "Updated todo item", "done": True}
        response = self.app.put("/todos/1", json=todo_data)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Todo updated successfully")

    def test_delete_todo(self):
        self.create_todo("Todo to delete")
        response = self.app.delete("/todos/1")
        self.assertEqual(response.status_code, 204)

if __name__ == "__main__":
    unittest.main()
