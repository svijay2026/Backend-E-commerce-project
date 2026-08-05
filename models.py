# Database structure

from sqlalchemy import Column,Integer,String,Float,Boolean,DateTime,ForeignKey # importing classes for table creation
from datetime import datetime,UTC

from database import Base  # importing base class from database module
class Category(Base):        # creating table name categories using base class
    __tablename__ = "categories"
    id = Column(Integer,primary_key = True)    # column creating with constraints
    name = Column(String(50),nullable = False , unique = True)   # column creating with constraints

class Product(Base):            # creating another table name products using base class
    __tablename__ = "products"
    id = Column(Integer,primary_key = True)   # column creating with constraints
    name = Column(String(50),nullable = False)   # column creating with constraints
    price = Column(Float,nullable = False)   # column creating with constraints
    description = Column(String(500),nullable = False)    # column creating with constraints
    category_id = Column(Integer,ForeignKey("categories.id"),nullable = False) 
    # column creating with constraints and make relationship with categories table using foreign key

# Base.metadata.create_all(bind=engine)   


class User(Base):   # Define the User table model
    __tablename__ = "users"   # Specify the database table name for this model
    id = Column(Integer,primary_key = True)   # Primary key for uniquely identifying each user
    username = Column(String(50),nullable = False,unique = True)  # Store a unique username for each user
    email = Column(String(100),unique = True,nullable = False)    # Store a unique email address for each user
    hashed_password = Column(String(255),nullable = False)        # Store the securely hashed password of the user
    role = Column(String(20), nullable=False, default="user")     # Store the user's role. Every new user gets the "user" role by default.
    is_active = Column(Boolean,default = True,nullable = False)   # Indicate whether the user account is active
    created_at = Column(DateTime,default = lambda:datetime.now(UTC),nullable = False)  # Store the date and time when the user account was created