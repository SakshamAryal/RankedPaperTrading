from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """ Application settings loaded from environment variables. """
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int


settings = Settings()
