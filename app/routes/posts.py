from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.models.post_model import PostModel
from app.models.user_model import UserModel
from app.schemas.post_schema import PostBaseSchema, PostCreateSchema, PostUpdateSchema
from app.utils.database import get_db
from app.utils.helpers import generate_ref
from app.utils.oauth2 import get_user_from_token

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.post('', status_code=status.HTTP_201_CREATED, response_model=PostBaseSchema)
def create_post(post: PostCreateSchema, db: Session = Depends(get_db),
                curr_user: UserModel = Depends(get_user_from_token)):
    try:
        ref = generate_ref()
        new_post = PostModel(ref=ref, owner_ref=curr_user.ref, **post.model_dump())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Some errors encountered. Please check the documentation')

@router.get('/today', response_model=PostBaseSchema)
def get_post(db: Session = Depends(get_db)):
    post = db.query(PostModel).one()
    return post

@router.get('', response_model=List[PostBaseSchema])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(PostModel).all()
    return posts

@router.get('/{ref}', response_model=PostBaseSchema)
def get_post(ref:str, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.ref == ref).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post not found')
    return post

@router.put('/{ref}', response_model=PostBaseSchema)
def update_post(data: PostUpdateSchema, ref:str, db: Session = Depends(get_db),
                curr_user: UserModel = Depends(get_user_from_token)):
    query = db.query(PostModel).filter(PostModel.ref == ref)
    post = query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post not found')
    if curr_user.ref != post.owner_ref:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Unauthorized action')
    query.update(data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post

@router.delete('/{ref}')
def delete_post(ref: str, db: Session = Depends(get_db), curr_user: UserModel = Depends(get_user_from_token)):
    query = db.query(PostModel).filter(PostModel.ref == ref)
    post = query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post could not be found')
    if curr_user.ref != post.owner_ref:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='This action is forbidden')
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
