from sqlalchemy import create_engine, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from utils.models import *
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
import time

class Exc(Exception):
    def __init__(self, msg):
        self.msg = msg

def create_session():
    engine = create_engine(
        f'postgresql://postgres:postgres@localhost:5432/course_work',
        pool_pre_ping=True)
    try:
        engine.connect()
        # print("БД успешно подключена!")
    except:
        print("Ошибка соединения c БД!")
        return
    Session = sessionmaker(bind=engine)
    db = Session()
    return db

def get_db():
    db = create_session()
    try:
        yield db
    finally:
        db.close()


# Get all
def get_all_groups(db, limit: int = 10, skip: int = 0):
    ofs = skip * limit
    groups = db.query(Group.id, Group.group_num, Group.faculty, Group.qualification,Group.creation).limit(limit).offset(ofs).all()
    return groups


def get_all_themes(db, limit: int = 10, skip: int = 0):
    ofs = skip * limit
    themes = db.query(Theme.id, Theme.name, Theme.complexity, Theme.first_time).limit(limit).offset(ofs).all()
    return themes

def get_all_sources(db, limit: int = 10, skip: int = 0):
    ofs = skip * limit
    sources = db.query(Source.id, Source.id, Source.type, Source.authors, Source.creation).limit(limit).offset(ofs).all()
    return sources

def get_all_students(db, limit: int = 10, skip: int = 0):
    ofs = skip * limit
    students = db.query(Student.id, Student.fio, Student.group_id, Student.book_num, Student.birth, Student.enrollment).limit(limit).offset(ofs).all()
    return students

def get_all_projects(db, limit: int = 10, skip: int = 0):
    ofs = skip * limit
    projects = db.query(Project.id, Project.theme_id, Project.author_id, Project.mark, Project.passed).limit(limit).offset(ofs).all()
    return projects


def get_all_source_projects(db, limit: int = 10, skip: int = 0):
    ofs = skip * limit
    projects = db.query(SourceProject.id, SourceProject.source_id, SourceProject.project_id).limit(limit).offset(ofs).all()
    return projects


# # Get one

def get_group(db, Id:int):
    group = db.query(Group.id, Group.group_num, Group.faculty, Group.qualification,Group.creation).filter(Group.id == Id).first()
    if not group:
        raise Exc(f'No group with given id={Id} found')
    return group

def get_theme(db, Id:int):
    theme = db.query(Theme.id, Theme.name, Theme.complexity, Theme.first_time).filter(Theme.id == Id).first()
    if not theme:
        raise Exc(f'No theme with given id={Id} found')
    return theme

def get_source(db, Id:int):
    source = db.query(Source.id, Source.name, Source.type, Source.authors, Source.creation).filter(Source.id == Id).first()
    if not source:
        raise Exc(f'No source with given id={Id} found')
    return source

def get_student(db, Id:int):
    student = db.query(Student.id, Student.fio, Student.group_id, Student.book_num, Student.birth, Student.enrollment).filter(Student.id == Id).first()
    if not student:
        raise Exc(f'No student with given id={Id} found')
    return student

def get_project(db, Id:int):
    project = db.query(Project.id, Project.theme_id, Project.author_id, Project.mark, Project.passed).filter(Project.id == Id).first()
    if not project:
        raise Exc(f'No project with given id={Id} found')
    return project

def get_source_project(db, Id:int):
    project = db.query(SourceProject.id, SourceProject.source_id, SourceProject.project_id).filter(SourceProject.id == Id).first()
    if not project:
        raise Exc(f'No relation with given id={Id} found')
    return project



# # Create

def create_group(db, dictionary):
    new_group = Group(**dictionary)
    try:
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
    except IntegrityError:
        raise Exc("Группа с такими значениями полей уже существует!")
    return [new_group.id, new_group.group_num, new_group.faculty, new_group.qualification, new_group.creation]

def create_student(db, dictionary):
    new_student = Student(**dictionary)
    gr = dictionary['group_id']
    group_query = db.query(Group).filter(Group.id == gr)
    db_group = group_query.first()
    if not db_group:
        raise Exc(f'No group with id={gr} found')
    try:
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
    except IntegrityError as e:
        raise Exc("Студент с такими значениями полей года поступления и номера зачетки уже существует!")
    return [new_student.id, new_student.fio, new_student.group_id, new_student.book_num, new_student.birth, new_student.enrollment]

def create_theme(db, dictionary):
    com = dictionary['complexity']
    if not (com == None or 0 < com < 11):
        raise Exc(f'Theme complexity must be an integer in [1, 10], not {com}')
    try:
        new_theme = Theme(**dictionary)
        db.add(new_theme)
        db.commit()
        db.refresh(new_theme)
    except IntegrityError:
         raise Exc("Тема с таким названием  уже существует!")
    return [new_theme.id, new_theme.name, new_theme.complexity, new_theme.first_time]

