# real-blog - FastAPI Full Stack Blog Platform

> A backend-first blog application built with FastAPI, PostgreSQL, and SQLAlchemy. Designed as a learning ground for production system architecture, authentication/authorization patterns, and AI integration.

---

## Tech Stack

| Layer      | Technology                            |
| ---------- | ------------------------------------- |
| Backend    | Python · FastAPI                      |
| Database   | PostgreSQL                            |
| ORM        | SQLAlchemy (async)                    |
| Validation | Pydantic v2                           |
| Auth       | JWT · bcrypt                          |
| Frontend   | HTML · CSS · Jinja2 (server-rendered) |
| API Docs   | Swagger UI / OpenAPI (built-in)       |

---

## Project Structure

```
real-blog/
├── main.py           # App entrypoint, exception handlers, lifespan
├── database.py       # Async engine + session setup
├── models.py         # SQLAlchemy ORM models
├── schema.py         # Pydantic request/response schemas
├── crud.py           # DB operations, separated from route logic
├── routers/
│   ├── users.py      # User API endpoints
│   ├── posts.py      # Post API endpoints
│   └── web.py        # HTML-rendering routes
├── templates/        # Jinja2 HTML templates
├── static/           # CSS, JS, assets
└── media/            # User-uploaded profile pictures
```

---

## Architecture Highlights

**Dual response system** - every route serves both a browser-facing HTML response and a JSON API response, with routing determined by the request path (`/api/*` for JSON, everything else for HTML).

**Layered separation** - CRUD logic lives in `crud.py`, schemas in `schema.py`, models in `models.py`. Routes stay thin and readable.

**Async-first** - the app uses `asynccontextmanager` for lifespan management and an async SQLAlchemy engine, making it ready to scale without blocking I/O.

**Graceful error handling** - custom exception handlers for HTTP errors and validation errors, returning HTML error pages for browser requests and JSON for API responses.

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
- Auto table creation via lifespan hook
- Proper model relationships and constraints

---

## Status

Auth and authorization are complete. Currently working on Docker and deployment.
After deployment: pagination, file uploads, and image validation.
Longer term: AI features like post summarization and auto-tagging via LLM.

## Running Locally

```bash
# Clone the repo
git clone https://github.com/abubakkersiddiqq/real-blog
cd real-blog

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql+asyncpg://user:password@localhost/blog_db
export SECRET_KEY=your-secret-key

# Run the server
uvicorn main:app --reload
```

API docs available at: `http://localhost:8000/docs`

---

## Learning Goals

This project is being built to develop a strong understanding of:

- Production backend architecture with FastAPI
- Authentication and authorization patterns (JWT, ownership-based access)
- Clean separation of concerns in a layered architecture
- Async database access with SQLAlchemy
- Containerization with Docker and cloud deployment
- Foundations for integrating AI/LLM features into backend systems

---

## Frontend Attribution

The base HTML/CSS frontend structure is adapted from Corey Schafer's tutorial content, used for learning purposes. All backend architecture — including CRUD separation, schema design, async setup, JWT auth, and API design — is independently implemented.

---

## License

MIT
