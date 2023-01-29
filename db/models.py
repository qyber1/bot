from db.base import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey


class User(BaseModel):

    __tablename__ = 'users'

    id = Column(Integer, unique=True, primary_key=True)
    username = Column(String, unique=False)
    child = relationship('Todo')

class Todo(BaseModel):

    __tablename__ = 'todo'

    id = Column(Integer, unique=True, primary_key=True, autoincrement= True)
    parent_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String, nullable=False)