def create_source(db, dictionary):
    new_source = Source(**dictionary)
    try:
        db.add(new_source)
        db.commit()
        db.refresh(new_source)
    except IntegrityError as e:
        raise Exc("Такой источник уже существует!")
    return [new_source.id, new_source.name, new_source.type, new_source.authors, new_source.creation]

def create_project(db, dictionary):
    m = dictionary["mark"]
    if not (m == None or 1 < m < 6):
        raise Exc(f'Project mark must be an integer in [2, 5], not {payload.mark}')
    auth = dictionary['author_id']
    student_query = db.query(Student).filter(Student.id == auth)
    db_student = student_query.first()
    if not db_student:
        raise Exc(f'No student(author) with id={auth} found')
    theme = dictionary['theme_id']
    theme_query = db.query(Theme).filter(Theme.id == theme)
    db_theme = theme_query.first()
    if not db_theme:
        raise Exc(f'No theme with id={theme} found')

    new_project = Project(**dictionary)
    try:
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
    except IntegrityError as e:
        raise Exc("Такой курсовой проект уже существует!")
    return [new_project.id, new_project.theme_id, new_project.author_id, new_project.mark, new_project.passed]

def create_source_project(db, dictionary):
    proj = dictionary['project_id']
    student_query = db.query(Project).filter(Project.id == proj)
    db_student = student_query.first()
    if not db_student:
        raise Exc(f'No project with id={auth} found')
    theme = dictionary['source_id']
    theme_query = db.query(Source).filter(Source.id == theme)
    db_theme = theme_query.first()
    if not db_theme:
        raise Exc(f'No source with id={theme} found')

    new_source_project = SourceProject(**dictionary)
    try:
        db.add(new_source_project)
        db.commit()
        db.refresh(new_source_project)
        return [new_source_project.id, new_source_project.source_id, new_source_project.project_id]
    except Exception as e:
        raise e

# # Update

def update_group(db, groupId: int, dictionary):
    group_query = db.query(Group).filter(Group.id == groupId)
    db_group = group_query.first()
    if not db_group:
        raise Exc(f'No group with given id={groupId} found')
    
    try:
        group_query.filter(Group.id == groupId).update(dictionary, synchronize_session=False)
    except IntegrityError:
        raise Exc("Группа с такими значениями полей уже существует!")
    db.commit()
    db.refresh(db_group)
    return [db_group.id, db_group.group_num, db_group.faculty, db_group.qualification, db_group.creation]

def update_student(db, studentId: int, dictionary):
    gr = dictionary['group_id']
    group_query = db.query(Group).filter(Group.id == gr)
    db_group = group_query.first()
    if not db_group:
        raise Exc(f'No group with id={gr} found')

    student_query = db.query(Student).filter(Student.id == studentId)
    db_student = student_query.first()
    if not db_student:
        raise Exc(f'No student with id={studentId} found')
    update_data = dictionary
    try:
        student_query.filter(Student.id == studentId).update(update_data, synchronize_session=False)
    except:
        raise Exc("Студент с такими значениями полей года поступления и номера зачетки уже существует!")
    db.commit()
    db.refresh(db_student)
    return [db_student.id, db_student.fio, db_student.group_id, db_student.book_num, db_student.birth, db_student.enrollment]

def update_theme(db, themeId: int, dictionary):
    com = dictionary['complexity']
    if not (com == None or 0 < com < 11):
        raise Exc(f'Theme complexity must be an integer in [1, 10], not {com}')
    theme_query = db.query(Theme).filter(Theme.id == themeId)
    db_theme = theme_query.first()
    if not db_theme:
        raise Exc(f'No theme with id={themeId} found')
    update_data = dictionary
    try:
        theme_query.filter(Theme.id == themeId).update(update_data, synchronize_session=False)
    except IntegrityError:
        raise Exc("Тема с таким названием  уже существует!")
    db.commit()
    db.refresh(db_theme)
    return [db_theme.id, db_theme.name, db_theme.complexity, db_theme.first_time]

    
def update_source(db, sourceId: int, dictionary):
    source_query = db.query(Source).filter(Source.id == sourceId)
    db_source = source_query.first()
    if not db_source:
        raise Exc(f'No source with id={sourceId} found')
    update_data = dictionary
    try:
        source_query.filter(Source.id == sourceId).update(update_data, synchronize_session=False)
    except IntegrityError:
        raise Exc("Такой источник уже существует!")
    db.commit()
    db.refresh(db_source)
    return [db_source.id, db_source.name, db_source.type, db_source.authors, db_source.creation]

