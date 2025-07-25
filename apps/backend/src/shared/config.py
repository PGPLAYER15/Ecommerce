from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


load_dotenv()
class Settings(BaseSettings):
    
    debug: bool = Field(...,env="DEBUG")
    
    # Postgresql
    
    postgresql_user: str = Field(..., env="POSTGRESQL_USER")
    postgresql_password: str = Field(..., env="POSTGRESQL_PASSWORD")
    postgresql_server: str = Field(..., env="POSTGRESQL_SERVER")
    postgresql_port: int = Field(..., env="POSTGRESQL_PORT")
    postgresql_name: str = Field(..., env="POSTGRESQL_NAME")
    
    # Supabase
    
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_api_key: str = Field(..., env="SUPABASE_API_KEY")
    supabase_bucket_name: str = Field(..., env="SUPABASE_BUCKET_NAME")
    
    # JWT
    
    secret_key: str = Field(...,env="SECRET_KEY")
    algorithm: str = Field(...,env="ALGORITHM")
    access_token_expire_minutes: int = Field(...,env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        extra = "allow" 
        

settings = Settings()