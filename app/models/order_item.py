"""
Order Item model with snapshot pattern.

This model demonstrates the snapshot pattern: we store product details
at the time of purchase, not just a reference to the product.

Why? Because products can change:
- Price can increase/decrease
- Name can be updated
- Product can be deleted

But your order history should always show what you actually bought
and what you paid at that moment.
"""

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid


class OrderItem(Base):
    """
    Individual item within an order.

    Key Feature: Snapshot Pattern
    - We store product_id (for reference/analytics)
    - BUT we also store product_name and price_at_purchase
    - This preserves historical accuracy even if product changes later

    Example:
    - You buy "iPhone 15 Pro" for $999 on May 1st
    - On May 2nd, product is renamed to "iPhone 15 Pro (Discontinued)"
    - On May 3rd, price increases to $1099
    - Your order still shows "iPhone 15 Pro" at $999 (correct!)
    """
    __tablename__ = "order_items"

    # Primary Key (UUID)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Foreign Keys
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    # ondelete="CASCADE": when order is deleted, all items are deleted too

    # Product Reference (for lookups/analytics)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False, index=True)
    # Note: We keep product_id even though we snapshot data
    # Useful for: "Show me all orders containing this product"

    # ===== SNAPSHOT FIELDS (captured at purchase time) =====
    # These fields preserve the state at the moment of purchase

    # Product name at time of order
    # Why snapshot? Product name can change or product can be deleted
    product_name = Column(String, nullable=False)

    # Price paid per unit at time of order
    # Why snapshot? Critical for invoices, refunds, accounting
    # This is THE price the customer was charged
    price_at_purchase = Column(Numeric(10, 2), nullable=False)

    # Quantity ordered
    quantity = Column(Integer, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    # Many-to-one: many order items belong to one order
    order = relationship("Order", back_populates="items")

    # Many-to-one: many order items reference one product
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, product='{self.product_name}', qty={self.quantity}, price={self.price_at_purchase})>"

    @property
    def subtotal(self):
        """
        Calculate subtotal for this order item.

        Returns: price_at_purchase * quantity
        Note: We use the SNAPSHOT price, not current product price!
        """
        return self.price_at_purchase * self.quantity

    @property
    def current_price_difference(self):
        """
        Compare price at purchase vs current product price.

        Useful for showing "You saved $X since purchase!" or
        "Price has increased $X since your order"

        Returns: Decimal (current_price - price_at_purchase)
        """
        if self.product:
            return self.product.price - self.price_at_purchase
        return None  # Product deleted, can't compare
