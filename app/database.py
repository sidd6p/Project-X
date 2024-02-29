from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
