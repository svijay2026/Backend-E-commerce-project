# Import Session for database session type hint
from sqlalchemy.orm import Session

# Import SessionLocal to create a database session
from database import Sessionlocal

# Import the User model
from models import User

# Import bcrypt for password hashing
import bcrypt


def create_default_admin():
    """
    Create a default admin account only if one does not already exist.
    """

    # Create a new database session
    db: Session = Sessionlocal()

    try:
        # Check whether any user with role 'admin' already exists
        admin = db.query(User).filter(User.role == "admin").first()

        # If an admin is already present, stop the function
        if admin:
            print("Admin already exists.")
            return

        # Convert the plain text password into a hashed password
        # Never store plain text passwords in the database
        hashed_password = bcrypt.hashpw(
            "Admin@123".encode("utf-8"),   # Convert password string into bytes
            bcrypt.gensalt()               # Generate a random salt
        ).decode("utf-8")                  # Convert hashed bytes back to string

        # Create a new User object for the default admin
        new_admin = User(

            # Default username
            username="Vijay",

            # Default email
            email="vijay@example.com",

            # Store the hashed password
            hashed_password=hashed_password,

            # Assign the admin role
            role="admin",

            # Mark the account as active
            is_active=True
        )

        # Add the admin object to the database session
        db.add(new_admin)

        # Save the record permanently in the database
        db.commit()

        # Refresh the object so it contains the latest values from the database
        db.refresh(new_admin)

        print("Default admin created successfully.")

    finally:
        # Always close the database session
        # This prevents connection leaks
        db.close()
