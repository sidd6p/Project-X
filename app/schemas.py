from pydantic import BaseModel, EmailStr
from fastapi import Form

class User(BaseModel):
    email: EmailStr
    pswd: str
    def __init__(self, email: EmailStr = Form(...), pswd: str = Form(...)):
       super().__init__(email, pswd)

class File(BaseModel):
    file_name: str
    class Config:
        orm_mode = True
        