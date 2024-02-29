from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class FileBase(BaseModel):
    file_name: str
    file_path: str


class FileCreate(FileBase):
    pass


class FileUpdate(FileBase):
    pass


class UserBase(BaseModel):
    email: EmailStr


class FileResponseBase(FileBase):
    created_at: datetime
    owner_id: int
    id: int
    owner: UserBase


class FileAccessResponse(FileResponseBase):
    file: FileResponseBase
    access: int


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    created_at: datetime
    id: int


class AccessTokenBase(BaseModel):
    access_token: str
    type: str


class TokenDataBase(BaseModel):
    id: Optional[int] = None


class AccessBase(BaseModel):
    file_id: int
    add_access: conint(le=1)  # type: ignore
