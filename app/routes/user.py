from fastapi import Request, Form, APIRouter
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .. import utils


routers = APIRouter(tags=["User"])

templates = Jinja2Templates(directory=str(utils.BASE_PATH/"templates"))


################# LOGIN PAGE ##################################
@routers.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



################# LOGIN PAGE ##################################
@routers.post("/login")
async def login(email:str = Form(...), pswd:str = Form(...)):
    return {email, pswd}



################# REGISTER PAGE ##################################
@routers.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})



################# REGISTER PAGE ##################################
@routers.post("/register")
async def logiregistern(email:str = Form(...), pswd:str = Form(...)):
    return {email, pswd}

