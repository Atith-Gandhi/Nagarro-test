import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

def generate_task_email(user_email, tasks):
    # Get current time
    current_time = datetime.now()

    # Constructing the email body
    email_body = "Tasks due within the next 24 hours:\n\n"
    for task in tasks:
        due_date = datetime.strptime(task['due_date'], "%Y-%m-%d %H:%M:%S")
        if due_date <= current_time + timedelta(days=1):
            email_body += f"Task Name: {task['name']}\n"
            email_body += f"Due Date: {task['due_date']}\n"
            email_body += f"Priority: {task['priority']}\n\n"

    # Email content setup
    msg = MIMEMultipart()
    msg['From'] = 'chenghao043@gmail.com'   # Replace with your email
    msg['To'] = user_email
    msg['Subject'] = 'Task List'

    # Attach the email body
    msg.attach(MIMEText(email_body, 'plain'))

    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('chenghao043@gmail.com', 'Atith@13')  # Replace with your email and password
        server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    print('Email sent successfully')

# Example tasks
# tasks = [
#     {'task name': 'Complete project proposal', 'due date': '2024-03-18 15:00:00', 'priority': 'High'},
#     {'task name': 'Review documentation', 'due date': '2024-03-18 18:00:00', 'priority': 'Medium'},
#     {'task name': 'Prepare presentation', 'due date': '2024-03-19 10:00:00', 'priority': 'Low'}
# ]

# Generate and send email
# generate_task_email(tasks)
