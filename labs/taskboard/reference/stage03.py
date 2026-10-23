"""Run: python -m uvicorn reference.stage03:app --host 127.0.0.1 --port 8000 --no-access-log"""
import logging
from reference.api import make_app
from reference.memory import MemoryStore
logging.basicConfig(level=logging.INFO, format="%(message)s")
app = make_app(MemoryStore(), stage="03")
