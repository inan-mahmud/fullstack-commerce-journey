"""
Cart Item model - represents individual products in a shopping cart.

Each cart item links a product to a cart with a specific quantity.
The UNIQUE constraint prevents duplicate products in the same cart.
"""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class CartItem(Base):
    """
    Individual item in a shopping cart.

    A cart item connects a product to a cart with a quantity.
    Each product can only appear once per cart (quantities are updated, not duplicated).
    """
    __tablename__ = "cart_items"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False, index=True)
    # ondelete="CASCADE": when cart is deleted, cart items are automatically deleted

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)

    # Quantity
    # How many of this product are in the cart
    # Must be >= 1 (enforced in application logic)
    quantity = Column(Integer, default=1, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Unique Constraint: prevent duplicate products in same cart
    # If user adds same product twice, we update quantity instead
    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),
    )

    # Relationships
    # Many-to-one: many cart items belong to one cart
    cart = relationship("Cart", back_populates="items")

    # Many-to-one: many cart items reference one product
    product = relationship("Product", back_populates="cart_items")

    def __repr__(self):
        return f"<CartItem(id={self.id}, cart_id={self.cart_id}, product_id={self.product_id}, qty={self.quantity})>"

    @property
    def subtotal(self):
        """
        Calculate subtotal for this cart item.

        Returns: product.price * quantity
        """
        return self.product.price * self.quantity
