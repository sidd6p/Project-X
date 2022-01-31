from xmlrpc.client import INTERNAL_ERROR
from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, ARRAY
from sqlalchemy.types import PickleType

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    pswd = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class File(Base):
    __tablename__ = "files"
    file_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

class Access(Base):
    __tablename__ = "access"
    file_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)
