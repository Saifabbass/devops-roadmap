"""HTTP adapter shared by the three teaching stages; read alongside README."""
import json
import logging
import os
import secrets
import time
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, StrictStr, field_validator

from reference.domain import DependencyUnavailable, normalize_title

log = logging.getLogger("taskboard.requests")


class CreateTask(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: StrictStr

    @field_validator("title")
    @classmethod
    def valid_title(cls, value):
        return normalize_title(value)


class ApiError(Exception):
    def __init__(self, status, code, message):
        self.status, self.code, self.message = status, code, message


def make_app(store, *, stage, auth_tokens=None):
    app = FastAPI(title="Taskboard", version="1.0", docs_url=None, redoc_url=None)
    app.state.store = store
    bearer = HTTPBearer(auto_error=False)
    if stage == "07":
        if not auth_tokens or len(auth_tokens) != 2 or len(set(auth_tokens.values())) != 2:
            raise RuntimeError("Stage 07 requires two distinct lab identities")
        if any(len(token) < 32 for token in auth_tokens):
            raise RuntimeError("Stage 07 requires two different tokens of at least 32 characters")

    def problem(request, status, code, message):
        headers = {"WWW-Authenticate": "Bearer"} if status == 401 else {}
        return JSONResponse({"error": {"code": code, "message": message},
                             "request_id": request.state.request_id}, status_code=status, headers=headers)

    @app.middleware("http")
    async def request_log(request: Request, call_next):
        started = time.monotonic()
        request.state.request_id = str(uuid4())
        try:
            response = await call_next(request)
        except Exception:
            response = problem(request, 500, "INTERNAL_ERROR", "Internal server error")
        response.headers["X-Request-ID"] = request.state.request_id
        route = request.scope.get("route")
        # Log the template, not URLs, queries, bodies, headers, or exception text.
        log.info(json.dumps({"request_id": request.state.request_id, "method": request.method,
            "path": getattr(route, "path", "<unmatched>"), "status": response.status_code,
            "duration_ms": round((time.monotonic() - started) * 1000, 2)}))
        return response

    @app.exception_handler(ApiError)
    async def api_error(request, exc):
        return problem(request, exc.status, exc.code, exc.message)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        return problem(request, 422, "VALIDATION_ERROR", "Request validation failed")

    @app.exception_handler(DependencyUnavailable)
    async def dependency_error(request, exc):
        return problem(request, 503, "DEPENDENCY_UNAVAILABLE", "Dependency unavailable")

    async def identity(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
        if stage != "07":
            return "local-student"
        if credentials and credentials.scheme.lower() == "bearer":
            supplied = credentials.credentials.encode("utf-8")
            for token, owner in auth_tokens.items():
                if secrets.compare_digest(supplied, token.encode("utf-8")):
                    return owner
        raise ApiError(401, "UNAUTHENTICATED", "Authentication required")

    def found(task):
        if task is None:
            raise ApiError(404, "TASK_NOT_FOUND", "Task not found")
        return task.public()

    @app.get("/livez")
    async def livez():
        return {"status": "ok"}

    @app.get("/version")
    async def version():
        return {"app_version": "v0.1" if stage == "03" else "v0.2",
                "api_contract": "1.0", "git_sha": os.getenv("GIT_SHA", "development")}

    if stage != "03":
        @app.get("/readyz")
        async def readyz():
            ready = await store.ready()
            return JSONResponse({"status": "ready" if ready else "not_ready"}, status_code=200 if ready else 503)

    @app.post("/tasks", status_code=201)
    async def create(body: CreateTask, owner=Depends(identity)):
        task = await store.create(owner, body.title)
        return JSONResponse(task.public(), status_code=201, headers={"Location": f"/tasks/{task.id}"})

    @app.get("/tasks")
    async def list_tasks(owner=Depends(identity)):
        return {"items": [t.public() for t in await store.list(owner)]}

    @app.get("/tasks/{task_id}")
    async def get_task(task_id: UUID, owner=Depends(identity)):
        return found(await store.get(owner, task_id))

    @app.post("/tasks/{task_id}/complete")
    async def complete_task(task_id: UUID, request: Request, owner=Depends(identity)):
        if await request.body():
            raise ApiError(422, "VALIDATION_ERROR", "Completion requires an empty body")
        return found(await store.complete(owner, task_id))

    return app
