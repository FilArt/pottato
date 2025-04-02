from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


def register_orm(app: FastAPI, db_url: str, generate_schemas=False):
    register_tortoise(
        app,
        db_url=db_url,
        modules={"models": ["models"]},
        generate_schemas=generate_schemas,
    )
