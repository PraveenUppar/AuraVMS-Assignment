Aura VMS Assignment

# Blog Review System

This project models a **blog review workflow** where writers submit posts, managers review them, and only approved posts are published.

Deployed link: https://auravms-assignment.onrender.com

## Features

- REST APIs built with **FastAPI**
- Swagger / OpenAPI documentation
- Role‑based access control (Writer / Manager)
- JSON‑file persistence (no database required)
- Markdown / text parsing for blog content
- Server‑side rendered UI using **Jinja2**
- cloud deployment (Render)

## Credentials to share (assignment requirement)

Writer login:

- username: writer
- password: writer123

Manager login:

- username: manager
- password: manager123

## Email Notifications

On post submission, the system triggers an email notification to the manager.

For simplicity and reliability, the email service currently logs the email
content. The email module can be easily extended to integrate Gmail SMTP if needed.

## Overview

```
app/
├── api/            # API schemas and request models
├── auth/           # Simple role‑based authentication
├── models/         # Core domain models
├── parser/         # Text / Markdown parsing logic
├── storage/        # JSON file persistence layer
├── templates/      # Jinja2 HTML templates
├── email/         # Email service
├── main.py         # FastAPI application entry point

.gitignore
requirements.txt
README.md
```

---

## Roles & Workflow

### Writer

- Submits a blog post
- Cannot approve or reject posts

### Manager

- Reviews submitted posts
- Can approve or reject posts

### Public User

- Can view only **approved** posts

---

## API Endpoints

### Create a Post (Writer)

```
POST /posts
```

Request body:

```json
{
  "author": "writer1",
  "text": "My First Blog Post\nThis is the content of the post."
}
```

---

### Review a Post (Manager)

```
POST /posts/{post_id}/review
```

Request body:

```json
{
  "action": "approve" // or "reject"
}
```

---

### List Approved Posts

```
GET /posts
```

---

## UI Routes

- `/` – Home page
- `/submit` – Submit a new blog post
- `/posts` – View approved posts

The UI is rendered using **Jinja2 templates** and communicates with the same backend logic used by the APIs.

---

## Local Development

### 1. Clone the repository

```bash
git clone <repo-url>
cd blog-review-system
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

Run Tests:

```
pytest
```

---
