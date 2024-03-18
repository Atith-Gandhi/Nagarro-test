# app/resources/user.py
from flask_restx import Resource, reqparse, Namespace, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from src.models import User, Task, db
from src.email.send_mail import generate_task_email

registerCtrl = Namespace('register', path = '/register', description='Register related operations')
registerCommand = registerCtrl.model("registerTask", {
    "email": fields.String(description="User email", required=True),
    "first_name": fields.String(description="User first name", required=True),
    "last_name": fields.String(description="User last name", required=True),
    "password": fields.String(description="User password", required=True)
})
@registerCtrl.route('/')
class UserRegistration(Resource):
    @registerCtrl.expect(registerCommand)
    def post(self):
        args = registerCtrl.payload
        return register_user(args['email'], args['first_name'], args['last_name'], args['password'])

def register_user(email, first_name, last_name, password):
    hashed_password = generate_password_hash(password)
    user = db.query(User).filter(User.email == email).first()
    if user:
        return {'message': 'User already exists. Please Log in!'}, 409
    user = User(email=email, first_name=first_name, last_name=last_name, password=hashed_password, access_token='')
    user.access_token = create_access_token(identity=user.id)
    db.add(user)
    db.commit()
    access_token = user.access_token
    return {'message': 'User created successfully', 'access_token': access_token}, 201

loginCtrl = Namespace('login', path = '/login', description='Login related operations')
loginCommand = loginCtrl.model("loginTask", {
    "email": fields.String(description="User email", required=True),
    "password": fields.String(description="User password", required=True)
})
@loginCtrl.route('')
class UserLogin(Resource):
    @loginCtrl.expect(loginCommand)
    def post(self):
        args = loginCtrl.payload
        return login_user(args['email'], args['password'])
    
def login_user(email, password):
    user = db.query(User).filter(User.email == email).first()
    if not user or not check_password_hash(user.password, password):
        return {'message': 'Invalid email or password. \n If you are not registered, Please create a new user account!'}, 401
    user.access_token = create_access_token(identity=user.id)
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    tasks = [task.__dict__ for task in tasks]
    for task in tasks:
        task['due_date'] = task['due_date'].strftime("%Y-%m-%d %H:%M:%S")

    # generate_task_email(user.email, tasks)
    db.commit()
    access_token = user.access_token
    return {'access_token': access_token}, 200
