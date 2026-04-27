# E-Commerce Backend Learning Project - Master Plan

## Project Overview
Build a production-grade e-commerce backend system using FastAPI, PostgreSQL, Redis, and Docker while learning backend engineering fundamentals through hands-on implementation.

**Learning Goals:**
- API design (FastAPI)
- Database design (PostgreSQL)
- Caching strategies (Redis)
- System design (monolith → microservices ready)
- Load balancing & scaling
- Background jobs & queues
- Docker & deployment
- Observability (logging, monitoring)
- Performance optimization

**Project Type:** Single-vendor E-commerce Platform (scalable to multi-vendor)

**Timeline:** 7+ weeks (1-3 hours/day)

---

## Phase 1: Project Setup & Core Commerce (Week 1-2)

### Step 1.1: Project Structure & Environment Setup

**What we'll create:**
```
backend_study/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── user.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── user.py
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── products.py
│   │       ├── categories.py
│   │       ├── cart.py
│   │       ├── orders.py
│   │       ├── auth.py
│   │       └── admin.py
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── product_service.py
│   │   ├── cart_service.py
│   │   ├── order_service.py
│   │   └── email_service.py
│   └── utils/                  # Helpers
│       ├── __init__.py
│       └── security.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
├── alembic/                    # Database migrations
│   └── versions/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── alembic.ini
├── README.md
└── PROJECT_PLAN.md (this file)
```

**Dependencies to install:**
- fastapi
- uvicorn[standard]
- sqlalchemy
- psycopg2-binary
- alembic
- pydantic-settings
- python-jose[cryptography]
- passlib[bcrypt]
- python-multipart
- redis
- celery
- pytest
- httpx

**You'll learn:**
- Project organization patterns
- Dependency management
- Environment variable configuration
- Separation of concerns (routes, services, models)

---

### Step 1.2: Database Design

**Core Entities:**

**1. Categories Table**
```sql
- id (UUID/Integer, PK)
- name (String, unique, indexed)
- slug (String, unique, indexed)
- parent_id (FK to categories.id, nullable)
- created_at (Timestamp)
- updated_at (Timestamp)
```

**2. Products Table**
```sql
- id (UUID/Integer, PK)
- name (String, indexed)
- slug (String, unique, indexed)
- description (Text)
- price (Decimal)
- stock (Integer)
- category_id (FK to categories.id)
- is_active (Boolean, default True)
- created_at (Timestamp)
- updated_at (Timestamp)
```

**3. Carts Table**
```sql
- id (UUID/Integer, PK)
- session_id (String, unique, indexed, nullable)
- user_id (FK to users.id, nullable, indexed)
- created_at (Timestamp)
- updated_at (Timestamp)
- expires_at (Timestamp)
```

**4. Cart Items Table**
```sql
- id (UUID/Integer, PK)
- cart_id (FK to carts.id)
- product_id (FK to products.id)
- quantity (Integer)
- created_at (Timestamp)
- updated_at (Timestamp)
- UNIQUE constraint on (cart_id, product_id)
```

**5. Orders Table**
```sql
- id (UUID/Integer, PK)
- order_number (String, unique, indexed)
- user_id (FK to users.id, nullable)
- email (String, indexed)
- phone (String)
- shipping_address (JSON/Text)
- status (Enum: pending, confirmed, shipped, delivered, cancelled)
- total_amount (Decimal)
- created_at (Timestamp)
- updated_at (Timestamp)
```

**6. Order Items Table**
```sql
- id (UUID/Integer, PK)
- order_id (FK to orders.id)
- product_id (FK to products.id)
- product_name (String) -- snapshot at purchase time
- quantity (Integer)
- price_at_purchase (Decimal) -- snapshot at purchase time
- created_at (Timestamp)
```

**You'll learn:**
- Relational database design
- Foreign key relationships
- Indexing strategies
- Data normalization
- Snapshot pattern (price/product name in order items)
- Soft deletes vs hard deletes
- Timestamps and audit fields

---

### Step 1.3: Core Product APIs

**Endpoints to build:**

```
GET    /api/v1/products              - List products (with pagination, filtering, search)
GET    /api/v1/products/{id}         - Get product details
GET    /api/v1/categories            - List categories (tree structure)
GET    /api/v1/categories/{id}       - Get category details
POST   /api/v1/admin/products        - Create product (admin only)
PUT    /api/v1/admin/products/{id}   - Update product (admin only)
DELETE /api/v1/admin/products/{id}   - Delete product (admin only)
```

**Query Parameters for Product Listing:**
- `page` (default: 1)
- `page_size` (default: 20, max: 100)
- `category_id` (filter by category)
- `search` (search in name and description)
- `min_price`, `max_price` (price range filter)
- `sort_by` (created_at, price, name)
- `order` (asc, desc)

