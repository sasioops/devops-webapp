"""
Tests for the devops-webapp FastAPI endpoints.
Run with:  pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
from main import app

client = TestClient(app)


# ── Health endpoint ───────────────────────────────────────────────────────────
def test_health_returns_200():
    r = client.get("/api/health")
    assert r.status_code == 200

def test_health_has_status_field():
    r = client.get("/api/health")
    assert r.json()["status"] == "healthy"

def test_health_has_timestamp():
    r = client.get("/api/health")
    assert "timestamp" in r.json()


# ── Tasks endpoint ────────────────────────────────────────────────────────────
def test_list_tasks_returns_200():
    r = client.get("/api/tasks")
    assert r.status_code == 200

def test_list_tasks_has_tasks_key():
    r = client.get("/api/tasks")
    assert "tasks" in r.json()

def test_create_task():
    r = client.post("/api/tasks", json={"title": "Test task"})
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Test task"
    assert body["done"] is False

def test_update_task():
    # create first
    task_id = client.post("/api/tasks", json={"title": "Toggle me"}).json()["id"]
    r = client.patch(f"/api/tasks/{task_id}", json={"done": True})
    assert r.status_code == 200
    assert r.json()["done"] is True

def test_delete_task():
    task_id = client.post("/api/tasks", json={"title": "Delete me"}).json()["id"]
    r = client.delete(f"/api/tasks/{task_id}")
    assert r.status_code == 204

def test_delete_nonexistent_task_returns_404():
    r = client.delete("/api/tasks/99999")
    assert r.status_code == 404
