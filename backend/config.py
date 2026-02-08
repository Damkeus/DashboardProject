"""Configuration management for NVIDIA Dashboard backend."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    fred_api_key: str
    alpha_vantage_api_key: str
    
    # Database
    database_url: str = "sqlite:///./nvidia_dashboard.db"
    
    # Scheduler
    update_schedule_hour: int = 9
    update_schedule_minute: int = 0
    update_schedule_timezone: str = "America/New_York"
    
    # Application
    environment: str = "development"
    debug: bool = True
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Data Collection
    data_cache_minutes: int = 30
    max_retries: int = 3
    request_timeout: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
