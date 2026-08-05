from pydantic_settings import BaseSettings    # Import BaseSettings to load configuration from environment variables or a .env file.
from pydantic import ConfigDict               # Import ConfigDict to configure how application settings are loaded.


class Settings(BaseSettings):                 # Define a settings class to load application configuration from the .env file.
    SECRET_KEY : str                          # Load the JWT secret key from the .env file.
    ALGORITHM : str                           # Load the JWT signing algorithm from the .env file.
    ACCESS_TOKEN_EXPIRE_MINUTES : int         # Load the JWT access token expiration time (in minutes) from the .env file.
    model_config = ConfigDict(                # Configure how the Settings class loads application configuration.
        env_file = ".env",                    # Specify the .env file that contains the application configuration.
        env_file_encoding = "utf-8",          # Read the .env file using UTF-8 encoding.
    )                         
settings = Settings()                         # Create a settings object and load all configuration values from the .env file.