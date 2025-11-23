from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str = "postgresql+asyncpg://akshay:123456789@localhost:5432/postgres"

    # JWT configuration
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # AI Service configuration
    GROQ_API_KEY: str = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    # Application configuration
    APP_NAME: str = "Book Manager API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_database_url(self) -> str:
        """Get database URL"""
        if "postgres" in self.DATABASE_URL:
            return self.DATABASE_URL


settings = Settings()
