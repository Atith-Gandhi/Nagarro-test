# test_task.py
import unittest
from unittest.mock import patch
from src.api.task import add_task, edit_task, delete_task
from src.models import Task, User

class TestTaskFunctions(unittest.TestCase):

    @patch('src.api.task.db')
    def test_add_task_when_already_exists(self, mock_db):
        mock_user = User(id=1, access_token="test_token")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user

        mock_task = Task(id=1, name="Test Task", due_date="2024-03-16 12:00:00", priority="high", user_id=1)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_task

        response = add_task("Test Task", "2024-03-16 12:00:00", 1, "test_token")
        print(response)
        self.assertEqual(response[1], 409)
        self.assertEqual(response[0]['message'], 'Task with Test Task already exists')
    
    @patch('src.api.task.db')
    def test_add_task_when_new_task(self, mock_db):
        mock_user = User(id=1, access_token="test_token")
        mock_db.query(User).return_value.filter.return_value.first.return_value = mock_user

        mock_task = None
        mock_db.query(Task).return_value.filter.return_value.first.return_value = mock_task

        response = add_task("New Task", "2024-03-16 12:00:00", 1, "test_token")

        print(response)
        self.assertEqual(response[0]['message'], 'Task with New Task already exists')

    @patch('src.api.task.db')
    def test_edit_task(self, mock_db):
        mock_user = User(id=1, access_token="test_token")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        mock_task = Task(id=1, name="Test Task", due_date="2024-03-16 12:00:00", priority="high", user_id=1)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_task

        response = edit_task("Test Task", "2024-03-17 12:00:00", "medium", "test_token")
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0]['message'], 'Task with Test Task updated successfully with new due date 2024-03-17 12:00:00 and new priority medium')

    @patch('src.api.task.db')
    def test_delete_task(self, mock_db):
        mock_user = User(id=1, access_token="test_token")
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        mock_task = Task(id=1, name="Test Task", due_date="2024-03-16 12:00:00", priority="high", user_id=1)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_task

        response = delete_task("Test Task", "test_token")
        self.assertEqual(response[1], 204)
        self.assertEqual(response[0]['message'], 'Task with name: Test Task deleted successfully')

if __name__ == '__main__':
    unittest.main()
