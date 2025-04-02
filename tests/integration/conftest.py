from contextlib import ExitStack
import os

from fastapi import FastAPI
import pytest
from httpx import ASGITransport, AsyncClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
from pytest_postgresql.executor import PostgreSQLExecutor

from pottato import init_app


test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest.fixture(scope="session", autouse=True)
def app(test_db: PostgreSQLExecutor):
    os.environ["TESTING"] = "True"

    host = test_db.host
    port = test_db.port
    user = test_db.user
    dbname = test_db.dbname

    with DatabaseJanitor(
        user=user,
        host=host,
        port=port,
        version=test_db.version,
        dbname=dbname,
    ):
        os.environ["DB_URL"] = f"asyncpg://{host}:{port}"
        with ExitStack():
            yield init_app()


@pytest.fixture
async def client(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
