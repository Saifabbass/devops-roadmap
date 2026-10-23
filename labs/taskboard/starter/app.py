"""A working starting point: GET /livez. Build one task endpoint at a time."""
from fastapi import FastAPI
app = FastAPI(title="My Taskboard")

@app.get("/livez")
def livez():
    return {"status": "ok"}

# After the pure-function tests pass, add a strict Pydantic request model.
# Then add create, list, get, and complete in that order. README gives checkpoints.
