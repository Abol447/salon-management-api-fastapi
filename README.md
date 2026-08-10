# Salon Management API

Backend API for Salon Management System built with **FastAPI**, **SQLAlchemy**, **Alembic** and **MySQL**.

---

## Technologies

- Python
- FastAPI
- SQLAlchemy ORM
- Alembic (Database Migration)
- MySQL
- Pydantic
- JWT Authentication

---

# Requirements

Before running the project, install these:

- Python 3.11+
- MySQL Server
- Git

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>

cd salon-management-api
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

---

### Linux / Mac

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file in the project root.

You can use `.env.example` as a template.

Example:

```env
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=
DATABASE_NAME=salon-management


SECRET_KEY=change_this_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=5
```

---

# Database Setup

Create MySQL database:

```sql
CREATE DATABASE salon-management;
```

Make sure your database information matches your `.env` file.

---

# Database Migration

This project uses Alembic for database migrations.

## Apply migrations

```bash
alembic upgrade head
```

---

## Create new migration

After changing models:

```bash
alembic revision --autogenerate -m "migration message"
```

Then apply:

```bash
alembic upgrade head
```

---

# Run Project

Start FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will run on:

```
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI provides automatic documentation.

Swagger:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

# Authentication

This API uses JWT authentication.

After login, send the access token in request headers:

```
Authorization: Bearer <access_token>
```

---

# Project Structure

```
app/
│
├── core/
│   └── Configuration files
│
├── db/
│   └── Database connection
│
├── models/
│   └── SQLAlchemy models
│
├── schemas/
│   └── Pydantic schemas
│
├── repositories/
│   └── Database operations
│
├── services/
│   └── Business logic
│
├── routers/
│   └── API endpoints
│
├── exceptions/
│   └── Custom exceptions
│
└── main.py


alembic/
│
├── versions/
│   └── Migration files


.env
.env.example
requirements.txt
README.md
```

---

# Update Dependencies

When adding a new package:

Install package:

```bash
pip install package_name
```

Update requirements:

```bash
pip freeze > requirements.txt
```

---

# Development

Run development server:

```bash
uvicorn app.main:app --reload
```

---

# Important Notes

- Never commit `.env` file to Git.
- Use `.env.example` for sharing environment variables.
- Each developer should create their own `.env`.
- Run database migrations before starting the project.


