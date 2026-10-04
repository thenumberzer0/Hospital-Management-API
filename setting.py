from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    DB_URL: str
    ALGORITHM:str
    SECRET_KEY: str
    TOKEN_EXPIRATION_TIME: int
    model_config=SettingsConfigDict(env_file=".env")

settings = Settings()
