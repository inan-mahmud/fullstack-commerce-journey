# Session 5: Product APIs with JSON:API Format & UUID Migration

**Date:** 2026-05-06
**Phase:** Phase 1 - Project Setup & Core Commerce
**Step:** Step 1.3 - Core Product APIs

---

## 🎯 What We Built Today

A fully functional Product API system with:
- ✅ **JSON:API response format** (industry standard)
- ✅ **UUID primary keys** (production-ready)
- ✅ **Recursive category filtering** (Option A - includes subcategories)
- ✅ **Advanced filtering & search**
- ✅ **Pagination with metadata**
- ✅ **13 test products across 8 categories**

---

## 📋 Major Decisions Made

### Decision 1: JSON:API Response Structure ✅

**You chose:** Full JSON:API format from the start

**Structure:**
```json
{
  "data": [{
    "id": "uuid",
    "type": "product",
    "attributes": { ... },
    "relationships": { ... }
  }],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20,
    "total_pages": 5
  },
  "links": {
    "self": "...",
    "first": "...",
    "next": "...",
    "last": "...",
    "prev": null
  }
}
```

**Benefits:**
- Industry standard (Netflix, Shopify use it)
- Self-documenting
- Consistent across all endpoints
- Frontend-friendly
- Better for learning

---

### Decision 2: UUID vs Integer for IDs ✅

**You chose:** UUID primary keys

#### Trade-offs Analysis:

| Aspect | Integer | UUID |
|--------|---------|------|
| **Storage** | 4 bytes ✅ | 16 bytes ❌ |
| **Performance** | Faster ✅ | ~20% slower ❌ |
| **Security** | Enumerable ❌ | Non-guessable ✅ |
| **Privacy** | Exposes counts ❌ | Obscured ✅ |
| **Distributed** | Needs coordination ❌ | Independent ✅ |
| **Human-readable** | Easy ✅ | Hard ❌ |
| **URL Length** | Short ✅ | Long ❌ |
| **Merging DBs** | Conflicts ❌ | No conflicts ✅ |

**Why UUID wins for e-commerce:**
1. **Security:** Can't enumerate users/orders
2. **Privacy:** Doesn't reveal business metrics
3. **Distributed systems:** Ready for microservices (Phase 6)
4. **Future-proof:** Easier to scale later
5. **Learning value:** Shows understanding of production systems

**Implementation:**
```python
from sqlalchemy.dialects.postgresql import UUID
import uuid

id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
```

---

### Decision 3: Category Filtering - Option A ✅

**You chose:** Always include subcategories (Option A)

**How it works:**
```
Electronics (UUID: ca2b...)
├── Mobile Phones (50 products)
│   ├── Android (30 products)
│   └── iOS (20 products)
└── Laptops (40 products)
```

**Query:** `/api/v1/products?category_id=ca2b...`
**Returns:** 90 products (Mobile + Android + iOS + Laptops)

**Implementation:** Recursive SQL CTE
```sql
WITH RECURSIVE category_tree AS (
    SELECT id FROM categories WHERE id = :category_id
    UNION ALL
    SELECT c.id FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM products WHERE category_id IN (SELECT id FROM category_tree)
```

**Why Option A?**
- ✅ Intuitive UX (users expect to see all electronics)
- ✅ No empty parent categories
- ✅ Progressive filtering (Electronics → Mobile → Android)
- ❌ Slower query (recursive CTE)
- ❌ Can't get exact category only (will add `include_subcategories` param in Phase 4)

---

## 🏗️ Architecture Implemented

### File Structure Created:

