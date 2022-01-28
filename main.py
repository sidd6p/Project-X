from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import models
from database import engine
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import List
import utils


models.Base.metadata.create_all(bind=engine)

while True:
    try:
        print("INSIDE DB APP")
        connection = psycopg2.connect(host="localhost", database="projectx-db", user="postgres", password="jbrEV2Grsd53", cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        connection.commit()
        break
    except Exception as error:
        print("Connection failed with error: {}".format(error))
        time.sleep(3)



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


################# HOME PAGE ##################################
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})



################# LOGIN PAGE ##################################
@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



################# LOGIN PAGE ##################################
@app.post("/login")
async def login(email:str = Form(...), pswd:str = Form(...)):
    return {email, pswd}



################# REGISTER PAGE ##################################
@app.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})



################# REGISTER PAGE ##################################
@app.post("/register")
async def logiregistern(email:str = Form(...), pswd:str = Form(...)):
    return {email, pswd}



################# UPLOAD FILES PAGE ##################################
@app.get("/uploadfiles")
def upload_file(request: Request):
    return templates.TemplateResponse("upload-file.html", {"request": request})



################# UPLOAD FILES PAGE ##################################
@app.post("/uploadfiles")
async def upload_file(files: List[UploadFile] = File(...)):
    utils.save_file(files)
    return "okok"