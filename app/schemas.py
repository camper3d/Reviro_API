from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

# перечисление статусов задачи
class EnumStatus(str, Enum):
    new = 'new'
    in_progress = 'in_progress'
    done = 'done'

# схема задачи
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date]
    status: EnumStatus = EnumStatus.new

# создание задачи(схема)
class TaskCreate(TaskBase):
    pass

# обновление задачи(схема)
class TaskUpdate(TaskBase):
    pass

# вывод задачи(схема)
class TaskOut(TaskBase):
    id: int


    class Config:
        from_attributes = True # поддержка орм моделей