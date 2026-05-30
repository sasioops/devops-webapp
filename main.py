from flask import Flask, jsonify, request, abort
from datetime import datetime
import platform

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Dockerise the app", "done": True},
    {"id": 2, "title": "Deploy behind Nginx", "done": False},
]
next_id = 3

# ── API 1: Health ─────────────────────────────────────────
@app.get("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "time": datetime.utcnow().isoformat() + "Z",
        "host": platform.node(),
        "python": platform.python_version(),
    })

# ── API 2: Tasks ──────────────────────────────────────────
@app.get("/api/tasks")
def list_tasks():
    return jsonify(tasks)

@app.post("/api/tasks")
def create_task():
    global next_id
    body = request.get_json(silent=True) or {}
    if not body.get("title"):
        abort(400, "title is required")
    task = {"id": next_id, "title": body["title"], "done": False}
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201

@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    body = request.get_json(silent=True) or {}
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = bool(body.get("done", task["done"]))
            return jsonify(task)
    abort(404, "task not found")

@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    global tasks
    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == before:
        abort(404, "task not found")
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)