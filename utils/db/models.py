from db.base import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime


class Departament(BaseModel):
    __tablename__ = "Departament"

    id = Column(Integer, unique=True, primary_key=True)
    title = Column(String(30))
    employers = relationship('User', back_populates="departament")


class User(BaseModel):
    __tablename__ = "User"

    id = Column(Integer, unique=True, primary_key=True)
    username = Column(String(60), unique=False)
    birthday = Column(DateTime)
    job_title = Column(String)
    departament_id = Column(Integer, ForeignKey("Departament.id"))
    departament = relationship("Departament", back_populates="employers")

