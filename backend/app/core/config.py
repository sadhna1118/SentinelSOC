"""
Core settings and configuration for SentinelSOC
"""
import os
from pathlib import Path

# Base Directory of Backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    PROJECT_NAME: str = "SentinelSOC"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database Configuration (SQLite for local dev, path points to backend/sentinelsoc.db)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{BASE_DIR}/sentinelsoc.db"
    )
    
    # Security & JWT Token Configurations
    SECRET_KEY: str = os.getenv("SECRET_KEY", "e2d8471c26f0b4d5a91f543e8c9d0b67a3f892c4b5e6d1a2f304958674b210dc")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 hours


settings = Settings()
