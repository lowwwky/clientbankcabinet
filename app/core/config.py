from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    max_failed_attempts: int = 5

class DbSettings(BaseModel):
    url: str = ""
    # Абсолютно всего должно быть False.
    echo: bool = False

class Settings(BaseSettings):
    db = DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()
    model_config =  SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
