import shutil
import os
from datetime import datetime, timedelta
from pathlib import Path
import secrets
from passlib.context import CryptContext
from .import database, models, schemas
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import EmailStr
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
import fastapi.security as security
from fastapi.security.oauth2 import OAuth2PasswordBearer


######################## VARIABLES #####################################

SECRET_KEY = "fdsgdfFGDH3425asDAFgjg968liuQSAFgf47246HNFGJmkgkjfwewqfv4gfn56"
ALGORITHM = "HS256"
EXP_TIME_MIN = 20
OAUTH2_SCHEMA = OAuth2PasswordBearer(tokenUrl="login")
BASE_PATH = Path(__file__).resolve().parent
PSWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2schema = security.OAuth2PasswordBearer(tokenUrl="login")




######################## DATABASE #########################################

def create_db():
    return database.Base.metadat.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



######################## USER #########################################

async def get_user(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()

async def create_user(email, pswd, db: Session):
    hashed_pswd = PSWD_CONTEXT.hash(pswd)
    user = models.User(**{"email" : email, "pswd" : hashed_pswd})
    db.add(user)
    db.commit()
    db.refresh(user)

async def authenticate_user(email: EmailStr, pswd: str, db: Session):
    user_db = await get_user(email, db)
    if not user_db or not PSWD_CONTEXT.verify(pswd, user_db.pswd):
        return False
    return user_db


def get_current_user(token: str = Depends(OAUTH2_SCHEMA), db: Session = Depends(get_db)):
    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credential_exceptions)
    user = db.query(models.User).filter(models.User.user_id == token.user_id).first()
    return user.user_id    



######################## TOKEN #########################################

def verify_access_token(token: str, credential_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if not user_id:
            raise credential_exceptions
        token_data = schemas.TokenData(user_id = user_id)
    except JWTError:
        raise credential_exceptions
    return token_data

def create_access_token(data: dict):
    to_encode = data.copy()
    expires_at = datetime.utcnow() + timedelta(minutes=EXP_TIME_MIN)
    to_encode.update({"exp": expires_at})
    jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, credential_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if not user_id:
            raise credential_exceptions
        token_data = schemas.TokenData(user_id = user_id)
    except JWTError:
        raise credential_exceptions
    return token_data




######################## FILE #########################################

async def file_selector(user: schemas.User, db: Session, id: int):
    file = (db.query(models.file).filter_by(owner_id=user.id).filter(models.file.id == id).first())
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="file does not exists")
    return file

async def delete_files_by_id(user: schemas.User, db: Session, id: int):
    file = await file_selector(user=user, id=id, db=db)
    db.delete(file)
    db.commit()

async def update_file_by_id(file: schemas.FileCreate, user: schemas.User, db: Session, id: int):
    pass
    
def save_file(file):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(file.filename)
    file_name = random_hex + file_ext
    file_path = os.path.join(BASE_PATH, 'static\\files', file_name)
    print(file_path)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return str(file_name)

def has_access(file_path: str, user_id: int, db: Session):
    file = db.query(models.Access).filter(models.File.file_path == file_path).first()
    acces = db.query(models.Access).filter(models.Access.user_id == user_id).filter(models.Access.file_id == file.file_id).first()
    if acces:
        return True
    else:
        return False