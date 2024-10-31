from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USERNAME = 'postgres'
DB_PASSWORD = 'root'
DB_HOSTNAME = 'localhost'
DB_DATABASE = 'citations'

MONGODB_URL = ''
POSTGRE_URL = 'postgresql://{}:{}@{}/{}'.format(
    DB_USERNAME, DB_PASSWORD, DB_HOSTNAME, DB_DATABASE
)

engine = create_engine(POSTGRE_URL)
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db_instance():
    """ Get a stream connexion with the database """
    db = LocalSession()
    try:
        yield db
    except:
        db.close()
