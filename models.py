from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


class Status(str, Enum):
    new = 'new'
    in_progress = 'in_progress'
    done = 'done'


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Status = Status.new


