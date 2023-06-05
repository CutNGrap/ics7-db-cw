from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from utils.models import *
from fastapi import FastAPI, Depends, HTTPException, status, Response
from utils.models import *
from utils.chemas import *
import uvicorn
from sqlalchemy.orm import Session
from pydantic import ValidationError

app = FastAPI()

def create_session():
    engine = create_engine(
        f'postgresql://postgres:postgres@localhost:5432/course_work',
        pool_pre_ping=True)
    try:
        engine.connect()
        print("БД успешно подключена!")
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

@app.get("/groups_read")
def get_all_groups(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    ofs = skip * limit
    groups = db.query(Group).limit(limit).offset(ofs).all()
    return {'status': 'success', 'results': len(groups), 'groups': groups}

@app.get("/themes_read")
def get_all_themes(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    ofs = skip * limit
    themes = db.query(Theme).limit(limit).offset(ofs).all()
    return {'status': 'success', 'results': len(themes), 'themes': themes}

@app.get("/sources_read")
def get_all_sources(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    ofs = skip * limit
    sources = db.query(Source).limit(limit).offset(ofs).all()
    return {'status': 'success', 'results': len(sources), 'sources': sources}

@app.get("/students_read")
def get_all_students(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    ofs = skip * limit
    students = db.query(Student).limit(limit).offset(ofs).all()
    return {'status': 'success', 'results': len(students), 'students': students}

@app.get("/projects_read")
def get_all_projects(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    ofs = skip * limit
    projects = db.query(Project).limit(limit).offset(ofs).all()
    return {'status': 'success', 'results': len(projects), 'projects': projects}

@app.get("/projects_read")
def get_all_source_projects(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):
    ofs = skip * limit
    projects = db.query(SourceProject).limit(limit).offset(ofs).all()
    return {'status': 'success', 'results': len(projects), 'source_project': projects}


# Get one

@app.get("/group_read")
def get_group(id:int,db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No group with given id={id} found')
    return {'status': 'success', 'group': group}

@app.get("/theme_read")
def get_theme(id:int,db: Session = Depends(get_db)):
    theme = db.query(Theme).filter(Theme.id == id).first()
    if not theme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No theme with given id={id} found')
    return {'status': 'success', 'theme': theme}

@app.get("/source_read")
def get_source(id:int,db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == id).first()
    if not source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No source with given id={id} found')
    return {'status': 'success', 'source': source}

@app.get("/student_read")
def get_student(id:int,db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No student with given id={id} found')
    return {'status': 'success', 'student': student}

@app.get("/project_read")
def get_project(id:int,db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No project with given id={id} found')
    return {'status': 'success', 'project': project}


# Create

@app.post("/group_create", status_code=status.HTTP_201_CREATED)
def create_group(payload: GroupSchema, db: Session = Depends(get_db)):
    try:
        new_group = Group(**payload.dict())
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        return {"status": "success", "group": new_group}
    except Exception as e:
        raise e

@app.post("/student_create", status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentSchema, db: Session = Depends(get_db)):
    try:
        new_student = Student(**payload.dict())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return {"status": "success", "student": new_student}
    except Exception as e:
        raise e

@app.post("/theme_create", status_code=status.HTTP_201_CREATED)
def create_theme(payload: ThemeSchema, db: Session = Depends(get_db)):
    if not (payload.complexity == None or 0 < payload.complexity < 11):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Theme complexity must be an integer in [1, 10], not {payload.complexity}')
    try:
        new_theme = Theme(**payload.dict())
        db.add(new_theme)
        db.commit()
        db.refresh(new_theme)
        return {"status": "success", "theme": new_theme}
    except Exception as e:
        raise e

@app.post("/source_create", status_code=status.HTTP_201_CREATED)
def create_source(payload: SourceSchema, db: Session = Depends(get_db)):
    try:
        new_source = Source(**payload.dict())
        db.add(new_source)
        db.commit()
        db.refresh(new_source)
        return {"status": "success", "source": new_source}
    except Exception as e:
        raise e

@app.post("/project_create", status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectSchema, db: Session = Depends(get_db)):
    if not (payload.mark == None or 1 < payload.mark < 6):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Project mark must be an integer in [2, 5], not {payload.mark}')
    try:
        new_project = Project(**payload.dict())
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return {"status": "success", "project": new_project}
    except Exception as e:
        raise e

@app.post("/source_project_create", status_code=status.HTTP_201_CREATED)
def create_source_project(payload: SourceProjectSchema, db: Session = Depends(get_db)):
    try:
        new_source_project = SourceProject(**payload.dict())
        db.add(new_source_project)
        db.commit()
        db.refresh(new_source_project)
        return {"status": "success", "new source_project": new_source_project}
    except Exception as e:
        raise e

# Update

@app.patch('/group_upd')
def update_group(groupId: int, payload: GroupSchema, db: Session = Depends(get_db)):
    group_query = db.query(Group).filter(Group.id == groupId)
    db_group = group_query.first()
    if not db_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No group with id={groupId} found')
    update_data = payload.dict(exclude_unset=True)
    group_query.filter(Group.id == groupId).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_group)
    return {"status": "success", "updated group": db_group}

@app.patch('/theme_upd')
def update_theme(themeId: int, payload: ThemeSchema, db: Session = Depends(get_db)):
    if not (payload.complexity == None or 0 < payload.complexity < 11):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Theme complexity must be an integer in [1, 10], not {payload.complexity}')
    theme_query = db.query(Theme).filter(Theme.id == themeId)
    db_theme = theme_query.first()
    if not db_theme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No theme with id={themeId} found')
    update_data = payload.dict(exclude_unset=True)
    theme_query.filter(Theme.id == themeId).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_theme)
    return {"status": "success", "updated theme": db_theme}

@app.patch('/student_upd')
def update_student(studentId: int, payload: StudentSchema, db: Session = Depends(get_db)):
    group_query = db.query(Group).filter(Group.id == payload.group_id)
    db_group = group_query.first()
    if not db_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No group with id={payload.group_id} found')
    

    student_query = db.query(Student).filter(Student.id == studentId)
    db_student = student_query.first()
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No student with id={studentId} found')
    update_data = payload.dict(exclude_unset=True)
    student_query.filter(Student.id == studentId).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_student)
    return {"status": "success", "updated student": db_student}

@app.patch('/source_upd')
def update_source(sourceId: int, payload: SourceSchema, db: Session = Depends(get_db)):
    source_query = db.query(Source).filter(Source.id == sourceId)
    db_source = source_query.first()
    if not db_source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No source with id={sourceId} found')
    update_data = payload.dict(exclude_unset=True)
    source_query.filter(Source.id == sourceId).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_source)
    return {"status": "success", "updated source": db_source}

@app.patch('/project_upd')
def update_project(projectId: int, payload: ProjectSchema, db: Session = Depends(get_db)):
    if not (payload.mark == None or 1 < payload.mark < 6):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Project mark must be an integer in [2, 5], not {payload.mark}')
    student_query = db.query(Student).filter(Student.id == payload.author_id)
    db_student = student_query.first()
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No student(author) with id={payload.author_id} found')
    theme_query = db.query(Theme).filter(Theme.id == payload.theme_id)
    db_theme = theme_query.first()
    if not db_theme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No theme with id={payload.theme_id} found')
    
    project_query = db.query(Project).filter(Project.id == projectId)
    db_project = project_query.first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No project with id={projectId} found')
    update_data = payload.dict(exclude_unset=True)
    project_query.filter(Project.id == projectId).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_project)
    return {"status": "success", "updated project": db_project}

@app.patch('/source_project_upd')
def update_source_project(source_projectId: int, payload: SourceProjectSchema, db: Session = Depends(get_db)):
    source_project_query = db.query(SourceProject).filter(SourceProject.id == source_projectId)
    db_source_project = source_project_query.first()
    if not db_source_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No source_project with id={source_projectId} found')
    update_data = payload.dict(exclude_unset=True)
    source_project_query.filter(SourceProject.id == source_projectId).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(db_source_project)
    return {"status": "success", "updated source_project": db_source_project}


# Delete

@app.delete('/group_delete')
def delete_group(groupId: int, db: Session = Depends(get_db)):
    group_query = db.query(Group).filter(Group.id == groupId)
    db_group = group_query.first()
    if not db_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No group with id={groupId} found')
    
    try:
        group_query.filter(Group.id == groupId).delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'There are students registered in given group (id={groupId}) in database')
    return {"status": "success"}

@app.delete('/theme_delete')
def delete_theme(themeId: int, db: Session = Depends(get_db)):
    theme_query = db.query(Theme).filter(Theme.id == themeId)
    db_theme = theme_query.first()
    if not db_theme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No theme with id={themeId} found')
    try:
        theme_query.filter(Group.id == themeId).delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'There are projects on given theme (id={themeId}) in database')
    return {"status": "success"}

@app.delete('/student_delete')
def delete_student(studentId: int, db: Session = Depends(get_db)):

    student_query = db.query(Student).filter(Student.id == studentId)
    db_student = student_query.first()
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No student with id={studentId} found')
    
    try:
        student_query.filter(Student.id == studentId).delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'There are projects created by given student (id={studentId}) in database')
    return {"status": "success"}

