# Session 4: Database Models Implementation

**Date:** 2026-05-04
**Phase:** Phase 1 - Project Setup & Core Commerce
**Step:** Step 1.2 - Database Design

---

## What We Built

Today we implemented all core database models for the e-commerce platform using SQLAlchemy ORM.

### Models Created

1. **User Model** (`app/models/user.py`)
   - Authentication fields (email, password_hash)
   - Profile information (full_name, phone)
   - Account status (is_active, is_verified)
   - Relationships to carts and orders

2. **Category Model** (`app/models/category.py`)
   - **Self-referential hierarchy** (parent_id)
   - Slug for URL-friendly names
   - Supports unlimited nesting depth
   - Added `full_path` property for breadcrumbs

3. **Product Model** (`app/models/product.py`)
   - Uses NUMERIC(10,2) for price precision
   - Stock tracking
   - Category association
   - Active status for soft deletes
   - Added helper properties: `is_available`, `price_decimal`

4. **Cart Model** (`app/models/cart.py`)
   - **Dual ownership**: session_id (guest) OR user_id (authenticated)
   - Database-level CHECK constraint ensures one or the other
   - Expiry timestamp management
   - Helper methods: `is_expired`, `is_guest_cart`, `calculate_total()`

5. **CartItem Model** (`app/models/cart_item.py`)
   - Links cart to product with quantity
   - UNIQUE constraint on (cart_id, product_id)
   - CASCADE delete when cart is removed
   - Subtotal calculation property

6. **Order Model** (`app/models/order.py`)
   - Order status enum (PENDING → CONFIRMED → SHIPPED → DELIVERED)
   - Supports both guest and registered users
   - Shipping address stored as JSON
   - Total amount snapshot
   - Helper properties: `is_cancellable`, `is_guest_order`

7. **OrderItem Model** (`app/models/order_item.py`)
   - **Snapshot pattern implementation**
   - Stores product_name and price_at_purchase
   - Preserves historical data even if product changes
   - Added `current_price_difference` property

---

## Key Design Patterns Learned

### 1. Self-Referential Foreign Key (Category Hierarchy)
```python
parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
parent = relationship("Category", remote_side=[id], backref="children")
```

**Use Case:** Build category trees like:
```
Electronics
├── Mobile Phones
│   ├── Android
│   └── iOS
└── Laptops
```

---

### 2. Mutually Exclusive Fields (Cart Ownership)
```python
# Database constraint
CheckConstraint(
    "(session_id IS NOT NULL AND user_id IS NULL) OR "
    "(session_id IS NULL AND user_id IS NOT NULL)",
    name="check_cart_owner"
)
```

**Why:** Ensures a cart belongs to either a guest OR a user, never both or neither.

---

### 3. Snapshot Pattern (Order Items)
```python
product_id = Column(Integer, ForeignKey("products.id"))  # For reference
product_name = Column(String, nullable=False)            # Snapshot
price_at_purchase = Column(Numeric(10, 2), nullable=False)  # Snapshot
```

**Why:**
- Product names can change → snapshot preserves original
- Prices fluctuate → snapshot shows what customer actually paid
- Products can be deleted → order history remains intact
- Legal/accounting requirement for accurate invoices

**Example:**
- Today: Buy "iPhone 15 Pro" for $999
- Tomorrow: Price changes to $1099, name changes to "iPhone 15 Pro (2024)"
- Your order still shows: "iPhone 15 Pro" at $999 ✅

---

### 4. NUMERIC vs FLOAT for Money
```python
price = Column(Numeric(10, 2), nullable=False)  # ✅ Correct
# price = Column(Float, nullable=False)         # ❌ Never use for money!
```

**Why:**
- FLOAT: 19.99 might be stored as 19.98999999... (precision errors)
- NUMERIC(10,2): 19.99 is stored exactly as 19.99
- Critical for financial calculations!

---

### 5. Cascade Deletes
```python
# On Cart model
items = relationship("CartItem", cascade="all, delete-orphan")

# On CartItem foreign key
cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"))
```

**Behavior:**
- When a cart is deleted → all its cart_items are automatically deleted
- Prevents orphaned records in cart_items table
- Database-level enforcement for data integrity

---

## Alembic Migration Setup

### What We Did:

1. **Initialized Alembic:**
```bash
alembic init alembic
```

2. **Configured env.py:**
   - Imported all models so Alembic can detect them
   - Set database URL from environment variables
   - Configured `target_metadata = Base.metadata`

