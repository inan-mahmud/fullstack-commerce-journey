"""
Order model for completed purchases.

Orders can be placed by both guest and registered users.
Each order tracks customer info, shipping details, and status.
"""

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class OrderStatus(enum.Enum):
    """
    Order status enumeration.

    Status flow:
    pending → confirmed → shipped → delivered
                ↓
            cancelled (can cancel from pending/confirmed only)
    """
    PENDING = "pending"          # Order created, payment pending/processing
    CONFIRMED = "confirmed"      # Payment confirmed, order being prepared
    SHIPPED = "shipped"          # Order dispatched for delivery
    DELIVERED = "delivered"      # Order delivered to customer
    CANCELLED = "cancelled"      # Order cancelled (by user or admin)


class Order(Base):
    """
    Customer order model.

    Orders can be placed by:
    - Guest users (user_id=NULL, email required)
    - Registered users (user_id set, email from user profile)

    Shipping address is stored as JSON for flexibility.
    """
    __tablename__ = "orders"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Order Identification
    # order_number: Human-readable unique identifier (e.g., "ORD-20260504-0001")
    # Generated in application logic
    order_number = Column(String, unique=True, index=True, nullable=False)

    # Customer Information
    # user_id: NULL for guest orders, set for registered users
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    # Email & phone are required for ALL orders (guest or registered)
    # For registered users, we copy from user profile
    # For guest users, they provide during checkout
    email = Column(String, index=True, nullable=False)
    phone = Column(String, nullable=False)

    # Shipping Address (stored as JSON for flexibility)
    # Example structure:
    # {
    #   "street": "123 Main St",
    #   "city": "New York",
    #   "state": "NY",
    #   "zip_code": "10001",
    #   "country": "USA"
    # }
    shipping_address = Column(JSON, nullable=False)

    # Order Status
    status = Column(
        SQLEnum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False,
        index=True
    )

    # Financial Information
    # total_amount: Snapshot of total at order creation time
    # This is the final amount charged to customer
    total_amount = Column(Numeric(10, 2), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    # Many-to-one: many orders can belong to one user
    user = relationship("User", back_populates="orders")

    # One order has many order items
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, order_number='{self.order_number}', status={self.status.value}, total={self.total_amount})>"

    @property
    def is_cancellable(self):
        """Check if order can be cancelled."""
        # Can only cancel pending or confirmed orders
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]

    @property
    def is_guest_order(self):
        """Check if this is a guest order."""
        return self.user_id is None
