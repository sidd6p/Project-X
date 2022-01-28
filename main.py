from sqlite3 import Cursor
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import models
from database import engine
import psycopg2
from psycopg2.extras import RealDictCursor
import time



models.Base.metadata.create_all(bind=engine)

while True:
    try:
        connection = psycopg2.connect(host="host", database="database", user="user", password="password", cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        connection.commit()
        break
    except Exception as error:
        print("Connection failed with error: {}".format(error))
        time.sleep(3)



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(email:str = Form(...), pswd:str = Form(...)):
    return {email, pswd}

@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def logiregistern(email:str = Form(...), pswd:str = Form(...)):
    return {email, pswd}
