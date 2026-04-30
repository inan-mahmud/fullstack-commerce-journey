from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import Generator

from app.config import settings


# Create database engine
# echo=True logs all SQL statements (useful for debugging in development)
engine = create_engine(
    settings.database_url,
    echo=False,  # Set to True to see SQL queries in console
    pool_pre_ping=True,  # Verify connections before using them
)

# Create SessionLocal class
# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Base class for all database models
class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    All models should inherit from this class.
    """
    pass


# Dependency for FastAPI routes
def get_db() -> Generator:
    """
    Database session dependency for FastAPI routes.

    Usage:
        @router.get("/products")
        def list_products(db: Session = Depends(get_db)):
            products = db.query(Product).all()
            return products

    The session is automatically closed after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
