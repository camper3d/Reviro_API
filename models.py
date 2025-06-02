from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, Enum
import enum


class TaskStatus(str, enum.Enum):
    new = 'new'
    in_progress = 'in_progress'
    done = 'done'


class Task(BaseModel):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(Date)
    status = Column(Enum(TaskStatus), default='new')


