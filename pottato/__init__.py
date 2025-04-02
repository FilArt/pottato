from contextlib import asynccontextmanager

from fastapi import FastAPI

from pottato.config import Config
from pottato.services.db import register_orm
from pottato.views import include_routers


def init_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):  # pylint: disable=unused-argument
        breakpoint()
        yield
        breakpoint()

    app = FastAPI(title="Pottato", lifespan=lifespan)

    include_routers(app)

    config = Config()
    register_orm(app, config.DB_URL, generate_schemas=config.TESTING)

    return app