```
app/
├── schemas/
│   ├── common.py           # JSON:API helpers (Links, Meta, Relationships)
│   ├── product.py          # Product schemas
│   ├── category.py         # Category schemas
│   └── __init__.py
├── services/
│   ├── product_service.py  # Product business logic with recursive CTE
│   ├── category_service.py # Category business logic
│   └── __init__.py
├── api/
│   ├── deps.py             # get_db dependency
│   └── v1/
│       ├── products.py     # Product endpoints
│       ├── categories.py   # Category endpoints
│       └── __init__.py
├── models/                 # ALL updated to UUID
│   ├── user.py             # ✅ UUID
│   ├── category.py         # ✅ UUID + self-referential FK
│   ├── product.py          # ✅ UUID
│   ├── cart.py             # ✅ UUID
│   ├── cart_item.py        # ✅ UUID
│   ├── order.py            # ✅ UUID
│   └── order_item.py       # ✅ UUID
└── main.py                 # ✅ Routers included

scripts/
└── seed_data.py            # Test data generator

alembic/
└── versions/
    └── f878e4ff8b53_initial_migration_with_uuid_primary_keys.py
```

---

## 🔌 API Endpoints Built

### Products

**`GET /api/v1/products`** - List products with filters

Query Parameters:
- `search` - Search in name & description
- `category_id` - Filter by category (includes subcategories!)
- `min_price` / `max_price` - Price range
- `in_stock` - Only show available products
- `sort_by` - name, price, created_at
- `order` - asc, desc
- `page` / `per_page` - Pagination (default: 20, max: 100)

Examples:
```bash
# All products
GET /api/v1/products

# Search
GET /api/v1/products?search=iphone

# Category (with subcategories)
GET /api/v1/products?category_id=ca2b2648-...

# Price range
GET /api/v1/products?min_price=1000&max_price=2000

# In stock only
GET /api/v1/products?in_stock=true

# Sort by price ascending
GET /api/v1/products?sort_by=price&order=asc

# Combined filters
GET /api/v1/products?search=pro&category_id=ca2b...&min_price=1000
```

**`GET /api/v1/products/{id}`** - Get single product

---

### Categories

**`GET /api/v1/categories`** - List all categories

**`GET /api/v1/categories/{id}`** - Get single category

---

## 🧪 Test Results

All tests passed! ✅

### Test 1: List Products (Pagination)
```bash
curl "http://localhost:8000/api/v1/products?per_page=3"
```
**Result:** ✅ Returned 3 products with pagination metadata

### Test 2: Category Filter (Option A - with subcategories)
```bash
curl "http://localhost:8000/api/v1/products?category_id=ca2b2648-..."
```
**Result:** ✅ Returned 9 products (Android + iOS + Laptops)

### Test 3: Search
```bash
curl "http://localhost:8000/api/v1/products?search=iphone"
```
**Result:** ✅ Returned 3 iPhones

### Test 4: Price Range
```bash
curl "http://localhost:8000/api/v1/products?min_price=1000&max_price=2000"
```
**Result:** ✅ Returned 3 products ($1199, $1499, $1799)

### Test 5: In Stock + Sort
```bash
curl "http://localhost:8000/api/v1/products?in_stock=true&sort_by=price&order=asc"
```
**Result:** ✅ Returned 12 products sorted by price (excluded out-of-stock iPhone 14)

