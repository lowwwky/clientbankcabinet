from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent

class AuthJWT(BaseModel):
    private_key_path: Path = ROOT_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = ROOT_DIR / "certs" / "jwt-public.pem"
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

    naming_convention: dict[str,str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


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
    model_config =  SettingsConfigDict(
        env_file= (
            ROOT_DIR / ".env",
            ROOT_DIR / ".env.template",
        ),
        extra="ignore",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )


settings = Settings()
