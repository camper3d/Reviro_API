from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


class EnumStatus(str, Enum):
    new = 'new'
    in_progress = 'in_progress'
    done = 'done'


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date]
    status: EnumStatus = EnumStatus.new


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: int


    class Config:
        from_attributes = True