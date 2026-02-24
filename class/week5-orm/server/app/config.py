from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@127.0.0.1:54332/postgres"
    supabase_url: str = ""
    supabase_anon_key: str = ""

    model_config = {"env_file": ".env"}


settings = Settings()
