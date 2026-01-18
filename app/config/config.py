from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    env: str = Field(default="dev", description="Environment (dev/prod)")

    database_url: Optional[str] = Field(
        default=None,
        description="Database URL from .env",
    )

    cors_origins: Optional[str] = Field(
        default=None, description="CORS origins (comma-separated, from .env)"
    )

    origins: List[str] = Field(default_factory=list, description="CORS allowed origins")

    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8081, description="Server port")
    debug: bool = Field(default=True, description="Debug mode")

    docs_url: Optional[str] = Field(default="/docs", description="Swagger docs URL")
    redoc_url: Optional[str] = Field(default="/redoc", description="ReDoc URL")

    base_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent,
        description="Base directory",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._configure_environment_specific_settings()

    def _configure_environment_specific_settings(self):
        if self.env == "prod":
            self.host = "0.0.0.0"
            self.port = 8080
            self.debug = False
            self.docs_url = None
            self.redoc_url = None
            if self.cors_origins:
                self.origins = [
                    origin.strip() for origin in self.cors_origins.split(",")
                ]
            else:
                self.origins = [
                    "https://example.com",
                    "http://example.com",
                    "https://api.example.com",
                    "http://api.example.com",
                ]
        else:
            self.host = "127.0.0.1"
            self.port = 8081
            self.debug = True
            self.docs_url = "/docs"
            self.redoc_url = "/redoc"
            if self.cors_origins:
                self.origins = [
                    origin.strip() for origin in self.cors_origins.split(",")
                ]
            else:
                self.origins = ["*"]


settings = Settings()
