from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Uses Pydantic Settings for type-safe configuration management.
    Automatically reads from .env file and validates required fields.
    """

    # Database Configuration
    database_url: str

    class Config:
        env_file = ".env"
        case_sensitive = False  # Allow DATABASE_URL or database_url


# Singleton instance - created once, imported everywhere
settings = Settings()
