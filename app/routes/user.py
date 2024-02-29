from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, utils, database


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
async def set_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    new_user = db.query(models.User).filter(models.User.email == user.email)

    if new_user.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with emai: {user.email} alreay exists",
        )
    else:
        user.password = utils.hash_password(user.password)
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse
)
async def get_users(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found",
        )
    else:
        return user
