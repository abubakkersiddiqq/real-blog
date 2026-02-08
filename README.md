# Blog Application (FastAPI – Backend-Centric Full Stack Project)

## Overview
This project is a **backend-focused full stack blog application** built using **FastAPI**, designed to demonstrate strong fundamentals in API design, data validation, database interaction, and clean project structure.

The application supports both:
- **HTML responses** for browser-based interaction
- **REST API responses** documented and testable via **Swagger (OpenAPI)**

Authentication and authorization are intentionally not implemented yet to keep the focus on **core backend correctness and logic**.

---

## Tech Stack
- **Backend:** Python (FastAPI)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Frontend:** HTML, CSS (server-rendered)
- **API Docs:** Swagger / OpenAPI (FastAPI built-in)

---

## Project Architecture
- FastAPI for API-first development
- SQLAlchemy ORM for database models and persistence
- PostgreSQL as a real relational database (not in-memory or mock)
- Pydantic schemas for request/response validation
- CRUD logic separated into dedicated modules for maintainability
- Clear separation between API routes and HTML-rendering routes

---

## Features Implemented

### Dual Response System
- HTML endpoints for UI-based interaction
- REST API endpoints accessible and testable via Swagger UI

### User Management (CRUD)
- Create user
- Update user
- Delete user
- Retrieve user(s)

### Post Management (CRUD)
- Create post
- Update post
- Delete post
- Retrieve post(s)

### Data Validation
- Strict backend-level validation using Pydantic schemas
- Invalid or malformed input rejected before database operations
- Consistent schema enforcement across API and HTML flows

### Database Integration
- PostgreSQL connected using SQLAlchemy
- Persistent relational data
- Defined models with constraints and relationships

---

## What Is Not Implemented Yet
- Authentication / authorization
- Login or signup system
- Role-based access control
- React or SPA frontend
- Production deployment

All current CRUD operations can be tested using **Swagger UI**.

---

## Frontend Attribution
The base HTML/CSS frontend structure is adapted from **Corey Schafer’s tutorial content** and used for learning and integration purposes.

Backend architecture decisions -- including CRUD separation, data validation, API design, and database integration - are independently implemented.

---

## Purpose of This Project
This project demonstrates:
- Real backend development using FastAPI
- Correct use of SQLAlchemy with PostgreSQL
- Clean CRUD architecture
- Proper data validation and error handling
- API-first design with optional HTML rendering
- A scalable foundation for production-ready systems

This is a **backend- and logic-first project**, not a UI showcase.

---

## Planned Enhancements
- Authentication and protected routes
- React frontend
- Pagination and filtering
- Dockerization and deployment

---

## Status
Core backend complete.  
Authentication and frontend planned.
