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
        connection = psycopg2.connect(host="localhost", database="projectx-db", user="postgres", password="jbrEV2Grsd53", cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        connection.commit()
        break
    except Exception as error:
        print("Connection failed with error: {}".format(error))
        time.sleep(3)



app = FastAPI(
                title="Project-X",
                description=""" ## Cloud Storage Service """,
                version="1.0.0",
                contact={"name": "Siddhartha", "email": "siddpurwar@gmail.com"},
                docs_url="/api-documentation",
                redoc_url=None,
                openapi_tags=[{
                            "name": "User", 
                            "description": "These are User Api"
                        }, 
                        {
                            "name": "File", 
                            "description": "These are File Api"
                        }, 
                        ]
            )


app.include_router(user.routers)
app.include_router(file.routers)



BASE_PATH = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))



################# HOME PAGE ##################################
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "homePage": True})

