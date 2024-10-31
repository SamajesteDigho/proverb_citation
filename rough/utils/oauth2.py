from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from rough.models import user_model
from rough.schemas import others
from rough.utils import db as database

oauth_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = ''
ALGORITHM = 'HS256'
ACCESS_TOKEN_LIFE_SPAN = 30

def create_access_token(payload: dict) -> str:
    """ Generate a token base on the givent algorihme and secret """
    to_encode = payload.copy()
    expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_LIFE_SPAN)
    to_encode.update({'exp': expiration})
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        ref = payload.get('ref')
        email = payload.get('email')
        if ref is None:
            raise credentials_exception
        token_data = others.TokenPayload(ref=ref, email=email)
        return token_data
    except:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth_schema),
                     db: Session = Depends(database.get_db_instance)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f'Could not authenticate you',
                                         headers={'WWW-Authenticate': 'Bearer'})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(user_model.User).filter(user_model.User.ref == token_data.ref).first()
    return user
