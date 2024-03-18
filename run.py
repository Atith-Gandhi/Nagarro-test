# run.py
from flask import Flask
from flask_restx import Api
from flask_restx import Namespace, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import Flask, render_template, request, redirect, session
import json

# import openai

# from flask_restful import swagger
from src.api.task import taskCtrl, listTaskCtrl, add_task, edit_task, delete_task, list_tasks
from src.api.user import registerCtrl, loginCtrl
from src.api.user import UserRegistration, UserLogin, login_user, register_user
from src.chatbot.prompt import parse_prompt
from src.auth import jwt
from src.models import db

from utils import is_valid_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = 'your_secret_key'
# db.init_app(app)
jwt.init_app(app)
conversation = []

@app.route("/apidocs")
def apidocs():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Task Manager API"
    return jsonify(swag)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Inside Login")
    if 'swagger' in request.headers.get('User-Agent', '').lower() or \
           'swagger' in request.headers.get('Referer', '').lower():
        # print(request.data.json())
        payload_body = request.data
        json_data = json.loads(payload_body.decode('utf-8'))
        return login_user(json_data['email'], json_data['password'])
    elif request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        
        response = login_user(session['username'], session['password'])
        if response[1] == 200:
            session['access_token'] = response[0]['access_token']
            return redirect('/chatbot')
        else:
            error_message = response[0]['message']
            return render_template('login.html', error=error_message) 
        
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Inside Register")
    if 'swagger' in request.headers.get('User-Agent', '').lower() or \
           'swagger' in request.headers.get('Referer', '').lower():
        payload_body = request.data
        json_data = json.loads(payload_body.decode('utf-8'))
        register_user_response = register_user(email=session['username'], first_name=session['first_name'], 
                                                last_name=session['last_name'], password=session['password'])
        print(register_user_response[0]['message'])
        if register_user_response[1] == 409:
            return register_user_response[0]['message']
        else:
            return register_user_response[0]['access_token']
        # return register_user(json_data['email'], json_data['first_name'], json_data['last_name'], json_data['password'])[0]['access_token']
    elif request.method == 'POST':
        # session['username'] = request.form['username']
        # session['password'] = request.form['password']
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']

        if not is_valid_email(session['username']):
            error_message = "Username is not valid. Username must be a valid email address."
            return render_template('register.html', error=error_message)

        register_user_response = register_user(email=session['username'], first_name=session['first_name'], 
                                                last_name=session['last_name'], password=session['password'])
        if register_user_response[1] == 409:
            error_message = register_user_response[0]['message']
            return render_template('register.html', error=error_message)
        
        session['access_token'] = register_user_response[0]['access_token']
        
        
        return redirect('/chatbot')
    
    return render_template('register.html')


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        if 'swagger' in request.headers.get('User-Agent', '').lower() or \
           'swagger' in request.headers.get('Referer', '').lower():
        # print(request.data.json())
            payload_body = request.data
            user_input = json.loads(payload_body.decode('utf-8'))
            # return login_user(json_data['email'], json_data['password'])
        else:
            user_input = request.form['user_input']
            conversation.append(user_input)
            user_input = parse_prompt(user_input)

        try:
            if user_input['task_type'] is None or user_input['task_type'] not in ["Create", "Edit", "Delete", "List"] :
                response = "Sorry I was not able to understand task type(Create, Edit, List, or Delete). Please try writing a new prompt which clearly talks about the task type!"
                print(response)
                conversation.append(response)
                return render_template('chatbot.html', username=session['username'], response=response, conversation=conversation)
            
            if user_input['task_name'] is None:
                response = "Sorry I was not able to understand the task name. Please try writing a new prompt which clearly talks about the task name!"
                print(response)
                conversation.append(response)
                return render_template('chatbot.html', username=session['username'], response=response, conversation=conversation)
            else:
                if user_input['task_name'][len(user_input['task_name'])-1] == ' ':
                    user_input['task_name'] = user_input['task_name'][:-1]
                    
            if user_input['task_type'] == "Create":
                if user_input['timestamp'] is None:
                    response = "Sorry I was not able to understand the due date. Please try writing a new prompt which clearly tells what is the due date of the task! The prompt should mention the Year, day and hour of the due date!"
                    print(response)
                    conversation.append(response)
                    return render_template('chatbot.html', username=session['username'], response=response, conversation=conversation)
                
                if user_input['priority'] is None:
                    response = "Sorry I was not able to understand the priority. Priority of the task should be between 1-5.  Please try writing a new prompt which clearly tells what is the priority(1-5) of the task!"
                    print(response)
                    conversation.append(response)
                    return render_template('chatbot.html', username=session['username'], response=response, conversation=conversation)
                
                response = add_task(user_input['task_name'], user_input['timestamp'], user_input['priority'], session['access_token'])
        
            
            if user_input['task_type'] == "Edit":
                if 'priority' not in user_input:
                    user_input['priority'] = None
                if 'timestamp' not in user_input:
                    user_input['timestamp'] = None

                response = edit_task(user_input['task_name'], user_input['timestamp'], user_input['priority'], session['access_token'])
                if response[1] == 404:
                    conversation.append(response[0]['message'])
                    print(response[0]['message'])
                    return render_template('chatbot.html', username=session['username'], response=response[0]['message'], conversation=conversation)
            
            if user_input['task_type'] == "Delete":
                print("Line 165")
                response = delete_task(user_input['task_name'], session['access_token'])
                print(response)
                conversation.append(response[0]['message'])
                return render_template('chatbot.html', username=session['username'], response=response[0]['message'], conversation=conversation)

            if user_input['task_type'] == "List":
                response = list_tasks(session['access_token'])
                print(response)
                conversation.append(response[0]['message'])
                return render_template('chatbot.html', username=session['username'], response=response[0]['message'], conversation=conversation)
            
            conversation.append(response[0]['message'])
            print(response[0]['message'])
            return render_template('chatbot.html', username=session['username'], response=response[0]['message'], conversation=conversation)

        except:
            response = "Sorry I was not able to understand the prompt. Please try writing a new prompt!"
            print(response)
            conversation.append(response)
            return render_template('chatbot.html', username=session['username'], response=response, conversation=conversation)
    
    return render_template('chatbot.html', username=session['username'])


# def generate_response(user_input):
   
#     return "Good Question"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


api = Api(app,
        title='CRUD APP with JWT',
        version='1.0',
        description='A simple CRUD application with JWT',
        doc = "/swagger/",
        validate=True
        )

api.add_namespace(taskCtrl)
api.add_namespace(registerCtrl)
api.add_namespace(loginCtrl)
api.add_namespace(listTaskCtrl)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
