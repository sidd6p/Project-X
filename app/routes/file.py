from typing import List, Optional
from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, database, oauth2


router = APIRouter(prefix="/files", tags=["Posts"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostResponseBase]
)
async def get_files(
    db: Session = Depends(database.get_db),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):
    files = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(offset)
        .all()
    )
    return files


@router.file(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponseBase
)
async def set_file(
    file: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    new_file = models.Post(**file.model_dump())
    new_file.owner_id = user_id
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponseBase
)
async def get_file(id: int, db: Session = Depends(database.get_db)):
    file = db.query(models.Post).filter(models.Post.id == id).first()

    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    else:
        return file


@router.put(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponseBase
)
async def update_file(
    id: int,
    updated_file: schemas.PostUpdate,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    file = db.query(models.Post).filter(models.Post.id == id)

    if file.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    elif user_id != file.first().owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can update only your files",
        )
    else:
        file.update(updated_file.model_dump(), synchronize_session=False)
        db.commit()
        return file.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    id: int,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    file = db.query(models.Post).filter(models.Post.id == id)

    if file.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found!",
        )
    elif user_id != file.first().owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can delete only your files",
        )
    else:
        file.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
