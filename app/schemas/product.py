"""
Pydantic schemas for Product API responses (JSON:API format).
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from app.schemas.common import JSONAPILinks, JSONAPIMeta, JSONAPIRelationship, JSONAPIRelationshipData


class ProductAttributes(BaseModel):
    """
    Product resource attributes (JSON:API).

    Contains all product fields except relationships.
    """
    name: str
    slug: str
    description: Optional[str] = None
    price: Decimal = Field(..., description="Product price (exact decimal)")
    stock: int = Field(..., ge=0, description="Available inventory")
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2: allows working with SQLAlchemy models
        json_encoders = {
            Decimal: str  # Serialize Decimal as string to avoid precision loss
        }


class ProductRelationships(BaseModel):
    """
    Product relationships (JSON:API).

    Links to related resources (category).
    """
    category: JSONAPIRelationship


class ProductResourceLinks(BaseModel):
    """
    Links for individual product resource (JSON:API).

    Contains link to the product detail endpoint.
    """
    self: str  # Link to this product's detail endpoint


class ProductResource(BaseModel):
    """
    Product resource in JSON:API format.

    Example:
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "type": "product",
        "attributes": {
            "name": "Wireless Headphones",
            "slug": "wireless-headphones",
            "description": "Premium noise-canceling headphones",
            "price": "99.99",
            "stock": 50,
            "is_active": true,
            "created_at": "2026-05-04T10:00:00Z",
            "updated_at": "2026-05-04T10:00:00Z"
        },
        "relationships": {
            "category": {
                "data": {
                    "id": "660e8400-e29b-41d4-a716-446655440000",
                    "type": "category"
                }
            }
        },
        "links": {
            "self": "/api/v1/products/550e8400-e29b-41d4-a716-446655440000"
        }
    }
    """
    id: str  # UUID as string
    type: str = "product"
    attributes: ProductAttributes
    relationships: ProductRelationships
    links: ProductResourceLinks


class ProductResponse(BaseModel):
    """
    Single product response (JSON:API).

    Example:
    {
        "data": {
            "id": "...",
            "type": "product",
            "attributes": {...},
            "relationships": {...}
        }
    }
    """
    data: ProductResource


class ProductListResponse(BaseModel):
    """
    Product list response with pagination (JSON:API).

    Example:
    {
        "data": [
            {
                "id": "...",
                "type": "product",
                "attributes": {...},
                "relationships": {...}
            }
        ],
        "meta": {
            "total": 100,
            "page": 1,
            "per_page": 20,
            "total_pages": 5
        },
        "links": {
            "self": "/api/v1/products?page=1&per_page=20",
            "first": "/api/v1/products?page=1&per_page=20",
            "next": "/api/v1/products?page=2&per_page=20",
            "last": "/api/v1/products?page=5&per_page=20",
            "prev": null
        }
    }
    """
    data: List[ProductResource]
    meta: JSONAPIMeta
    links: JSONAPILinks