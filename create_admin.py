# Import Session class for database session type hint
from sqlalchemy.orm import Session

# Import SessionLocal to create a database session
from database import SessionLocal

# Import the User model
from models import User

# Import the password hashing function
# Replace get_password_hash with your actual function name if it is different.
from auth import get_password_hash


def create_default_admin():
    """
    Creates the first admin account only if an admin does not already exist.
    """

    # Create a new database session
    db: Session = SessionLocal()

    try:
        # Check whether an admin user already exists
        admin = db.query(User).filter(User.role == "admin").first()

        # If an admin already exists, stop the function
        if admin:
            print("Admin already exists.")
            return

        # Create a new admin user object
        new_admin = User(

            # Default username
            username="admin",

            # Default email
            email="admin@example.com",

            # Store the password in hashed form (Never store plain text passwords)
            hashed_password=get_password_hash("Admin@123"),

            # Assign admin role
            role="admin",

            # Mark the account as active
            is_active=True
        )

        # Add the admin object to the session
        db.add(new_admin)

        # Save the record permanently in the database
        db.commit()

        # Refresh the object so it contains the latest database values
        db.refresh(new_admin)

        print("Default admin created successfully.")

    finally:
        # Always close the database session
        db.close()