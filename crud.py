from sqlalchemy.orm import Session
# Session is used to communicate with the database
# and perform CRUD operations through SQLAlchemy.

from models import Product,Category,User
# Import both SQLAlchemy models because crud.py will perform
# database operations for products and categories.

from schemas import CategoryCreate,ProductCreate,ProductUpdate,CategoryUpdate,UserCreate
# Import Pydantic schemas to receive and validate product/category data
# before using that data with the SQLAlchemy database models.

from fastapi import HTTPException
import bcrypt        # Import bcrypt for password hashing and verification

# Create operations for the product and category
def create_product(db : Session,product : ProductCreate): # Creates a new product using the database session and validated product data received through the ProductCreate schema.
    new_product = Product(     # Create a SQLAlchemy Product object from the validated ProductCreate data so it can be stored in the database.
        name = product.name,   # Copy the product name from the validated Pydantic schema into the name field of the new SQLAlchemy Product object.
        price = product.price, # Copy the validated price from the ProductCreate object into the price field of the new Product object.
        description = product.description,  # Copy the validated description from the ProductCreate object into the description field of the new Product object.
        category_id = product.category_id   # Copy the category ID from the validated ProductCreate object into the category_id field of the new Product object.
    )
    db.add(new_product)      # Add the new Product object to the SQLAlchemy session so it can be inserted into the database.
    db.commit()              # Commit the transaction so the new product is saved permanently in the database.
    db.refresh(new_product)  # Reloads the object from the database to get the latest saved values
    return new_product       # Return the newly created product object to the code that called the CRUD function.


def create_category(db : Session,category : CategoryCreate): # Creates a new category using the database session and validated category data.
    new_category = Category(   # Create a new Category SQLAlchemy object from the validated category data.
        name = category.name   # Copy the category name from the validated CategoryCreate object into the new Category object.
    )
    db.add(new_category)        # Add the new Category object to the SQLAlchemy session for insertion into the database.
    db.commit()                 # Commit the transaction so the new category is permanently saved in the database.
    db.refresh(new_category) # Reloads the object from the database to get the latest saved values 
    return new_category         # Return the newly created category object to the code that called the CRUD function.

def create_user(db: Session,user: UserCreate):   # Create and store a new user in the database
    existing_user = get_user_by_email(db,user.email)   # Check whether the email is already registered
    if existing_user:   # Check if a user with this email already exists
        raise HTTPException(status_code = 400,detail = "Email already taken")  # Raise an error if the email is already registered

    existing_username = get_user_by_username(db,user.username) # Check whether the username is already registered
    if existing_username:
        raise HTTPException(status_code =400,detail = "Username already taken")  # Raise an error if the username is already registered

    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = User(                       # Create a new User model instance
        username = user.username,          # Set the username from the registration data
        email = user.email,                # Set the email from the registration data
        hashed_password = hashed_password,  # Store the hashed password in the User model
        role="user"                        # Assign the default role as "user".
    )
    db.add(new_user)                   # Add the new user object to the database session
    db.commit()                        # Commit the transaction to permanently save the user in the database
    db.refresh(new_user)               # Refresh the object with the latest database values
    return new_user                    # Return the newly created user object


# Read operations for product
# get all products
def get_products(db : Session):     # Defines a function to fetch product records from the database
    return db.query(Product).all()  # Fetches all product records from the database and returns them as a list

# get one product
def get_product(db : Session,product_id : int):   # Defines a function to fetch one product using its ID
    return db.query(Product).filter(Product.id == product_id).first()  # Finds and returns the first product whose ID matches the given product_id

# get all cateogries
def get_categories(db: Session):     # Defines a function to fetch all category records from the database
    return db.query(Category).all()  # Fetches and returns all category records from the database

# get one category
def get_category(db : Session,category_id : int):  # Defines a function to fetch one category using its ID
    return db.query(Category).filter(Category.id == category_id).first() # Finds and returns the first category whose ID matches the given category_id


def get_user_by_email(db: Session,email: str):   # Retrieve a user from the database using email address
    return db.query(User).filter(User.email == email).first()  # Find and return a user by email from the database

def get_user_by_username(db: Session,username: str):    # Retrieve a user from the database using username
    return db.query(User).filter(User.username == username).first()   # Find and return a user by username from the database

# Update operations for product
def update_product(db: Session,product_id: int,product: ProductUpdate):  # Defines a function to update a product using its ID and optional new product data
    product_db = db.query(Product).filter(Product.id == product_id).first()  # Finds the existing product in the database using its ID
    if product_db:   # Checks whether the requested product exists before updating it
        if product.name is not None:          # Checks whether a new product name was provided
            product_db.name = product.name    # Updates the existing product name with the provided new name

        if product.price is not None:         # Checks whether a new product price was provided
            product_db.price = product.price  # Updates the existing product price with the provided new price

        if product.description is not None:   # Checks whether a new product description was provided
            product_db.description = product.description  # Updates the existing product description with the provided new description
 
        if product.category_id is not None:   # Checks whether a new category ID was provided
            product_db.category_id = product.category_id   # Updates the existing product category ID with the provided new category ID

        db.commit()            # Permanently saves all the product changes to the database
        db.refresh(product_db) # Reloads the object from the database to get the latest saved values
        return product_db      # Returns the updated product object
    return None                # Returns None when the requested product does not exist



def update_category(db: Session,category_id: int,category :CategoryUpdate):  # Defines a function to update a category using its ID and optional new category data
    category_db = db.query(Category).filter(Category.id == category_id).first()  # Finds the existing category in the database using its ID
    if category_db:                     # Checks whether the requested category exists before updating it
        if category.name is not None:   # Checks whether a new category name was provided
            category_db.name = category.name  # Updates the existing category name with the provided new name
        db.commit()              # Permanently saves the category changes to the database
        db.refresh(category_db)  # Reloads the object from the database to get the latest saved values
        return category_db       # Returns the updated category object
    return None                  # Returns None when the requested category does not exist


# Delete operation

def delete_product(db: Session,product_id: int):  # Defines a function to delete a product using its ID
    product_db = db.query(Product).filter(Product.id == product_id).first()  # Finds the product in the database using its ID before deleting it
    if product_db:             # Checks whether the requested product exists before deleting it
        db.delete(product_db)  # Marks the product for deletion from the database
        db.commit()            # Permanently deletes the product from the database
        return product_db      # Returns the deleted product object
    return None                # Returns None when the requested product does not exist


def delete_category(db: Session,category_id: int):   # Defines a function to delete a category using its ID
    category_db = db.query(Category).filter(Category.id == category_id).first()  # Finds the category in the database using its ID before deleting it
    if category_db:             # Checks whether the requested category exists before deleting it
        db.delete(category_db)  # Marks the category for deletion from the database
        db.commit()             # Permanently deletes the category from the database
        return category_db      # Returns the deleted category objecta
    return None                 # Returns None when the requested category does not exist

