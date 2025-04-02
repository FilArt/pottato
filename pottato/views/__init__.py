from fastapi import FastAPI

from .root import router as root_router


def include_routers(app: FastAPI):
    app.include_router(router=root_router, prefix="", tags=["root"])
