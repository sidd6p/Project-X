from fastapi import Depends, Request, Form, APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from sqlalchemy.orm import Session
from ..import utils, schemas
from ..utils import get_db

routers = APIRouter(tags=["User"])

templates = Jinja2Templates(directory=str(utils.BASE_PATH/"templates"))


################# LOGIN PAGE ##################################
@routers.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



################# LOGIN PAGE ##################################
@routers.post("/login")
async def login(request: Request, email: EmailStr = Form(...), pswd: str = Form(...),  db: Session = Depends(get_db)):
    user = await utils.authenticate_user(email=email, pswd=pswd, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    utils.create_access_token(data = {"user_id": user.user_id})
    return templates.TemplateResponse("home.html", {"request": request})



################# REGISTER PAGE ##################################
@routers.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})



################# REGISTER PAGE ##################################
@routers.post("/register", response_model=schemas.UserSend)
async def register(request: Request, email: EmailStr = Form(...), pswd: str = Form(...), db: Session = Depends(get_db)):
    await utils.create_user(email=email, pswd=pswd, db=db)
    return templates.TemplateResponse("home.html", {"request": request})
