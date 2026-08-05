from fastapi import APIRouter,Depends,HTTPException,status   # Import FastAPI utilities for routing, dependency injection, exceptions, and HTTP status codes.
from sqlalchemy.orm import Session   # Import SQLAlchemy Session type for database dependency injection.
from database import get_db          # Import the reusable database dependency that provides a session for each request.
import crud,schemas                  # Import the CRUD layer for database operations and Pydantic schemas for request/response validation.

router = APIRouter(prefix="/products",tags = ["products"])  # Create a router for Product APIs with a common URL prefix and Swagger documentation tag.

@router.get("/")   # Handle GET requests to retrieve all products.
def get_products(db: Session = Depends(get_db)):   # Define the endpoint and inject a database session using FastAPI dependency injection.
    return crud.get_products(db)         # Retrieve all products through the CRUD layer and return them as the API response.

@router.get("/{product_id}")          # Handle GET requests to retrieve a specific product by its ID.
def get_product(product_id: int,db: Session = Depends(get_db)):  # Define the endpoint to retrieve a single product by its ID and inject the database session.
    product = crud.get_product(db,product_id)    # Fetch the requested product from the database using its ID.
    if product is None:     # Check whether the requested product exists before returning it.
        raise HTTPException(status_code = 404,detail = "Product Not Found")     # Return a 404 error response when the requested product is not found.

    return product     # Return the requested product after confirming it exists.

@router.post("/",status_code = status.HTTP_201_CREATED)   # Handle POST requests to create a new product and return a 201 Created response.
def create_product(product: schemas.ProductCreate,db: Session = Depends(get_db)):  # Receive validated product data and inject a database session for creating a new product.
    return crud.create_product(db,product)   # Create the product through the CRUD layer and return the saved product.

@router.put("/{product_id}")     # Handle PUT requests to update a specific product using its ID.
def update_product(product_id: int,product: schemas.ProductUpdate,db: Session = Depends(get_db)):  # Receive product ID, validated update data, and inject a database session.
    product_db = crud.update_product(db,product_id,product)   # Update the product through the CRUD layer using the provided ID and update data.
    if product_db is None:    # Check whether the product exists before returning the updated result.
        raise HTTPException(status_code = 404,detail = "Product Not Found")   # Return a 404 error when the requested product does not exist.

    return product_db  # Return the updated product after successful modification.

@router.delete("/{product_id}")  # Handle DELETE requests to remove a product using its ID.
def delete_product(product_id: int,db: Session = Depends(get_db)):  # Recive the product id and inject the database session for deletion
    product = crud.delete_product(db,product_id)      # Delete the product through the CRUD layer using its ID.
    if product is None:        # Check whether the product existed before deletion.
        raise HTTPException(status_code = 404,detail = "Product Not Found")    # Return a 404 error when the requested product does not exist.
    
    return product   # Return the deleted product after successful removal.
