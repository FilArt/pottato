from contextlib import asynccontextmanager

from fastapi import FastAPI

from pottato.views import include_routers

from .config import Config
from .services.database import sessionmanager


def init_app(init_db: bool = True) -> FastAPI:
    title = "Pottato"
    if init_db:
        sessionmanager.init(Config.DB_CONFIG)

        @asynccontextmanager
        async def lifespan(app: FastAPI):  # pylint: disable=unused-argument
            yield
            if not sessionmanager.is_initialized:
                await sessionmanager.close()

        server = FastAPI(title=title, lifespan=lifespan)
    else:
        server = FastAPI(title=title)

    include_routers(server)

    return server
