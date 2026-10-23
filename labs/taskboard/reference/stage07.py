"""Week 7 adds two disposable identities; never expose this teaching auth publicly."""
import logging
import os
from reference.api import make_app
from reference.postgres import PostgresStore
logging.basicConfig(level=logging.INFO, format="%(message)s")
app = make_app(PostgresStore(), stage="07", auth_tokens={
    os.environ["LAB_ALICE_TOKEN"]: "lab-alice", os.environ["LAB_BOB_TOKEN"]: "lab-bob"})
