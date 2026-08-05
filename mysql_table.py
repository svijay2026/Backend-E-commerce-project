# For creating table structure in database from python

from database import Base,engine
from models import Base

Base.metadata.create_all(bind=engine)   # line used to create table structure using model module from python in mysql