# Session 6: Shopping Cart - Planning Phase

**Date:** 2026-05-06
**Phase:** Phase 1 - Project Setup & Core Commerce
**Step:** Step 1.4 - Shopping Cart Implementation (Planning)

---

## 📝 Session Overview

This was a **continuation session** where we:
1. ✅ Reviewed previous session's accomplishments (Session 5)
2. ✅ Identified next task from PROJECT_PLAN.md (Step 1.4: Shopping Cart)
3. ✅ Prepared design questions for cart implementation

**Session Type:** Planning & Design Discussion (No Implementation)

---

## 🎯 What We Did Today

### 1. Context Restoration

The conversation was continued from a previous session that ran out of context. I received a comprehensive summary of Session 5 which included:

**Session 5 Accomplishments:**
- ✅ Full JSON:API response format implemented
- ✅ UUID migration completed across 7 models
- ✅ Recursive category filtering (Option A - includes subcategories)
- ✅ Product listing with advanced filters (search, price range, stock, sort)
- ✅ Pagination with metadata and links
- ✅ 8 categories and 13 test products seeded
- ✅ All endpoints tested successfully

**Files Modified in Session 5:**
- All model files (user.py, category.py, product.py, cart.py, cart_item.py, order.py, order_item.py)
- New schemas (common.py, product.py, category.py)
- New services (product_service.py, category_service.py)
- New API routes (products.py, categories.py)
- Migration regenerated with UUID

---

### 2. Next Task Identification

User asked: "what's our next task? check the documents"

I identified from PROJECT_PLAN.md:
- ✅ Step 1.1: Project Setup (completed)
- ✅ Step 1.2: Database Design (completed)
- ✅ Step 1.3: Core Product APIs (completed in Session 5)
- ⏭️ **Step 1.4: Shopping Cart Implementation** (next)

---

### 3. Cart Design Questions Prepared

Following the mentoring strategy of asking thought-provoking questions before implementation, I prepared 5 key design questions:

#### Question 1: Guest Cart Identification
**Options presented:**
- **Option A**: Cookie-based (set a session_id cookie)
- **Option B**: Header-based (client sends X-Session-ID header)
- **Option C**: Hybrid (support both)

**Trade-offs discussed:**
- Cookies: Automatic, browser handles it, works across requests
- Headers: More explicit, better for mobile apps, requires client implementation
- Security: Should session_id be a simple UUID or a signed token?

---

#### Question 2: Cart Merging Strategy

**Scenario presented:**
```
Guest cart: 2x iPhone 15 Pro, 1x AirPods
User cart (from previous session): 1x iPhone 15 Pro, 1x MacBook Pro
```

**Options:**
- **Option A**: Add quantities (3x iPhone 15 Pro, 1x AirPods, 1x MacBook Pro)
- **Option B**: Override with guest cart (2x iPhone 15 Pro, 1x AirPods) - lose user cart
- **Option C**: Ask user via API response (return conflict, let frontend decide)

---

#### Question 3: Cart Expiry

**Questions to consider:**
- Guest carts: 7 days? 30 days? Never expire?
- User carts: 30 days? 90 days? Never expire?
- Should we implement background cleanup now or in Phase 4?

---

#### Question 4: Stock Validation

**Options:**
- **Option A**: Check stock immediately, reject if insufficient
- **Option B**: Allow adding any quantity, validate at checkout
- **Option C**: Check stock but allow overselling with warning

---

#### Question 5: API Response Format (JSON:API)

**Option A - Embedded products (simpler):**
```json
{
  "data": {
    "id": "cart-uuid",
    "type": "cart",
    "attributes": {
      "items": [
        {
          "id": "item-uuid",
          "product_id": "product-uuid",
          "product_name": "iPhone 15 Pro",
          "quantity": 2,
          "price": "1199.99",
          "subtotal": "2399.98"
        }
      ],
      "total": "2399.98"
    }
  }
}
```

**Option B - Relationships with included resources (more JSON:API compliant):**
```json
{
  "data": {
    "id": "cart-uuid",
    "type": "cart",
    "relationships": {
      "items": {
        "data": [{"id": "item-uuid", "type": "cart_item"}]
      }
    }
  },
  "included": [
    {
      "id": "item-uuid",
      "type": "cart_item",
      "attributes": {...},
      "relationships": {
        "product": {"data": {"id": "product-uuid", "type": "product"}}
      }
    },
    {
      "id": "product-uuid",
      "type": "product",
      "attributes": {...}
    }
  ]
}
```

**Trade-off:** Option A is simpler and easier to consume, Option B is more JSON:API compliant but verbose.

---

## 📋 Endpoints to Implement (Step 1.4)

According to PROJECT_PLAN.md, we need to build:

```
POST   /api/v1/cart/items        - Add item to cart
GET    /api/v1/cart              - Get current cart
PUT    /api/v1/cart/items/{id}   - Update quantity
DELETE /api/v1/cart/items/{id}   - Remove item
DELETE /api/v1/cart              - Clear cart
```

