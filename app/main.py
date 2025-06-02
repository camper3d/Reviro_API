from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from . import crud, database, models, schemas
from datetime import date
from .models import TaskStatus

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/tasks/{task_id}', response_model=List[schemas.TaskOut])
def read_tasks(
        status: Optional[TaskStatus],
        due_date_from: Optional[date] = Query(None),
        due_date_to: Optional[date] = Query(None),
        db: Session = Depends(get_db),
):
    return crud.get_tasks(db, status, due_date_from, due_date_to)


@app.post('/tasks', response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_task(db, task)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail='Ошибка базы данных')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Неправильный ввод: {str(e)}')


@app.put('/tasks/{task_id}', response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated = crud.update_task(db, task_id, task)
    if updated is None:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    return updated

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    return {'msg': 'Задача удалена'}