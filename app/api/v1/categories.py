"""
Category API endpoints (v1).

Provides basic category listing and detail endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db
from app.services import category_service
from app.schemas.category import (
    CategoryListResponse,
    CategoryResponse,
    CategoryResource,
    CategoryAttributes,
    CategoryRelationships,
    CategoryResourceLinks
)
from app.schemas.common import JSONAPIRelationship, JSONAPIRelationshipData

router = APIRouter()


def build_category_resource(category, base_url: str = "/api/v1") -> CategoryResource:
    """
    Convert a Category SQLAlchemy model to JSON:API CategoryResource.

    Args:
        category: Category model instance
        base_url: Base URL for API (default: /api/v1)

    Returns:
        CategoryResource (JSON:API format)
    """
    relationships = None
    if category.parent_id:
        relationships = CategoryRelationships(
            parent={
                "data": {
                    "id": str(category.parent_id),
                    "type": "category"
                }
            }
        )

    return CategoryResource(
        id=str(category.id),
        type="category",
        attributes=CategoryAttributes(
            name=category.name,
            slug=category.slug,
            created_at=category.created_at,
            updated_at=category.updated_at,
        ),
        relationships=relationships,
        links=CategoryResourceLinks(
            self=f"{base_url}/categories/{category.id}"
        )
    )


@router.get("/categories", response_model=CategoryListResponse)
def list_categories(db: Session = Depends(get_db)):
    """
    List all categories.

    Returns all categories in the system.
    In Phase 2, we'll enhance this to return a hierarchical tree structure.

    **Example:**
    `GET /api/v1/categories`
    """
    categories = category_service.list_categories(db)

    return CategoryListResponse(
        data=[build_category_resource(c) for c in categories]
    )


@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get a single category by ID.

    **Example:**
    `GET /api/v1/categories/550e8400-e29b-41d4-a716-446655440000`

    Returns 404 if category not found.
    """
    category = category_service.get_category_by_id(db, category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail=f"Category with id {category_id} not found"
        )

    return CategoryResponse(
        data=build_category_resource(category)
    )