from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import platform
import os

app = FastAPI(
    title="DevOps Portfolio API",
    description="A simple Python API deployed with Docker + Nginx",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── In-memory task store (swap for a real DB in production) ──────────────────
tasks: list[dict] = [
    {"id": 1, "title": "Set up CI/CD pipeline", "done": True},
    {"id": 2, "title": "Dockerise the app",     "done": True},
    {"id": 3, "title": "Deploy behind Nginx",   "done": False},
]
next_id = 4


# ── Models ────────────────────────────────────────────────────────────────────
class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    done: bool


# ── API 1: System health / info ───────────────────────────────────────────────
@app.get("/api/health", tags=["System"])
def health_check():
    """Liveness probe — returns service status and runtime info."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "host": platform.node(),
        "python": platform.python_version(),
        "env": os.getenv("APP_ENV", "development"),
    }


# ── API 2: Task manager CRUD ─────────────────────────────────────────────────
@app.get("/api/tasks", tags=["Tasks"])
def list_tasks():
    """Return all tasks."""
    return {"tasks": tasks, "total": len(tasks)}


@app.post("/api/tasks", status_code=201, tags=["Tasks"])
def create_task(body: TaskCreate):
    """Create a new task."""
    global next_id
    task = {"id": next_id, "title": body.title, "done": False}
    tasks.append(task)
    next_id += 1
    return task


@app.patch("/api/tasks/{task_id}", tags=["Tasks"])
def update_task(task_id: int, body: TaskUpdate):
    """Toggle a task's done status."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = body.done
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/api/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: int):
    """Delete a task by id."""
    global tasks
    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == before:
        raise HTTPException(status_code=404, detail="Task not found")
