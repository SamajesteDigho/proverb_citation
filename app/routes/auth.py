from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.models.logging import LoginModel
from app.schemas.others import TokenResponse
from app.schemas.user_schema import UserFullSchema
from app.utils.database import get_db
from app.utils.helpers import verify_pass
from app.utils.oauth2 import create_access_token, get_user_from_token

router = APIRouter(prefix='', tags=['Authentication'])

@router.post('/login', response_model=TokenResponse)
def login(cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == cred.username).first()
    print(user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    if not verify_pass(cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    token = create_access_token(payload={'ref': user.ref, 'email': user.email})
    loginInfo = LoginModel(user_ref=user.ref, token=token, location='China')
    db.add(loginInfo)
    db.commit()
    return {'access_token': token, 'token_type': 'Bearer'}

@router.get('/me', response_model=UserFullSchema)
def return_me(curr_user: UserModel = Depends(get_user_from_token)):
    return curr_user
