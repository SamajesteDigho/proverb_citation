from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from rough.models import user_model
from rough.schemas import user_schema
from rough.utils import db as database, helpers, oauth2

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/')
def create_user(data: user_schema.UserCreate,
                db: Session = Depends(database.get_db_instance),
                # curr_user: user_model.User = Depends(oauth2.get_current_user)
                ):
    try:
        data.ref = helpers.generate_ref()
        data.password = helpers.hash_pass(data.password)
        new_user = user_model.User(**data.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")

@router.get('/')
def get_users(db: Session = Depends(database.get_db_instance)):
    users = db.query(user_model.User).all()
    return users