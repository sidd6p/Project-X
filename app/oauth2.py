from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models, database
from .config import settings
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expires_at = datetime.utcnow() + timedelta(
        minutes=settings.JWT_EXPIRATION_TIME_IN_MINUTE
    )
    to_encode["expires_at"] = str(expires_at)
    encoded_jwt = jwt.encode(
        claims=to_encode, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_access_toke(token: str):
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        token_data = schemas.TokenDataBase(id=payload.get("id"))
        if token_data.id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cannot validate the access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            return token_data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot validate the access token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)
):
    token_data = verify_access_toke(token)
    user_id = db.query(models.User).filter(models.User.id == token_data.id).first().id
    return user_id
