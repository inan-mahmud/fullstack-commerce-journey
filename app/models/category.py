"""
Category model with hierarchical (tree) structure.

Categories can have parent-child relationships:
- Electronics (parent_id=NULL)
  - Mobile Phones (parent_id=Electronics.id)
    - Android (parent_id=Mobile Phones.id)
    - iOS (parent_id=Mobile Phones.id)

This enables browsing by category hierarchy.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Category(Base):
    """
    Product category with support for hierarchical structure.

    The self-referential foreign key (parent_id) allows us to build
    category trees of arbitrary depth.
    """
    __tablename__ = "categories"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Category Information
    name = Column(String, unique=True, index=True, nullable=False)
    # slug: URL-friendly version (e.g., "mobile-phones" from "Mobile Phones")
    slug = Column(String, unique=True, index=True, nullable=False)

    # Hierarchical Structure
    # parent_id points to another category (or NULL for top-level categories)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True, index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    # Self-referential relationship: a category can have a parent category
    parent = relationship("Category", remote_side=[id], backref="children")
    # backref="children" automatically creates a `children` attribute on the parent

    # One category can have many products
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        parent_info = f", parent_id={self.parent_id}" if self.parent_id else ""
        return f"<Category(id={self.id}, name='{self.name}'{parent_info})>"

    @property
    def full_path(self):
        """
        Returns the full category path (e.g., "Electronics > Mobile Phones > Android")
        Useful for breadcrumbs and display.
        """
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name