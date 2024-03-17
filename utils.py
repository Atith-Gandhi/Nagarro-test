import re
from datetime import datetime

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def text_to_dict(text):
    lines = text.strip().split('\n')
    result = {}
    for line in lines:
        if ': ' not in line:
            continue
        key, value = line.split(': ', 1)
        if value.lower() == 'null':
            value = None
        result[key] = value
    return result

def get_datetime_from_string(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
