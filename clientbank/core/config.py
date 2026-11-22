from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn

BASE_DIR = Path(__file__).resolve().parent.parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    max_failed_attempts: int = 5

class DbSettings(BaseModel):
    url: PostgresDsn
    # Абсолютно всего должно быть False.
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000

class ApiPrefix(BaseModel):
    prefix: str = "/api"

class Settings(BaseSettings):
    db: DbSettings
    auth_jwt: AuthJWT = AuthJWT()
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    model_config =  SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
