import asyncio
from uuid import uuid4
import psycopg
from psycopg import sql
import pytest
from reference.migrate import apply
from reference.domain import new_task
from reference.postgres import OPTIONS, PostgresStore


def connect(database):
    dsn, schema = database
    conn = psycopg.connect(dsn, connect_timeout=2, options=OPTIONS)
    conn.execute(sql.SQL("SET LOCAL search_path TO {}").format(sql.Identifier(schema)))
    return conn


def test_roundtrip_ownership_and_concurrent_completion(store):
    async def scenario():
        assert await store.ready()
        task = await store.create("alice", "  Ship  ")
        assert (await store.get("alice", task.id)).title == "Ship"
        assert await store.get("bob", task.id) is None
        assert await store.complete("bob", task.id) is None
        assert await store.list("bob") == []
        results = await asyncio.gather(store.complete("alice", task.id), store.complete("alice", task.id))
        assert results[0].completed_at == results[1].completed_at
        assert (await store.get("alice", task.id)).completed_at == results[0].completed_at
    asyncio.run(scenario())


def test_database_constraint_and_transaction_rollback(database, store):
    task = new_task("alice", "rolled-back")
    with pytest.raises(psycopg.errors.CheckViolation):
        with connect(database) as conn:
            conn.execute("INSERT INTO tasks(id, owner_id, title, created_at) VALUES(%s,%s,%s,%s)",
                         (task.id, task.owner_id, task.title, task.created_at))
            conn.execute("UPDATE tasks SET completed=true WHERE id=%s", (task.id,))
    with connect(database) as conn:
        assert conn.execute("SELECT count(*) FROM tasks WHERE id=%s", (task.id,)).fetchone()[0] == 0

@pytest.mark.parametrize("title", ["", "   ", "x" * 121])
def test_invalid_direct_sql_is_rejected(database, store, title):
    with pytest.raises(psycopg.errors.CheckViolation):
        with connect(database) as conn:
            conn.execute("INSERT INTO tasks(id, owner_id, title, created_at) VALUES(%s,%s,%s,clock_timestamp())",
                         (uuid4(), "alice", title))


def test_upgrade_populated_schema_preserves_meaning(database):
    dsn, schema = database
    apply(dsn, schema, through=1)
    async def seed():
        store = PostgresStore(dsn, schema)
        task = await store.create("lab-alice", "Previous release")
        return await store.complete("lab-alice", task.id)
    before = asyncio.run(seed())
    apply(dsn, schema)
    apply(dsn, schema)  # A repeated migration command is safe.
    after = asyncio.run(PostgresStore(dsn, schema).get("lab-alice", before.id))
    assert before == after
    assert asyncio.run(PostgresStore(dsn, schema).ready())


def test_migration_failure_rolls_back_then_recovery(database, tmp_path, monkeypatch):
    import reference.migrate as migrate
    dsn, schema = database
    apply(dsn, schema, through=1)
    original = migrate.MIGRATIONS
    # This disposable migration directory is intentionally wrong; original files stay intact.
    for file in original.glob("*.sql"):
        (tmp_path / file.name).write_text(file.read_text())
    (tmp_path / "003_deliberate_failure.sql").write_text("CREATE TABLE temporary_change (id integer); SELECT 1/0;")
    monkeypatch.setattr(migrate, "MIGRATIONS", tmp_path)
    with pytest.raises(psycopg.errors.DivisionByZero):
        migrate.apply(dsn, schema)
    with connect(database) as conn:
        assert conn.execute("SELECT max(version) FROM schema_migrations").fetchone()[0] == 1
        assert conn.execute("SELECT to_regclass('temporary_change')").fetchone()[0] is None
    monkeypatch.setattr(migrate, "MIGRATIONS", original)
    migrate.apply(dsn, schema)
    assert asyncio.run(PostgresStore(dsn, schema).ready())