**You'll learn:**
- RESTful API design principles
- Request validation with Pydantic
- Query parameter handling
- Pagination patterns (offset/limit)
- Filtering and searching
- Error handling and status codes
- Response schemas

---

### Step 1.4: Shopping Cart Implementation

**Endpoints to build:**

```
POST   /api/v1/cart/items            - Add item to cart
GET    /api/v1/cart                  - Get current cart
PUT    /api/v1/cart/items/{id}       - Update item quantity
DELETE /api/v1/cart/items/{id}       - Remove item from cart
DELETE /api/v1/cart                  - Clear cart
```

**Cart Logic:**
- Guest users: cart tracked by session_id (stored in cookie/header)
- Registered users: cart tracked by user_id
- On login: merge guest cart with user cart
- Cart expiry: 30 days for registered, 7 days for guests

**You'll learn:**
- Session management
- Cookie/header-based identification
- Cart merging logic
- State management (guest → authenticated)
- Cart persistence strategies

---

### Step 1.5: Checkout & Order Creation

**Endpoints to build:**

```
POST   /api/v1/checkout              - Create order from cart
GET    /api/v1/orders/{id}           - Get order details (guest: via email token, user: authenticated)
```

**Checkout Flow:**
1. Validate cart is not empty
2. Validate all products still exist and are active
3. Check stock availability (within transaction)
4. Calculate total amount
5. Create order and order items
6. Decrement product stock (atomic operation)
7. Clear cart
8. Send order confirmation email (synchronous for now)
9. Return order details

**Critical Concepts:**
- Database transactions (ACID)
- Stock validation race conditions
- Transaction isolation levels
- Rollback on failure
- Error handling (out of stock, payment failure, etc.)

**You'll learn:**
- Database transactions
- Race condition handling
- Atomic operations
- Transaction isolation
- Error recovery
- Email integration (SMTP)
- Order number generation

---

## Phase 2: Authentication & User Management (Week 3)

### Step 2.1: User Registration & Login

**Users Table:**
```sql
- id (UUID/Integer, PK)
- email (String, unique, indexed)
- password_hash (String)
- full_name (String)
- phone (String, nullable)
- is_active (Boolean, default True)
- is_verified (Boolean, default False)
- created_at (Timestamp)
- updated_at (Timestamp)
```

**Endpoints to build:**

```
POST   /api/v1/auth/register         - User registration
POST   /api/v1/auth/login            - User login (returns access + refresh token)
POST   /api/v1/auth/refresh          - Refresh access token
POST   /api/v1/auth/logout           - Logout (invalidate refresh token)
```

**JWT Token Strategy:**
- Access token: 15 minutes expiry
- Refresh token: 7 days expiry
- Store refresh tokens in database (for revocation)
- Include user_id in token payload

**You'll learn:**
- Password hashing (bcrypt)
- JWT token generation and validation
- Access vs refresh token pattern
- Token revocation strategies
- Security best practices (password strength, rate limiting)

---

### Step 2.2: Protected Routes & User Profile

**Endpoints to build:**

```
GET    /api/v1/users/me              - Get current user profile
PUT    /api/v1/users/me              - Update user profile
GET    /api/v1/users/me/orders       - Get user's order history
```

**Auth Dependency:**
- Create `get_current_user` dependency
- Extract and validate JWT from Authorization header
- Attach user to request context
- Handle token expiry, invalid tokens

**You'll learn:**
- FastAPI dependency injection
- Authentication middleware
- Authorization patterns
- Route protection
- User context management

---

### Step 2.3: Guest to Registered User Conversion

**Features to build:**
- On registration/login with existing guest email: link guest orders to user account
- On login: merge guest cart (session-based) with user cart

**Logic:**
```python
# On login:
1. Find guest cart by session_id
2. Find user cart by user_id
3. Merge items (sum quantities for duplicate products)
4. Delete guest cart
5. Update user cart

# On registration with email that has guest orders:
1. Find orders with matching email and null user_id
2. Update those orders to set user_id
```

**You'll learn:**
- Data migration patterns
- User account linking
- Guest to authenticated state transition
- Edge case handling

---

## Phase 3: Background Jobs & Admin Panel (Week 4-5)

### Step 3.1: Async Email with Celery

**Setup:**
- Install Celery + Redis
- Create `celery_app.py` configuration
- Create `tasks/` directory for background tasks

**Tasks to create:**
```python
@celery.task
def send_order_confirmation_email(order_id)
    - Fetch order details
    - Generate email template
    - Send via SMTP
    - Log success/failure
    - Retry on failure (max 3 retries, exponential backoff)

@celery.task
def send_order_status_update_email(order_id, new_status)
    - Fetch order details
    - Generate status update email
    - Send via SMTP
    - Retry logic
```

