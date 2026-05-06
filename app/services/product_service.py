"""
Product service - Business logic for product operations.

This service handles complex product queries including:
- Recursive category filtering (Option A: always include subcategories)
- Full-text search
- Price range filtering
- Stock filtering
- Pagination
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, text
from typing import Optional, List, Tuple
from decimal import Decimal
from uuid import UUID

from app.models.product import Product
from app.models.category import Category


def get_descendant_category_ids(category_id: UUID, db: Session) -> List[UUID]:
    """
    Get all descendant category IDs using recursive SQL CTE.

    This implements Option A: always include subcategories.

    Example:
    - Input: Electronics (id=5)
    - Output: [5, 10, 11, 12, 20, 21, 22] (Electronics + all subcategories)

    Uses PostgreSQL recursive CTE for performance:
    WITH RECURSIVE category_tree AS (
        SELECT id FROM categories WHERE id = :category_id
        UNION ALL
        SELECT c.id FROM categories c
        INNER JOIN category_tree ct ON c.parent_id = ct.id
    )
    SELECT id FROM category_tree

    Args:
        category_id: UUID of the parent category
        db: Database session

    Returns:
        List of UUIDs including the parent and all descendants
    """
    # Recursive CTE query
    cte_query = text("""
        WITH RECURSIVE category_tree AS (
            -- Base case: start with the given category
            SELECT id FROM categories WHERE id = :category_id

            UNION ALL

            -- Recursive case: find all children
            SELECT c.id
            FROM categories c
            INNER JOIN category_tree ct ON c.parent_id = ct.id
        )
        SELECT id FROM category_tree
    """)

    result = db.execute(cte_query, {"category_id": str(category_id)})
    category_ids = [row[0] for row in result]

    return category_ids


def list_products(
    db: Session,
    *,
    # Search
    search: Optional[str] = None,
    # Filters
    category_id: Optional[UUID] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    in_stock: Optional[bool] = None,
    # Sorting
    sort_by: str = "created_at",
    order: str = "desc",
    # Pagination
    skip: int = 0,
    limit: int = 20,
) -> Tuple[List[Product], int]:
    """
    List products with filtering, searching, sorting, and pagination.

    This function builds a dynamic query based on provided filters.

    Args:
        db: Database session
        search: Search term (searches in name and description)
        category_id: Filter by category (includes subcategories - Option A)
        min_price: Minimum price filter
        max_price: Maximum price filter
        in_stock: If True, only show products with stock > 0
        sort_by: Field to sort by (name, price, created_at)
        order: Sort order (asc, desc)
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return

    Returns:
        Tuple of (products_list, total_count)
    """
    # Base query with eager loading of category relationship
    # joinedload prevents N+1 query problem
    query = db.query(Product).options(joinedload(Product.category))

    # Build filter conditions
    filters = []

    # 1. Category filter (with subcategories - Option A)
    if category_id:
        # Get all descendant category IDs using recursive CTE
        category_ids = get_descendant_category_ids(category_id, db)
        filters.append(Product.category_id.in_(category_ids))

    # 2. Search filter (name and description)
    if search:
        search_term = f"%{search}%"
        filters.append(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )

    # 3. Price range filters
    if min_price is not None:
        filters.append(Product.price >= min_price)

    if max_price is not None:
        filters.append(Product.price <= max_price)

    # 4. Stock filter
    if in_stock:
        filters.append(Product.stock > 0)

    # 5. Always show only active products (unless explicitly requested otherwise)
    filters.append(Product.is_active == True)

    # Apply all filters
    if filters:
        query = query.filter(and_(*filters))

    # Get total count before pagination
    total = query.count()

    # Sorting
    sort_column = getattr(Product, sort_by, Product.created_at)
    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Pagination
    products = query.offset(skip).limit(limit).all()

    return products, total


def get_product_by_id(db: Session, product_id: UUID) -> Optional[Product]:
    """
    Get a single product by ID.

    Args:
        db: Database session
        product_id: Product UUID

    Returns:
        Product object or None if not found
    """
    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product_id, Product.is_active == True)
        .first()
    )


def get_product_by_slug(db: Session, slug: str) -> Optional[Product]:
    """
    Get a single product by slug (URL-friendly identifier).

    Args:
        db: Database session
        slug: Product slug

    Returns:
        Product object or None if not found
    """
    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.slug == slug, Product.is_active == True)
        .first()
    )
