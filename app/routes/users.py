from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreateSchema, UserFullSchema, UserUpdateSchema
from app.utils import helpers
from app.utils.database import get_db
from app.utils.oauth2 import get_user_from_token

router = APIRouter(prefix='/users', tags=['Users'])

@router.post('', status_code=status.HTTP_201_CREATED, response_model=UserFullSchema)
def create_user(data: UserCreateSchema, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if user is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'This email is already used. Try another one')
    ref = helpers.generate_ref()
    data.password = helpers.hash_pass(data.password)
    new_user = UserModel(ref=ref, **data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('', response_model=List[UserFullSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

@router.get('/{ref}', response_model=UserFullSchema)
def get_user(ref: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.ref == ref).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with ref: {ref} does not exist.')
    return user

@router.put('/{ref}', response_model=UserFullSchema)
def update_user(ref:str, data: UserUpdateSchema, db: Session = Depends(get_db),
                curr_user: UserModel = Depends(get_user_from_token)):
    if curr_user is None or curr_user.ref != ref:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to perform this action')
    query = db.query(UserModel).filter(UserModel.ref == ref)
    user = query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User instance not found')
    query.update(data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(user)
    return user

@router.delete('/{ref}')
def delete_user(ref: str, db: Session = Depends(get_db),
                curr_user: UserModel = Depends(get_user_from_token)):
    if curr_user is None or curr_user.ref != ref:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to perform this action')
    query = db.query(UserModel).filter(UserModel.ref == ref)
    user = query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'User instance not found')
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
