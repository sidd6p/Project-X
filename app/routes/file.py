from fastapi import Request, APIRouter, UploadFile, File
from .. import utils
from typing import List
from fastapi.templating import Jinja2Templates
from pathlib import Path


routers = APIRouter(tags=["File"])

templates = Jinja2Templates(directory=str(utils.BASE_PATH/"templates"))



################# UPLOAD FILES PAGE ##################################
@routers.get("/uploadfiles")
def upload_file(request: Request):
    return templates.TemplateResponse("upload-file.html", {"request": request})



################# UPLOAD FILES PAGE ##################################
@routers.post("/uploadfiles")
async def upload_file(files: List[UploadFile] = File(...)):
    utils.save_file(files)
    return "okok"