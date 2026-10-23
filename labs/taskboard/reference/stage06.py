"""Week 6 replaces only storage. Run migrations before starting."""
import logging
from reference.api import make_app
from reference.postgres import PostgresStore
logging.basicConfig(level=logging.INFO, format="%(message)s")
app = make_app(PostgresStore(), stage="06")
