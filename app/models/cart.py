"""
Shopping cart model with support for both guest and authenticated users.

Cart Ownership:
- Guest users: identified by session_id (stored in cookie/header)
- Authenticated users: identified by user_id
- Only ONE of these fields should be set (enforced in application logic)

Cart Lifecycle:
- Created when first item is added
- Expires after inactivity period (7 days for guests, 30 days for users)
- Converted to order during checkout
"""

from sqlalchemy import Column, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime, timedelta
import uuid


class Cart(Base):
    """
    Shopping cart that can belong to either a guest or registered user.

    Important: Either session_id OR user_id must be set, but not both.
    This is enforced at the application layer (we'll implement validation in services).
    """
    __tablename__ = "carts"

    # Primary Key (UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Cart Ownership (mutually exclusive)
    # For guest users: random session ID (UUID) stored in cookie
    session_id = Column(String, unique=True, index=True, nullable=True)

    # For authenticated users: foreign key to users table
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)

    # Database constraint: at least one of session_id or user_id must be set
    # Note: This constraint ensures we know who owns the cart
    __table_args__ = (
        CheckConstraint(
            "(session_id IS NOT NULL AND user_id IS NULL) OR (session_id IS NULL AND user_id IS NOT NULL)",
            name="check_cart_owner"
        ),
    )

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Expiry Management
    # expires_at: Cart is considered abandoned after this time
    # Default: 7 days for guest, 30 days for authenticated (set in application logic)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    # Many-to-one: many carts can belong to one user
    user = relationship("User", back_populates="carts")

    # One cart has many cart items
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    # cascade="all, delete-orphan": when cart is deleted, all its items are also deleted

    def __repr__(self):
        owner = f"user_id={self.user_id}" if self.user_id else f"session_id={self.session_id}"
        return f"<Cart(id={self.id}, {owner}, items={len(self.items)})>"

    @property
    def is_expired(self):
        """Check if cart has expired."""
        return datetime.utcnow() > self.expires_at

    @property
    def is_guest_cart(self):
        """Check if this is a guest cart."""
        return self.session_id is not None

    @property
    def is_user_cart(self):
        """Check if this is an authenticated user's cart."""
        return self.user_id is not None

    def calculate_total(self):
        """
        Calculate total cart value.

        Returns: Decimal representing total price of all items in cart.
        """
        from decimal import Decimal
        total = Decimal("0.00")
        for item in self.items:
            total += item.product.price * item.quantity
        return total
