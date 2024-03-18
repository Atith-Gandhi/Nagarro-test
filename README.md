# Nagarro-test

## To run the app using docker, run the below commands in the root directory
* docker build -t nagarro .
* docker run -p 5000:5000 -d nagarro
* The app would be running at http://localhost:5000/login or http://127.0.0.1:5000

## To run the app in local environment, run the below commands in the root directory
* python python .\run.py
* The app would be running at [http://localhost:5000/](http://localhost:5000/) or [http://127.0.0.1:5000](http://127.0.0.1:5000)


### Running the app

## Test the Rest APIs using swagger:
* Access the swagger docs at [http://localhost:5000/swagger/](http://localhost:5000/swagger/)
* Before accessing any APIs, first get the access token through the login API. If you haven't registered before, first register and then login to get the access token.
* The access token would be required for all the task APIs.
* There are three task APIs (POST, PUT, and DELETE) for adding, updating, and deleting tasks for each user respectively.
* Additions, there is listtasks, which will list all the task names for a user

## User Interface
* In the User Interface, ask the app clearly whether you want to **create** a new task, **edit** an existing task,  **delete** a task, **list** all tasks for the user.
* Create task instructions should have details about the task name, due date (Time(Hour), Day, Month, Year), and priority of the task (1-5)
* Edit task instructions should have clear details about the task name, and what you want to change - due date (Time(Hour), Day, Month, Year) and/or priority of the task (1-5)
* Delete task instructions should have clear details about the task name that you want to delete
* List task instructions should just mention that you want to list all the tasks.

## CI pipeline
* I am using github to build a demo pipeline. (build, test)
* The details about the pipeline are there in .github/workflows/ci.yml file/
* Additionally, you can also find the pipeline details on the GitHub page https://github.com/Atith-Gandhi/Nagarro-test/.

The UI of the app is self-explanatory and easy to login and register new acccount.