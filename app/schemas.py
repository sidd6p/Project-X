from pydantic import BaseModel, EmailStr
from typing import List


##################### USER ###########################

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    pswd: str

class UserSend(UserBase):
    is_active: bool
    
    class Config:
        orm_mode = True

class User(UserBase):
    user_id: int
    
    class Config:
        orm_mode = True



##################### FILE ###########################

class FileBase(BaseModel):
    file_name: str
    file_path: str

class FileCreate(FileBase):
    owner_id: int
    user_id: List[int]
    