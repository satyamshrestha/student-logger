# Student Management API

A production-style backend application built with FastAPI that demonstrates modern backend engineering practices including authentication, authorization, caching, rate limiting, asynchronous task processing, structured logging, Dockerized deployment, and PostgreSQL persistence.

---

## Overview

This project follows a layered architecture and is designed to simulate how a real-world backend service is structured and deployed.

The application provides:

- Student Management
- Course Management
- User Authentication
- Role-Based Access Control
- Redis Caching
- Background Task Processing
- Request Tracking & Logging
- Rate Limiting
- Dockerized Infrastructure

---

## Features

### Authentication & Security

- JWT Authentication
- Access Tokens
- Refresh Tokens
- Password Hashing with bcrypt
- Protected Endpoints
- Role-Based Access Control (RBAC)

Roles:

- Admin
- Teacher
- Student

Permissions:

| Role | Permissions |
|--------|-------------|
| Admin | Create, Read, Update, Delete, Admin Only |
| Teacher | Create, Read, Update |
| Student | Read |

---

### Student Management

- Create Student
- Retrieve Student
- Retrieve All Students
- Update Student
- Delete Student
- Student Count Endpoint

Advanced Query Features:

- Pagination
- Filtering
- Search
- Sorting

---

### Course Management

- Create Course
- View Courses
- Student-Course Relationship

---

### Performance Optimization

#### Redis Caching

Student list queries are cached in Redis.

Features:

- Cache Key Generation
- TTL Expiration
- Targeted Cache Invalidation

---

### Rate Limiting

Implemented using SlowAPI.

Examples:

- Login: 3 requests/minute
- Student Creation: 30 requests/minute
- Read Endpoints: 100 requests/minute

---

### Logging & Observability

#### Request Logging

Every request logs:

- Request Method
- URL
- Response Status
- Request Duration

#### Request Tracking

Each request receives a unique Request ID.

Example:

```
2026-05-30 12:00:00 INFO [Request ID: abc123]
Incoming request: GET /students
```

#### Audit Logging

Sensitive actions are tracked:

- Student Deletion
- User Role Changes

---

### Background Tasks

Implemented using Celery + Redis.

Example:

- Welcome Email Task

Executed asynchronously without blocking API responses.

---

### Database

#### PostgreSQL

Primary relational database.

#### SQLAlchemy ORM

Used for:

- Models
- Relationships
- CRUD Operations

#### Alembic

Used for:

- Schema Migrations
- Database Version Control

---

## Architecture

```text
Client
   │
   ▼
FastAPI Application
   │
   ├── Authentication
   ├── Authorization
   ├── Middleware
   ├── Services
   ├── Database Layer
   │
   ├── PostgreSQL
   ├── Redis Cache
   │
   └── Celery Worker
          │
          ▼
     Background Tasks
```

---

## Project Structure

```text
project/
│
├── api/
├── auth/
├── db/
├── middleware/
├── models/
├── routers/
├── schemas/
├── services/
├── tests/
├── utils/
│
├── alembic/
│
├── app.py
├── celery_worker.py
├── tasks.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Tech Stack

### Backend

- FastAPI
- Python

### Database

- PostgreSQL
- SQLAlchemy
- Alembic

### Authentication

- JWT
- bcrypt

### Caching

- Redis

### Background Processing

- Celery

### Infrastructure

- Docker
- Docker Compose
- pgAdmin

### Testing

- Pytest

---

## Running the Project

### Clone Repository

```bash
git clone https://github.com/satyamshrestha/student-logger
cd project
```

### Configure Environment Variables

Create `.env`

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
DATABASE_URL=postgresql://postgres:password@db:5432/student_logger_db
REDIS_URL=redis://redis:6379
```

### Start Services

```bash
docker compose up --build
```

### Run Database Migrations

```bash
alembic upgrade head
```

---

## Available Services

### API

```
http://localhost:8000
```

### pgAdmin

```
http://localhost:5050
```

### PostgreSQL

```
localhost:5432
```

### Redis

```
localhost:6379
```

---

## Testing

Run:

```bash
pytest
```

---

## Concepts Demonstrated

- FastAPI Architecture
- Dependency Injection
- JWT Authentication
- Refresh Tokens
- Role-Based Access Control
- SQLAlchemy ORM
- Alembic Migrations
- PostgreSQL
- Redis Caching
- Cache Invalidation
- Rate Limiting
- Structured Logging
- Request Tracking
- Audit Logging
- Background Task Processing
- Celery Workers
- Docker Deployment
- API Testing

---

Built to learn production-oriented backend engineering concepts and modern API development practices.