# app/models.py
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    # def __init__(self, email, first_name, last_name, password, access_token):
    #     self.email = email
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.password = password
    #     self.access_token = access_token
    __tablename__ = 'User'

    id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(120), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    access_token = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}'), password='{self.password}', access_token='{self.access_token}')>"
    

class Task(Base):
    __tablename__ = 'Task'

    id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(120), nullable=False)
    due_date = Column(DateTime, nullable=False)
    priority = Column(Integer, nullable=False)
    user_id = Column(String(255), ForeignKey('User.id'), nullable=False)
    # user = relationship('User', back_populates="tasks")

    def __repr__(self):
        return f"<Task(id='{self.id}', name='{self.name}', due_date='{self.due_date}', priority='{self.priority}', user_id='{self.user_id}')>"


engine = create_engine("sqlite:///temp.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db = Session()
Base = declarative_base()