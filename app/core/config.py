from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = ""
    max_failed_attempts: int = 5
    session_hours: int = 12
    model_config =  SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
