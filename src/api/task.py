# app/resources/task.py
from datetime import datetime
from flask_restx import Resource, reqparse, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import Task, db, User
from utils import get_datetime_from_string


taskCtrl = Namespace('tasks', path = '/tasks/', description='Task related operations')
listTaskCtrl = Namespace('listTasks', path = '/listTasks/', description='List Task related operations')

taskPostCommand = taskCtrl.model("taskPost", {
    "name": fields.String(description="Task name", required=True),
    "due_date": fields.String(description="Task due date", required=True, default='2024-03-15 21:00:00'),
    "priority": fields.Integer(description="Task priority", required=True, default=5),
    "access_token": fields.String(description="User access token", required=True)
})

taskPUTCommand = taskCtrl.model("taskPut", {
    "name": fields.String(description="Task name", required=True),
    "due_date": fields.String(description="Task due date", required=True, default='2024-03-15 21:00:00'),
    "priority": fields.Integer(description="Task priority", required=True, default=5),
    "access_token": fields.String(description="User access token", required=True)
})

taskDeleteCommand = taskCtrl.model("taskDelete", {
    "name": fields.String(description="Task name", required=True),
    "access_token": fields.String(description="User access token", required=True)
})

listTaskPostCommand = listTaskCtrl.model("listTaskPost", {
    "access_token": fields.String(description="User access token", required=True)
})

@taskCtrl.route('/')
class TaskResource(Resource):
    @taskCtrl.expect(taskPostCommand)
    def post(self):
        args = taskCtrl.payload
        return add_task(args['name'], args['due_date'], args['priority'], args['access_token'])

    @taskCtrl.expect(taskPUTCommand)
    def put(self):
        args = taskCtrl.payload
        return edit_task(args['name'], args['due_date'], args['priority'], args['access_token'])

    @taskCtrl.expect(taskDeleteCommand)
    def delete(self):
        args = taskCtrl.payload
        return delete_task(args['name'], args['access_token'])
    
    # @listTaskCtrl.expect(listTaskPostCommand)
    # def get(self):
    #     args = taskCtrl.payload
    #     return get_tasks(args['access_token'])

@listTaskCtrl.route('/')
class ListTaskResource(Resource):
    @listTaskCtrl.expect(listTaskPostCommand)
    def post(self):
        args = listTaskCtrl.payload
        return list_tasks(args['access_token'])
    
def add_task(name, due_date, priority, access_token):
    print("Line 47")
    user = db.query(User).filter(User.access_token == access_token).first()
    task = db.query(Task).filter(Task.name == name and Task.user_id == user.id).first()
    # print(task)
    
    if task:
        return {'message': f'Task with name: "name: "{name}"" already exists'}, 409
    
    task = Task(name=name, due_date=get_datetime_from_string(due_date), priority=priority, user_id=user.id)
    db.add(task)
    db.commit()
    return {'message': f'Task with name: "{name}" created successfully'}, 201

def edit_task(name, due_date, priority, access_token):
    user = db.query(User).filter(User.access_token == access_token).first()
    message = f'Task with name: "{name}" updated successfully'
    task = db.query(Task).filter(Task.name == name and Task.user_id == user.id).first()
    if not task:
        return {'message': f'Task name: "{name}" not found'}, 404
    if due_date is not None:
        task.due_date = get_datetime_from_string(due_date)
        message = message + f' with new due date {due_date}'
    if priority is not None:
        task.priority = priority
        message = message + f' and new priority {priority}'

    db.commit()
    return {'message': message}, 200

def delete_task(name, access_token):
    user = db.query(User).filter(User.access_token == access_token).first()
    task = db.query(Task).filter(Task.name == name and Task.user_id == user.id).first()
    print("Line 77")
    if not task:
        return {'message': f'Task with name: "{name}" not found'}, 404
    db.delete(task)
    db.commit()
    return {'message': f'Task with name: "{name}" deleted successfully'}, 204

def list_tasks(access_token):
    user = db.query(User).filter(User.access_token == access_token).first()
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    if not tasks:
        return {'message': 'No tasks found for you'}, 404
    tasks = [task.__dict__ for task in tasks]
    # print(tasks)
    for task in tasks:
        task['due_date'] = task['due_date'].strftime("%Y-%m-%d %H:%M:%S")

    task_names = [t['name'] for t in tasks]
    return {'message': f'Your tasks are : {task_names}'}, 200
    