3. **Generated migration:**
```bash
alembic revision --autogenerate -m "Initial migration - create all core tables"
```

4. **Applied migration:**
```bash
alembic upgrade head
```

### Tables Created:
- users
- categories (with self-referential FK)
- products
- carts (with CHECK constraint)
- cart_items (with UNIQUE constraint)
- orders (with ENUM status)
- order_items (with snapshot fields)
- alembic_version (migration tracking)

---

## Database Schema Verification

Verified the following in PostgreSQL:

1. ✅ All 8 tables created successfully
2. ✅ Foreign key constraints in place
3. ✅ Indexes created on all indexed columns
4. ✅ Check constraint on carts.check_cart_owner
5. ✅ Unique constraint on cart_items(cart_id, product_id)
6. ✅ CASCADE delete on cart_items and order_items
7. ✅ NUMERIC(10,2) precision for money fields
8. ✅ Enum type for order status

---

## Important Concepts Discussed

### Q: Why does Category have parent_id?
**A:** Enables category hierarchy/tree structure. Example: Electronics > Mobile > Android

### Q: Why do we need both session_id AND user_id in Cart?
**A:**
- session_id: For guest users (tracked by cookie)
- user_id: For authenticated users
- On login: merge guest cart into user cart

### Q: Why duplicate data in OrderItem (product_name, price)?
**A:** **Snapshot pattern** - preserves historical accuracy:
- Product prices change over time
- Product names can be updated
- Products can be deleted
- But order history must show what was ACTUALLY purchased at THAT price

### Q: Why NUMERIC instead of FLOAT for prices?
**A:** FLOAT has precision errors. $19.99 might become $19.989999... in calculations.
NUMERIC stores exact decimal values - critical for money!

---

## File Structure Created

```
app/
├── models/
│   ├── __init__.py          # Exports all models
│   ├── user.py              # User model
│   ├── category.py          # Category with hierarchy
│   ├── product.py           # Product catalog
│   ├── cart.py              # Shopping cart (guest + user)
│   ├── cart_item.py         # Cart item junction table
│   ├── order.py             # Order with status enum
│   └── order_item.py        # Order item with snapshots

alembic/
├── versions/
│   └── e7ea1dd35214_initial_migration_create_all_core_tables.py
├── env.py                   # Configured for our models
└── script.py.mako

alembic.ini                  # Alembic configuration
```

---

## SQLAlchemy Patterns Used

### 1. Relationships
```python
# One-to-Many
category = relationship("Category", back_populates="products")
products = relationship("Product", back_populates="category")

# Self-referential
parent = relationship("Category", remote_side=[id], backref="children")

# One-to-Many with cascade
items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
```

### 2. Timestamps with Defaults
```python
created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

### 3. Indexes
```python
email = Column(String, unique=True, index=True, nullable=False)  # Unique index
name = Column(String, index=True, nullable=False)                # Regular index
```

### 4. Foreign Keys with Constraints
```python
cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
```

### 5. Check Constraints
```python
__table_args__ = (
    CheckConstraint("condition", name="constraint_name"),
)
```

### 6. Unique Constraints
```python
__table_args__ = (
    UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),
)
```

---

## Next Steps (Phase 1, Step 1.3)

Now that we have the database models, the next step is to:

1. **Create Pydantic schemas** (for request/response validation)
2. **Build Product APIs:**
   - GET /api/v1/products (list with pagination, filtering)
   - GET /api/v1/products/{id} (product details)
   - GET /api/v1/categories (category tree)
   - POST /api/v1/admin/products (create - admin only)
   - PUT /api/v1/admin/products/{id} (update - admin only)
   - DELETE /api/v1/admin/products/{id} (delete - admin only)

3. **Learn:**
   - Pydantic for request/response validation
   - FastAPI route creation
   - Query parameters (pagination, filtering, search)
   - Database querying with SQLAlchemy
   - Error handling and HTTP status codes

---

## Key Takeaways

1. **Design before coding:** We discussed the "why" behind each design decision before implementation
2. **Data integrity:** Database constraints (CHECK, UNIQUE, FK) enforce business rules at the DB level
3. **Money handling:** Always use NUMERIC/DECIMAL, never FLOAT for currency
4. **Historical accuracy:** Snapshot pattern preserves data even when source changes
5. **Cascade operations:** Use carefully to maintain referential integrity
6. **Alembic migrations:** Track database changes over time, enable collaboration

---

**Status:** ✅ Step 1.2 Complete - All core database models implemented and migrated

**Next Session:** Step 1.3 - Core Product APIs
