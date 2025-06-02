from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from . import crud, database, models, schemas
from datetime import date
from .models import TaskStatus
from .auth import verify_token


app = FastAPI()

models.Base.metadata.create_all(bind=database.engine) # Создание таблиц на основе моделей в sqlite

bearer_scheme = HTTPBearer() # инициализация авторизации

app.openapi_schema = None # обнуляем схему, и меняем на свою

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi # меняем стандартную схему на свою

# получение сессии БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# получение списка задач с фильтрами и авторизацией
@app.get('/tasks', response_model=List[schemas.TaskOut])
def read_tasks(
        status: Optional[TaskStatus] = Query(None),
        due_date_from: Optional[date] = Query(None),
        due_date_to: Optional[date] = Query(None),
        db: Session = Depends(get_db),
        token: None = Depends(verify_token),
):
    return crud.get_tasks(db, status, due_date_from, due_date_to)

# создание задач
@app.post('/tasks', response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_task(db, task)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail='Ошибка базы данных')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Неправильный ввод: {str(e)}')

# обновление задач
@app.put('/tasks/{task_id}', response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated = crud.update_task(db, task_id, task)
    if updated is None:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    return updated

# удаление задачи
@app.delete('/tasks/{task_id}')
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Задача не найдена')
    return {'msg': 'Задача удалена'}