from fastapi import APIRouter,Depends,HTTPException   # Import APIRouter to group related endpoints and Depends for dependency injection.
from sqlalchemy.orm import Session      # Import SQLAlchemy Session to perform database operations with type annotations.
from database import get_db             # Import SQLAlchemy Session to perform database operations with type annotations.
from schemas import CategoryCreate,CategoryUpdate  # Import Pydantic schemas to validate category creation and update requests.
from auth import get_current_admin      # Import the dependency that allows only admin users.
from models import User                 # Import the User model for type hinting.
import crud                             # Import the CRUD module to perform category database operations.


router = APIRouter(                     # Create a router and configure it with settings in the following lines.
    prefix = "/categories",             # Add a common URL prefix for all category endpoints in this router.
    tags = ["categories"]               # Group all category endpoints under the "Categories" section in the API documentation.
    )    

@router.get("")      # Register a GET endpoint to retrieve all categories using the router's prefix.
def get_categories(db: Session = Depends(get_db)):   # Receive a database session automatically through FastAPI's dependency injection.
    return crud.get_categories(db)      # Call the CRUD function to fetch categories and return the result to the client.

@router.get("/{category_id}")     # Register a GET endpoint to retrieve a specific category by its ID.
def get_category(category_id: int,db: Session = Depends(get_db)):    # Receive the category ID from the URL and inject a database session automatically.
    category = crud.get_category(db,category_id)    # Retrieve the category first so it can be validated before returning it.
    if category is None:              # Check whether the requested category exists before returning a response.
        raise HTTPException(status_code = 404, detail = "Category Not Found")  # Raise a 404 error if the requested category does not exist.
    return category

@router.post("/")                                             # Create a POST endpoint for creating a category.
def create_category(                                          # Define the create_category function.
    category: CategoryCreate,                                # Receive category data from the request body.
    db: Session = Depends(get_db),                           # Get a database session.
    current_user: User = Depends(get_current_admin)):          # Allow only authenticated admin users.
    return crud.create_category(db,category)    # Pass the validated category data to the CRUD layer and return the created category.

@router.put("/")    # Register a PUT endpoint to update a specific category by its ID.
def update_category(category_id: int,category: CategoryUpdate,db: Session = Depends(get_db)):   # Receive the category ID, validated update data, and a database session automatically.
    category = crud.update_category(db,category_id,category)    # Update the category in the database and store the result for validation.
    if category is None:   # Check whether the category exists before returning the updated result.
        raise HTTPException(status_code = 404,detail = "Category Not Found")   # Return a 404 error if the category to update does not exist.
    
    return category       # Return the updated category after confirming the update was successful.

@router.delete("/")       # Register a DELETE endpoint to remove a specific category by its ID.
def delete_category(category_id: int,db: Session = Depends(get_db)):   # Receive the category ID and database session to delete the specified category.
    category = crud.delete_category(db,category_id)    # Delete the category from the database and store the result for validation.
    if category is None:          # Check whether the category existed before confirming the deletion.
        raise HTTPException(status_code = 404,detail = "Category Not Found") # Return a 404 error if the category to delete does not exist.
    
    return category   # Return the deleted category after confirming it existed and was removed successfully.