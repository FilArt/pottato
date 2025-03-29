from contextlib import ExitStack

from fastapi import FastAPI
import pytest
from httpx import ASGITransport, AsyncClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from pottato import init_app
from pottato.services.database import get_db, sessionmanager


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)


@pytest.fixture
async def client(app: FastAPI):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api") as ac:
        yield ac


test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest.fixture(scope="session", autouse=True)
async def connection_test(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        user=pg_user,
        host=pg_host,
        port=pg_port,
        version=test_db.version,
        dbname=pg_db,
        password=pg_password,
    ):
        connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override
