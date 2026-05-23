# Student Logger Backend

A backend project built with FastAPI while learning production-style backend engineering concepts.

The project started as a simple CRUD API and gradually evolved into a more structured backend system with authentication, role-based access control, Redis caching, Dockerized deployment, migrations, logging, middleware, and testing.

---

## What this project includes

* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Alembic migrations
* JWT authentication
* Role-based access control (RBAC)
* Redis caching
* Docker & Docker Compose
* Background tasks
* Logging middleware
* Global exception handling
* Rate limiting
* Layered architecture
* Basic testing with Pytest

---

## Project structure

```bash
.
├── alembic/
├── api/
├── auth/
├── db/
├── models/
├── routers/
├── schemas/
├── services/
├── tests/
├── utils/
├── app.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Architecture

The project follows a layered architecture approach.

### Routers

Handle:

* endpoints
* request validation
* dependencies
* responses

### Services

Handle:

* business logic
* database operations
* caching logic

### Models

Handle:

* database tables
* relationships

### Schemas

Handle:

* request/response validation

---

## Authentication

Authentication is implemented using JWT.

### Signup flow

1. User sends credentials
2. Password is hashed using bcrypt
3. User gets stored in PostgreSQL

### Login flow

1. User submits credentials
2. Password is verified
3. JWT access token is generated
4. Protected routes use token verification

---

## RBAC (Role-Based Access Control)

Supported roles:

* admin
* teacher
* student

Permissions are enforced through FastAPI dependencies.

Example:

```python
Depends(require_permission("create"))
```

---

## Redis caching

Student list responses are cached using Redis.

Cache is automatically cleared after:

* create
* update
* delete operations

---

## Rate limiting

Rate limiting is implemented using SlowAPI.

Example:

```python
@limiter.limit("30/minute")
```

---

## Logging

The project includes:

* request logging
* response logging
* login logging
* audit logging
* error logging

Logs are stored inside:

```bash
app.log
```

---

## Running the project

### Start containers

```bash
docker compose up --build
```

### Run migrations

```bash
docker compose exec api alembic upgrade head
```

---

## Environment variables

Example `.env`:

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
DATABASE_URL=your-postgresql-url
REDIS_URL=your-redis-url
```

---

## Main endpoints

### Auth

| Method | Endpoint              |
| ------ | --------------------- |
| POST   | `/api/v1/auth/signup` |
| POST   | `/api/v1/auth/login`  |

### Students

| Method | Endpoint                        |
| ------ | ------------------------------- |
| POST   | `/api/v1/students`              |
| GET    | `/api/v1/students`              |
| GET    | `/api/v1/students/{student_id}` |
| PUT    | `/api/v1/students/{student_id}` |
| DELETE | `/api/v1/students/{student_id}` |

### Users

| Method | Endpoint                        |
| ------ | ------------------------------- |
| GET    | `/api/v1/users/me`              |
| GET    | `/api/v1/users`                 |
| PUT    | `/api/v1/users/{username}/role` |

---

## Testing

Run tests using:

```bash
pytest
```

---

## What I learned building this

This project helped me understand:

* backend architecture
* dependency injection
* authentication & authorization
* database relationships
* Redis caching
* middleware flow
* Dockerized development
* API protection
* migrations
* service-layer design
* production-style backend structure

---

## Future improvements

Things I plan to add later:

* async SQLAlchemy
* async Redis
* refresh tokens
* Celery workers
* CI/CD pipelines
* Kubernetes
* cloud deployment
* advanced testing setup
* query optimization

---

Built while learning backend engineering and production API design.
-Satyam Shrestha