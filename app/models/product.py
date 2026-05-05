"""
Product model for e-commerce catalog.

Products belong to categories and can be added to carts or orders.
We track inventory (stock) and active status for availability management.
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    """
    Product catalog model.

    Each product belongs to one category and tracks its own inventory.
    Price is stored as NUMERIC for precision (important for money calculations).
    """
    __tablename__ = "products"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Product Information
    name = Column(String, index=True, nullable=False)
    # slug: URL-friendly identifier (e.g., "dell-xps-15-laptop")
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    # Pricing & Inventory
    # NUMERIC(10, 2) = up to 99,999,999.99 (10 digits total, 2 after decimal)
    # We use NUMERIC instead of FLOAT to avoid floating-point precision errors
    # Example: 19.99 stored exactly as 19.99, not 19.989999...
    price = Column(Numeric(10, 2), nullable=False)

    # Stock quantity (can be 0 for out-of-stock)
    stock = Column(Integer, default=0, nullable=False)

    # Category Association
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)

    # Status
    # is_active: Controls if product is visible/purchasable
    # False = hidden from catalog (soft delete, discontinued, etc.)
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    # Many-to-one: many products belong to one category
    category = relationship("Category", back_populates="products")

    # One product can be in many cart items
    cart_items = relationship("CartItem", back_populates="product")

    # One product can be in many order items
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock})>"

    @property
    def is_available(self):
        """Check if product is available for purchase."""
        return self.is_active and self.stock > 0

    @property
    def price_decimal(self):
        """Returns price as a Python Decimal for precise calculations."""
        return self.price
