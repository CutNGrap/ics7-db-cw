from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from sqlalchemy.types import Float
from sqlalchemy import PrimaryKeyConstraint, Identity

BASE = declarative_base()


class Group(BASE):
    __tablename__ = 'grouptab'
    
    id = Column(Integer, Identity(always=True), primary_key=True)
    group_num = Column(Integer)
    faculty = Column(Text)
    qualification = Column(Text)
    creation = Column(Integer)


class Student(BASE):
    __tablename__ = 'student'
    
    id = Column(Integer, Identity(always=True), primary_key=True)
    fio = Column(Text)
    group_id = Column(Integer)
    book_num = Column(Integer)
    birth = Column(Date)
    enrollment = Column(Integer)


class Theme(BASE):
    __tablename__ = 'theme'
    
    id = Column(Integer, Identity(always=True), primary_key=True)
    name = Column(Text)
    complexity = Column(Integer)
    first_time = Column(Integer)



class Source(BASE):
    __tablename__ = 'source'
    
    id = Column(Integer, Identity(always=True), primary_key=True)
    name = Column(Text)
    type = Column(Text)
    authors = Column(Text)
    creation = Column(Integer)


class Project(BASE):
    __tablename__ = 'project'
    
    id = Column(Integer, Identity(always=True), primary_key=True)
    theme_id = Column(Integer, ForeignKey('theme.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    mark = Column(Integer)
    passed = Column(Date)

class SourceProject(BASE):
    __tablename__ = 'source_project'
    
    id = Column(Integer, Identity(always=True), primary_key=True)
    source_id = Column(Integer, ForeignKey('source.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)
