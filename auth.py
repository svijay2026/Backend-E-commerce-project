from datetime import datetime, timedelta, timezone    # Import classes to create timezone-aware JWT expiration times.
from jose import JWTError,jwt                         # Import JWT functions and the exception used for invalid or expired tokens.
import bcrypt                                         # Import bcrypt to verify hashed passwords during login.
from fastapi import HTTPException,status,Depends              # Import HTTPException for authentication errors and status for standard HTTP status codes.
from sqlalchemy.orm import Session                    # Import SQLAlchemy Session for database operations.
import database,crud                                  # Import the database module and CRUD functions for authentication.
from models import User
from configure import settings                        # Import the application settings loaded from the .env file.
from fastapi.security import OAuth2PasswordBearer     # Import OAuth2PasswordBearer to extract JWT access tokens from the Authorization header.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")  # Create an OAuth2 password bearer scheme to extract JWT tokens from the Authorization header.

def create_access_token(data: dict):                  # Create a JWT access token using the provided payload data.
    to_encode = data.copy()                           # Create a copy of the payload to avoid modifying the original data.
    expire = datetime.now(timezone.utc) + timedelta(  # Get the current UTC date and time.
    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(                         # Encode the payload data into a JWT token using the secret key and algorithm.
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM)
    return encoded_jwt


# Define a function to compare the user's plain password with the stored hashed password.
def verify_password(plain_password: str, hashed_password: str) -> bool:

    return bcrypt.checkpw(                # Check whether the plain password matches the bcrypt hashed password and return the result.
        plain_password.encode("utf-8"),   # Convert the plain password string into bytes because bcrypt works with bytes.
        hashed_password.encode("utf-8"))  # Convert the stored hashed password string into bytes for bcrypt comparison.


def authenticate_user(db: Session, email: str, password: str):   # Authenticate a user by checking email existence and verifying the password.
    user = crud.get_user_by_email(db, email)           # Retrieve the user from the database using the provided email.
    if not user:           # Check whether a user with the given email exists.
        return False       # Return False when the user does not exist.

    if not verify_password(password,user.hashed_password):  # Check whether the entered password matches the stored hashed password.
        return False            # Return False when the password does not match the stored hash.
    return user                 # Return the authenticated user after successful verification.


def get_current_user(                                         # Define a function to get the currently authenticated user.
    token: str = Depends(oauth2_scheme),                      # Extract the JWT token from the Authorization header.
    db: Session = Depends(database.get_db)                    # Get a database session using dependency injection.
):
    try:                                                      # Start a try block to catch JWT decoding errors.

        payload = jwt.decode(                                 # Decode and verify the JWT token.
            token,                                            # JWT token received from the client.
            settings.SECRET_KEY,                              # Secret key used to verify the token signature.
            algorithms=[settings.ALGORITHM]                   # JWT algorithm used during encoding.
        )

        email = payload.get("sub")                            # Read the email stored in the "sub" claim of the token.

        if email is None:                                     # Check whether the token contains an email.
            raise HTTPException(                              # Raise an HTTP exception if email is missing.
                status_code=status.HTTP_401_UNAUTHORIZED,     # Return HTTP 401 Unauthorized.
                detail="Invalid authentication token",        # Error message sent to the client.
                headers={"WWW-Authenticate": "Bearer"}        # Tell the client to use Bearer authentication.
            )

    except JWTError:                                          # Catch any JWT decoding or validation errors.

        raise HTTPException(                                  # Raise an HTTP exception for an invalid token.
            status_code=status.HTTP_401_UNAUTHORIZED,         # Return HTTP 401 Unauthorized.
            detail="Could not validate credentials",          # Error message sent to the client.
            headers={"WWW-Authenticate": "Bearer"}            # Tell the client to use Bearer authentication.
        )

    user = crud.get_user_by_email(db, email)                  # Retrieve the user from the database using the email.

    if user is None:                                          # Check whether the user exists.
        raise HTTPException(                                  # Raise an HTTP exception if the user is not found.
            status_code=status.HTTP_401_UNAUTHORIZED,         # Return HTTP 401 Unauthorized.
            detail="User not found",                          # Error message sent to the client.
            headers={"WWW-Authenticate": "Bearer"}            # Tell the client to use Bearer authentication.
        )

    return user                                               # Return the authenticated user object.


def get_current_admin(                                          # Define a function to allow only admin users.
    current_user: User = Depends(get_current_user)              # Get the currently authenticated user.
):
    if current_user.role != "admin":                            # Check whether the user's role is not "admin".
        raise HTTPException(                                    # Raise an HTTP exception.
            status_code=status.HTTP_403_FORBIDDEN,              # Return HTTP 403 Forbidden.
            detail="You do not have permission to perform this action."  # Inform the client that admin access is required.
        )

    return current_user                                         # Return the authenticated admin user.