**Update checkout flow:**
- Replace synchronous email with: `send_order_confirmation_email.delay(order.id)`
- Email sent asynchronously, checkout doesn't wait

**Docker setup:**
- Add Redis service to docker-compose.yml
- Add Celery worker service to docker-compose.yml

**You'll learn:**
- Message queues (Redis as broker)
- Task workers (Celery)
- Asynchronous processing
- Retry strategies and exponential backoff
- Task monitoring
- Idempotent task design
- Failure handling

---

### Step 3.2: Admin Panel Setup

**Approach:** Use React Admin library (pre-built components)

**Frontend Setup:**
```bash
# Separate directory for admin frontend
admin-panel/
├── src/
│   ├── App.tsx
│   ├── dataProvider.ts       # FastAPI integration
│   ├── resources/
│   │   ├── products.tsx
│   │   ├── orders.tsx
│   │   └── categories.tsx
│   └── authProvider.ts
```

**Backend Requirements:**
- Add CORS middleware to FastAPI
- Create admin-specific endpoints
- Implement admin authentication (separate admin role/flag)

**Admin Features:**
- Product CRUD (Create, Read, Update, Delete)
- Order list and details
- Order status management
- Category management

**You'll learn:**
- React basics (components, hooks, state)
- TypeScript basics
- React Admin library
- CORS configuration
- Admin authentication patterns
- Frontend-backend integration

---

### Step 3.3: Order Status Management

**Order Status Flow:**
```
pending → confirmed → shipped → delivered
                  ↓
              cancelled (can cancel from pending/confirmed)
```

**Endpoints:**
```
PUT    /api/v1/admin/orders/{id}/status    - Update order status
GET    /api/v1/admin/orders/{id}/history   - Get status change history
```

**Order Status History Table:**
```sql
- id (PK)
- order_id (FK to orders.id)
- from_status (Enum)
- to_status (Enum)
- changed_by_user_id (FK to users.id, nullable)
- notes (Text, nullable)
- created_at (Timestamp)
```

