# NOTE: this is the comment router file to handle all the comments routes operations

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database, oauth2


# creates the router for the comments endpoints
router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(comment: schemas.CreateComment, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(
        models.Post.id == comment.com_post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {comment.com_post_id} does not exist')
    new_comment = models.Comment(
        com_owner_id=current_user.id, com_post_id=comment.com_post_id, content=comment.content)

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    comment_query = db.query(models.Comment).filter(models.Comment.id == id)
    comment_ = comment_query.first()

    if not comment_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Comment with id: {id} does not exist')
    elif comment_.com_owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perfrom rquested action')

    comment_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Comment deleted"}


@router.get("/", response_model=List[schemas.CommentResponse])
def get_comments(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    comments = db.query(models.Comment).all()

    return comments
