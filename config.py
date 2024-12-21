from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    database_url: str
    secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    algorithm: str
    permit_api_key: str
    permit_pdp: str
    env: str

    class Config:
        env_file = ".env"  # This points to the .env file
