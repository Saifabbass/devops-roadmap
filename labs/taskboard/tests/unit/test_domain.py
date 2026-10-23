import asyncio
from dataclasses import replace
import pytest
from pydantic import ValidationError
from reference.domain import normalize_title, new_task, complete
from reference.api import CreateTask
from reference.memory import MemoryStore

@pytest.mark.parametrize("value,expected", [("  Ship  ", "Ship"), ("x" * 120, "x" * 120), ("\u2003🚀\u2003", "🚀")])
def test_title(value, expected):
    assert normalize_title(value) == expected

@pytest.mark.parametrize("value", ["", "  ", "\n\t", "x" * 121, None, 3, True, [], {}])
def test_invalid_title(value):
    with pytest.raises(ValueError):
        normalize_title(value)

@pytest.mark.parametrize("data", [{"title": 1}, {"title": None}, {"title": "x", "owner_id": "bob"}, {}, {"title": " "}])
def test_strict_request_model(data):
    with pytest.raises(ValidationError):
        CreateTask.model_validate(data)


def test_completion_is_idempotent():
    original = new_task("alice", "Ship")
    finished = complete(original)
    assert finished.completed and finished.completed_at >= original.created_at
    assert complete(finished) == finished
    assert original.completed is False


def test_public_shape_hides_owner():
    task = new_task("private-owner", "Ship")
    assert set(task.public()) == {"id", "title", "completed", "created_at", "completed_at"}
    assert task.public()["created_at"].endswith("Z")


def test_memory_ownership_order_and_completion():
    async def scenario():
        store = MemoryStore()
        one = await store.create("alice", "One")
        two = await store.create("bob", "Two")
        assert await store.get("bob", one.id) is None
        assert await store.complete("bob", one.id) is None
        assert not (await store.get("alice", one.id)).completed
        assert [task.id for task in await store.list("alice")] == [one.id]
        results = await asyncio.gather(store.complete("alice", one.id), store.complete("alice", one.id))
        assert results[0].completed_at == results[1].completed_at
        assert (await store.get("bob", two.id)).title == "Two"
    asyncio.run(scenario())