**Logic:**
- Validate status transitions (e.g., can't go from delivered → pending)
- Record status change in history
- Trigger email notification task
- Return updated order

**You'll learn:**
- State machines
- Audit logging
- Event-driven architecture
- Status transition validation
- History tracking

---

## Phase 4: Caching & Performance (Week 6)

### Step 4.1: Redis Caching

**Cache Strategy: Cache-Aside Pattern**

**What to cache:**
1. Product catalog (product list by category)
2. Category tree
3. Individual product details
4. Product search results

**Implementation:**
```python
# Pseudo-code example
def get_products(category_id, page):
    cache_key = f"products:category:{category_id}:page:{page}"

    # Try cache first
    cached = redis.get(cache_key)
    if cached:
        return cached

    # Cache miss: fetch from DB
    products = db.query(Product).filter_by(category_id=category_id).all()

    # Store in cache with TTL
    redis.setex(cache_key, 300, products)  # 5 minutes

    return products
```

**Cache Invalidation:**
- On product create/update/delete: invalidate related caches
- Pattern-based invalidation (delete all keys matching `products:category:{id}:*`)

**You'll learn:**
- Caching patterns (cache-aside, write-through, write-behind)
- TTL (Time To Live) strategies
- Cache invalidation challenges
- Cache key design
- Cache stampede prevention
- Redis data structures

---

### Step 4.2: Database Optimization

**Indexes to add:**
```sql
-- Product search
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_slug ON products(slug);
CREATE INDEX idx_products_category_id ON products(category_id);

-- Order lookup
CREATE INDEX idx_orders_email ON orders(email);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- Cart lookup
CREATE INDEX idx_carts_session_id ON carts(session_id);
CREATE INDEX idx_carts_user_id ON carts(user_id);
```

**Query Optimization:**
- Use `select_related`/`joinedload` to avoid N+1 queries
- Add `EXPLAIN ANALYZE` to identify slow queries
- Optimize pagination with cursor-based approach for large datasets

**Monitoring:**
- Enable SQLAlchemy query logging
- Log queries taking > 100ms
- Create performance monitoring dashboard

**You'll learn:**
- Database indexing strategies
- Query optimization techniques
- N+1 query problem and solutions
- EXPLAIN plan analysis
- Database query profiling
- Eager loading vs lazy loading

---

### Step 4.3: API Performance

**Optimizations to implement:**

1. **Response Compression:**
   - Add GZip middleware to FastAPI
   - Compress responses > 1KB

2. **Pagination Optimization:**
   - Implement cursor-based pagination for large datasets
   - Add `Link` headers for pagination navigation

3. **Rate Limiting:**
   - Install `slowapi` library
   - Add rate limiting: 100 req/min per IP for public endpoints
   - 1000 req/min for authenticated users

4. **Request/Response Logging:**
   - Log all API requests with timing
   - Track slow endpoints (> 200ms)

5. **Connection Pooling:**
   - Configure SQLAlchemy connection pool
   - Set min/max pool size

**You'll learn:**
- Performance monitoring
- Rate limiting strategies
- Compression techniques
- Connection pooling
- API optimization best practices
- Logging and observability

---

## Phase 5: Advanced Features (Week 7+)

> **Note:** Phase 5 focuses on advanced features within the monolith. After completing Phase 5, you can optionally continue to **Phase 6: Polyglot Microservices Architecture** to learn multi-language service communication patterns.

---

### Step 5.1: Stock Reservation System

**Goal:** Reserve stock when item added to cart, release after 15 minutes if not checked out

**Implementation with Redis:**

**Cart Items Table Update:**
```sql
- reservation_expires_at (Timestamp, nullable)
- is_reserved (Boolean, default False)
```

**Logic:**
```python
# On add to cart:
1. Check if product has available stock (stock - reserved_quantity)
2. Create Redis entry: SET "reservation:{product_id}:{cart_item_id}" quantity EX 900 (15 min)
3. Increment reserved_quantity in Redis: HINCRBY "product:{product_id}:reserved" quantity
4. Update cart_item: is_reserved=True, reservation_expires_at=now+15min
5. Return success

# Background job (every minute):
1. Find expired reservations (reservation_expires_at < now AND is_reserved=True)
2. For each: delete Redis reservation key, decrement reserved count
3. Update cart_item: is_reserved=False

# On checkout:
1. Validate reservations still active
2. Decrement actual stock
3. Delete Redis reservations
4. Clear reservation flags

# On cart item delete:
1. If reserved: release reservation (delete Redis key, decrement count)
```

**You'll learn:**
- Distributed locking with Redis
- Race condition handling
- Expiry mechanisms
- Background cleanup jobs
- Stock reservation patterns
- Optimistic vs pessimistic locking

---

### Step 5.2: Promo Code System

**Promo Codes Table:**
```sql
- id (PK)
- code (String, unique, indexed)
- description (Text)
- discount_type (Enum: percentage, fixed)
- discount_value (Decimal)
- min_order_amount (Decimal, nullable)
- max_discount_amount (Decimal, nullable for percentage type)
- usage_limit (Integer, nullable) -- total usage limit
- usage_limit_per_user (Integer, nullable)
- valid_from (Timestamp)
- valid_until (Timestamp)
- is_active (Boolean)
- created_at (Timestamp)
```

**Promo Code Usage Table:**
```sql
- id (PK)
- promo_code_id (FK)
- user_id (FK, nullable)
- order_id (FK)
- discount_amount (Decimal)
- used_at (Timestamp)
```

**Endpoints:**
```
POST   /api/v1/cart/apply-promo       - Apply promo code to cart
DELETE /api/v1/cart/promo              - Remove promo code from cart
POST   /api/v1/admin/promo-codes      - Create promo code
GET    /api/v1/admin/promo-codes      - List promo codes
```

**Validation Logic:**
```python
def validate_promo_code(code, user_id, cart_total):
    1. Check code exists and is_active
    2. Check valid_from <= now <= valid_until
    3. Check min_order_amount <= cart_total
    4. Check total usage < usage_limit (if set)
    5. Check user usage < usage_limit_per_user (if set)
    6. Return discount amount
```

**You'll learn:**
- Complex business logic implementation
- Discount calculation strategies
- Usage tracking
- Validation rules
- Edge case handling

---

### Step 5.3: Analytics & Reporting

**Endpoints:**
```
GET /api/v1/admin/analytics/revenue           - Revenue over time
GET /api/v1/admin/analytics/top-products      - Best-selling products
GET /api/v1/admin/analytics/order-stats       - Order statistics
GET /api/v1/admin/analytics/customer-insights - Customer metrics
```

**Metrics to track:**
- Total revenue (daily, weekly, monthly)
- Order count
- Average order value
- Top products by revenue
- Top products by quantity sold
- New vs returning customers
- Cart abandonment rate

**Implementation:**
- Use SQL aggregation queries
- Add materialized views for expensive queries
- Cache analytics data (refresh hourly)

**You'll learn:**
- Aggregation queries (GROUP BY, SUM, COUNT, AVG)
- Window functions
- Materialized views
- Data aggregation patterns
- Reporting APIs

---

## Phase 6: Polyglot Microservices Architecture (Optional - Week 8+)

> **Goal:** Learn how to build and orchestrate microservices in different programming languages/frameworks, and make them communicate effectively.

This phase teaches you:
- Breaking a monolith into microservices
- Service-to-service communication (REST, gRPC, message queues)
- API Gateway patterns
- Service discovery
- Distributed tracing
- Cross-language integration

---

### Step 6.1: Architecture Planning - Identifying Service Boundaries

**Before writing any code, you'll learn to identify logical service boundaries:**

**Potential Services:**

1. **Product Catalog Service** (FastAPI - Python)
   - Manages products, categories
   - Already exists in your monolith
   - Read-heavy workload

2. **Order Processing Service** (Spring Boot - Java/Kotlin)
   - Handles order creation, status updates
   - Write-heavy, transaction-critical
   - Good fit for Java's robust ecosystem
   - **NEW SERVICE TO BUILD**

3. **Inventory Service** (FastAPI or Go)
   - Stock management, reservations
   - High-concurrency operations
   - Could use Go for performance (optional)

4. **Notification Service** (Node.js/TypeScript or Python)
   - Email, SMS notifications
   - Async, event-driven
   - Uses message queues

5. **API Gateway** (FastAPI or Spring Cloud Gateway)
   - Single entry point
   - Request routing
   - Authentication
   - Rate limiting

**Project Structure:**
```
backend_study/
├── services/
│   ├── product-catalog/        # FastAPI (existing)
│   │   ├── app/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── order-service/          # Spring Boot (NEW)
│   │   ├── src/
│   │   │   └── main/
│   │   │       ├── java/com/ecommerce/order/
│   │   │       └── resources/
│   │   ├── build.gradle
│   │   └── Dockerfile
│   ├── inventory-service/      # FastAPI or Go
│   │   ├── app/ (or main.go)
│   │   ├── Dockerfile
│   │   └── requirements.txt (or go.mod)
│   ├── notification-service/   # Python/Node.js
│   │   ├── app/
│   │   ├── Dockerfile
│   │   └── package.json or requirements.txt
│   └── api-gateway/            # FastAPI or Kong
│       ├── app/
│       ├── Dockerfile
│       └── requirements.txt
├── shared/
│   ├── proto/                  # gRPC proto files (shared contracts)
│   └── events/                 # Event schemas (for message queue)
├── docker-compose.microservices.yml
└── k8s/                        # Kubernetes manifests (advanced)
```

**You'll learn:**
- Domain-driven design (DDD) basics
- Service boundary identification
- Conway's Law
- When NOT to use microservices

---

### Step 6.2: Building Order Service in Spring Boot

**Why Spring Boot for Order Service?**
- Different tech stack exposure (Java/Kotlin)
- Enterprise-grade transaction management
- Strong ecosystem for distributed systems
- Industry standard for order/payment systems

**What you'll build:**

**Order Service Responsibilities:**
- Create orders
- Update order status
- Retrieve order details
- Communicate with Product Catalog (for product info)
- Communicate with Inventory Service (for stock checks)
- Publish order events to message queue

**Technology Stack:**
- Spring Boot 3.x
- Spring Data JPA
- PostgreSQL (separate database for this service)
- Kafka or RabbitMQ for events
- RestTemplate/WebClient for HTTP calls
- gRPC client (optional)

**Entities:**
```java
// Order.java
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    private String orderNumber;
    private UUID userId;
    private String email;
    private String phone;

    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    private BigDecimal totalAmount;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL)
    private List<OrderItem> items;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}

// OrderItem.java
@Entity
@Table(name = "order_items")
public class OrderItem {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "order_id")
    private Order order;

    private UUID productId;
    private String productName;
    private Integer quantity;
    private BigDecimal priceAtPurchase;
}
```

**REST Endpoints:**
```
POST   /api/v1/orders              - Create order
GET    /api/v1/orders/{id}         - Get order details
PUT    /api/v1/orders/{id}/status  - Update order status
GET    /api/v1/orders              - List orders (with filters)
```

**You'll learn:**
- Spring Boot basics (Controllers, Services, Repositories)
- Spring Data JPA
- Java/Kotlin syntax
- Gradle/Maven build tools
- Spring Boot configuration (application.yml)
- Exception handling in Spring

---

### Step 6.3: Service-to-Service Communication Patterns

**Pattern 1: Synchronous REST Communication**

**Scenario:** Order Service needs product details from Product Catalog

**Implementation:**

**In Spring Boot (Order Service):**
```java
@Service
public class ProductCatalogClient {
    private final WebClient webClient;

    public ProductCatalogClient(WebClient.Builder builder) {
        this.webClient = builder
            .baseUrl("http://product-catalog:8000")
            .build();
    }

    public ProductDTO getProduct(UUID productId) {
        return webClient.get()
            .uri("/api/v1/products/{id}", productId)
            .retrieve()
            .bodyToMono(ProductDTO.class)
            .block();
    }
}
```

**In FastAPI (Product Catalog Service):**
```python
# Just expose existing endpoint
@router.get("/api/v1/products/{product_id}")
async def get_product(product_id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

**Challenges to solve:**
- Service discovery (how does Order Service find Product Catalog?)
- Fault tolerance (what if Product Catalog is down?)
- Latency (blocking calls slow down request)
- Circuit breaker pattern

**You'll learn:**
- REST inter-service communication
- HTTP client libraries (WebClient, requests, httpx)
- Service discovery (DNS, Eureka, Consul)
- Circuit breakers (Resilience4j, Tenacity)
- Retry logic

---

**Pattern 2: Asynchronous Message Queue Communication**

**Scenario:** When order is created, notify multiple services without coupling

**Flow:**
```
Order Service → Kafka/RabbitMQ → [Notification Service, Inventory Service, Analytics Service]
```

**Implementation:**

**Order Service (Spring Boot) - Producer:**
```java
@Service
public class OrderEventPublisher {
    private final KafkaTemplate<String, OrderCreatedEvent> kafkaTemplate;

    public void publishOrderCreated(Order order) {
        OrderCreatedEvent event = new OrderCreatedEvent(
            order.getId(),
            order.getUserId(),
            order.getEmail(),
            order.getTotalAmount(),
            order.getCreatedAt()
        );

        kafkaTemplate.send("order.created", order.getId().toString(), event);
    }
}
```

**Notification Service (Python) - Consumer:**
```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'order.created',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    order_event = message.value
    send_order_confirmation_email(
        email=order_event['email'],
        order_id=order_event['order_id']
    )
```

**You'll learn:**
- Message queue fundamentals (Kafka, RabbitMQ)
- Event-driven architecture
- Publishers and subscribers
- Event schema design
- Eventual consistency
- Message serialization (JSON, Avro, Protobuf)

---

**Pattern 3: gRPC Communication (Optional - High Performance)**

**Scenario:** Inventory Service provides stock check via gRPC for low latency

**Define Proto Contract:**
```protobuf
// inventory.proto
syntax = "proto3";

package inventory;

service InventoryService {
  rpc CheckStock(StockCheckRequest) returns (StockCheckResponse);
  rpc ReserveStock(ReserveRequest) returns (ReserveResponse);
}

message StockCheckRequest {
  string product_id = 1;
  int32 quantity = 2;
}

message StockCheckResponse {
  bool available = 1;
  int32 current_stock = 2;
}
```

**Inventory Service (Python) - gRPC Server:**
```python
import grpc
from concurrent import futures
import inventory_pb2
import inventory_pb2_grpc

class InventoryServiceServicer(inventory_pb2_grpc.InventoryServiceServicer):
    def CheckStock(self, request, context):
        product = get_product(request.product_id)
        available = product.stock >= request.quantity

        return inventory_pb2.StockCheckResponse(
            available=available,
            current_stock=product.stock
        )

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
inventory_pb2_grpc.add_InventoryServiceServicer_to_server(
    InventoryServiceServicer(), server
)
server.add_insecure_port('[::]:50051')
server.start()
```

**Order Service (Spring Boot) - gRPC Client:**
```java
@Service
public class InventoryGrpcClient {
    private final InventoryServiceGrpc.InventoryServiceBlockingStub stub;

    public boolean checkStock(UUID productId, int quantity) {
        StockCheckRequest request = StockCheckRequest.newBuilder()
            .setProductId(productId.toString())
            .setQuantity(quantity)
            .build();

        StockCheckResponse response = stub.checkStock(request);
        return response.getAvailable();
    }
}
```

**You'll learn:**
- gRPC basics
- Protocol Buffers (protobuf)
- Binary serialization vs JSON
- Performance comparison (gRPC vs REST)
- Code generation from proto files

---

### Step 6.4: API Gateway Implementation

**Purpose:**
- Single entry point for all client requests
- Route requests to appropriate microservices
- Handle cross-cutting concerns (auth, rate limiting, logging)

**Options:**

**Option A: Build with FastAPI**
```python
from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://product-catalog:8000/api/v1/products/{product_id}"
        )
        return response.json()

