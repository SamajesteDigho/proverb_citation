from fastapi import FastAPI

from app.routes import users
from app.utils.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router=users.router)

app.get('/')
def welcome():
    return {
        'version': '1.0.0',
        'messages': 'Welcome to the CITATION API'
    }
