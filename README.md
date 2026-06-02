# Trackpen — Job Application Tracker API

A RESTful backend API built with **FastAPI** and **PostgreSQL** to help users track their job applications. Supports full authentication with JWT (access + refresh tokens) and full CRUD for job applications.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Running](#setup--running)
  - [With Docker (Recommended)](#with-docker-recommended)
  - [Without Docker (Local)](#without-docker-local)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [API Endpoints](#api-endpoints)

---

## Overview

Trackpen lets users register, log in, and manage their job applications — tracking company name, position, application status, and notes. All job application routes are protected and scoped to the authenticated user.

---

## Features

- JWT-based authentication (access + refresh token rotation)
- Secure password hashing with bcrypt
- Full CRUD for job applications
- Filter jobs by company name, position, or status
- Dockerized with PostgreSQL and health checks
- Alembic-managed database migrations

---

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Framework   | FastAPI                           |
| Database    | PostgreSQL 15                     |
| ORM         | SQLAlchemy 2.0                    |
| Migrations  | Alembic                           |
| Auth        | python-jose (JWT), bcrypt         |
| Server      | Uvicorn                           |
| Packaging   | uv                                |
| Container   | Docker + Docker Compose           |

---

## Project Structure

```
Trackpen/
├── alembic/                  # Migration scripts
│   └── versions/
├── core/
│   └── utils.py              # JWT, hashing, auth dependencies
├── db/
│   └── database.py           # DB engine, session, Base
├── models/
│   ├── users.py              # User ORM model
│   └── job_application.py    # JobApplication ORM model + Status enum
├── routers/
│   ├── users.py              # Auth routes
│   ├── job_applications.py   # Job CRUD routes
│   └── dummy.py              # Protected test route
├── schemas/
│   ├── user_schema.py        # Pydantic schemas for users
│   └── job_schema.py         # Pydantic schemas for jobs
├── main.py                   # FastAPI app entry point
├── dockerfile
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml
└── requirements.txt
```

---

## Setup & Running

### With Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Trackpen
   ```

2. Create a `.env` file (see [Environment Variables](#environment-variables)).

3. Build and start all services:
   ```bash
   docker compose up --build
   ```

4. API is available at `http://localhost:8000`
   Interactive docs at `http://localhost:8000/docs`

> Migrations run automatically on container startup.

---

### Without Docker (Local)

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Create a `.env` file (see [Environment Variables](#environment-variables)).

4. Make sure PostgreSQL is running locally, then run migrations:
   ```bash
   uv run alembic upgrade head
   ```

5. Start the server:
   ```bash
   uv run uvicorn main:app --reload
   ```

---

## Environment Variables

Create a `.env` file in the project root:

```env
DB_PASSWORD=your_postgres_password
JWT_ACCESS_SECRET_KEY=your_access_secret
JWT_REFRESH_SECRET_KEY=your_refresh_secret
```

> Access tokens expire in **30 minutes**. Refresh tokens expire in **7 days**.

---

## Database Migrations

```bash
# Apply all migrations
alembic upgrade head

# Create a new migration after model changes
alembic revision --autogenerate -m "your message"

# Rollback one step
alembic downgrade -1
```

---

## API Endpoints

### Health

| Method | Endpoint  | Auth | Description        |
|--------|-----------|------|--------------------|
| GET    | `/health` | ❌   | Health check       |

---

### Auth — `/auth`

| Method | Endpoint         | Auth | Description                        |
|--------|------------------|------|------------------------------------|
| POST   | `/auth/register` | ❌   | Register a new user                |
| POST   | `/auth/login`    | ❌   | Login and receive tokens           |
| POST   | `/auth/refresh`  | ❌   | Refresh access token               |
| POST   | `/auth/logout`   | ✅   | Logout (invalidates refresh token) |

---

### Job Applications

| Method | Endpoint           | Auth | Description                                                         |
|--------|--------------------|------|---------------------------------------------------------------------|
| POST   | `/create_job`      | ✅   | Create a new job application                                        |
| GET    | `/get_jobs`        | ✅   | Get all jobs (filter by `id`, `company_name`, `position`, `status`) |
| PATCH  | `/update_job/{id}` | ✅   | Update a job application by ID                                      |
| DELETE | `/delete_job/{id}` | ✅   | Delete a job application by ID                                      |

#### Job Status Values
`APPLIED` | `INTERVIEWING` | `OFFERED` | `REJECTED`

---

### Private (Test)

| Method | Endpoint         | Auth | Description               |
|--------|------------------|------|---------------------------|
| GET    | `/private/hello` | ✅   | Test authenticated access |

---

> ✅ = Requires `Authorization: Bearer <access_token>` header
