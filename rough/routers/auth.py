from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from rough.models import logging, user_model
from rough.utils.db import get_db_instance
from rough.utils import db as database, helpers, oauth2

router = APIRouter(prefix='', tags=['Authentication'])

@router.post('/login')
def login_user(
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_instance)):
    """ Login a user """
    print("Here is what we want to do")
    user = db.query(user_model.User).filter(user_model.User.email == data.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid credentials')
    # if helpers.verify_pass(data.password, user.password):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f'Invalid credentials')
    # Log in info are correct
    # token = oauth2.create_access_token(payload={'ref': user.ref, 'email': user.email})
    # logging.LoginTable(user_ref=user.ref, token=token, location='China', ip_address='127.0.0.1')
    # db.commit()
    # return {'access_token': token, 'token_type': 'Bearer'}
    return {'token': "Tokenize"}