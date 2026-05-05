"""
SQLAlchemy Models

This package contains all database models for the e-commerce application.

Import all models here to ensure they're registered with SQLAlchemy
before creating tables with Base.metadata.create_all()
"""

# Import all models so they're registered with SQLAlchemy Base
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem

# Export all models for easy importing elsewhere
__all__ = [
    "User",
    "Category",
    "Product",
    "Cart",
    "CartItem",
    "Order",
    "OrderStatus",
    "OrderItem",
]