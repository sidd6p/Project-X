from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AccessTokenBase,
)
async def login(
    user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)
):
    user_db = db.query(models.User).filter(models.User.email == user.username).first()

    if user_db is None or not utils.is_correct_hash(user.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Wrong Credentials"
        )
    else:
        access_token = oauth2.create_access_token(data={"id": user_db.id})
        return {"access_token": access_token, "type": "bearer"}
