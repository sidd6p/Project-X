from fastapi import Request, APIRouter, UploadFile, File, Depends, HTTPException, status
from typing import List
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .. import models, utils
from fastapi.responses import FileResponse, RedirectResponse

routers = APIRouter(tags=["File"])


templates = Jinja2Templates(directory=str(utils.BASE_PATH/"templates"))




################# UPLOAD FILES  ##################################
@routers.get("/uploadfiles")
def upload_file(request: Request):
    return templates.TemplateResponse("upload-file.html", {"request": request, "uploadFilePage": True})




################# UPLOAD FILES  ##################################
@routers.post("/uploadfiles")
async def upload_file(request: Request, files: List[UploadFile] = File(...), db: Session = Depends(utils.get_db), token:str = Depends(utils.OAUTH2_SCHEMA)):
    user_id = utils.get_current_user(token)
    if not user_id:
        return templates.TemplateResponse("login.html", {"request": request, "loginPage":True})
    return_names = []
    for file in files:
        return_names.append({"file_name" :file.filename})
        file_path = utils.save_file(file)
        file = models.File(**{"file_path": file_path, "owner_id":user_id, "file_name": str(file.filename)})
        db.add(file)
        db.commit()
        db.refresh(file)
        access = models.Access(**{"file_id": int(file.file_id), "user_id": user_id})
        db.add(access)
        db.commit()
    return templates.TemplateResponse("upload-file.html", {"request": request})




################# SHOW FILES  ##################################
@routers.get("/showfile/")
async def show_my_file(request: Request, db: Session = Depends(utils.get_db), token: str = Depends(utils.OAUTH2_SCHEMA)):
    user_id = utils.get_current_user(token)
    if not user_id:
        return RedirectResponse("http://127.0.0.1:8000/login")
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate User Try Login or check you Credentials", )
    files = db.query(models.File).filter(models.File.owner_id == user_id).all()
    file_details = []
    for file in files:
        file_details.append({"file_name": file.file_name, "file_id": file.file_id})
    print(file_details)
    return templates.TemplateResponse("show-file.html", {"request": request, "file_details": file_details})


################# ACCESS FILES  ##################################
@routers.get("/static/files/{file_path}")
async def view_file(file_path:str, db: Session = Depends(utils.get_db), token:str = Depends(utils.OAUTH2_SCHEMA)):
    user_id = utils.get_current_user(token)
    if utils.has_access(file_path, user_id, db):
        return FileResponse(path="app\\static\\files\\" + file_path)
    else:
        return "NOT ALLOWED"



################# UPDATE FILES  ##################################
@routers.get("/files/{file_id}")
async def access_my_file(request: Request, file_id:int, db: Session = Depends(utils.get_db), token:str = Depends(utils.OAUTH2_SCHEMA)):
    user_id = utils.get_current_user(token)
    file = utils.get_file(user_id, file_id, db)
    if not file:
        return "NOT ALLOWED"
    else:
        accesses = utils.get_all_access(file_id=file_id, db=db)
        return templates.TemplateResponse("file.html", {"request": request, "file": file, "accesses": accesses})
