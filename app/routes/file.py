from fastapi import Request, APIRouter, UploadFile, File, Depends
from typing import List
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import utils, schemas


routers = APIRouter(tags=["File"])


templates = Jinja2Templates(directory=str(utils.BASE_PATH/"templates"))



################# UPLOAD FILES PAGE ##################################
@routers.get("/uploadfiles")
def upload_file(request: Request):
    return templates.TemplateResponse("upload-file.html", {"request": request})



################# UPLOAD FILES PAGE ##################################
@routers.post("/uploadfiles")
async def upload_file(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    return_names = []
    for file in files:
        return_names.append(file.filename)
        file_path = utils.save_file(file)
        file = models.File(**{"file_path": file_path, "user_id": 2, "file_name": str(file.filename)})
        db.add(file)
        db.commit()
    return return_names