**Learning Objectives:**
- Session management (guest users)
- Cart merging (guest → authenticated)
- State management
- JSON:API for create/update operations

---

## 🎓 Key Concepts to Learn (Next Session)

When we implement shopping cart, we'll learn:

### 1. Session Management
- Cookie vs Header-based identification
- Session ID generation and storage
- Session expiry and cleanup

### 2. State Management
- Guest cart tracking
- User cart persistence
- Cart merging logic

### 3. JSON:API for Mutations
- POST request format
- PUT request format
- DELETE responses
- Error responses in JSON:API

### 4. Business Logic
- Stock validation
- Quantity updates
- Price calculations
- Cart totals

### 5. Database Transactions
- Atomic cart operations
- Race condition handling
- Optimistic locking (if needed)

---

## 🗂️ Existing Database Models (Already Implemented)

From Session 4, we already have cart models:

**app/models/cart.py**
```python
class Cart(Base):
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    session_id = Column(String, nullable=True, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Check constraint: either user_id or session_id must be set
    __table_args__ = (
        CheckConstraint(
            "(session_id IS NOT NULL AND user_id IS NULL) OR "
            "(session_id IS NULL AND user_id IS NOT NULL)",
            name="check_cart_owner"
        ),
    )

    # Relationships
    user = relationship("User", back_populates="carts")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
```

**app/models/cart_item.py**
```python
class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id", ondelete="CASCADE"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Composite unique constraint: one product per cart
    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cart_product"),
    )

    # Relationships
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
```

**Key Features Already in Models:**
- ✅ UUID primary keys
- ✅ Guest support (session_id) and user support (user_id)
- ✅ Check constraint (exactly one of user_id or session_id)
- ✅ Composite unique constraint (one product per cart)
- ✅ Cascade delete (deleting cart deletes items)
- ✅ Timestamps (created_at, updated_at)

---

## 📖 Session Summary

**What Happened:**
1. User returned to continue from previous session
2. I provided context summary of Session 5 accomplishments
3. User asked: "what's our next task? check the documents"
4. I identified Step 1.4: Shopping Cart Implementation
5. I prepared 5 design questions for cart implementation
6. User said: "I'll go out now. create conversation summary"

**Current Status:**
- ✅ Session 5 completed: Product APIs with JSON:API
- ✅ Session 6: Planning phase for shopping cart
- ⏭️ Next session: User will answer design questions, then we implement cart

**No Code Written:** This session was purely planning and design discussion.

**No Implementation Yet:** Waiting for user to return and answer design questions before implementing.

---

## 🎯 Next Session Plan

When user returns, we'll:

1. **Discuss Design Questions**
   - Get user's answers on 5 design questions
   - Explain trade-offs for each decision
   - Document final decisions

2. **Implementation Plan**
   - Create cart schemas (CartResource, CartItemResource, etc.)
   - Create cart service (cart_service.py)
   - Create cart API routes (app/api/v1/cart.py)
   - Implement session management
   - Test all endpoints

3. **Testing**
   - Test guest cart (cookie/header)
   - Test adding items
   - Test updating quantities
   - Test removing items
   - Test clearing cart
   - Test cart merging on login (if implemented)

---

## 💡 Key Decisions to Make (Next Session)

User needs to decide on:

1. **Session ID Method**: Cookie, Header, or Hybrid?
2. **Cart Merging**: Add quantities, Override, or Ask user?
3. **Cart Expiry**: 7/30/90 days? Background job now or later?
4. **Stock Validation**: Immediate reject, Allow and validate at checkout, or Allow with warning?
5. **Response Format**: Embedded (Option A) or Relationships (Option B)?

---

## 📚 Homework (For User's Return)

Think about these real-world scenarios:

**Scenario 1: Guest Cart**
- User browses products
- Adds 2x iPhone to cart (no login)
- Closes browser
- Opens browser next day
- Should cart still be there? For how long?

**Scenario 2: Login Merge**
- Guest adds 2x iPhone
- Logs in
- Already has 1x iPhone in user cart from last week
- What should happen? 3x total or 2x total?

**Scenario 3: Out of Stock**
- User adds 5x Product A to cart
- Product A only has 3 in stock
- Should we reject? Allow and warn? Or block until checkout?

**Scenario 4: Price Changes**
- User adds Product A to cart at $100
- Product price changes to $90
- User checks cart
- Show $100 (original) or $90 (current)?

Think about these! We'll discuss when you return. 🚀

---

**Status:** ✅ Session 6 Complete - Planning phase for shopping cart

**Next Session:** User answers design questions, then implementation begins

**Background Servers:** Still running (uvicorn processes)
- Background Bash 2d02df: uvicorn running on port 8000
- Background Bash 1f1acb: uvicorn running on port 8000 (duplicate?)

**Note:** May need to clean up duplicate background processes in next session.