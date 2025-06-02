from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = 'sqlite:///./db_tasks.db' # подключаемся к sqlite

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False} # создаём движок
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # создание локальной сессии


Base = declarative_base() # базовый класс для моделей