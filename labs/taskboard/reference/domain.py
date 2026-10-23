"""Week 3: behavior that needs neither HTTP nor a database."""
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from uuid import uuid4


def normalize_title(value: object) -> str:
    if type(value) is not str:
        raise ValueError("Title must be a string")
    title = value.strip()
    if not 1 <= len(title) <= 120:
        raise ValueError("Title must contain 1 to 120 characters")
    return title


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def rfc3339(value: datetime | None) -> str | None:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z") if value else None


@dataclass(frozen=True)
class Task:
    id: str
    owner_id: str
    title: str
    completed: bool
    created_at: datetime
    completed_at: datetime | None

    def public(self) -> dict:
        return {"id": self.id, "title": self.title, "completed": self.completed,
                "created_at": rfc3339(self.created_at), "completed_at": rfc3339(self.completed_at)}


def new_task(owner: str, title: object) -> Task:
    return Task(str(uuid4()), owner, normalize_title(title), False, utc_now(), None)


def complete(task: Task) -> Task:
    return task if task.completed else replace(task, completed=True, completed_at=utc_now())


class DependencyUnavailable(Exception):
    """Internal signal. Details must never reach HTTP clients or request logs."""
