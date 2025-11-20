# lib/models.py
from datetime import datetime
from sqlalchemy import create_engine # type: ignore
from sqlalchemy import (CheckConstraint, UniqueConstraint, # type: ignore
    Column, DateTime, Integer, String, ForeignKey)
from sqlalchemy.orm import relationship # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore

engine = create_engine('sqlite:///migrations_test.db')
Base = declarative_base()

class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), index=True)
    subject = Column(String())

    students = relationship("Student", back_populates="teacher")

    def __repr__(self):
        return

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        UniqueConstraint('email',
            name='unique_email'),
        CheckConstraint('grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12')
    )

    id = Column(Integer(), primary_key=True)
    name = Column(String(), index=True)
    email = Column(String(55))
    grade = Column(Integer())
    nickname = Column(String(), nullable=False, default='No Nickname')
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    teacher_id = Column(Integer(), ForeignKey('teachers.id')) 
    teacher = relationship("Teacher", back_populates="students") 

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"