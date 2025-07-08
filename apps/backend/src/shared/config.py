from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Postgresql
    
    postgresql_username: str = Field(..., env="POSTGRES_USER")
    postgresql_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgresql_host: str = Field(..., env="POSTGRES_HOST")
    postgresql_port: int = Field(..., env="POSTGRES_PORT")
    postgresql_database: str = Field(..., env="POSTGRES_DB")
    
    # Supabase
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_key: str = Field(..., env="SUPABASE_API_KEY")
    supabase_bucket: str = Field(..., env="BUCKET_NAME")
    
    # JWT
    secret_key: str = Field(...,env="SECRET_KEY")
    algorithm: str = Field(...,env="ALGORITHM")
    access_token_expire_minutes: int = Field(...,env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()