from fastapi import Depends, Request, APIRouter, Depends, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..import utils, schemas
from ..utils import get_db, get_current_user
from fastapi.responses import RedirectResponse

routers = APIRouter(tags=["User"])

templates = Jinja2Templates(directory=str(utils.BASE_PATH/"templates"))


################# LOGIN PAGE ##################################
@routers.get("/login")
def login(request: Request, token: str = Depends(utils.OAUTH2_SCHEMA)):
    if not get_current_user(token):
        return templates.TemplateResponse("login.html", {"request": request, "loginPage":True})
    else:
        return RedirectResponse("http://127.0.0.1:8000")
      



################# LOGIN TOKEN ##################################
@routers.post("/login/token")
async def login( response: Response, request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    user = await utils.authenticate_user(email=form_data.get("email"), pswd=form_data.get("pswd"), db=db)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request,"loginPage": True})
    token = utils.create_access_token(data = {"user_id": user.user_id})
    response = templates.TemplateResponse("home.html", {"request": request,"loginPage": True})
    response.set_cookie(key="access_token", value = f"Bearer {token}", httponly=True)
    return response  


################# REGISTER PAGE ##################################
@routers.get("/register")
def register(request: Request, token: str = Depends(utils.OAUTH2_SCHEMA)):
    if not get_current_user(token):
        return templates.TemplateResponse("register.html", {"request": request, "registerPage":True})
    else:
        return RedirectResponse("http://127.0.0.1:8000")
      



################# REGISTER PAGE ##################################
@routers.post("/register", response_model=schemas.UserSend)
async def register( response: Response, request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    await utils.create_user(email=form_data.get("email"), pswd=form_data.get("pswd"), db=db)
    return RedirectResponse("http://127.0.0.1:8000")
