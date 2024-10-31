from fastapi import FastAPI

from rough.routers import auth, users
from rough.utils import db as database

database.Base.metadata.create_all(bind=database.engine)

# Initialie the app entity
app = FastAPI()

# Link the routes
app.include_router(router=auth.router)
app.include_router(router=users.router)

# Description route
@app.get('/')
def welcome():
    """ Send a description of the API """
    return {
        'message': 'Welcome to CITATION_PROVERB API',
        'version': '1.0.0'
    }
