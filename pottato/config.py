import os


# pylint: disable=too-few-public-methods
class Config:
    DB_CONFIG = os.getenv(
        "DB_CONFIG",
        # pylint: disable=consider-using-f-string
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=os.getenv("USER"),
            DB_PASSWORD=os.getenv("DB_PASSWORD", "postgres"),
            DB_HOST=os.getenv("DB_HOST", "localhost"),
            DB_NAME=os.getenv("DB_NAME", "postgres"),
        ),
    )
