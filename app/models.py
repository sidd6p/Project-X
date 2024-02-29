import time
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))


class Access(Base):
    __tablename__ = "votes"

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    file_id = Column(
        Integer,
        ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
