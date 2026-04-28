# Fullstack Commerce Journey

A comprehensive e-commerce backend learning project built with FastAPI, PostgreSQL, Redis, and Docker. This project demonstrates the evolution from a monolithic architecture to polyglot microservices, showcasing production-ready backend engineering practices.

## 🎯 Project Goals

This is a **learning-focused project** designed to master:
- RESTful API design with FastAPI
- Relational database modeling with PostgreSQL
- Caching strategies with Redis
- Background job processing with Celery
- Authentication & authorization (JWT)
- System design (monolith → microservices)
- Docker containerization
- Performance optimization
- Observability and monitoring

## 🏗️ Architecture Evolution

### Phase 1-5: Monolithic Application (Current)
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **Cache/Queue:** Redis
- **Background Jobs:** Celery
- **Admin Panel:** React Admin

### Phase 6: Polyglot Microservices (Planned)
- **Product Catalog Service:** FastAPI (Python)
- **Order Service:** Spring Boot (Java/Kotlin)
- **Inventory Service:** FastAPI or Go
- **Notification Service:** Python/Node.js
- **API Gateway:** FastAPI or Kong
- **Communication:** REST, gRPC, Kafka/RabbitMQ

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Database:** PostgreSQL 15
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Validation:** Pydantic
- **Authentication:** JWT (python-jose)
- **Password Hashing:** passlib with bcrypt
- **Caching/Queue:** Redis
- **Background Jobs:** Celery
- **Containerization:** Docker & Docker Compose
- **Testing:** pytest

## 📋 Features

### Current (Phase 1)
- [ ] Product catalog with categories
- [ ] Shopping cart (guest + authenticated users)
- [ ] Order management
- [ ] Guest checkout

### Planned
- [ ] User authentication & authorization (JWT)
- [ ] Admin panel for product/order management
- [ ] Async email notifications
- [ ] Redis caching for performance
- [ ] Stock reservation system
- [ ] Promo code system
- [ ] Analytics & reporting
- [ ] Microservices architecture (polyglot)

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/fullstack-commerce-journey.git
   cd fullstack-commerce-journey
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   The default values work for local development.

5. **Start PostgreSQL with Docker Compose**
   ```bash
   docker compose up -d postgres
   ```

6. **Run database migrations**
   ```bash
   # (Migrations will be created as we build the project)
   alembic upgrade head
   ```

### Running the Application

**Development (current):**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production (for future deployment):**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at: `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

Alternative API documentation: `http://localhost:8000/redoc`

## 📁 Project Structure

```
fullstack-commerce-journey/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── user.py
│   ├── schemas/                # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── user.py
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependencies (auth, db session, etc.)
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
│   └── utils/                  # Helper functions
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
├── conversation_summaries/     # Learning session notes
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── alembic.ini
├── README.md
├── PROJECT_PLAN.md
└── MENTORING_STRATEGY.md
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_products.py
```

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PROJECT_PLAN.md](PROJECT_PLAN.md) - Detailed phase-by-phase plan
- [MENTORING_STRATEGY.md](MENTORING_STRATEGY.md) - Learning approach

## 🎓 Learning Journey

This project follows a structured learning path documented in [PROJECT_PLAN.md](PROJECT_PLAN.md):

- **Week 1-2:** Core commerce features (products, cart, orders)
- **Week 3:** Authentication & user management
- **Week 4-5:** Background jobs & admin panel
- **Week 6:** Caching & performance optimization
- **Week 7+:** Advanced features (stock reservation, promo codes, analytics)
- **Week 8+:** Polyglot microservices architecture (optional)

Session notes and key learnings are documented in the `conversation_summaries/` directory.

## 🤝 Contributing

This is a personal learning project, but suggestions and feedback are welcome! Feel free to open an issue if you spot any improvements.

## 📝 License

MIT License - feel free to use this project for your own learning!

---

**Built with ❤️ as a journey from monolith to microservices**
