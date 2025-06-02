from .database import Base
from sqlalchemy import Column, Integer, String, Date, Enum
import enum

# перечисление статусов
class TaskStatus(str, enum.Enum):
    new = 'new'
    in_progress = 'in_progress'
    done = 'done'

# моделья для таблицы задач
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(Date)
    status = Column(Enum(TaskStatus, native_enum=False), default='new')


