from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Evolution of Todo"
    DATABASE_URL: str = "sqlite:///./todo.db"  # Default/Fallback - SQLite for local testing
    SECRET_KEY: str = "CHANGE_THIS_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BETTER_AUTH_SECRET: str = "CHANGE_THIS_BETTER_AUTH_SECRET"

    class Config:
        env_file = ".env"

settings = Settings()