@app.post("/orders")
async def create_order(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://order-service:8080/api/v1/orders",
            json=body
        )
        return response.json()
```

**Option B: Use Kong or Traefik (Production-grade)**

**You'll learn:**
- API Gateway pattern
- Request routing
- Service orchestration
- Load balancing
- Authentication/authorization at gateway level

---

### Step 6.5: Database Per Service Pattern

**Key Principle:** Each microservice owns its database

**Current State:**
```
Monolith DB (PostgreSQL)
├── products
├── categories
├── orders
├── order_items
├── users
└── carts
```

**After Microservices:**
```
Product Catalog DB (PostgreSQL)
├── products
└── categories

Order Service DB (PostgreSQL)
├── orders
└── order_items

Inventory DB (PostgreSQL or Redis)
├── stock_levels
└── reservations

User Service DB (PostgreSQL)
├── users
└── profiles
```

**Challenges:**
- No cross-database joins
- Distributed transactions (avoid or use Saga pattern)
- Data consistency across services
- Data duplication (denormalization)

**You'll learn:**
- Database per service pattern
- Distributed data management
- Saga pattern for distributed transactions
- Event sourcing (optional)
- CQRS (Command Query Responsibility Segregation - optional)

---

### Step 6.6: Service Discovery & Configuration

**Problem:** Services need to find each other dynamically

**Solutions:**

**1. DNS-based (Simple - for Docker Compose):**
```yaml
# docker-compose.microservices.yml
services:
  product-catalog:
    hostname: product-catalog

  order-service:
    hostname: order-service
    environment:
      - PRODUCT_CATALOG_URL=http://product-catalog:8000
