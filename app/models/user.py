"""
User model for authentication and user management.

This model handles both guest and registered users.
Guest users can place orders with email only (user_id will be NULL in orders).
Registered users get full account features.
"""

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid


class User(Base):
    """
    User model for registered customers.

    Authentication fields (password_hash, is_verified) will be used in Phase 2.
    For now, we're setting up the structure.
    """
    __tablename__ = "users"

    # Primary Key (UUID for security and distributed system compatibility)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Authentication & Contact
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)  # bcrypt hash (Phase 2)

    # Profile Information
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    # Account Status
    is_active = Column(Boolean, default=True, nullable=False)
    # is_verified: Email verification status (we'll implement email verification in Phase 2)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Timestamps (automatically managed)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    # One user can have many carts (though typically only one active cart)
    carts = relationship("Cart", back_populates="user", cascade="all, delete-orphan")

    # One user can have many orders
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', full_name='{self.full_name}')>"