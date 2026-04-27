# Session 01: Project Planning & Architecture Design
**Date:** 2026-04-27
**Duration:** ~1 hour
**Phase:** Planning & Setup

---

## Session Goals
1. Establish mentoring relationship and learning approach
2. Define project scope (e-commerce backend)
3. Choose tech stack
4. Create comprehensive project plan
5. Understand project setup best practices

---

## Key Discussions

### 1. Learning Approach & Mentoring Style

**Initial Request:**
- Learner wants to transition from Senior Mobile Developer to Backend Engineer
- Project-based learning approach
- Mentor should guide, not code-dump
- Force critical thinking through questions

**Agreed Methodology:**
- Discussion → Decision → Implementation (only when learner says "implement")
- Always present 2-3 options with trade-offs
- Ask probing questions before giving answers
- Teach "why" not just "how"

---

### 2. Project Selection: E-Commerce Platform

**Learner's Initial Scope:**
- Products, categories, brands, business sellers, customers
- Cart (guest + authenticated)
- Orders with delivery status
- Payment: Cash on delivery (MVP)
- Promo codes (later phase)

**Key Clarifications Made:**

**Q: Guest Checkout Strategy**
- Learner's answer: Track by session ID, require email/phone, allow conversion to registered user
- **Decision:** Session-based cart for guests, DB cart for registered users

**Q: Stock Management**
- Learner initially missed this
- Presented 3 options: reserve on add-to-cart, reserve on checkout, no reservation
- Learner chose: Reserve with 15-min expiry (good instinct!)
- **Mentor guidance:** Start simpler (check at checkout), evolve to reservation in Phase 5

**Q: Single vs Multi-Vendor**
- **Decision:** Single-vendor MVP, design for multi-vendor scalability

**Q: Email Service Failure Handling**
- Learner didn't know
- Taught 3 approaches: fail checkout, log and continue, async queue with retries
- **Decision:** Async queue (Phase 3), sync with try/catch (Phase 1)

---

### 3. Tech Stack Decisions

**Backend Framework:** FastAPI (Python)
- Modern, fast, async support
- Great for learning API design
- Type hints for better code quality

**Database:** PostgreSQL
- Relational data (products, orders, users)
- ACID compliance for transactions
- Industry standard

**Caching/Message Broker:** Redis
- Caching product catalog
- Background job queue (with Celery)
- Session storage

**Background Jobs:** Celery
- Async email sending
- Stock reservation expiry cleanup

**Admin Panel:** React Admin (pre-built library)
- Learner wants to learn frontend too
- Balance: Use library initially, build custom later

**Containerization:** Docker
- Consistent dev environment
- Multi-service orchestration

---

### 4. Project Phases Defined

**Phase 1: Core Commerce (Week 1-2)**
- Project setup
- Database design
- Product APIs
- Shopping cart
- Checkout & orders

**Phase 2: Authentication (Week 3)**
- User registration/login
- JWT tokens
- Protected routes
- Guest → registered user conversion

**Phase 3: Background Jobs & Admin (Week 4-5)**
- Celery + async emails
- React Admin panel
- Order status management

**Phase 4: Performance (Week 6)**
- Redis caching
- Database optimization
- API performance (compression, rate limiting)

**Phase 5: Advanced Features (Week 7+)**
- Stock reservation with expiry
- Promo codes
- Analytics

