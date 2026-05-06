"""
Pydantic schemas for API request/response validation.
"""

from app.schemas.common import (
    JSONAPILinks,
    JSONAPIMeta,
    JSONAPIRelationship,
    JSONAPIRelationshipData,
)
from app.schemas.product import (
    ProductAttributes,
    ProductRelationships,
    ProductResource,
    ProductResponse,
    ProductListResponse,
)
from app.schemas.category import (
    CategoryAttributes,
    CategoryRelationships,
    CategoryResource,
    CategoryResponse,
    CategoryListResponse,
)

__all__ = [
    # Common
    "JSONAPILinks",
    "JSONAPIMeta",
    "JSONAPIRelationship",
    "JSONAPIRelationshipData",
    # Product
    "ProductAttributes",
    "ProductRelationships",
    "ProductResource",
    "ProductResponse",
    "ProductListResponse",
    # Category
    "CategoryAttributes",
    "CategoryRelationships",
    "CategoryResource",
    "CategoryResponse",
    "CategoryListResponse",
]