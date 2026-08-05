from fastapi import APIRouter,Depends,HTTPException      # Import APIRouter to create and manage user-related API routes. 
# Import OAuth2PasswordRequestForm to receive username and password during login.
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user,create_access_token,get_current_user
from database import get_db                  # Get database session from FastAPI dependency injection
from sqlalchemy.orm import Session          # Import SQLAlchemy Session for database operations in the login endpoint.
from schemas import UserCreate
from models import User
import crud

router = APIRouter()               # Create a router instance to define and group user authentication endpoints.

@router.post("/login")             # Create a POST endpoint for user login authentication.
# Receive username and password from the login request using OAuth2 form data.
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)): 

    # Authenticate user credentials and return the user object if valid
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:    # Check whether authentication failed
        raise HTTPException(status_code = 400,detail = "Invalid username or password")  # Return error when login credentials are invalid
    return {"access_token": create_access_token(data={"sub": user.email}), "token_type": "bearer"}  # Generate JWT token and return it after successful login


@router.post("/register")                      # Create a POST endpoint for user registration.
def register(                                 # Define the register function.
    user: UserCreate,                         # Receive user registration data from the request body.
    db: Session = Depends(get_db)             # Get a database session using dependency injection.
):
    new_user = crud.create_user(db, user)          # Call the CRUD function to create a new user in the database.

    if not new_user:                          # Check whether user creation failed.
        raise HTTPException(                  # Raise an HTTP exception if registration fails.
            status_code=400,                  # Return HTTP 400 (Bad Request).
            detail="Username or Email already exists"   # Send an error message to the client.
        )

    return {                                 # Return a success response.
        "message": "User registered successfully"   # Inform the client that registration succeeded.
    }


@router.get("/me")                                  # Create a GET endpoint to return the logged-in user's details.
def get_me(current_user: User = Depends(get_current_user)):   # Get the authenticated user using JWT.
    return current_user                             # Return the authenticated user's information.