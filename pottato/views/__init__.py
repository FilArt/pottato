from fastapi import FastAPI

from .root import router as root_router
from .user import router as user_router


def include_routers(app: FastAPI):
    app.include_router(router=root_router, prefix="", tags=["root"])
    app.include_router(router=user_router, prefix="/api", tags=["user"])
