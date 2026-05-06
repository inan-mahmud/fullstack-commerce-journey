"""
Pydantic schemas for Category API responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class CategoryAttributes(BaseModel):
    """Category resource attributes (JSON:API)."""
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic v2 to work with SQLAlchemy models


class CategoryRelationships(BaseModel):
    """Category relationships (JSON:API)."""
    parent: Optional[dict] = None  # Will contain {"data": {"id": "...", "type": "category"}}


class CategoryResourceLinks(BaseModel):
    """
    Links for individual category resource (JSON:API).

    Contains link to the category detail endpoint.
    """
    self: str  # Link to this category's detail endpoint


class CategoryResource(BaseModel):
    """
    Category resource in JSON:API format.

    Example:
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "type": "category",
        "attributes": {
            "name": "Electronics",
            "slug": "electronics",
            "created_at": "2026-05-04T10:00:00Z",
            "updated_at": "2026-05-04T10:00:00Z"
        },
        "relationships": {
            "parent": {
                "data": null
            }
        },
        "links": {
            "self": "/api/v1/categories/550e8400-e29b-41d4-a716-446655440000"
        }
    }
    """
    id: str
    type: str = "category"
    attributes: CategoryAttributes
    relationships: Optional[CategoryRelationships] = None
    links: CategoryResourceLinks


class CategoryResponse(BaseModel):
    """Single category response (JSON:API)."""
    data: CategoryResource


class CategoryListResponse(BaseModel):
    """List of categories response (JSON:API)."""
    data: List[CategoryResource]