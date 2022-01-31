from fastapi import Request, APIRouter, UploadFile, File, Depends
from typing import List
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .. import models, utils
from fastapi.responses import FileResponse


routers = APIRouter(tags=["File"])


templates = Jinja2Templates(directory=str(utils.BASE_PATH/"templates"))




################# UPLOAD FILES  ##################################
@routers.get("/uploadfiles")
def upload_file(request: Request):
    return templates.TemplateResponse("upload-file.html", {"request": request})




################# UPLOAD FILES  ##################################
@routers.post("/uploadfiles")
async def upload_file(request: Request, files: List[UploadFile] = File(...), db: Session = Depends(utils.get_db)):
    return_names = []
    for file in files:
        return_names.append({"file_name" :file.filename})
        file_path = utils.save_file(file)
        file = models.File(**{"file_path": file_path, "owner_id": 1, "file_name": str(file.filename)})
        db.add(file)
        db.commit()
        db.refresh(file)
        access = models.Access(**{"file_id": int(file.file_id), "user_id": 1})
        db.add(access)
        db.commit()
    return templates.TemplateResponse("upload-file.html", {"request": request})




################# SHOW FILES  ##################################
@routers.get("/showfile/")
async def show_my_file(request: Request, db: Session = Depends(utils.get_db)):
    files = db.query(models.File).filter(models.File.owner_id == 1).all()
    file_details = []
    for file in files:
        file_details.append({"file_name": file.file_name, "file_path": file.file_path})
    print(file_details)
    return templates.TemplateResponse("show-file.html", {"request": request, "file_details": file_details})


################# ACCESS FILES  ##################################
@routers.get("/static/files/{file_path}")
async def access_my_file(file_path:str, db: Session = Depends(utils.get_db)):
    if utils.has_access(file_path, 1, db):
        return FileResponse(path="app\\static\\files\\" + file_path)
    else:
        return "NOT ALLOWED"
