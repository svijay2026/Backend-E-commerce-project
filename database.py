# Database connection/session/Base
from sqlalchemy import create_engine  # we importing class variable from sqlalchemy library

from sqlalchemy.orm import sessionmaker , declarative_base
# we importing classes from sqlalchemy module that is ORM(object relational mapping)

DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/ecommerece"  # Creating url to connect with database from python

engine = create_engine(DATABASE_URL)  
# creating connection through create_engine class with database_url(creating object name engine from class create_engine)

Sessionlocal = sessionmaker(   # creating session object from class sessionmaker and maintain changes and it was connected to connection
    autocommit = False,
    autoflush = False,
    bind = engine
)
Base = declarative_base()   # creating base object it have table like structure later it will inherit to child class


def get_db():           # Dependency function that creates, provides, and closes a database session for each request.
    db = Sessionlocal() # Create a new SQLAlchemy database session for the current request.
    try :               # Provide the database session to the API endpoint.
        yield db        # Pause here, hand the session to FastAPI, and resume after the request finishes.
    finally:            # Always execute cleanup, even if an exception occurs.
        db.close()      # Close the database session and release its resources.