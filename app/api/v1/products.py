"""
Product API endpoints (v1).

Provides product listing, filtering, search, and detail endpoints
with JSON:API response format.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
from decimal import Decimal
from uuid import UUID
import math

from app.api.deps import get_db
from app.services import product_service
from app.schemas.product import (
    ProductListResponse,
    ProductResponse,
    ProductResource,
    ProductAttributes,
    ProductRelationships,
    ProductResourceLinks
)
from app.schemas.common import JSONAPILinks, JSONAPIMeta, JSONAPIRelationship, JSONAPIRelationshipData

router = APIRouter()


def build_product_resource(product, base_url: str = "/api/v1") -> ProductResource:
    """
    Convert a Product SQLAlchemy model to JSON:API ProductResource.

    Args:
        product: Product model instance
        base_url: Base URL for API (default: /api/v1)

    Returns:
        ProductResource (JSON:API format)
    """
    return ProductResource(
        id=str(product.id),
        type="product",
        attributes=ProductAttributes(
            name=product.name,
            slug=product.slug,
            description=product.description,
            price=product.price,
            stock=product.stock,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
        ),
        relationships=ProductRelationships(
            category=JSONAPIRelationship(
                data=JSONAPIRelationshipData(
                    id=str(product.category_id),
                    type="category"
                )
            )
        ),
        links=ProductResourceLinks(
            self=f"{base_url}/products/{product.id}"
        )
    )


def build_pagination_links(request: Request, page: int, per_page: int, total_pages: int) -> JSONAPILinks:
    """
    Build JSON:API pagination links.

    Args:
        request: FastAPI request object (to get base URL)
        page: Current page number
        per_page: Items per page
        total_pages: Total number of pages

    Returns:
        JSONAPILinks object
    """
    base_url = str(request.url).split('?')[0]  # Remove existing query params
    query_params = dict(request.query_params)
    query_params["per_page"] = per_page

    def make_url(page_num: int) -> str:
        query_params["page"] = page_num
        params_str = "&".join(f"{k}={v}" for k, v in query_params.items())
        return f"{base_url}?{params_str}"

    return JSONAPILinks(
        self=make_url(page),
        first=make_url(1),
        last=make_url(total_pages),
        prev=make_url(page - 1) if page > 1 else None,
        next=make_url(page + 1) if page < total_pages else None,
    )


@router.get("/products", response_model=ProductListResponse)
def list_products(
    request: Request,
    # Search
    search: Optional[str] = Query(None, description="Search in product name and description"),
    # Filters
    category_id: Optional[UUID] = Query(None, description="Filter by category (includes subcategories)"),
    min_price: Optional[Decimal] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[Decimal] = Query(None, ge=0, description="Maximum price"),
    in_stock: Optional[bool] = Query(None, description="Only show products in stock"),
    # Sorting
    sort_by: str = Query("created_at", regex="^(name|price|created_at)$", description="Sort by field"),
    order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    # Database
    db: Session = Depends(get_db)
):
    """
    List products with optional filtering, searching, sorting, and pagination.

    **Examples:**
    - `/api/v1/products` - All products
    - `/api/v1/products?search=wireless` - Search for "wireless"
    - `/api/v1/products?category_id=550e8400-...` - Filter by category
    - `/api/v1/products?min_price=50&max_price=200` - Price range
    - `/api/v1/products?in_stock=true` - Only in-stock products
    - `/api/v1/products?sort_by=price&order=asc` - Sort by price ascending

    **Category Filtering (Option A):**
    When filtering by `category_id`, products from subcategories are AUTOMATICALLY included.

    Example:
    - Category: Electronics (id=550e8400-...)
      - Subcategory: Mobile Phones
      - Subcategory: Laptops

    `GET /api/v1/products?category_id=550e8400-...` returns products from Electronics, Mobile Phones, AND Laptops.
    """
    # Calculate pagination offset
    skip = (page - 1) * per_page

    # Get products and total count
    products, total = product_service.list_products(
        db,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=per_page,
    )

    # Calculate pagination metadata
    total_pages = math.ceil(total / per_page) if total > 0 else 1

    # Convert products to JSON:API resources
    product_resources = [build_product_resource(p) for p in products]

    # Build response
    return ProductListResponse(
        data=product_resources,
        meta=JSONAPIMeta(
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        ),
        links=build_pagination_links(request, page, per_page, total_pages)
    )


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get a single product by ID.

    **Example:**
    `GET /api/v1/products/550e8400-e29b-41d4-a716-446655440000`

    Returns 404 if product not found or not active.
    """
    product = product_service.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found"
        )

    return ProductResponse(
        data=build_product_resource(product)
    )