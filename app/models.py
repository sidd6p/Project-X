from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    pswd = Column(String, nullable=False)

class File(Base):
    __tablename__ = "files"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    pswd = Column(String, nullable=False)
