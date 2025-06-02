from sqlalchemy .orm import Session
from typing import Optional
from datetime import date
from . import models, schemas

# Получение задач с фильтрацией
def get_tasks(db: Session,
              status: Optional[models.TaskStatus] = None,
              due_date_from: Optional[date] = None,
              due_date_to: Optional[date] = None,
):
    query = db.query(models.Task)

    if status:
        query = query.filter(models.Task.status == status)
    if due_date_from:
        query = query.filter(models.Task.due_date >= due_date_from)
    if due_date_to:
        query = query.filter(models.Task.due_date <= due_date_to)

    return query.all()



# получение задачи по id
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# Создание новой задачи
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# обновление задачи
def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    for key, value in task_data.dict().items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

# удаление задачи
def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    db.delete(db_task)
    db.commit()
    return True
