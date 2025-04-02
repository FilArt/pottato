from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_URL: str
    TESTING: bool = False
    DEBUG: bool = False
    PRINT_SQL: bool = False

    model_config = SettingsConfigDict()
