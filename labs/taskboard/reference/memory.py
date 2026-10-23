"""Week 3 reference store. Process-local, disposable, one Uvicorn worker."""
import asyncio
from reference.domain import complete, new_task


class MemoryStore:
    def __init__(self):
        self.tasks = {}
        self.lock = asyncio.Lock()

    async def create(self, owner, title):
        async with self.lock:
            task = new_task(owner, title)
            self.tasks[task.id] = task
            return task

    async def get(self, owner, task_id):
        task = self.tasks.get(str(task_id))
        return task if task and task.owner_id == owner else None

    async def list(self, owner):
        return sorted((t for t in self.tasks.values() if t.owner_id == owner),
                      key=lambda t: (t.created_at, t.id))

    async def complete(self, owner, task_id):
        async with self.lock:
            task = await self.get(owner, task_id)
            if task:
                task = complete(task)
                self.tasks[task.id] = task
            return task

    async def ready(self):
        return True
