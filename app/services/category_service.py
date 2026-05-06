"""
Category service - Business logic for category operations.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.models.category import Category


def list_categories(db: Session) -> List[Category]:
    """
    List all categories.

    Returns all categories (we'll add hierarchy building in Phase 2).

    Args:
        db: Database session

    Returns:
        List of Category objects
    """
    return db.query(Category).order_by(Category.name).all()


def get_category_by_id(db: Session, category_id: UUID) -> Optional[Category]:
    """
    Get a single category by ID.

    Args:
        db: Database session
        category_id: Category UUID

    Returns:
        Category object or None if not found
    """
    return db.query(Category).filter(Category.id == category_id).first()