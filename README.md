# real-blog - FastAPI Full Stack Blog Platform

> A backend-first blog application built with FastAPI, PostgreSQL, and SQLAlchemy. Designed as a learning ground for production system architecture, authentication/authorization patterns, and AI integration.

**Live:** https://real-blog.onrender.com

## _Note: If the app doesn’t load (cold start), open https://real-blog.onrender.com/health once, then revisit the main link._

## Tech Stack

| Layer      | Technology                            |
| ---------- | ------------------------------------- |
| Backend    | Python · FastAPI                      |
| Database   | PostgreSQL (Supabase)                 |
| ORM        | SQLAlchemy (async)                    |
| Validation | Pydantic v2                           |
| Auth       | JWT · bcrypt                          |
| Frontend   | HTML · CSS · Jinja2 (server-rendered) |
| DevOps     | Docker · Render                       |
| API Docs   | Swagger UI / OpenAPI (built-in)       |

---

## Project Structure

```
real-blog/
├── main.py               # App entrypoint, exception handlers, lifespan, health
├── database.py           # Async engine + session setup
├── models.py             # SQLAlchemy ORM models
├── schema.py             # Pydantic request/response schemas
├── crud.py               # DB operations, separated from route logic
├── routers/
│   ├── users.py          # User API endpoints
│   ├── posts.py          # Post API endpoints
│   └── web.py            # HTML-rendering routes
├── templates/            # Jinja2 HTML templates
├── static/               # CSS, JS, assets
├── media/
│   └── profile_pics/     # User-uploaded profile pictures -(for now - we use default image)
├── Dockerfile            # Container build instructions
├── docker-compose.yml    # Local dev orchestration (app + PostgreSQL)
├── requirements.txt      # Production dependencies
└── .dockerignore         # Files excluded from Docker build
```

---

## Architecture Highlights

**Dual response system** - every route serves both a browser-facing HTML response and a JSON API response, with routing determined by the request path (`/api/*` for JSON, everything else for HTML).

**Layered separation** - CRUD logic lives in `crud.py`, schemas in `schema.py`, models in `models.py`. Routes stay thin and readable.

**Async-first** - uses `asynccontextmanager` for lifespan management and an async SQLAlchemy engine, making it ready to scale without blocking I/O.

**Graceful error handling** - custom exception handlers for HTTP errors and validation errors, returning HTML error pages for browser requests and JSON for API responses.

**Containerized** - fully Dockerized with a multi-service `docker-compose.yml` for local development. Deployed to Render via Docker.

---

## Features Implemented

### Authentication & Authorization

- JWT-based authentication - token issuance, verification, and expiry
- Password hashing with bcrypt
- Protected routes using FastAPI dependency injection
- Owner-only authorization - users can only edit or delete their own posts and their own account

### User Management

- Create, read, update, delete users
- Profile picture upload support

### Post Management

- Create, read, update, delete blog posts
- Author relationship enforced at the schema and authorization level

### Data Validation

- Pydantic v2 schemas enforce strict input validation before any DB operation
- Consistent schema enforcement across both API and HTML flows

### Database

- PostgreSQL with async SQLAlchemy
- Hosted on Supabase (free tier) with Session Pooler for IPv4 compatibility
- Auto table creation via lifespan hook
- Proper model relationships and constraints

---

## Status

Authentication and authorization are complete. The app is fully containerized with Docker and deployed live on Render with Supabase as the database.

Next up: pagination, filtering, file uploads, and image validation.

Longer term: AI features like post summarization and auto-tagging via LLM APIs.

---

## Running Locally

### With Docker (recommended)

```bash
git clone https://github.com/abubakkersiddiqq/real-blog
cd real-blog

# Create .env file
echo "DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/blog_db" > .env
echo "SECRET_KEY=your-secret-key" >> .env

# Start app + database
docker-compose up --build
```

### Without Docker

```bash
git clone https://github.com/abubakkersiddiqq/real-blog
cd real-blog

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql+asyncpg://user:password@localhost/blog_db
export SECRET_KEY=your-secret-key

uvicorn main:app --reload
```

API docs available at: `http://localhost:8000/docs`

---

## Learning Goals

This project was built to develop a strong understanding of:

- Production backend architecture with FastAPI
- Authentication and authorization patterns (JWT, ownership-based access)
- Clean separation of concerns in a layered architecture
- Async database access with SQLAlchemy
- Containerization with Docker and cloud deployment
- Foundations for integrating AI/LLM features into backend systems

---

## Frontend Attribution

The base HTML/CSS frontend structure is adapted from Corey Schafer's tutorial content, used for learning purposes. All backend architecture - including CRUD separation, schema design, async setup, JWT auth, authorization, and Docker deployment - is independently implemented.

---

## License

MIT