@app.delete('/source_delete')
def delete_source(sourceId: int, db: Session = Depends(get_db)):
    source_query = db.query(Source).filter(Source.id == sourceId)
    db_source = source_query.first()
    if not db_source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No source with id={sourceId} found')
    try:
        source_query.filter(Source.id == sourceId).delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'There are projects utilizing given source (id={sourceId}) in database')
    return {"status": "success"}

@app.delete('/project_delete')
def delete_project(projectId: int, db: Session = Depends(get_db)):

    project_query = db.query(Project).filter(Project.id == projectId)
    db_project = project_query.first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No project with id={projectId} found')
    try:
        source_project_query = db.query(SourceProject).filter(SourceProject.project_id == projectId)
        source_project_query.delete(synchronize_session=False)
        project_query.filter(Project.id == projectId).delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Unknown Error')
    return {"status": "success"}


@app.delete('/source_project_delete')
def delete_source_project(source_projectId: int, db: Session = Depends(get_db)):
    source_project_query = db.query(SourceProject).filter(SourceProject.id == source_projectId)
    db_source_project = source_project_query.first()
    if not db_source_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No source_project with id={source_projectId} found')
    try:
        source_project_query = db.query(SourceProject).filter(SourceProject.id == source_projectId)
        source_project_query.delete(synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Unknown Error')
    return {"status": "success"}


@app.delete('/group_delete')
def delete_group(groupId: str, db: Session = Depends(get_db)):
    group_query = db.query(Group).filter(Group.id == groupId)
    group = group_query.first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No group with this id: {id} found')
    group_query.delete(synchronize_session=False)
    db.commit()
    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)


