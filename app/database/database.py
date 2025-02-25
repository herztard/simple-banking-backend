# app/database/database.py
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

class DatabaseConnection:
    _engine = None
    _SessionLocal = None

    _database_url = URL.create(
        drivername=settings.DB_DRIVER_NAME,
        username=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_DATABASE,
    )

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls._engine = create_engine(cls._database_url)
        return cls._engine

    @classmethod
    def get_session(cls):
        if cls._SessionLocal is None:
            engine = cls.get_engine()
            cls._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return cls._SessionLocal()

    @classmethod
    def get_db_url(cls):
        return cls._database_url

def get_db() -> Generator:
    db = DatabaseConnection.get_session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from app.models.base import Base
    engine = DatabaseConnection.get_engine()
    Base.metadata.create_all(bind=engine)