```

**2. Service Registry (Advanced - Consul/Eureka):**

**Spring Boot with Eureka:**
```java
@SpringBootApplication
@EnableDiscoveryClient
public class OrderServiceApplication {
    // Auto-registers with Eureka
}
```

**3. Kubernetes Service Discovery (Production):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: product-catalog
spec:
  selector:
    app: product-catalog
  ports:
    - port: 8000
```

**You'll learn:**
- Service discovery mechanisms
- Dynamic configuration
- Health checks
- Service mesh basics (Istio - optional)

---

### Step 6.7: Observability in Distributed Systems

**Challenges:**
- Single request spans multiple services
- Where did the request fail?
- Which service is slow?

**Solutions:**

**1. Distributed Tracing (Jaeger/Zipkin):**

**FastAPI:**
```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

tracer = trace.get_tracer(__name__)

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    with tracer.start_as_current_span("get_product"):
        # Your code
        return product
```

**Spring Boot:**
```java
@Service
public class OrderService {
    @NewSpan("create_order")
    public Order createOrder(OrderRequest request) {
        // Your code
    }
}
```

**Trace visualization:**
```
[API Gateway] → [Order Service] → [Product Catalog]
     50ms            30ms               20ms
                                    ↓
                              [Inventory Service]
                                    15ms
```

