from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, oauth2, schemas, models


router = APIRouter(prefix="/votes", tags=["File"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def set_vote(
    access_payload: schemas.VoteBase,
    db: Session = Depends(database.get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    file_id = access_payload.file_id
    add_vote = bool(access_payload.add_vote)

    post = db.query(models.Post).filter(models.Post.id == file_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File with id: {file_id} not found",
        )
    voted = (
        db.query(models.File)
        .filter(models.File.file_id == file_id)
        .filter(models.File.user_id == user_id)
    )
    if add_vote:
        if voted.first() is None:
            file = models.File()
            file.user_id = user_id
            file.file_id = file_id
            db.add(file)
            db.commit()
            return {"message": f"Voted post with id: {file_id}"}
        else:
            return {"message": f"Post with id: {file_id} is already voted"}
    if not add_vote:
        if voted.first():
            voted.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
