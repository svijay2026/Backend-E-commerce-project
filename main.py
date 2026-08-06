from fastapi import FastAPI                 # Import FastAPI to create the backend application instance.
from routers import categories,products,user     # Import API routers to register different resource endpoints with the FastAPI application.
from create_admin import create_default_admin


# For creating table structure in database from python

from database import Base,engine
from models import Base

Base.metadata.create_all(bind=engine)   # line used to create table structure using model module from python in mysql
create_default_admin()


app=FastAPI()          # Create the main FastAPI application instance.

app.include_router(categories.router)  # Register category routes with the main FastAPI application.
app.include_router(products.router)    # Register product routes with the main FastAPI application.
app.include_router(user.router)        # Register all user-related API endpoints with the FastAPI application

@app.get("/")
def home():
    return {"Message" : "Welcome to E-commerce API"}
