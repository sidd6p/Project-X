from fastapi import Depends, Request, Form, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from sqlalchemy.orm import Session
from .. import utils
from ..database import get_db
from .. import models
from .. import schemas


routers = APIRouter(tags=["User"])

templates = Jinja2Templates(directory=str(utils.BASE_PATH/"templates"))


################# LOGIN PAGE ##################################
@routers.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



################# LOGIN PAGE ##################################
@routers.post("/login")
async def login(email: EmailStr = Form(...), pswd: str = Form(...), db: Session = Depends(get_db)):
    return "okok"



################# REGISTER PAGE ##################################
@routers.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})



################# REGISTER PAGE ##################################
@routers.post("/register")
async def registern(email: EmailStr = Form(...), pswd: str = Form(...), db: Session = Depends(get_db)):
    user = models.User(**{"email" : email, "pswd" : pswd})
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