### Test 6: Combined Filters
```bash
curl "http://localhost:8000/api/v1/products?search=pro&category_id=ca2b...&min_price=1000"
```
**Result:** ✅ Returned 2 products (iPhone 15 Pro Max, MacBook Pro 16")

---

## 📊 Test Data Created

**8 Categories:**
- Electronics
  - Mobile Phones
    - Android
    - iOS
  - Laptops
- Clothing
  - Men's Clothing
  - Women's Clothing

**13 Products:**
- 3 Android phones ($699-$999)
- 3 iOS phones ($799-$1199)
- 3 Laptops ($1499-$2499)
- 4 Clothing items ($19-$49)

**Product Distribution:**
- Android: 3 products
- iOS: 3 products (including 1 out-of-stock)
- Laptops: 3 products
- Men's Clothing: 2 products
- Women's Clothing: 2 products

---

## 🎓 Key Concepts Learned

### 1. JSON:API Standard

**Structure:**
```json
{
  "data": {
    "id": "...",
    "type": "product",
    "attributes": { ... },
    "relationships": { ... }
  },
  "meta": { ... },
  "links": { ... }
}
```

**Benefits:**
- Standardized format
- Self-describing
- Relationship management
- Pagination support

---

### 2. Recursive SQL CTE (Common Table Expression)

**Purpose:** Get all descendant categories

```sql
WITH RECURSIVE category_tree AS (
    -- Base case
    SELECT id FROM categories WHERE id = :category_id

    UNION ALL

    -- Recursive case
    SELECT c.id
    FROM categories c
    INNER JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT id FROM category_tree
```

**Why it's powerful:**
- Single database query
- Database does the recursion
- Efficient for hierarchical data
- Supports arbitrary depth

---

### 3. SQLAlchemy Best Practices

**N+1 Query Prevention:**
```python
query = db.query(Product).options(joinedload(Product.category))
```

Without `joinedload`:
```
SELECT * FROM products;        -- 1 query
SELECT * FROM categories WHERE id = 1;  -- Query per product
SELECT * FROM categories WHERE id = 2;  -- N queries!
```

With `joinedload`:
```
SELECT * FROM products
LEFT JOIN categories ON products.category_id = categories.id;  -- 1 query!
```

**Dynamic Query Building:**
```python
filters = []
if search:
    filters.append(Product.name.ilike(f"%{search}%"))
if category_id:
    filters.append(Product.category_id.in_(category_ids))

query = query.filter(and_(*filters))
```

---

### 4. Pydantic with SQLAlchemy

**Configuration:**
```python
class ProductAttributes(BaseModel):
    name: str
    price: Decimal
    # ...

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)
        json_encoders = {
            Decimal: str  # Prevent precision loss in JSON
        }
```

**Usage:**
```python
product_model = db.query(Product).first()  # SQLAlchemy model
product_schema = ProductAttributes.from_orm(product_model)  # Pydantic model
```

---

### 5. FastAPI Dependency Injection

**Define dependency:**
```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Use in route:**
```python
@router.get("/products")
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products
```

**Benefits:**
- Automatic resource cleanup
- Reusable across routes
- Easy to test (mock dependencies)

---

### 6. Pagination Math

```python
# Calculate offset
skip = (page - 1) * per_page

# Example: page=3, per_page=20
# skip = (3 - 1) * 20 = 40

# Calculate total pages
total_pages = math.ceil(total_count / per_page)

# Example: 97 products, 20 per page
# total_pages = ceil(97 / 20) = 5
```

---

## 🚀 Performance Considerations

### What We Optimized:

1. **Eager Loading (joinedload)**
   - Prevents N+1 queries
   - Loads category with products in 1 query

2. **Database Indexes**
   - `ix_products_category_id` - for category filtering
   - `ix_products_name` - for search
   - `ix_products_is_active` - for active filter
   - `ix_products_slug` - for slug lookups

3. **Query Optimization**
   - Count query separate from data query
   - Only fetch requested page of data
   - Filter before sorting and pagination

### What We'll Optimize Later (Phase 4):

1. **Caching**
   - Redis cache for product list
   - Category tree caching
   - Cache invalidation on updates

2. **Full-text Search**
   - PostgreSQL `ts_vector` for better search
   - Search ranking
   - Typo tolerance

3. **Database Optimization**
   - Connection pooling
   - Read replicas
   - Query performance monitoring

---

## 🐛 Edge Cases Handled

1. **Empty Results**
   - Returns empty array with total=0
   - total_pages=1 (not 0)

2. **Out of Bounds Page**
   - page > total_pages returns empty results
   - Links still generated correctly

3. **Out of Stock Products**
   - Included by default
   - Excluded with `in_stock=true` filter

4. **Inactive Products**
   - Always excluded from public API
   - is_active filter is automatic

5. **Invalid UUID**
   - FastAPI validates UUID format
   - Returns 422 Unprocessable Entity

6. **Product Not Found**
   - Returns 404 with clear message
   - No stack trace exposed

---

## 🔒 Security Improvements from UUID

**Before (Integer IDs):**
```
GET /api/v1/products/1
GET /api/v1/products/2
GET /api/v1/products/3
→ Attacker can scrape all products
→ Can estimate business metrics
```

**After (UUID):**
```
GET /api/v1/products/ca66347d-0a23-400d-a791-a9c5909e6a19
GET /api/v1/products/??? (can't guess)
→ Enumeration impossible
→ Business metrics hidden
```

---

## 📖 Code Quality Highlights

### 1. Separation of Concerns

- **Models:** Database structure
- **Schemas:** API contract (request/response)
- **Services:** Business logic
- **Routes:** HTTP handling

### 2. Type Safety

```python
def list_products(
    db: Session,
    search: Optional[str] = None,
    category_id: Optional[UUID] = None,  # Type-safe!
    min_price: Optional[Decimal] = None,
) -> Tuple[List[Product], int]:  # Return type declared
    ...
```

### 3. Documentation

- Docstrings on all functions
- Route descriptions in FastAPI
- Query parameter descriptions
- Example usage in docs

### 4. Error Handling

```python
if not product:
    raise HTTPException(
        status_code=404,
        detail=f"Product with id {product_id} not found"
    )
```

---

## 🎯 Next Steps (Phase 1, Step 1.4)

Now that we have Product APIs, next we'll build:

**Step 1.4: Shopping Cart Implementation**

Endpoints to create:
```
POST   /api/v1/cart/items        - Add item to cart
GET    /api/v1/cart              - Get current cart
PUT    /api/v1/cart/items/{id}   - Update quantity
DELETE /api/v1/cart/items/{id}   - Remove item
DELETE /api/v1/cart              - Clear cart
```

**What you'll learn:**
- Session management (guest users)
- Cart merging (guest → authenticated)
- State management
- JSON:API for create/update operations

---

## 💡 What You Accomplished Today

1. ✅ **Migrated entire database to UUID** (7 models updated)
2. ✅ **Implemented JSON:API standard** (production-ready format)
3. ✅ **Built recursive category filtering** (SQL CTE - Option A)
4. ✅ **Created advanced filtering system** (search, price, stock, sort)
5. ✅ **Implemented pagination** (with metadata and links)
6. ✅ **Wrote reusable service layer** (business logic separation)
7. ✅ **Tested all endpoints** (6 different filter combinations)
8. ✅ **Seeded test data** (8 categories, 13 products)

---

## 🏆 Skills Gained

**Backend Engineering:**
- JSON:API implementation
- UUID vs Integer trade-offs
- Recursive SQL queries (CTE)
- N+1 query prevention
- Dynamic query building

**Architecture:**
- Service layer pattern
- Dependency injection
- Separation of concerns
- Type-safe APIs

**Database:**
- UUID primary keys
- Recursive CTEs
- Query optimization
- Eager loading

**API Design:**
- RESTful endpoints
- Pagination patterns
- Filter composition
- Response standardization

---

## 📝 Homework (Optional Thinking)

Before Step 1.4 (Shopping Cart), think about:

1. **Guest Cart Tracking:**
   - How do we identify a guest user?
   - Cookie? Header? Session ID?
   - How long should guest carts persist?

2. **Cart Merging:**
   - Guest adds 2x iPhone to cart
   - Then logs in
   - Already has 1x iPhone in their user cart
   - Final result: 3x iPhone or 2x iPhone? (Override vs Add)

3. **Cart Expiry:**
   - Guest cart: 7 days?
   - User cart: 30 days?
   - Background job to clean expired carts?

Think about these! We'll discuss before implementing. 🚀

---

**Status:** ✅ Step 1.3 Complete - Product APIs with JSON:API format fully functional

**Next Session:** Step 1.4 - Shopping Cart Implementation