def update_project(db, projectId: int, dictionary):
    m = dictionary["mark"]
    if not (m == None or 1 < m < 6):
        raise Exc(f'Project mark must be an integer in [2, 5], not {payload.mark}')
    auth = dictionary['author_id']
    student_query = db.query(Student).filter(Student.id == auth)
    db_student = student_query.first()
    if not db_student:
        raise Exc(f'No student(author) with id={auth} found')
    theme = dictionary['theme_id']
    theme_query = db.query(Theme).filter(Theme.id == theme)
    db_theme = theme_query.first()
    if not db_theme:
        raise Exc(f'No theme with id={theme} found')
    
    project_query = db.query(Project).filter(Project.id == projectId)
    db_project = project_query.first()
    if not db_project:
        raise Exc(f'No project with id={projectId} found')
    update_data = dictionary
    try:
        project_query.filter(Project.id == projectId).update(update_data, synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise Exc(f'Такой проект уже существует!')
    project_query = db.query(Project).filter(Project.id == projectId)
    db_project = project_query.first()
    return [db_project.id, db_project.theme_id, db_project.author_id, db_project.mark, db_project.passed]

def update_source_project(db, source_projectId: int, dictionary):
    proj = dictionary['project_id']
    student_query = db.query(Project).filter(Project.id == proj)
    db_student = student_query.first()
    if not db_student:
        raise Exc(f'No project with id={proj} found')
    theme = dictionary['source_id']
    theme_query = db.query(Source).filter(Source.id == theme)
    db_theme = theme_query.first()
    if not db_theme:
        raise Exc(f'No source with id={theme} found')

    source_project_query = db.query(SourceProject).filter(SourceProject.id == source_projectId)
    db_source_project = source_project_query.first()
    if not db_source_project:
        raise Exc(f'No project with id={projectId} found')
    update_data = dictionary
    try:
        source_project_query.filter(SourceProject.id == source_projectId).update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(db_source_project)
    except IntegrityError:
        raise Exc(f'Такая связь уже существует!')
    return [db_source_project.id, db_source_project.source_id, db_source_project.project_id]


# # Delete

def delete_group(db, groupId: int):
    group_query = db.query(Group).filter(Group.id == groupId)
    db_group = group_query.first()
    if not db_group:
        raise Exc(f'No group with id={groupId} found')
    
    try:
        group_query.filter(Group.id == groupId).delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise Exc(f'There are students registered in given group (id={groupId}) in database')
    return {"status": "success"}


def delete_student(db, studentId: int):

    student_query = db.query(Student).filter(Student.id == studentId)
    db_student = student_query.first()
    if not db_student:
        raise Exc(f'No student with id={studentId} found')
    
    try:
        student_query.filter(Student.id == studentId).delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise Exc(f'There are projects created by given student (id={studentId}) in database')
    return {"status": "success"}

def delete_theme(db, themeId: int):
    theme_query = db.query(Theme).filter(Theme.id == themeId)
    db_theme = theme_query.first()
    if not db_theme:
        raise Exc(f'No theme with id={themeId} found')
    try:
        theme_query.filter(Group.id == themeId).delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise Exc(f'There are projects on given theme (id={themeId}) in database')
    return {"status": "success"}


def delete_source(db, sourceId: int):
    source_query = db.query(Source).filter(Source.id == sourceId)
    db_source = source_query.first()
    if not db_source:
        raise Exc(f'No source with id={sourceId} found')
    try:
        source_query.filter(Source.id == sourceId).delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise Exc(f'There are projects utilizing given source (id={sourceId}) in database')
    return {"status": "success"}

def delete_project(db, projectId: int):
    project_query = db.query(Project).filter(Project.id == projectId)
    db_project = project_query.first()
    if not db_project:
        raise Exc(f'No project with id={projectId} found')
    try:
        source_project_query = db.query(SourceProject).filter(SourceProject.project_id == projectId)
        source_project_query.delete(synchronize_session=False)
        project_query.filter(Project.id == projectId).delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise Exc(f'Unpredicted Error')
    return {"status": "success"}


def delete_source_project(db, source_projectId: int):
    source_project_query = db.query(SourceProject).filter(SourceProject.id == source_projectId)
    db_source_project = source_project_query.first()
    if not db_source_project:
        raise Exc(f'No source_project with id={source_projectId} found')
    try:
        source_project_query = db.query(SourceProject).filter(SourceProject.id == source_projectId)
        source_project_query.delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise Exc(f'Unknown Error')
    return {"status": "success"}


def get_more_avg(db, limit: int = 10, skip: int = 0):
    ofs = skip * limit
    groups = db.query(func.public.more_than_avg_sources()).limit(limit).offset(ofs).all()
    return groups

def get_time1(n):
    st = 0

    for i in range(n):
        db = create_session()
        # db.execute("SET enable_seqscan TO on;")
        start = time.time()
        db.query(func.public.test1()).all()
        end = time.time()
        db.close()
        st += (end - start)  * 1000
        
    print(1, st/n)

def get_time2( n):
    st = 0

    for i in range(n):
        db = create_session()
        # db.execute("SET enable_seqscan TO on;")
        start = time.time()
        s = db.query(func.public.test2()).all()
        end = time.time()
        db.close()
        st += (end - start)  * 1000

    print(2, st/n)
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5000)


