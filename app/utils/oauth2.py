from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.schemas.others import TokenPayload
from app.utils.database import get_db

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = 'samajesteDigho'
ALGORITHM = 'HS256'
EXPIRATION_TIME_IN_MINUTES = 30

def create_access_token(payload: dict) -> str:
    to_encode = payload.copy()
    expiration = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME_IN_MINUTES)
    to_encode.update({'exp': expiration})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str, credential_exception) -> TokenPayload:
    """ Verify the token """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data = TokenPayload(**payload)
        if data.ref is None or data.email is None:
            raise credential_exception
        return data
    except JWTError as e:
        print(e)
        raise  credential_exception

def get_user_from_token(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    """ Get User by decoding the token """
    print(f"Token: {token}")
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='Authentication token non conformant',
                                         headers={'WWW-Authenticate': 'Bearer'})
    payload = verify_access_token(token, credential_exception)
    user = db.query(UserModel).filter(UserModel.ref == payload.ref).first()
    return user