**Phase 6: Polyglot Microservices (Optional)**
- **NEW ADDITION (learner's request)**
- Build Order Service in Spring Boot (Java)
- Learn inter-service communication (REST, gRPC, message queues)
- API Gateway pattern
- Distributed tracing

---

### 5. Polyglot Microservices Discussion

**Learner's Vision:**
"I can add different stack code in this project. Suppose I can create another service written in Spring. Both services can communicate with each other."

**Mentor Response:**
- Added comprehensive Phase 6 to plan
- Covers breaking monolith into microservices
- Multiple languages: Python (FastAPI), Java (Spring Boot), optionally Go/Node.js
- Communication patterns:
  - Synchronous REST
  - Asynchronous message queues (Kafka/RabbitMQ)
  - gRPC for high performance
- Database per service pattern
- Service discovery, distributed tracing, observability

**Learning Goals for Phase 6:**
- When to use microservices vs monolith
- Cross-language service integration
- Distributed systems challenges
- Real-world architecture decisions

---

### 6. Project Setup Best Practices

**Discussion: "What file should we create first?"**

**Learner's Initial Answer:**
- README or main file
- requirements.txt

**Mentor Probing:**
- What if dependencies aren't installed?
- What about configuration (database URLs, secrets)?
- What prevents committing secrets to Git?

**Learner's Refined Answer:**
1. README (called it "Run.md" initially)
2. requirements.txt
3. Need to tell devs about architecture, tools, practices

**Correct Order Taught:**
1. **README.md** (not Run.md - GitHub auto-displays this)
2. **requirements.txt** (Python dependencies)
3. **.env.example** (configuration template - learner missed this!)
4. **.gitignore** (prevent committing secrets)
5. **docker-compose.yml** (easy dev environment)
6. **app/main.py** (actual code - comes LAST)

**Key Lesson:**
Think about developer experience. What frustrates developers when cloning a new project?

---

## Decisions Made

| Decision Point | Options Considered | Chosen Approach | Reasoning |
|----------------|-------------------|-----------------|-----------|
| **Vendor Model** | Single vs Multi-vendor | Single-vendor MVP | Learn fundamentals first, scale later |
| **Stock Reservation** | Add-to-cart vs Checkout vs None | Checkout check (MVP), reservation (Phase 5) | Simpler first, teach complexity later |
| **Admin UI** | Django Admin vs React Admin vs Custom | React Admin library | Balance backend focus + frontend learning |
| **Email Strategy** | Sync vs Async | Sync (Phase 1), Async (Phase 3) | Progressive complexity |
| **Cart Storage** | Session vs DB vs Redis | Session (guest) + DB (registered) | Standard pattern, easy to implement |
| **Auth** | JWT vs OAuth vs Sessions | JWT | Stateless, scalable, industry standard |
| **Microservices** | Monolith only vs Polyglot | Both (Phases 1-5 monolith, Phase 6 microservices) | Learn both paradigms |

---

## Key Learnings

### Technical Concepts Introduced:
1. **Session management** for guest users
2. **Race conditions** in stock management
3. **Database transactions** and ACID properties
4. **Async vs sync** processing
5. **Retry logic** with exponential backoff
6. **Cache invalidation** strategies
7. **Database per service** pattern (microservices)
8. **Service discovery** and API Gateway
9. **Distributed tracing**

### System Design Thinking:
- Always consider failure scenarios (email service down)
- Think about scale (1000 concurrent users)
- Understand trade-offs (simplicity vs scalability)
- Design for evolution (monolith → microservices)
- Security first (never hardcode secrets)

### Project Management:
- Start with MVP, iterate
- Phase-based learning (just-in-time concepts)
- Documentation is critical (README, .env.example)
- Developer experience matters (easy setup)

---

## Files Created This Session

1. **PROJECT_PLAN.md**
   - Complete 7-week roadmap
   - Phase 1-5: Monolith (FastAPI)
   - Phase 6: Polyglot microservices
   - Database schemas
   - API endpoints
   - Learning objectives per phase

2. **MENTORING_STRATEGY.md**
   - Mentoring principles
   - Working agreement (Discussion → Implement → Review)
   - Teaching style guidelines
   - Success metrics

3. **conversation_summaries/2026-04-27_session_01_project_planning.md** (this file)

---

## Questions Learner Asked

1. "What if email service is down during checkout?" → Taught async queues with retries
2. "How to track guest user's cart?" → Session ID pattern
3. "Can I add Spring Boot service to communicate with FastAPI?" → Added Phase 6 for microservices
4. "What file to create first?" → Taught project setup order

---

## Mistakes Made & Corrections

**Mistake:** Learner said "Run.md" instead of "README.md"
**Correction:** Explained GitHub auto-displays README.md, not custom names

**Mistake:** Missed .env.example in setup files
**Correction:** Taught configuration management, secrets handling

**Mistake:** Wanted to implement stock reservation from day 1 (complex)
**Correction:** Guided to simpler approach first, add complexity later

---

## Session End Discussion: README Planning

### Project Name Discussion

**Learner's Requirements:**
- Learning-based name
- Audience: primarily learner, but will add to CV for future interviews
- Should work well for interview conversations

**Mentor's Recommendation:** `backend-engineering-hub`

**Why?**
- Shows it's a learning journey (not pretending to be a startup)
- "Engineering" > "learning" (sounds more professional)
- "Hub" implies multiple services/technologies (fits Phase 6 microservices)
- Interview talking point: "I built this hub to master backend engineering from monolith to microservices"

**Alternative Options Discussed:**
- `production-ready-ecommerce` (emphasizes quality)
- `scalable-commerce-backend` (emphasizes architecture)
- `backend-masterclass-project` (emphasizes depth)

**STATUS: PENDING LEARNER'S FINAL CHOICE**

---

### Setup Steps Discussion

**Learner's Initial Answers:**
- Database: Docker Compose ✅
- Virtual environment: Yes, but didn't understand why initially
- Config: .env file ✅
- Running app: `python app/main.py` ⚠️ (needs correction to `uvicorn`)

**Key Concepts Taught:**

#### 1. Why Virtual Environment?

**Problem without venv:**
- Version conflicts between projects
- Can't tell which packages THIS project needs
- Messy requirements.txt

**Solution:**
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

**Benefits:**
- Isolation per project
- Reproducibility
- No conflicts
- Clean uninstall

**LEARNER UNDERSTANDS NOW ✅**

---

#### 2. Docker Compose Scope

**Question for Tomorrow:** Should docker-compose.yml include:
- **Option A:** Only PostgreSQL now, add Redis/Kafka later when needed
- **Option B:** PostgreSQL + Redis + everything upfront (even if unused)

**Follow-up Question:** Should the FastAPI app itself run in Docker?

**Option A: DB in Docker, App Local**
```bash
docker-compose up -d postgres
python app/main.py
```
**Pros:** Faster dev, easier debugging
**Cons:** Less environment consistency

**Option B: Everything in Docker**
```bash
docker-compose up
```
**Pros:** 100% consistent environment
**Cons:** Slower dev cycle, harder debugging

**STATUS: AWAITING LEARNER'S DECISION**

---

#### 3. .env vs .env.example

**Learner understands the concept ✅**

Two files:
- `.env.example` - Committed to Git, template with placeholders
- `.env` - NOT committed (in .gitignore), has real secrets

**Question for Tomorrow:** With Docker Compose, should DATABASE_URL be:
- **Option A:** `postgresql://user:password@localhost:5432/dbname`
- **Option B:** `postgresql://user:password@postgres:5432/dbname`

**Hint given:** Think about Docker networking - service name is `postgres`, not `localhost`

**STATUS: AWAITING LEARNER'S ANSWER**

---

#### 4. Running FastAPI App

**Learner said:** `python app/main.py`

**Mentor correction needed:** FastAPI is ASGI (async), needs ASGI server

**Correct command:**
```bash
uvicorn app.main:app --reload
```

**Breakdown:**
- `uvicorn` - ASGI server
- `app.main` - module path (app/main.py)
- `app` - FastAPI instance variable name
- `--reload` - auto-restart on code changes (dev only)

**Options for README:**

**Option A (simpler but wrong):**
```bash
python app/main.py
```

**Option B (correct for FastAPI):**
```bash
uvicorn app.main:app --reload
```

**Option C (production-ready):**
```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**STATUS: AWAITING LEARNER'S CHOICE**

---

## PENDING TASKS FOR NEXT SESSION (Session 02)

### IMMEDIATE: Answer These Questions

Before we create README.md, learner needs to decide:

1. **Final project name:**
   - `backend-engineering-hub` (mentor recommendation)
   - OR learner's alternative based on discussed principles

2. **Docker Compose scope:**
   - Just PostgreSQL now (minimal) OR all services upfront (complete)?
   - App in Docker OR run locally?

3. **DATABASE_URL in .env.example:**
   - `localhost` OR `postgres` (Docker service name)?

4. **Running the app command:**
   - Which option (A, B, or C) for the README?

---

### TASK: Draft Getting Started Section

Learner should complete this template:

```markdown
## Getting Started

### Prerequisites
- ???
- ???

### Installation

1. Clone the repository
   ```bash
   ???
   ```

2. ??? (Virtual environment step)

3. ??? (Install dependencies)

4. ??? (Start database with Docker Compose)

5. ??? (Set up environment variables)

### Running the Application

```bash
???
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`
```

**Learner should fill in based on:**
- Python version requirement (3.11+)
- Docker requirement
- Virtual environment setup
- Dependency installation
- Docker Compose for database
- Environment file setup (.env.example → .env)
- How to run the app (uvicorn command)

---

## Next Session Plan (Session 02)

### Part 1: Finalize Decisions (15 minutes)
1. Review learner's answers to pending questions
2. Discuss and refine choices
3. Finalize Getting Started section draft

### Part 2: Create README.md (20 minutes)
1. Learner says "implement"
2. Create README.md with:
   - Project description
   - Tech stack (FastAPI initially, mention evolution to microservices)
   - Getting Started section
   - Project structure overview
   - Learning objectives
   - License

### Part 3: Create Supporting Files (30 minutes)
1. **requirements.txt**
   - Learner lists dependencies (FastAPI, what else?)
   - Mentor reviews and adds missing ones
   - Discuss versioning strategies

2. **.env.example**
   - Discuss what config is needed
   - Create template

3. **.gitignore**
   - Discuss what to exclude
   - Create file

4. **docker-compose.yml**
   - Create based on decisions from Part 1
   - Explain each service
   - Test that it works

### Part 4: Initialize FastAPI App (20 minutes)
1. Create `app/` directory structure
2. Create `app/main.py` with basic FastAPI setup
3. Test that it runs: `uvicorn app.main:app --reload`
4. Visit `http://localhost:8000/docs`

### Part 5: Git Setup (10 minutes)
1. Initialize Git repository
2. First commit with all setup files
3. Discuss commit message conventions

---

## Files to Create Next Session

1. ✅ README.md
2. ✅ requirements.txt
3. ✅ .env.example
4. ✅ .gitignore
5. ✅ docker-compose.yml
6. ✅ app/main.py
7. ✅ app/__init__.py

---

## Learner Homework (Optional - Thinking Only, No Coding)

Before next session, **think about** (don't code):

1. What Python packages does a FastAPI project need?
   - Hint: FastAPI, database driver, ORM, validation, etc.

2. What environment variables will our app need?
   - Database connection?
   - Secret keys?
   - What else?

3. What should be in .gitignore?
   - Virtual environment?
   - Secrets?
   - What else?

**No need to write code - just think about these questions!**

---

## Learner Progress Assessment

**Strengths Shown:**
- ✅ Thinks about guest vs authenticated users
- ✅ Identifies need for stock management (after prompting)
- ✅ Wants to learn multiple tech stacks (polyglot)
- ✅ Values documentation (asked for conversation summaries)
- ✅ Understands separation of concerns

**Areas for Growth:**
- ⚠️ Configuration management (missed .env.example)
- ⚠️ Tendency to jump to complex solutions (reservation system)
- ⚠️ Need to think more about failure scenarios upfront

**Overall:** Strong start! Good instincts, willing to learn, asks clarifying questions.

---

## Mentor Notes

- Learner is engaged and thoughtful
- Responds well to Socratic method
- Prefers discussion before implementation (perfect!)
- Transition from mobile → backend means need to unlearn some patterns
- Watch for: oversimplifying distributed systems (mobile devs often underestimate backend complexity)
- Encourage: asking "what breaks if..." questions

---

## Key Quotes

**Learner:** "I didn't think about it. Not sure what should be the solution to this. Give me suggestions."
- Good! Admits gaps, asks for guidance

**Learner:** "Another thing to add in the plan is that I can add different stack code in this project."
- Shows ambition, wants breadth + depth

**Working Agreement:** "You will do the code but before doing any code we will have discussions... then when I say implement you will do the code."
- Perfect understanding of learning approach

---

*End of Session 01*

**Next Session:** README.md creation and project initialization
