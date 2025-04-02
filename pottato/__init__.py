from fastapi import FastAPI

from pottato.config import Config
from pottato.services.db import register_orm
from pottato.views import include_routers


def init_app() -> FastAPI:
    app = FastAPI(title="Pottato")

    include_routers(app)

    config = Config()
    register_orm(app, config.DB_URL, generate_schemas=config.TESTING, print_sql=config.PRINT_SQL)

    return app
