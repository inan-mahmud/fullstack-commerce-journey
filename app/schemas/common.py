"""
Common Pydantic schemas for JSON:API responses.

These schemas provide the standard JSON:API structure for all endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class JSONAPILinks(BaseModel):
    """
    JSON:API Links object for pagination.

    Example:
    {
        "self": "/api/v1/products?page=2",
        "first": "/api/v1/products?page=1",
        "last": "/api/v1/products?page=10",
        "prev": "/api/v1/products?page=1",
        "next": "/api/v1/products?page=3"
    }
    """
    self: str
    first: Optional[str] = None
    last: Optional[str] = None
    prev: Optional[str] = None
    next: Optional[str] = None


class JSONAPIMeta(BaseModel):
    """
    JSON:API Meta object for pagination metadata.

    Example:
    {
        "total": 100,
        "page": 2,
        "per_page": 20,
        "total_pages": 5
    }
    """
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")


class JSONAPIRelationshipData(BaseModel):
    """
    JSON:API Relationship data (resource identifier).

    Example:
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "type": "category"
    }
    """
    id: str
    type: str


class JSONAPIRelationship(BaseModel):
    """
    JSON:API Relationship object.

    Example:
    {
        "data": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "type": "category"
        }
    }
    """
    data: Optional[JSONAPIRelationshipData] = None
