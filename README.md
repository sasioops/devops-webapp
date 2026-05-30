# devops-webapp

A production-ready Python REST API deployed behind Nginx using Docker — built as a DevOps portfolio project.

## Tech stack

| Layer      | Technology                    |
|------------|-------------------------------|
| API        | Python 3.12 + FastAPI         |
| Server     | Uvicorn (ASGI, 2 workers)     |
| Proxy      | Nginx 1.25 (reverse proxy)    |
| Container  | Docker (multi-stage build)    |
| Compose    | Docker Compose v2             |
| CI/CD      | GitHub Actions                |
| Registry   | GitHub Container Registry     |

## APIs

### GET /api/health
Liveness probe. Returns service status, hostname, Python version, and environment.

### GET /api/tasks
List all tasks.

### POST /api/tasks
Create a task. Body: `{"title": "string"}`

### PATCH /api/tasks/{id}
Update done status. Body: `{"done": true}`

### DELETE /api/tasks/{id}
Delete a task.

Interactive docs: http://localhost/docs

## Run locally (Docker Compose)

```bash
# Clone and enter the project
git clone <your-repo>
cd devops-webapp

# Build + start both containers
docker compose up --build

# Visit
curl http://localhost/api/health
curl http://localhost/api/tasks
open http://localhost/docs
```

## Run tests

```bash
pip install -r app/requirements.txt pytest httpx
pytest tests/ -v
```

## Build Docker image manually

```bash
# Build
docker build -t devops-webapp:1.0.0 .

# Run standalone (no Nginx)
docker run -p 8000:8000 devops-webapp:1.0.0

# Inspect layers
docker history devops-webapp:1.0.0
```

## Architecture

```
Browser / curl
      │
      ▼
  Nginx :80          ← security headers, rate limiting, static files
      │  /api/*
      ▼
 FastAPI :8000       ← business logic, request validation, OpenAPI docs
      │
      ▼
 (in-memory store)   ← swap for PostgreSQL in production
```

## Project structure

```
devops-webapp/
├── app/
│   ├── main.py            # FastAPI application
│   └── requirements.txt
├── nginx/
│   └── nginx.conf         # reverse proxy config
├── tests/
│   └── test_api.py        # pytest suite
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # GitHub Actions pipeline
├── Dockerfile             # multi-stage build
├── docker-compose.yml
└── README.md
```

## Resume bullet

> "Built and containerised a Python FastAPI REST API using a multi-stage Docker build, deployed behind an Nginx reverse proxy with Docker Compose; automated testing, image publishing to GHCR, and SSH-based deployment via GitHub Actions."