**2. Centralized Logging (ELK Stack):**
- Elasticsearch: Store logs
- Logstash/Fluentd: Collect and forward logs
- Kibana: Visualize logs

**3. Metrics (Prometheus + Grafana):**
- Request count per service
- Error rates
- Latency percentiles (p50, p95, p99)
- Resource usage (CPU, memory)

**You'll learn:**
- Distributed tracing
- Correlation IDs
- Centralized logging
- Metrics aggregation
- Observability best practices

---

### Step 6.8: Docker Compose for Microservices

**Updated docker-compose.microservices.yml:**
```yaml
version: '3.8'

services:
  # Databases
  product-db:
    image: postgres:15
    environment:
      POSTGRES_DB: product_catalog

  order-db:
    image: postgres:15
    environment:
      POSTGRES_DB: orders

  inventory-db:
    image: postgres:15
    environment:
      POSTGRES_DB: inventory

  # Message Queue
  kafka:
    image: confluentinc/cp-kafka:latest

  # Redis for caching & sessions
  redis:
    image: redis:7-alpine

  # Services
  product-catalog:
    build: ./services/product-catalog
    ports:
      - "8001:8000"
    environment:
      - DATABASE_URL=postgresql://product-db:5432/product_catalog
      - REDIS_URL=redis://redis:6379

  order-service:
    build: ./services/order-service
    ports:
      - "8002:8080"
    environment:
      - SPRING_DATASOURCE_URL=jdbc:postgresql://order-db:5432/orders
      - PRODUCT_CATALOG_URL=http://product-catalog:8000
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092

  inventory-service:
    build: ./services/inventory-service
    ports:
      - "8003:8000"
    environment:
      - DATABASE_URL=postgresql://inventory-db:5432/inventory

  notification-service:
    build: ./services/notification-service
    environment:
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092

  api-gateway:
    build: ./services/api-gateway
    ports:
      - "8000:8000"
    environment:
      - PRODUCT_CATALOG_URL=http://product-catalog:8000
      - ORDER_SERVICE_URL=http://order-service:8080
      - INVENTORY_SERVICE_URL=http://inventory-service:8000

  # Observability
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
```

