
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # --- App Config ---
    APP_ENV: str = Field(default="development", description="Environment: dev, staging, prod")
    DEBUG: bool = Field(default=True, description="Debug mode flag")

    # --- LiveKit (REQ-VOX-002, 003) ---
    LIVEKIT_URL: str = Field(..., description="LiveKit WebSocket URL")
    LIVEKIT_API_KEY: str = Field(..., description="LiveKit API Key")
    LIVEKIT_API_SECRET: str = Field(..., description="LiveKit API Secret")

    # --- Database & Cache (REQ-VOX-004, 005) ---
    DATABASE_URL: str = Field(..., description="PostgreSQL async connection string")
    REDIS_URL: str = Field(..., description="Redis connection string")

    # --- AI Providers (M3 ke liye, abhi optional hain) ---
    DEEPGRAM_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    ELEVENLABS_API_KEY: str | None = None

    # --- Security (M6 ke liye, abhi optional) ---
    FERNET_KEY: str | None = None

    # Pydantic ko batata hai ke .env file kahan hai aur kaise padhni hai
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Agar .env mein koi extra variable ho toh ignore kar do
    )

# Global settings instance
settings = Settings()