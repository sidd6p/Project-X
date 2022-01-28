from .database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    pswd = Column(String, nullable=False)

class File(Base):
    __tablename__ = "files"
    file_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
