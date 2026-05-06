"""
FastAPI dependencies for API routes.

Dependencies are reusable components that can be injected into route functions.
"""

from typing import Generator
from sqlalchemy.orm import Session
from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.

    Yields a database session and ensures it's closed after use.

    Usage in route:
    @app.get("/products")
    def list_products(db: Session = Depends(get_db)):
        products = db.query(Product).all()
        return products
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