**You'll learn:**
- Multi-service orchestration
- Service dependencies
- Network configuration
- Environment-specific configs

---

## Summary: Monolith vs Microservices Journey

| Aspect | Phase 1-5 (Monolith) | Phase 6 (Microservices) |
|--------|---------------------|------------------------|
| **Deployment** | Single application | Multiple services |
| **Database** | Shared database | Database per service |
| **Technology** | Python/FastAPI only | Python, Java, Go, Node.js |
| **Communication** | Function calls | REST, gRPC, message queues |
| **Scaling** | Scale entire app | Scale services independently |
| **Complexity** | Low | High |
| **Development speed** | Fast | Slower (coordination needed) |
| **Fault isolation** | Single point of failure | Service failures isolated |

**When to use Microservices:**
- Large teams (multiple teams owning different services)
- Different scaling requirements per feature
- Need for technology diversity
- Independent deployment cycles

**When to use Monolith:**
- Small team
- Early stage product
- Uncertain domain boundaries
- Faster development speed needed

**You'll learn:**
- Polyglot programming (multiple languages)
- Distributed systems challenges
- Inter-service communication
- Trade-offs between monolith and microservices
- Real-world architecture decisions

---

## Continuous Learning Throughout All Phases

### Docker & Deployment

**Docker Setup:**
```yaml
# docker-compose.yml structure
services:
  app:          # FastAPI application
  postgres:     # Database
  redis:        # Cache + message broker
  celery:       # Background worker
  admin:        # React Admin panel (optional)
```

**Production Considerations:**
- Multi-stage Docker builds
- Environment-based configuration (dev, staging, prod)
- Health check endpoints
- Graceful shutdown
- Database migration automation
- Secret management

**You'll learn:**
- Docker containerization
- Multi-container orchestration
- Environment configuration
- Production deployment patterns
- Container networking

---

### Testing Strategy

**Test Types:**

1. **Unit Tests:**
   - Service layer logic
   - Utility functions
   - Validation logic

2. **Integration Tests:**
   - API endpoint tests
   - Database operations
   - Cart/order flows

3. **Test Fixtures:**
   - Database setup/teardown
   - Test data factories
   - Mock external services

**Testing Tools:**
- pytest
- pytest-asyncio
- httpx (for API testing)
- factory_boy (for test data)

**You'll learn:**
- Test-driven development (TDD)
- Unit vs integration testing
- Test fixtures and factories
- Mocking strategies
- Testing async code
- Database testing patterns

---

### Observability & Monitoring

**Logging:**
- Structured logging (JSON format)
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Request ID tracking
- Log aggregation

**Metrics:**
- Request count, latency
- Error rates
- Database query time
- Cache hit/miss rate

**Monitoring:**
- Health check endpoint (`/health`)
- Readiness check endpoint (`/ready`)
- Application metrics endpoint (`/metrics`)

**Tools:**
- Python logging module
- Prometheus (metrics - optional)
- Grafana (dashboards - optional)

**You'll learn:**
- Structured logging
- Metrics collection
- Health checks
- Observability best practices
- Debugging production issues

---

## Success Criteria

By the end of this project, you will be able to:

1. Design and implement a production-ready REST API
2. Model complex relational databases
3. Handle race conditions and concurrency
4. Implement caching strategies
5. Build async background job systems
6. Secure APIs with authentication and authorization
7. Optimize database queries and API performance
8. Containerize applications with Docker
9. Test backend systems comprehensively
10. Think about scalability and system design trade-offs

---

## Recommended Learning Path

1. **Don't skip phases** - each builds on previous knowledge
2. **Make mistakes** - that's how you learn
3. **Ask "why"** before implementing
4. **Review code after completing each feature**
5. **Write tests for critical paths**
6. **Document decisions in code comments**
7. **Simulate production scenarios** (high load, failures)

---

## Resources & References

**Official Documentation:**
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Pydantic: https://docs.pydantic.dev/
- Celery: https://docs.celeryq.dev/
- Redis: https://redis.io/docs/
- React Admin: https://marmelab.com/react-admin/

**Learning Resources:**
- Database design patterns
- REST API best practices
- System design fundamentals
- Python async/await
- SQL optimization

---

## Next Steps After Plan Approval

1. Set up project structure
2. Initialize Git repository
3. Create Docker Compose file
4. Set up FastAPI skeleton
5. Design database schema (you'll draft first)
6. Create first migration
7. Build first endpoint (products list)

**Remember:** The goal is not just to complete the project, but to **understand every decision** and be able to explain **why** you made specific choices.

Let's build something great together!
