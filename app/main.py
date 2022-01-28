from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import models
from .database import engine
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .routes import user, file
from pathlib import Path


models.Base.metadata.create_all(bind=engine)


while True:
    try:
        connection = psycopg2.connect(host="localhost", database="xxxxxxx", user="xxxxxx", password="xxxxxxx", cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        connection.commit()
        break
    except Exception as error:
        print("Connection failed with error: {}".format(error))
        time.sleep(3)



app = FastAPI(title="Project-X")


app.include_router(user.routers)
app.include_router(file.routers)


BASE_PATH = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))



################# HOME PAGE ##################################
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})



