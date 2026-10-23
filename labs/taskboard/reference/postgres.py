"""Week 6: SQL and transactions live at one explicit boundary."""
import asyncio
import os
import re

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from reference.domain import Task, DependencyUnavailable, new_task

SCHEMA_VERSION = 2
COLUMNS = "id, owner_id, title, completed, created_at, completed_at"
OPTIONS = "-c statement_timeout=2000 -c lock_timeout=1500 -c idle_in_transaction_session_timeout=3000"


def schema_name():
    name = os.getenv("TASKBOARD_DB_SCHEMA", "public")
    if not re.fullmatch(r"[a-z][a-z0-9_]{0,62}", name):
        raise RuntimeError("Invalid schema name")
    return name


def as_task(row):
    if row is None:
        return None
    row = dict(row)
    row["id"] = str(row["id"])
    return Task(**row)


class PostgresStore:
    def __init__(self, dsn=None, schema=None):
        self.dsn = dsn or os.environ["DATABASE_URL"]
        self.schema = schema or schema_name()

    async def _operation(self, action):
        async with await psycopg.AsyncConnection.connect(
            self.dsn, connect_timeout=2, options=OPTIONS, row_factory=dict_row
        ) as conn:
            await conn.execute(sql.SQL("SET LOCAL search_path TO {}").format(sql.Identifier(self.schema)))
            return await action(conn)

    async def _run(self, action):
        try:
            # Includes connection, SQL, and commit; do not retry a possibly committed POST.
            operation = asyncio.create_task(self._operation(action))
            done, _ = await asyncio.wait({operation}, timeout=4.0)
            if not done:
                # Do not wait for network cancellation to finish before returning 503.
                operation.cancel()
                operation.add_done_callback(lambda task: task.exception() if not task.cancelled() else None)
                raise TimeoutError()
            return operation.result()
        except (TimeoutError, psycopg.OperationalError, psycopg.InterfaceError) as exc:
            raise DependencyUnavailable() from exc

    async def create(self, owner, title):
        task = new_task(owner, title)
        async def action(conn):
            cursor = await conn.execute(
                "INSERT INTO tasks (id, owner_id, title, completed, created_at, completed_at) "
                "VALUES (%s, %s, %s, %s, %s, %s) RETURNING " + COLUMNS,
                (task.id, task.owner_id, task.title, task.completed, task.created_at, task.completed_at))
            return as_task(await cursor.fetchone())
        return await self._run(action)

    async def get(self, owner, task_id):
        async def action(conn):
            cursor = await conn.execute("SELECT " + COLUMNS + " FROM tasks WHERE id=%s AND owner_id=%s",
                                        (task_id, owner))
            return as_task(await cursor.fetchone())
        return await self._run(action)

    async def list(self, owner):
        async def action(conn):
            cursor = await conn.execute("SELECT " + COLUMNS + " FROM tasks WHERE owner_id=%s ORDER BY created_at, id",
                                        (owner,))
            return [as_task(row) for row in await cursor.fetchall()]
        return await self._run(action)

    async def complete(self, owner, task_id):
        async def action(conn):
            # PostgreSQL locks the row. The second concurrent update sees the first timestamp.
            cursor = await conn.execute("UPDATE tasks SET completed=true, "
                "completed_at=COALESCE(completed_at, clock_timestamp()) "
                "WHERE id=%s AND owner_id=%s RETURNING " + COLUMNS, (task_id, owner))
            return as_task(await cursor.fetchone())
        return await self._run(action)

    async def ready(self):
        async def action(conn):
            version = await (await conn.execute("SELECT max(version) AS version FROM schema_migrations")).fetchone()
            await conn.execute("SELECT " + COLUMNS + " FROM tasks LIMIT 0")
            return version["version"] == SCHEMA_VERSION
        try:
            return await self._run(action)
        except (DependencyUnavailable, psycopg.Error):
            return False
